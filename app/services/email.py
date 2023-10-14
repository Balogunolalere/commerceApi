import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.config import settings
from pydantic import EmailStr

# Define a smtp instance with the admin email and password
smtp = smtplib.SMTP_SSL(settings.email_host, settings.email_port)
smtp.login(settings.email_username, settings.email_password)



# Define a function to send a verification email given an email and a token
async def send_verification_email(email: EmailStr, token: str):
    # Create a verification link with the token as a query parameter
    link = f"{settings.app_url}/verify/{token}"
    # Create a message schema with the email, subject, body, and subtype
    message = MIMEMultipart('alternative')
    message['Subject'] = "Verify your email"
    message['From'] = settings.admin_email
    message['To'] = email
    html = f"""\
    <html>
        <head></head>
        <body>
            <p>Hello, please click on the link below to verify your email:</p>
            <p><a href="{link}">{link}</a></p>
        </body>
    </html>
    """
    part = MIMEText(html, 'html')
    message.attach(part)
    # Send the message using the smtp
    smtp.send_message(message)
    smtp.quit()
    

# Define a function to send a password reset email given an email and a token
async def send_password_reset_email(email: EmailStr, token: str):
    # Create a password reset link with the token as a query parameter
    link = f"{settings.app_url}/reset-password/{token}"
    # Create a message schema with the email, subject, body, and subtype
    message = MIMEMultipart('alternative')
    message['Subject'] = "Reset your password"
    message['From'] = settings.admin_email
    message['To'] = email
    html = f"""\
    <html>
        <head></head>
        <body>
            <p>Hello, please click on the link below to reset your password:</p>
            <p><a href="{link}">{link}</a></p>
        </body>
    </html>
    """
    part = MIMEText(html, 'html')
    message.attach(part)
    # Send the message using the smtp
    smtp.send_message(message)
    smtp.quit()

# Define a function to send an order confirmation email given an email and an order id
async def send_order_confirmation_email(email: EmailStr, order_id: str):
    # Create an order details link with the order id as a query parameter
    link = f"{settings.app_url}/order-details/{order_id}"
    # Create a message schema with the email, subject, body, and subtype
    message = MIMEMultipart('alternative')
    message['Subject'] = "Order confirmation"
    message['From'] = settings.admin_email
    message['To'] = email
    html = f"""\
    <html>
        <head></head>
        <body>
            <p>Hello, please click on the link below to view your order details:</p>
            <p><a href="{link}">{link}</a></p>
        </body>
    </html>
    """
    part = MIMEText(html, 'html')
    message.attach(part)
    # Send the message using the smtp
    smtp.send_message(message)
    smtp.quit()
