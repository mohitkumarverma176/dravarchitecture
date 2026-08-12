import os
import uuid
from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from admin import admin_bp
import crud
from auth_utils import verify_password
from database import db
from models import Admin, Statistic, SiteSetting

try:
    from PIL import Image as PILImage
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

ALLOWED_IMAGE_EXTS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
ALLOWED_PDF_EXTS = {'pdf'}
MAX_IMAGE_PX = 1920
IMAGE_QUALITY = 85


def _allowed_file(filename, exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in exts


def _upload_image(file_obj) -> str:
    """Save uploaded image, compress with Pillow if available. Returns relative path from static/."""
    ext = file_obj.filename.rsplit('.', 1)[1].lower()
    new_name = f"{uuid.uuid4().hex}.{ext}"
    uploads_dir = os.path.join(current_app.static_folder, 'uploads', 'images')
    os.makedirs(uploads_dir, exist_ok=True)
    dest = os.path.join(uploads_dir, new_name)

    if PILLOW_AVAILABLE and ext in ('jpg', 'jpeg', 'png', 'webp'):
        img = PILImage.open(file_obj)
        img = img.convert('RGB')
        if img.width > MAX_IMAGE_PX:
            ratio = MAX_IMAGE_PX / img.width
            img = img.resize((MAX_IMAGE_PX, int(img.height * ratio)), PILImage.LANCZOS)
        save_ext = 'JPEG' if ext in ('jpg', 'jpeg') else ext.upper()
        img.save(dest, save_ext, quality=IMAGE_QUALITY, optimize=True)
    else:
        file_obj.save(dest)

    return f'uploads/images/{new_name}'


def _upload_pdf(file_obj) -> str:
    """Save uploaded PDF. Returns relative path from static/."""
    new_name = f"{uuid.uuid4().hex}.pdf"
    uploads_dir = os.path.join(current_app.static_folder, 'uploads', 'pdfs')
    os.makedirs(uploads_dir, exist_ok=True)
    dest = os.path.join(uploads_dir, new_name)
    file_obj.save(dest)
    return f'uploads/pdfs/{new_name}'


# ── Auth ──────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin = crud.get_admin_by_username(username)
        if admin and verify_password(password, admin.password_hash):
            login_user(admin, remember=True)
            return redirect(url_for('admin_bp.dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_bp.login'))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    from models import Project, MediaFile, Service, TeamMember, Testimonial
    stats = {
        'projects': Project.query.count(),
        'media': MediaFile.query.count(),
        'services': Service.query.count(),
        'team': TeamMember.query.count(),
        'testimonials': Testimonial.query.count(),
    }
    recent_projects = crud.get_projects(limit=5)
    return render_template('admin/dashboard.html', stats=stats, recent_projects=recent_projects)


# ── Projects ──────────────────────────────────────────────────────────────────

@admin_bp.route('/projects')
@login_required
def projects():
    projects = crud.get_projects(featured_only=False)
    return render_template('admin/projects.html', projects=projects)


@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def project_new():
    media_images = crud.get_media_files(file_type='image')
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Title is required.', 'error')
            return render_template('admin/project_form.html', project=None, media_images=media_images)

        slug = _slugify(title)
        # ensure unique slug
        from models import Project as P
        existing = P.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{uuid.uuid4().hex[:6]}"

        cover_image = None
        if 'cover_image' in request.files and request.files['cover_image'].filename:
            f = request.files['cover_image']
            if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
                path = _upload_image(f)
                crud.create_media(
                    filename=os.path.basename(path),
                    original_name=secure_filename(f.filename),
                    file_type='image',
                    file_path=path
                )
                cover_image = path
        elif request.form.get('cover_image_select'):
            cover_image = request.form.get('cover_image_select')

        data = {
            'title': title,
            'slug': slug,
            'description': request.form.get('description', ''),
            'category': request.form.get('category', '').strip(),
            'category_display': request.form.get('category_display', '').strip(),
            'location': request.form.get('location', '').strip(),
            'client': request.form.get('client', '').strip(),
            'area_sqft': request.form.get('area_sqft', '').strip(),
            'year': int(request.form.get('year') or 0) or None,
            'services_provided': request.form.get('services_provided', '').strip(),
            'status': request.form.get('status', 'Completed'),
            'is_featured': 'is_featured' in request.form,
            'display_order': int(request.form.get('display_order') or 0),
            'cover_image': cover_image,
        }
        project = crud.create_project(data)

        # gallery images upload
        gallery_files = request.files.getlist('gallery_images')
        for i, gf in enumerate(gallery_files):
            if gf and gf.filename and _allowed_file(gf.filename, ALLOWED_IMAGE_EXTS):
                path = _upload_image(gf)
                crud.create_media(
                    filename=os.path.basename(path),
                    original_name=secure_filename(gf.filename),
                    file_type='image',
                    file_path=path
                )
                crud.add_project_image(project.id, path, display_order=i)

        # PDF upload
        pdf_files = request.files.getlist('pdf_files')
        pdf_labels = request.form.getlist('pdf_labels')
        for pdf_file, label in zip(pdf_files, pdf_labels):
            if pdf_file and pdf_file.filename and _allowed_file(pdf_file.filename, ALLOWED_PDF_EXTS):
                path = _upload_pdf(pdf_file)
                crud.create_media(
                    filename=os.path.basename(path),
                    original_name=secure_filename(pdf_file.filename),
                    file_type='pdf',
                    file_path=path
                )
                crud.add_project_pdf(project.id, path, label=label or pdf_file.filename)

        flash(f'Project "{title}" created successfully.', 'success')
        return redirect(url_for('admin_bp.projects'))

    return render_template('admin/project_form.html', project=None, media_images=media_images)


@admin_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def project_edit(project_id):
    project = crud.get_project_by_id(project_id)
    if not project:
        flash('Project not found.', 'error')
        return redirect(url_for('admin_bp.projects'))
    media_images = crud.get_media_files(file_type='image')

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Title is required.', 'error')
            return render_template('admin/project_form.html', project=project, media_images=media_images)

        cover_image = project.cover_image
        if 'cover_image' in request.files and request.files['cover_image'].filename:
            f = request.files['cover_image']
            if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
                path = _upload_image(f)
                crud.create_media(
                    filename=os.path.basename(path),
                    original_name=secure_filename(f.filename),
                    file_type='image',
                    file_path=path
                )
                cover_image = path
        elif request.form.get('cover_image_select'):
            cover_image = request.form.get('cover_image_select')

        data = {
            'title': title,
            'description': request.form.get('description', ''),
            'category': request.form.get('category', '').strip(),
            'category_display': request.form.get('category_display', '').strip(),
            'location': request.form.get('location', '').strip(),
            'client': request.form.get('client', '').strip(),
            'area_sqft': request.form.get('area_sqft', '').strip(),
            'year': int(request.form.get('year') or 0) or None,
            'services_provided': request.form.get('services_provided', '').strip(),
            'status': request.form.get('status', 'Completed'),
            'is_featured': 'is_featured' in request.form,
            'display_order': int(request.form.get('display_order') or 0),
            'cover_image': cover_image,
        }
        crud.update_project(project_id, data)

        # gallery images upload
        gallery_files = request.files.getlist('gallery_images')
        existing_count = len(project.images)
        for i, gf in enumerate(gallery_files):
            if gf and gf.filename and _allowed_file(gf.filename, ALLOWED_IMAGE_EXTS):
                path = _upload_image(gf)
                crud.create_media(
                    filename=os.path.basename(path),
                    original_name=secure_filename(gf.filename),
                    file_type='image',
                    file_path=path
                )
                crud.add_project_image(project_id, path, display_order=existing_count + i)

        # PDF upload
        pdf_files = request.files.getlist('pdf_files')
        pdf_labels = request.form.getlist('pdf_labels')
        for pdf_file, label in zip(pdf_files, pdf_labels):
            if pdf_file and pdf_file.filename and _allowed_file(pdf_file.filename, ALLOWED_PDF_EXTS):
                path = _upload_pdf(pdf_file)
                crud.create_media(
                    filename=os.path.basename(path),
                    original_name=secure_filename(pdf_file.filename),
                    file_type='pdf',
                    file_path=path
                )
                crud.add_project_pdf(project_id, path, label=label or pdf_file.filename)

        flash(f'Project "{title}" updated successfully.', 'success')
        return redirect(url_for('admin_bp.projects'))

    return render_template('admin/project_form.html', project=project, media_images=media_images)


@admin_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def project_delete(project_id):
    project = crud.get_project_by_id(project_id)
    if project:
        name = project.title
        crud.delete_project(project_id)
        flash(f'Project "{name}" deleted.', 'success')
    return redirect(url_for('admin_bp.projects'))


@admin_bp.route('/projects/<int:project_id>/images/<int:image_id>/delete', methods=['POST'])
@login_required
def project_image_delete(project_id, image_id):
    crud.delete_project_image(image_id)
    flash('Image removed from project.', 'success')
    return redirect(url_for('admin_bp.project_edit', project_id=project_id))


@admin_bp.route('/projects/<int:project_id>/pdfs/<int:pdf_id>/delete', methods=['POST'])
@login_required
def project_pdf_delete(project_id, pdf_id):
    crud.delete_project_pdf(pdf_id)
    flash('PDF removed from project.', 'success')
    return redirect(url_for('admin_bp.project_edit', project_id=project_id))


# ── Media ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/media')
@login_required
def media():
    images = crud.get_media_files(file_type='image')
    pdfs = crud.get_media_files(file_type='pdf')
    return render_template('admin/media.html', images=images, pdfs=pdfs)


@admin_bp.route('/media/upload', methods=['POST'])
@login_required
def media_upload():
    files = request.files.getlist('files')
    uploaded = 0
    for f in files:
        if not f or not f.filename:
            continue
        ext = f.filename.rsplit('.', 1)[-1].lower() if '.' in f.filename else ''
        if ext in ALLOWED_IMAGE_EXTS:
            path = _upload_image(f)
            crud.create_media(
                filename=os.path.basename(path),
                original_name=secure_filename(f.filename),
                file_type='image',
                file_path=path
            )
            uploaded += 1
        elif ext in ALLOWED_PDF_EXTS:
            path = _upload_pdf(f)
            crud.create_media(
                filename=os.path.basename(path),
                original_name=secure_filename(f.filename),
                file_type='pdf',
                file_path=path
            )
            uploaded += 1
    flash(f'{uploaded} file(s) uploaded successfully.', 'success')
    return redirect(url_for('admin_bp.media'))


@admin_bp.route('/media/<int:media_id>/delete', methods=['POST'])
@login_required
def media_delete(media_id):
    m = crud.delete_media(media_id)
    if m:
        try:
            full_path = os.path.join(current_app.static_folder, m.file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception:
            pass
        flash('File deleted.', 'success')
    return redirect(url_for('admin_bp.media'))


# ── Services ──────────────────────────────────────────────────────────────────

@admin_bp.route('/services')
@login_required
def services():
    services = crud.get_services(active_only=False)
    return render_template('admin/services.html', services=services)


@admin_bp.route('/services/new', methods=['POST'])
@login_required
def service_new():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Title is required.', 'error')
        return redirect(url_for('admin_bp.services'))

    image_path = None
    if 'image' in request.files and request.files['image'].filename:
        f = request.files['image']
        if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
            image_path = _upload_image(f)
            crud.create_media(
                filename=os.path.basename(image_path),
                original_name=secure_filename(f.filename),
                file_type='image',
                file_path=image_path
            )

    count = crud.get_services(active_only=False)
    crud.create_service({
        'title': title,
        'description': request.form.get('description', ''),
        'icon_class': request.form.get('icon_class', 'flaticon-compass'),
        'image_filename': image_path or request.form.get('image_filename', ''),
        'display_order': len(count),
        'is_active': True,
    })
    flash('Service added.', 'success')
    return redirect(url_for('admin_bp.services'))


@admin_bp.route('/services/<int:service_id>/edit', methods=['POST'])
@login_required
def service_edit(service_id):
    image_path = None
    if 'image' in request.files and request.files['image'].filename:
        f = request.files['image']
        if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
            image_path = _upload_image(f)
            crud.create_media(
                filename=os.path.basename(image_path),
                original_name=secure_filename(f.filename),
                file_type='image',
                file_path=image_path
            )

    data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', ''),
        'icon_class': request.form.get('icon_class', 'flaticon-compass'),
        'is_active': 'is_active' in request.form,
    }
    if image_path:
        data['image_filename'] = image_path
    elif request.form.get('image_filename'):
        data['image_filename'] = request.form.get('image_filename')

    crud.update_service(service_id, data)
    flash('Service updated.', 'success')
    return redirect(url_for('admin_bp.services'))


@admin_bp.route('/services/<int:service_id>/delete', methods=['POST'])
@login_required
def service_delete(service_id):
    crud.delete_service(service_id)
    flash('Service deleted.', 'success')
    return redirect(url_for('admin_bp.services'))


# ── Team ──────────────────────────────────────────────────────────────────────

@admin_bp.route('/team')
@login_required
def team():
    members = crud.get_team(active_only=False)
    return render_template('admin/team.html', members=members)


@admin_bp.route('/team/new', methods=['POST'])
@login_required
def team_new():
    name = request.form.get('name', '').strip()
    if not name:
        flash('Name is required.', 'error')
        return redirect(url_for('admin_bp.team'))

    photo_path = None
    if 'photo' in request.files and request.files['photo'].filename:
        f = request.files['photo']
        if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
            photo_path = _upload_image(f)
            crud.create_media(
                filename=os.path.basename(photo_path),
                original_name=secure_filename(f.filename),
                file_type='image',
                file_path=photo_path
            )

    count = crud.get_team(active_only=False)
    crud.create_team_member({
        'name': name,
        'role': request.form.get('role', ''),
        'bio': request.form.get('bio', ''),
        'photo_filename': photo_path or request.form.get('photo_filename', ''),
        'display_order': len(count),
        'is_active': True,
    })
    flash('Team member added.', 'success')
    return redirect(url_for('admin_bp.team'))


@admin_bp.route('/team/<int:member_id>/edit', methods=['POST'])
@login_required
def team_edit(member_id):
    photo_path = None
    if 'photo' in request.files and request.files['photo'].filename:
        f = request.files['photo']
        if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
            photo_path = _upload_image(f)
            crud.create_media(
                filename=os.path.basename(photo_path),
                original_name=secure_filename(f.filename),
                file_type='image',
                file_path=photo_path
            )

    data = {
        'name': request.form.get('name', '').strip(),
        'role': request.form.get('role', ''),
        'bio': request.form.get('bio', ''),
        'is_active': 'is_active' in request.form,
    }
    if photo_path:
        data['photo_filename'] = photo_path
    elif request.form.get('photo_filename'):
        data['photo_filename'] = request.form.get('photo_filename')

    crud.update_team_member(member_id, data)
    flash('Team member updated.', 'success')
    return redirect(url_for('admin_bp.team'))


@admin_bp.route('/team/<int:member_id>/delete', methods=['POST'])
@login_required
def team_delete(member_id):
    crud.delete_team_member(member_id)
    flash('Team member deleted.', 'success')
    return redirect(url_for('admin_bp.team'))


# ── Hero Slides ───────────────────────────────────────────────────────────────

@admin_bp.route('/hero')
@login_required
def hero():
    slides = crud.get_hero_slides(active_only=False)
    return render_template('admin/hero.html', slides=slides)


@admin_bp.route('/hero/new', methods=['POST'])
@login_required
def hero_new():
    image_path = None
    if 'image' in request.files and request.files['image'].filename:
        f = request.files['image']
        if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
            image_path = _upload_image(f)
            crud.create_media(
                filename=os.path.basename(image_path),
                original_name=secure_filename(f.filename),
                file_type='image',
                file_path=image_path
            )

    if not image_path and not request.form.get('filename'):
        flash('Image is required for a hero slide.', 'error')
        return redirect(url_for('admin_bp.hero'))

    count = crud.get_hero_slides(active_only=False)
    crud.create_hero_slide({
        'filename': image_path or request.form.get('filename', ''),
        'heading': request.form.get('heading', ''),
        'subheading': request.form.get('subheading', ''),
        'display_order': len(count),
        'is_active': True,
    })
    flash('Hero slide added.', 'success')
    return redirect(url_for('admin_bp.hero'))


@admin_bp.route('/hero/<int:slide_id>/edit', methods=['POST'])
@login_required
def hero_edit(slide_id):
    image_path = None
    if 'image' in request.files and request.files['image'].filename:
        f = request.files['image']
        if _allowed_file(f.filename, ALLOWED_IMAGE_EXTS):
            image_path = _upload_image(f)
            crud.create_media(
                filename=os.path.basename(image_path),
                original_name=secure_filename(f.filename),
                file_type='image',
                file_path=image_path
            )

    data = {
        'heading': request.form.get('heading', ''),
        'subheading': request.form.get('subheading', ''),
        'display_order': int(request.form.get('display_order') or 0),
        'is_active': 'is_active' in request.form,
    }
    if image_path:
        data['filename'] = image_path

    crud.update_hero_slide(slide_id, data)
    flash('Hero slide updated.', 'success')
    return redirect(url_for('admin_bp.hero'))


@admin_bp.route('/hero/<int:slide_id>/delete', methods=['POST'])
@login_required
def hero_delete(slide_id):
    crud.delete_hero_slide(slide_id)
    flash('Hero slide deleted.', 'success')
    return redirect(url_for('admin_bp.hero'))


# ── Testimonials ──────────────────────────────────────────────────────────────

@admin_bp.route('/testimonials')
@login_required
def testimonials():
    testimonials = crud.get_testimonials(active_only=False)
    return render_template('admin/testimonials.html', testimonials=testimonials)


@admin_bp.route('/testimonials/new', methods=['POST'])
@login_required
def testimonial_new():
    client_name = request.form.get('client_name', '').strip()
    text = request.form.get('text', '').strip()
    if not client_name or not text:
        flash('Client name and text are required.', 'error')
        return redirect(url_for('admin_bp.testimonials'))

    count = crud.get_testimonials(active_only=False)
    initials = ''.join(w[0].upper() for w in client_name.split()[:2])
    crud.create_testimonial({
        'client_name': client_name,
        'company': request.form.get('company', ''),
        'text': text,
        'initials': initials,
        'display_order': len(count),
        'is_active': True,
    })
    flash('Testimonial added.', 'success')
    return redirect(url_for('admin_bp.testimonials'))


@admin_bp.route('/testimonials/<int:testimonial_id>/edit', methods=['POST'])
@login_required
def testimonial_edit(testimonial_id):
    client_name = request.form.get('client_name', '').strip()
    initials = ''.join(w[0].upper() for w in client_name.split()[:2]) if client_name else ''
    crud.update_testimonial(testimonial_id, {
        'client_name': client_name,
        'company': request.form.get('company', ''),
        'text': request.form.get('text', ''),
        'initials': initials,
        'is_active': 'is_active' in request.form,
    })
    flash('Testimonial updated.', 'success')
    return redirect(url_for('admin_bp.testimonials'))


@admin_bp.route('/testimonials/<int:testimonial_id>/delete', methods=['POST'])
@login_required
def testimonial_delete(testimonial_id):
    crud.delete_testimonial(testimonial_id)
    flash('Testimonial deleted.', 'success')
    return redirect(url_for('admin_bp.testimonials'))


# ── Settings ──────────────────────────────────────────────────────────────────

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Update site settings
        setting_keys = [
            'contact_phone', 'contact_email', 'contact_whatsapp', 'contact_address',
            'footer_tagline', 'social_instagram', 'social_linkedin', 'social_facebook',
            'about_headline', 'about_body', 'philosophy_text',
            'mission_text', 'vision_text',
        ]
        for key in setting_keys:
            val = request.form.get(key, '')
            crud.set_setting(key, val)

        # Update statistics
        stat_ids = request.form.getlist('stat_id')
        stat_labels = request.form.getlist('stat_label')
        stat_values = request.form.getlist('stat_value')
        stat_suffixes = request.form.getlist('stat_suffix')
        for stat_id, label, value, suffix in zip(stat_ids, stat_labels, stat_values, stat_suffixes):
            try:
                crud.update_stat(int(stat_id), {
                    'label': label,
                    'value': int(value or 0),
                    'suffix': suffix,
                })
            except (ValueError, TypeError):
                pass

        flash('Settings saved.', 'success')
        return redirect(url_for('admin_bp.settings'))

    site_settings = crud.get_settings_dict()
    stats = crud.get_stats()
    return render_template('admin/settings.html', settings=site_settings, stats=stats)


@admin_bp.route('/settings/stats/new', methods=['POST'])
@login_required
def stat_new():
    try:
        value = int(request.form.get('value', 0))
    except ValueError:
        value = 0
    existing = crud.get_stats()
    crud.create_stat({
        'label': request.form.get('label', '').strip(),
        'value': value,
        'suffix': request.form.get('suffix', ''),
        'display_order': len(existing),
    })
    flash('Statistic added.', 'success')
    return redirect(url_for('admin_bp.settings'))


@admin_bp.route('/settings/stats/<int:stat_id>/delete', methods=['POST'])
@login_required
def stat_delete(stat_id):
    crud.delete_stat(stat_id)
    flash('Statistic deleted.', 'success')
    return redirect(url_for('admin_bp.settings'))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text
