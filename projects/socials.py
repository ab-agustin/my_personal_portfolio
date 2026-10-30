import os
import smtplib
from email.message import EmailMessage
from flask import render_template, request


def register_socials(app):

    facebook = "https://www.facebook.com/atashabernadette.agustin/"
    instagram = "https://www.instagram.com/yoolovr_ash/"
    linkedin = "https://www.linkedin.com/in/atasha-bernadette-agustin-30907b445/"
    email = os.environ.get("GMAIL_ADDRESS", "")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        success = None
        error = None

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            sender_email = request.form.get("email", "").strip()
            subject = request.form.get("subject", "").strip()
            message = request.form.get("message", "").strip()

            if not all([name, sender_email, subject, message]):
                error = "Please complete all fields."

            else:
                gmail_address = os.environ.get("GMAIL_ADDRESS")
                gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

                if not gmail_address or not gmail_password:
                    error = (
                        "Email sending is currently unavailable. "
                        "Please contact me through my social media links."
                    )

                else:
                    email_message = EmailMessage()
                    email_message["Subject"] = f"Portfolio Contact: {subject}"
                    email_message["From"] = gmail_address
                    email_message["To"] = gmail_address
                    email_message["Reply-To"] = sender_email

                    email_message.set_content(
                        f"New message from your portfolio website\n\n"
                        f"Name: {name}\n"
                        f"Email: {sender_email}\n"
                        f"Subject: {subject}\n\n"
                        f"Message:\n{message}"
                    )

                    try:
                        with smtplib.SMTP_SSL(
                            "smtp.gmail.com", 465
                        ) as server:
                            server.login(gmail_address, gmail_password)
                            server.send_message(email_message)

                        success = "Your message was sent successfully!"

                    except Exception:
                        app.logger.exception("Email sending failed")
                        error = (
                            "Sorry, the message could not be sent. "
                            "Please try again later."
                        )

        return render_template(
            "contact.html",
            facebook=facebook,
            instagram=instagram,
            linkedin=linkedin,
            email=email,
            success=success,
            error=error
        )

