import requests
from bs4 import BeautifulSoup
import smtplib
import os

email_user = os.environ.get('EMAIL_USER')
email_pass = os.environ.get('EMAIL_PASS')


def check_price(url):
    headers = {"User-Agent": "Mozilla/5.0"} # Prevents some sites from blocking you
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # You'll need to find the specific ID for each site
    price = soup.find(id="priceblock_ourprice").get_text()
    return price

def send_email(report):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("EMAIL_USER", "enter-app-password")
    server.sendmail("EMAIL_USER", "EMAIL_USER", report)
  
