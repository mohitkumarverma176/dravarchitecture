
import os, smtplib, ssl
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret")

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/projects")
def projects():
    return render_template("projects.html")

@app.get("/project-single")
def project_single():
    return render_template("project-single.html")

@app.get("/services")
def services():
    return render_template("services.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip()
        phone = request.form.get("phone","").strip()
        subject = request.form.get("subject","").strip() or "New Contact Form Message"
        message = request.form.get("message","").strip()

        if not name or not email or not message:
            flash("Please fill in Name, Email, and Message.", "error")
            return redirect(url_for("contact"))

        body = """New contact form submission:

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject}

Message:
{message}
""".format(name=name, email=email, phone=phone, subject=subject, message=message)

        try:
            send_email(
                recipient=os.environ.get("CONTACT_RECIPIENT", "smartmohitverma@gmail.com"),
                subject=f"[Website] {subject}",
                body=body
            )
            flash("Thanks! Your message has been sent.", "success")
        except Exception as e:
            flash(f"Sorry, something went wrong: {e}", "error")

        return redirect(url_for("contact"))
    return render_template("contact.html")

def send_email(recipient: str, subject: str, body: str):
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    sender = os.environ.get("SMTP_SENDER", smtp_user)

    if not (smtp_user and smtp_pass and sender):
        raise RuntimeError("SMTP credentials not set. Please set SMTP_USER, SMTP_PASS, and SMTP_SENDER env vars.")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
