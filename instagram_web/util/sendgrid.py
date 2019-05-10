import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import SENGRID_API_KEY


def send_email():
    message = Mail(
        from_email='sandraoverlord@nextagram.com',
        to_emails=email,
        subject='Congrats! Donation Received',
        html_content='You have received a donation!')
    try:
        sg = SendGridAPIClient(SENGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
