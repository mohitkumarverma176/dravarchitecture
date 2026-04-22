# Drav Architecture — Website

A professional architecture and landscape design website for **Drav Architecture / Urban Axis**, built with Python (Flask) + Jinja2 templates + Bootstrap 5.

---

## Project Overview

- **Firm:** Drav Architecture (landscape consultancy wing: Urban Axis)
- **Services:** Architecture, Landscape Design, Interior Design, Engineering Planning, 3D Visualisation, Floor Plans
- **Project locations:** Lucknow, Greater Noida, Dehradun, New Delhi, Bihar
- **Backend:** Flask 3.0.3 with Flask-WTF (CSRF protection, contact form email)
- **Frontend:** Bootstrap 5, custom CSS (`drav-custom.css`), AOS animations, Tiny Slider carousels
- **Templates:** Full Jinja2 template inheritance via `base.html`

---

## Pages

| Route | Template | Description |
|---|---|---|
| `/` | `index.html` | Homepage — hero, stats, services, projects, CTA |
| `/about` | `about.html` | About page — mission/vision, process, team |
| `/services` | `services.html` | Services — 6 service cards, process, testimonials |
| `/projects` | `projects.html` | Portfolio — 9 real projects with filter |
| `/project-single` | `project-single.html` | Single project detail — Munirika Residence |
| `/single` | `single.html` | Article/insights page |
| `/contact` | `contact.html` | Contact form + info, sends email via SMTP |

---

## Local Setup

### Prerequisites

- Python 3.10+ (tested with Python 3.12)

### Install & Run

```bash
# 1. Clone / download the project
cd dravarchitecture

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 4. Install dependencies
python -m pip install -r requirements.txt

# 5. Create your .env file
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux

# 6. Edit .env and set your values (see below)

# 7. Run the dev server
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Environment Variables (`.env`)

```env
FLASK_SECRET_KEY=your-secret-key-here

# Contact form email recipient
CONTACT_RECIPIENT=smartmohitverma@gmail.com

# SMTP credentials (Gmail App Password recommended)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=yourgmail@gmail.com
SMTP_PASS=your_app_password
SMTP_SENDER=yourgmail@gmail.com
```

> **Note:** The contact form will fail gracefully if SMTP credentials are not set — it shows an error flash message but does not crash.

---

## Project Structure

```
dravarchitecture/
├── app.py                          # Flask routes and email logic
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .env                            # Your local env file (not committed)
├── passenger_wsgi.py               # WSGI entry point for cPanel/Passenger hosting
├── templates/
│   ├── base.html                   # Master layout (nav, footer, scripts)
│   ├── footer.html                 # Shared footer partial
│   ├── index.html                  # Homepage
│   ├── about.html                  # About page
│   ├── services.html               # Services page
│   ├── projects.html               # Projects portfolio
│   ├── project-single.html         # Single project detail
│   ├── single.html                 # Article / insights page
│   └── contact.html                # Contact form
└── static/
    ├── css/
    │   ├── style.css               # Original compiled theme CSS
    │   └── drav-custom.css         # Custom styles (stats bar, cards, CTA, etc.)
    ├── js/
    │   ├── custom.js               # Custom JS (stats counter, project filter)
    │   └── ...                     # Theme JS files
    ├── images/                     # Project and background images
    └── fonts/                      # Icon fonts (icomoon, flaticon)
```

---

## Deployment — GoDaddy (cPanel / Passenger)

1. Zip and upload this folder via cPanel File Manager.
2. Extract under your domain path (e.g., `public_html/dravarchitecture`).
3. In cPanel → **Setup Python App**:
   - Python version: 3.10+
   - Application root: path to this folder
   - Application startup file: `passenger_wsgi.py`
4. Add Environment Variables in the app UI:
   - `FLASK_SECRET_KEY`
   - `CONTACT_RECIPIENT`
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_SENDER`
5. Click **Restart**.

---

## Key Features

- **Jinja2 template inheritance** — single `base.html` for nav, footer, scripts; all pages extend it
- **Contact form** — POST to `/contact`, validates fields, sends email via SMTP with flash feedback
- **CSRF protection** — Flask-WTF on all POST routes
- **Animated stats counter** — IntersectionObserver triggers count-up animation when stats bar enters viewport
- **Project filter** — client-side JS filter by category (All / Landscape / Architecture / Institutional)
- **Floating WhatsApp CTA** — fixed bottom-right button linking to WhatsApp
- **AOS scroll animations** — fade-in effects on sections

---

## Credits

- Designed & developed by **Mohit Kumar Verma**
- Built for **Drav Architecture / Urban Axis**
