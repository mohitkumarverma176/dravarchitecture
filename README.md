# Flask + Frontend (Drav Architecture)

This wraps your provided frontend with a Python (Flask) backend that emails contact form submissions to `smartmohitverma@gmail.com`.

## Local run
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_SECRET_KEY="change-me"
export CONTACT_RECIPIENT="smartmohitverma@gmail.com"
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="yourgmail@gmail.com"
export SMTP_PASS="your_app_password"   # Gmail App Password
export SMTP_SENDER="yourgmail@gmail.com"
python app.py

## GoDaddy (cPanel Python/Passenger)
1) Zip & upload this folder via File Manager.
2) Extract under your domain path (e.g., `flaskapp`).
3) cPanel -> **Setup Python App** -> Python 3.10+
   - Application root: path to this folder
   - Application startup file: `passenger_wsgi.py`
4) Add Environment Variables in the app UI:
   - FLASK_SECRET_KEY
   - CONTACT_RECIPIENT=smartmohitverma@gmail.com
   - SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_SENDER
5) Restart the application.
6) Put all assets (css, js, images, fonts) in `/static` keeping the same folder names.

Contact page route: `/contact` (GET shows page, POST sends email).
