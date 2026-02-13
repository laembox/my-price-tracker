import requests
from lxml import html
import smtplib
import os

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        # Convert the page content into a searchable tree
        tree = html.fromstring(response.content)
        
        # Use your specific XPath
        # .xpath returns a list, so we take the first element [0]
        price_element = tree.xpath("//*[@id='ProductPrice-price-value']")
        
        if price_element:
            return price_element[0].text_content().strip()
        return "Price element not found"
    except Exception as e:
        return f"Error: {e}"

def send_email(report_content):
    email_user = os.environ.get('EMAIL_USER')
    email_pass = os.environ.get('EMAIL_PASS')
    
    subject = "Daily Price Tracker Report"
    # Basic email formatting
    body = f"Subject: {subject}\n\n{report_content}"
    
    # Using Port 465 for SSL (Standard for Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email_user, email_pass)
        server.sendmail(email_user, email_user, body)

if __name__ == "__main__":
    items = {
        "Anti-Wrestling": "https://bjjfanatics.com/products/the-anti-wrestling-equation-by-craig-jones",
        "Ageless top game": "https://bjjfanatics.com/products/ageless-jiu-jitsu-winning-when-youre-older-or-less-athletic-top-game-gi-by-john-danaher",
        # Add your other 4 URLs here
    }
    
    full_report = "Here are your daily prices:\n\n"
    
    for name, url in items:
        price = get_price(url)
        full_report += f"Item: {name} Price: {price}\n\n"
    
    # print(full_report)
    send_email(full_report)
  
