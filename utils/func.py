import datetime
from email import encoders
from email.mime.base import MIMEBase
import json
import os
import random
import string

def generateRandomString(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))

def generateCapitalReferralCode():
    return generateRandomString(6).upper()

def generateVerificationCode():
    return generateRandomString(64)

def send_project_generation_report(email: str, file_paths: list[str], status: str = "success", extra_message: str = ""):
    username = "no-reply-tietprojreport@skullzbones.com"
    password = "<Secret>"
    smtp_server = "mail.skullzbones.com"
    port = 587  # For SSL

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = username
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = f"[{status}] Report | Generation Report"
    message["From"] = sender_email
    message["To"] = receiver_email

    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(f.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(file_path)}"')
            message.attach(mime_base)

    text = f"Attached below are the project generation report and data, Generated at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n" + extra_message

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def send_user_feedback_email(all_data_dict: dict):
    username = "no-reply-tietprojreport@skullzbones.com"
    password = "<Secret>"
    smtp_server = "mail.skullzbones.com"
    port = 587  # For SSL

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = username
    receiver_email = "hari01584@gmail.com"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"[tietprojgen] Feedback Received | {all_data_dict['name']}"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""\
    Hi,
    Feedback received from {all_data_dict['name']} ({all_data_dict['email']}):
    {all_data_dict['feedback']}

    {json.dumps(all_data_dict, indent=2)}
    """

    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Feedback received from {all_data_dict['name']} ({all_data_dict['email']}):<br>
        {all_data_dict['feedback']}<br>
        <br>
        {json.dumps(all_data_dict, indent=2)}
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def send_verification_email(email, verification_code, hook_domain):
    username = "no-reply-tietprojreport@skullzbones.com"
    password = "<Secret>"
    smtp_server = "mail.skullzbones.com"
    port = 587  # For SSL

    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = username
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email address | TietProjReport"
    message["From"] = sender_email
    message["To"] = receiver_email

    verification_link = f"{hook_domain}/Verify_Code&verification_code={verification_code}"

    text = f"""\
    Hi,
    Thank you for signing up! Please verify your email address by clicking the link below:
    {verification_link}

    If you did not sign up for this account, please ignore this email.
    Best regards,
    Your Company
    """

    # Create the plain-text and HTML version of your message
    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Thank you for signing up! Please verify your email address by clicking the link below: <a href="{verification_link}">Verify your email</a><br>
        If you did not sign up for this account, please ignore this email.<br>
        <br>
        Best regards,<br>
        Your Company
        </p>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

# if __name__ == '__main__':
#     send_verification_email("hari01584@gmail.com", "123456", "http://localhost:8501")