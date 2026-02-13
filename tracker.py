import requests
from bs4 import BeautifulSoup
import smtplib
import os

def get_price(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Using the Meta Tag method we discussed, as it's more reliable
    price_tag = soup.find("meta", property="og:price:amount")
    if price_tag:
        return price_tag["content"]
    return "Price not found"

def send_email(report_content):
    email_user = os.environ.get('EMAIL_USER')
    email_pass = os.environ.get('EMAIL_PASS')
    
    subject = "Daily Price Tracker Report"
    body = f"Subject: {subject}\n\n{report_content}"
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_user, email_pass)
        server.sendmail(email_user, email_user, body)

# --- THE "ENGINE" ---
if __name__ == "__main__":
    items = [
        "https://bjjfanatics.com/products/the-anti-wrestling-equation-by-craig-jones",
        # Add your other 4 URLs here...
    ]
    
    full_report = "Here are your daily prices:\n\n"
    
    for url in items:
        price = get_price(url)
        full_report += f"Item: {url}\nPrice: {price}\n\n"
    
    print(full_report) # This helps you see it in GitHub Action logs
    send_email(full_report)
  
