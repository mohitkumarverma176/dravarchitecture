from datetime import datetime
from flask_login import UserMixin
from database import db


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def get_id(self):
        return str(self.id)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))            # filter key: landscape, architecture, institutional
    category_display = db.Column(db.String(100))   # e.g. "Landscape Design"
    location = db.Column(db.String(200))
    client = db.Column(db.String(200))
    area_sqft = db.Column(db.String(100))
    year = db.Column(db.Integer)
    services_provided = db.Column(db.String(300))
    status = db.Column(db.String(50), default='Completed')
    cover_image = db.Column(db.String(300))        # relative path from static/, e.g. "images/img_1.jpg"
    is_featured = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('ProjectImage', backref='project',
                             cascade='all, delete-orphan',
                             order_by='ProjectImage.display_order')
    pdfs = db.relationship('ProjectPDF', backref='project',
                           cascade='all, delete-orphan')

    @property
    def cover_image_url(self):
        return self.cover_image or 'images/img_1.jpg'


class ProjectImage(db.Model):
    __tablename__ = 'project_image'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    caption = db.Column(db.String(300))
    display_order = db.Column(db.Integer, default=0)


class ProjectPDF(db.Model):
    __tablename__ = 'project_pdf'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    label = db.Column(db.String(200))


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon_class = db.Column(db.String(100), default='flaticon-compass')
    image_filename = db.Column(db.String(300))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class HeroSlide(db.Model):
    __tablename__ = 'hero_slide'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    heading = db.Column(db.String(300))
    subheading = db.Column(db.String(500))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class TeamMember(db.Model):
    __tablename__ = 'team_member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200))
    bio = db.Column(db.Text)
    photo_filename = db.Column(db.String(300))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Testimonial(db.Model):
    __tablename__ = 'testimonial'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200))
    text = db.Column(db.Text, nullable=False)
    initials = db.Column(db.String(10))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Statistic(db.Model):
    __tablename__ = 'statistic'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0)
    suffix = db.Column(db.String(20), default='')
    display_order = db.Column(db.Integer, default=0)


class SiteSetting(db.Model):
    __tablename__ = 'site_setting'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    label = db.Column(db.String(200))
    setting_type = db.Column(db.String(50), default='text')  # text, html, email, phone, url


class MediaFile(db.Model):
    __tablename__ = 'media_file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    original_name = db.Column(db.String(300))
    file_type = db.Column(db.String(20))     # image, pdf, other
    file_path = db.Column(db.String(500))    # relative path from static/, e.g. "uploads/images/abc.jpg"
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
