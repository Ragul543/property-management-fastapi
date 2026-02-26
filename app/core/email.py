import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


def send_email(to: str, subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["From"] = settings.smtp_user
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(settings.smtp_user, to, msg.as_string())


def send_enquiry_confirmation(enquiry, property_title: str):
    subject = f"Enquiry Received – {property_title}"
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px;border:1px solid #e0e0e0;border-radius:8px">
      <h2 style="color:#2c3e50">Thank you for your enquiry, {enquiry.name}!</h2>
      <p>We have received your enquiry for <strong>{property_title}</strong> and will get back to you shortly.</p>
      <table style="width:100%;border-collapse:collapse;margin:16px 0">
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Name</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.name}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Email</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.email}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Phone</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.phone}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Message</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.message or "—"}</td></tr>
      </table>
      <p style="color:#888;font-size:13px">If you did not submit this enquiry, please ignore this email.</p>
    </div>
    """
    send_email(enquiry.email, subject, html)


def send_enquiry_admin_notification(enquiry, property_title: str):
    subject = f"New Enquiry – {property_title} (from {enquiry.name})"
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:20px;border:1px solid #e0e0e0;border-radius:8px">
      <h2 style="color:#2c3e50">New Enquiry Received</h2>
      <p>A new enquiry has been submitted for <strong>{property_title}</strong>.</p>
      <table style="width:100%;border-collapse:collapse;margin:16px 0">
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Name</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.name}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Email</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.email}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Phone</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.phone}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Message</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.message or "—"}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Property</td><td style="padding:8px;border-bottom:1px solid #eee">{property_title}</td></tr>
        <tr><td style="padding:8px;border-bottom:1px solid #eee;color:#888">Status</td><td style="padding:8px;border-bottom:1px solid #eee">{enquiry.status}</td></tr>
      </table>
    </div>
    """
    send_email(settings.admin_email, subject, html)
