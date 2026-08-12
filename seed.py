"""
Run once to populate the database with current hardcoded site content.
Usage: python seed.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

from app import app
from database import db
from models import Admin, Project, ProjectImage, Service, HeroSlide, TeamMember, Testimonial, Statistic, SiteSetting
from auth_utils import hash_password

ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'drav@2024')


def seed():
    with app.app_context():
        db.create_all()

        # ── Admin ──────────────────────────────────────────────────────────
        if not Admin.query.first():
            db.session.add(Admin(
                username=ADMIN_USER,
                password_hash=hash_password(ADMIN_PASS)
            ))
            db.session.commit()
            print(f'Admin created: {ADMIN_USER}')

        # ── Hero Slides ────────────────────────────────────────────────────
        if not HeroSlide.query.first():
            slides = [
                ('images/img_2.jpg', 0),
                ('images/img_3.jpg', 1),
                ('images/img_5.jpg', 2),
            ]
            for filename, order in slides:
                db.session.add(HeroSlide(filename=filename, display_order=order, is_active=True))
            db.session.commit()
            print('Hero slides seeded.')

        # ── Statistics ─────────────────────────────────────────────────────
        if not Statistic.query.first():
            stats = [
                ('Years of Experience', 10, '', 0),
                ('Projects Completed', 50, '', 1),
                ('States Served', 8, '', 2),
                ('% Client Satisfaction', 100, '%', 3),
            ]
            for label, value, suffix, order in stats:
                db.session.add(Statistic(label=label, value=value, suffix=suffix, display_order=order))
            db.session.commit()
            print('Statistics seeded.')

        # ── Services ───────────────────────────────────────────────────────
        if not Service.query.first():
            services = [
                ('Architecture Design',
                 'We design residential, commercial, and institutional buildings with a focus on functional efficiency, structural integrity, and aesthetic excellence — tailored to each site and client.',
                 'flaticon-compass', 'images/img_7.jpg', 0),
                ('Landscape Design',
                 'Our landscape practice creates outdoor environments that enhance community life and ecological resilience. Parks, gardens, recreational amenities, and green infrastructure for large housing developments and urban settings.',
                 'flaticon-plan', 'images/img_2.jpg', 1),
                ('Interior Design',
                 'Interiors that balance comfort, functionality, and aesthetic character. From space planning and furniture layouts to material palettes and lighting — our interiors reflect the identity of the people who inhabit them.',
                 'flaticon-architect', 'images/img_3.jpg', 2),
                ('Engineering & Structural Plans',
                 'Precise engineering drawings and structural plans that coordinate all disciplines — civil, structural, and MEP — ensuring designs are fully buildable, code-compliant, and efficiently executed on site.',
                 'flaticon-wall', 'images/img_4.jpg', 3),
                ('3D Visualization & Rendering',
                 'Photorealistic 3D renderings and walkthrough animations that allow clients to experience their project before construction begins — enabling informed decisions and confident approvals at every design stage.',
                 'flaticon-compass', 'images/img_5.jpg', 4),
                ('Floor Plans & Site Layouts',
                 'Clear, dimensioned floor plans and site layout drawings that communicate design intent effectively to clients, contractors, and statutory bodies — the foundation of every successful project.',
                 'flaticon-plan', 'images/img_6.jpg', 5),
            ]
            for title, desc, icon, img, order in services:
                db.session.add(Service(
                    title=title, description=desc, icon_class=icon,
                    image_filename=img, display_order=order, is_active=True
                ))
            db.session.commit()
            print('Services seeded.')

        # ── Team Members ───────────────────────────────────────────────────
        if not TeamMember.query.first():
            members = [
                ('Principal Architect', 'Founder & Design Lead',
                 'Leads architectural design and client relationships with over a decade of experience.',
                 'images/person_1.jpg', 0),
                ('Landscape Architect', 'Head of Landscape',
                 'Specialises in large-scale landscape masterplans for parks, housing communities, and campuses.',
                 'images/person_2.jpg', 1),
                ('Interior Designer', 'Head of Interiors',
                 'Brings spaces to life through material selection, spatial planning, and considered lighting design.',
                 'images/person_3.jpg', 2),
                ('Structural Engineer', 'Engineering Consultant',
                 'Ensures structural soundness and code compliance, coordinating closely with the design team.',
                 'images/person_4.jpg', 3),
            ]
            for name, role, bio, photo, order in members:
                db.session.add(TeamMember(
                    name=name, role=role, bio=bio,
                    photo_filename=photo, display_order=order, is_active=True
                ))
            db.session.commit()
            print('Team members seeded.')

        # ── Testimonials ───────────────────────────────────────────────────
        if not Testimonial.query.first():
            testimonials = [
                ('Mr. Sunil Munirika', 'Residential Client, Darbhanga', 'SM',
                 'The team at Drav Architecture understood exactly what we wanted for our home. They were attentive, professional, and delivered a design that exceeded our expectations. The attention to detail in both the exterior elevations and the interior layouts was outstanding.',
                 0),
                ('Project Manager', 'Amrapali Group, Prayagraj', 'AM',
                 "Drav Architecture's landscape designs for our housing communities have been received extremely well by residents. Their ability to integrate recreational amenities, greenery, and pedestrian-friendly pathways into tight urban sites is impressive.",
                 1),
                ('Site Director', 'SDRF Campus, Ayodhya', 'SD',
                 'The landscape masterplan for our campus struck the right balance between functional infrastructure and natural greenery. The Miyawaki forest and reflexology paths are particularly appreciated. Great work by the Drav team.',
                 2),
            ]
            for name, company, initials, text, order in testimonials:
                db.session.add(Testimonial(
                    client_name=name, company=company, initials=initials,
                    text=text, display_order=order, is_active=True
                ))
            db.session.commit()
            print('Testimonials seeded.')

        # ── Projects ───────────────────────────────────────────────────────
        if not Project.query.first():
            projects_data = [
                {
                    'title': 'Urban Woods',
                    'slug': 'urban-woods',
                    'description': 'A large-scale urban landscape project integrating greenery, pedestrian pathways, and recreational spaces within a dense residential community in Lucknow.',
                    'category': 'landscape',
                    'category_display': 'Landscape Design',
                    'location': 'Lucknow, Uttar Pradesh',
                    'client': 'Urban Axis',
                    'services_provided': 'Landscape Design',
                    'status': 'Completed',
                    'cover_image': 'images/img_8.jpg',
                    'is_featured': True,
                    'display_order': 0,
                },
                {
                    'title': 'Amaravati Midtown Housing',
                    'slug': 'amaravati-midtown-housing',
                    'description': 'Landscape masterplan for Amaravati Midtown Housing — integrating ecology, recreation, and visual delight across the residential township.',
                    'category': 'landscape',
                    'category_display': 'Landscape Design',
                    'location': 'Lucknow, Uttar Pradesh',
                    'client': 'Amaravati Developers',
                    'services_provided': 'Landscape Design',
                    'status': 'Completed',
                    'cover_image': 'images/img_2.jpg',
                    'is_featured': True,
                    'display_order': 1,
                },
                {
                    'title': 'Amrapali Leisure Park',
                    'slug': 'amrapali-leisure-park',
                    'description': 'Comprehensive landscape design for Amrapali Leisure Park — creating community-focused outdoor spaces for residents in Prayagraj.',
                    'category': 'landscape',
                    'category_display': 'Landscape Design',
                    'location': 'Prayagraj, UP',
                    'client': 'Amrapali Group',
                    'services_provided': 'Landscape Design',
                    'status': 'Completed',
                    'cover_image': 'images/img_3.jpg',
                    'is_featured': True,
                    'display_order': 2,
                },
                {
                    'title': 'Amrapali Golf Homes & Kingswood',
                    'slug': 'amrapali-golf-homes-kingswood',
                    'description': 'Landscape design for premium golf-fronting residential township in Prayagraj, integrating golf course edges with residential green spaces.',
                    'category': 'landscape',
                    'category_display': 'Landscape Design',
                    'location': 'Prayagraj, UP',
                    'client': 'Amrapali Group',
                    'services_provided': 'Landscape Design',
                    'status': 'Completed',
                    'cover_image': 'images/img_4.jpg',
                    'is_featured': True,
                    'display_order': 3,
                },
                {
                    'title': 'Amrapali Centurian Park',
                    'slug': 'amrapali-centurian-park',
                    'description': 'Landscape design and site planning for Amrapali Centurian Park residential development in Ayodhya.',
                    'category': 'landscape',
                    'category_display': 'Landscape Design',
                    'location': 'Ayodhya, UP',
                    'client': 'Amrapali Group',
                    'services_provided': 'Landscape Design',
                    'status': 'Completed',
                    'cover_image': 'images/img_5.jpg',
                    'is_featured': True,
                    'display_order': 4,
                },
                {
                    'title': 'SDRF Campus Landscape',
                    'slug': 'sdrf-campus-landscape',
                    'description': 'Institutional campus landscape design for SDRF (State Disaster Response Force) in Ayodhya — featuring Miyawaki forest, reflexology paths, and functional green infrastructure.',
                    'category': 'institutional',
                    'category_display': 'Institutional',
                    'location': 'Ayodhya, UP',
                    'client': 'State Disaster Response Force, UP',
                    'services_provided': 'Landscape Design',
                    'status': 'Completed',
                    'cover_image': 'images/img_6.jpg',
                    'is_featured': True,
                    'display_order': 5,
                },
                {
                    'title': 'Munirika Residence',
                    'slug': 'munirika-residence',
                    'description': 'A landmark residential project demonstrating Drav Architecture\'s expertise in blending modern design sensibilities with practical living requirements. The project encompasses architectural planning, landscape design, and interior coordination.',
                    'category': 'architecture',
                    'category_display': 'Residential Architecture',
                    'location': 'Darbhanga, Bihar',
                    'client': 'Mr. Sunil Munirika',
                    'services_provided': 'Architecture + Landscape',
                    'status': 'Completed',
                    'cover_image': 'images/img_7.jpg',
                    'is_featured': True,
                    'display_order': 6,
                },
                {
                    'title': 'Star Flour Mill',
                    'slug': 'star-flour-mill',
                    'description': 'Commercial architecture and facility planning for Star Flour Mill in Pandaul, Bihar — combining functional industrial design with clean aesthetics.',
                    'category': 'architecture',
                    'category_display': 'Commercial Architecture',
                    'location': 'Pandaul, Bihar',
                    'client': 'Star Industries',
                    'services_provided': 'Architecture Design + Engineering Plans',
                    'status': 'Completed',
                    'cover_image': 'images/img_8.jpg',
                    'is_featured': False,
                    'display_order': 7,
                },
                {
                    'title': 'Farm House Landscape',
                    'slug': 'farm-house-landscape',
                    'description': 'Landscape design for a private farm house in Lucknow — integrating productive gardens, ornamental planting, and outdoor entertaining spaces.',
                    'category': 'landscape',
                    'category_display': 'Landscape Design',
                    'location': 'Lucknow, UP',
                    'client': 'Private Client',
                    'services_provided': 'Landscape Design',
                    'status': 'Completed',
                    'cover_image': 'images/img_2.jpg',
                    'is_featured': False,
                    'display_order': 8,
                },
            ]
            for p_data in projects_data:
                db.session.add(Project(**p_data))
            db.session.commit()
            print(f'{len(projects_data)} projects seeded.')

        # ── Site Settings ──────────────────────────────────────────────────
        if not SiteSetting.query.first():
            settings = {
                'contact_phone': '+91 88788 60664',
                'contact_email': 'dravarchitecture@outlook.com',
                'contact_whatsapp': '918878860664',
                'contact_address': 'India — Pan-India Projects',
                'footer_tagline': 'A multidisciplinary design studio specialising in Architecture, Landscape Design, and Interior Planning. Creating spaces that endure — across India.',
                'social_instagram': '#',
                'social_linkedin': '#',
                'social_facebook': '#',
                'about_headline': 'Architecture & Landscape, Unified.',
                'about_body': 'Drav Architecture is a multidisciplinary design studio rooted in the belief that great design improves lives. We bring together architecture, landscape, and interior expertise to create spaces that are both beautiful and deeply functional.',
                'philosophy_text': 'At Drav Architecture, we believe that the built environment profoundly shapes human experience. Our work begins with rigorous site analysis and deep listening to our clients — understanding not just what they want to build, but how they want to live.',
                'mission_text': 'To create architecture and landscapes that enrich lives, strengthen communities, and respect the natural environment.',
                'vision_text': "To be India's most trusted multidisciplinary design studio, known for integrity, innovation, and lasting impact.",
            }
            for key, value in settings.items():
                db.session.add(SiteSetting(key=key, value=value))
            db.session.commit()
            print('Site settings seeded.')

        print('\nSeed complete.')
        print(f'  Admin login: {ADMIN_USER} / {ADMIN_PASS}')
        print('  Run: flask run  (or python app.py)')
        print('  Admin panel: http://localhost:5000/admin')


if __name__ == '__main__':
    seed()
