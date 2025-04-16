'''import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASS = os.getenv("EMAIL_PASS")

def send_email(to_address, subject, html):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))

    server = smtpllib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, PASS)
    server.send_message(msg)
    server.quit()'''




import smtplib  
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASS = os.getenv("EMAIL_PASS")

def send_email(to_address, subject, html):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(html, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, PASS)
    server.send_message(msg)
    server.quit()
