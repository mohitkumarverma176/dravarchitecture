import os
import smtplib
import ssl
import datetime
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, abort, make_response
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret-key-in-production")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///drav.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30 MB upload limit

# Extensions
csrf = CSRFProtect(app)

from database import init_db
init_db(app)

from auth_utils import login_manager
login_manager.init_app(app)

from admin import admin_bp
app.register_blueprint(admin_bp)

import crud


# ── Context Processor — inject settings into every template ───────────────────

@app.context_processor
def inject_footer_settings():
    """Make site settings available to all templates (used by footer.html)."""
    try:
        return {'footer_settings': crud.get_settings_dict()}
    except Exception:
        return {'footer_settings': {}}


# ── Public Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def home():
    hero_slides = crud.get_hero_slides()
    stats = crud.get_stats()
    featured_projects = crud.get_projects(featured_only=True, limit=6)
    services = crud.get_services()[:4]
    testimonials = crud.get_testimonials()
    settings = crud.get_settings_dict()
    return render_template('index.html',
                           hero_slides=hero_slides,
                           stats=stats,
                           featured_projects=featured_projects,
                           services=services,
                           testimonials=testimonials,
                           settings=settings)


@app.route('/projects')
def projects():
    all_projects = crud.get_projects(featured_only=False)
    categories = crud.get_categories()
    return render_template('projects.html', projects=all_projects, categories=categories)


@app.route('/projects/<slug>')
def project_detail(slug):
    project = crud.get_project_by_slug(slug)
    if not project:
        abort(404)
    related = crud.get_projects(featured_only=False, limit=4, exclude_id=project.id)
    testimonials = crud.get_testimonials()
    return render_template('project-single.html',
                           project=project,
                           related=related,
                           testimonials=testimonials)


# Legacy static project page — redirect to first project if one exists
@app.route('/project-single')
def project_single():
    from models import Project
    first = Project.query.order_by(Project.display_order).first()
    if first:
        return redirect(url_for('project_detail', slug=first.slug))
    return redirect(url_for('projects'))


@app.route('/single')
def single():
    return render_template('single.html')


@app.route('/services')
def services():
    all_services = crud.get_services()
    testimonials = crud.get_testimonials()
    return render_template('services.html', services=all_services, testimonials=testimonials)


@app.route('/about')
def about():
    team = crud.get_team()
    stats = crud.get_stats()
    settings = crud.get_settings_dict()
    return render_template('about.html', team=team, stats=stats, settings=settings)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = crud.get_settings_dict()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip() or 'New Contact Form Message'
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('Please fill in Name, Email, and Message.', 'error')
            return redirect(url_for('contact'))

        body = (
            'New contact form submission:\n\n'
            f'Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\n\nMessage:\n{message}'
        )

        try:
            send_email(
                recipient=os.environ.get('CONTACT_RECIPIENT',
                                         settings.get('contact_email', 'dravarchitecture@outlook.com')),
                subject=f'[Website] {subject}',
                body=body
            )
            flash('Thanks! Your message has been sent.', 'success')
        except Exception as e:
            flash(f'Sorry, something went wrong: {e}', 'error')

        return redirect(url_for('contact'))

    return render_template('contact.html', settings=settings)


def send_email(recipient: str, subject: str, body: str):
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.office365.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_pass = os.environ.get('SMTP_PASS')
    sender = os.environ.get('SMTP_SENDER', smtp_user)

    if not (smtp_user and smtp_pass and sender):
        raise RuntimeError('SMTP credentials not set. Please set SMTP_USER, SMTP_PASS, and SMTP_SENDER env vars.')

    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.route('/robots.txt')
def robots_txt():
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        '',
        f'Sitemap: {request.host_url}sitemap.xml',
    ]
    resp = make_response('\n'.join(lines))
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route('/sitemap.xml')
def sitemap_xml():
    from models import Project
    pages = [
        (url_for('home', _external=True), '1.0', 'weekly'),
        (url_for('projects', _external=True), '0.9', 'weekly'),
        (url_for('services', _external=True), '0.8', 'monthly'),
        (url_for('about', _external=True), '0.7', 'monthly'),
        (url_for('contact', _external=True), '0.7', 'monthly'),
    ]
    today = datetime.date.today().isoformat()
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority, freq in pages:
        parts.append(
            f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod>'
            f'<changefreq>{freq}</changefreq><priority>{priority}</priority></url>'
        )
    for proj in Project.query.all():
        loc = url_for('project_detail', slug=proj.slug, _external=True)
        parts.append(
            f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod>'
            f'<changefreq>monthly</changefreq><priority>0.6</priority></url>'
        )
    parts.append('</urlset>')
    resp = make_response('\n'.join(parts))
    resp.headers['Content-Type'] = 'application/xml'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')), debug=True)
