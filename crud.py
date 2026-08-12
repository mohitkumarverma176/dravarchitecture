from models import (
    Project, ProjectImage, ProjectPDF, Service, HeroSlide,
    TeamMember, Testimonial, Statistic, SiteSetting, MediaFile, Admin
)
from database import db


# ── Projects ──────────────────────────────────────────────────────────────────

def get_projects(featured_only=False, limit=None, exclude_id=None):
    q = Project.query.order_by(Project.display_order, Project.created_at.desc())
    if featured_only:
        q = q.filter_by(is_featured=True)
    if exclude_id:
        q = q.filter(Project.id != exclude_id)
    if limit:
        q = q.limit(limit)
    return q.all()


def get_project_by_slug(slug):
    return Project.query.filter_by(slug=slug).first()


def get_project_by_id(project_id):
    return Project.query.get(project_id)


def get_categories():
    rows = db.session.query(Project.category, Project.category_display).distinct().all()
    return [(r.category, r.category_display) for r in rows if r.category]


def create_project(data: dict) -> Project:
    p = Project(**data)
    db.session.add(p)
    db.session.commit()
    return p


def update_project(project_id, data: dict) -> Project:
    p = Project.query.get(project_id)
    for k, v in data.items():
        setattr(p, k, v)
    db.session.commit()
    return p


def delete_project(project_id):
    p = Project.query.get(project_id)
    if p:
        db.session.delete(p)
        db.session.commit()


def add_project_image(project_id, filename, caption='', display_order=0):
    img = ProjectImage(project_id=project_id, filename=filename,
                       caption=caption, display_order=display_order)
    db.session.add(img)
    db.session.commit()
    return img


def delete_project_image(image_id):
    img = ProjectImage.query.get(image_id)
    if img:
        db.session.delete(img)
        db.session.commit()


def add_project_pdf(project_id, filename, label=''):
    pdf = ProjectPDF(project_id=project_id, filename=filename, label=label)
    db.session.add(pdf)
    db.session.commit()
    return pdf


def delete_project_pdf(pdf_id):
    pdf = ProjectPDF.query.get(pdf_id)
    if pdf:
        db.session.delete(pdf)
        db.session.commit()


# ── Services ──────────────────────────────────────────────────────────────────

def get_services(active_only=True):
    q = Service.query.order_by(Service.display_order)
    if active_only:
        q = q.filter_by(is_active=True)
    return q.all()


def get_service_by_id(service_id):
    return Service.query.get(service_id)


def create_service(data: dict) -> Service:
    s = Service(**data)
    db.session.add(s)
    db.session.commit()
    return s


def update_service(service_id, data: dict) -> Service:
    s = Service.query.get(service_id)
    for k, v in data.items():
        setattr(s, k, v)
    db.session.commit()
    return s


def delete_service(service_id):
    s = Service.query.get(service_id)
    if s:
        db.session.delete(s)
        db.session.commit()


# ── Hero Slides ───────────────────────────────────────────────────────────────

def get_hero_slides(active_only=True):
    q = HeroSlide.query.order_by(HeroSlide.display_order)
    if active_only:
        q = q.filter_by(is_active=True)
    return q.all()


def get_hero_slide_by_id(slide_id):
    return HeroSlide.query.get(slide_id)


def create_hero_slide(data: dict) -> HeroSlide:
    s = HeroSlide(**data)
    db.session.add(s)
    db.session.commit()
    return s


def update_hero_slide(slide_id, data: dict) -> HeroSlide:
    s = HeroSlide.query.get(slide_id)
    for k, v in data.items():
        setattr(s, k, v)
    db.session.commit()
    return s


def delete_hero_slide(slide_id):
    s = HeroSlide.query.get(slide_id)
    if s:
        db.session.delete(s)
        db.session.commit()


# ── Team ──────────────────────────────────────────────────────────────────────

def get_team(active_only=True):
    q = TeamMember.query.order_by(TeamMember.display_order)
    if active_only:
        q = q.filter_by(is_active=True)
    return q.all()


def get_team_member_by_id(member_id):
    return TeamMember.query.get(member_id)


def create_team_member(data: dict) -> TeamMember:
    m = TeamMember(**data)
    db.session.add(m)
    db.session.commit()
    return m


def update_team_member(member_id, data: dict) -> TeamMember:
    m = TeamMember.query.get(member_id)
    for k, v in data.items():
        setattr(m, k, v)
    db.session.commit()
    return m


def delete_team_member(member_id):
    m = TeamMember.query.get(member_id)
    if m:
        db.session.delete(m)
        db.session.commit()


# ── Testimonials ──────────────────────────────────────────────────────────────

def get_testimonials(active_only=True):
    q = Testimonial.query.order_by(Testimonial.display_order)
    if active_only:
        q = q.filter_by(is_active=True)
    return q.all()


def get_testimonial_by_id(testimonial_id):
    return Testimonial.query.get(testimonial_id)


def create_testimonial(data: dict) -> Testimonial:
    t = Testimonial(**data)
    db.session.add(t)
    db.session.commit()
    return t


def update_testimonial(testimonial_id, data: dict) -> Testimonial:
    t = Testimonial.query.get(testimonial_id)
    for k, v in data.items():
        setattr(t, k, v)
    db.session.commit()
    return t


def delete_testimonial(testimonial_id):
    t = Testimonial.query.get(testimonial_id)
    if t:
        db.session.delete(t)
        db.session.commit()


# ── Statistics ────────────────────────────────────────────────────────────────

def get_stats():
    return Statistic.query.order_by(Statistic.display_order).all()


def get_stat_by_id(stat_id):
    return Statistic.query.get(stat_id)


def create_stat(data: dict) -> Statistic:
    s = Statistic(**data)
    db.session.add(s)
    db.session.commit()
    return s


def update_stat(stat_id, data: dict) -> Statistic:
    s = Statistic.query.get(stat_id)
    for k, v in data.items():
        setattr(s, k, v)
    db.session.commit()
    return s


def delete_stat(stat_id):
    s = Statistic.query.get(stat_id)
    if s:
        db.session.delete(s)
        db.session.commit()


# ── Site Settings ─────────────────────────────────────────────────────────────

def get_settings_dict():
    rows = SiteSetting.query.all()
    return {r.key: r.value for r in rows}


def get_all_settings():
    return SiteSetting.query.order_by(SiteSetting.key).all()


def set_setting(key, value):
    s = SiteSetting.query.filter_by(key=key).first()
    if s:
        s.value = value
    else:
        s = SiteSetting(key=key, value=value)
        db.session.add(s)
    db.session.commit()


def bulk_update_settings(data: dict):
    for key, value in data.items():
        set_setting(key, value)


# ── Media Files ───────────────────────────────────────────────────────────────

def get_media_files(file_type=None):
    q = MediaFile.query.order_by(MediaFile.uploaded_at.desc())
    if file_type:
        q = q.filter_by(file_type=file_type)
    return q.all()


def get_media_by_id(media_id):
    return MediaFile.query.get(media_id)


def create_media(filename, original_name, file_type, file_path) -> MediaFile:
    m = MediaFile(filename=filename, original_name=original_name,
                  file_type=file_type, file_path=file_path)
    db.session.add(m)
    db.session.commit()
    return m


def delete_media(media_id):
    m = MediaFile.query.get(media_id)
    if m:
        db.session.delete(m)
        db.session.commit()
    return m


# ── Admin ─────────────────────────────────────────────────────────────────────

def get_admin_by_id(admin_id):
    return Admin.query.get(int(admin_id))


def get_admin_by_username(username):
    return Admin.query.filter_by(username=username).first()
