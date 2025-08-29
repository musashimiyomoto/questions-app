import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings.smtp import smtp_settings


def send_email(email: str, html_content: str, subject: str) -> None:
    """Send email to user

    Args:
        email: Email address to send the email to.
        html_content: HTML content of the email.
        subject: Subject of the email.

    """
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = smtp_settings.username
    message["To"] = email
    message.attach(payload=MIMEText(html_content, "html"))

    smtp_class = smtplib.SMTP_SSL if smtp_settings.ssl else smtplib.SMTP

    with smtp_class(host=smtp_settings.host, port=smtp_settings.port) as server:
        if smtp_settings.ssl:
            server.login(user=smtp_settings.username, password=smtp_settings.password)

        server.sendmail(
            from_addr=smtp_settings.username,
            to_addrs=email,
            msg=message.as_string(),
        )
