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
    # The list
    items = {
        "Open Guard": "https://bjjfanatics.com/products/new-wave-jiu-jitsu-open-guard-vol-2-sweeps-and-reversals-by-john-danaher",
        "Ageless top":"https://bjjfanatics.com/products/ajj-top",
        "Anaconda attach - Danaher":"https://bjjfanatics.com/products/master-the-move-the-anaconda-strangle-by-john-danaher",
        "Arm Drags - Danaher":"https://bjjfanatics.com/collections/instructional-videos/products/master-the-move-arm-drags-by-john-danaher",
        "Leg Locks - Danaher":"https://bjjfanatics.com/collections/instructional-videos/products/leglocks-enter-the-system-by-john-danaher",
        "K-Guard - Mikey Musumeci":"https://bjjfanatics.com/collections/instructional-videos/products/k-guard-and-matrix-system-attacking-the-legs-from-the-knees-part-1-by-mikey-musumeci",
        "Head locks attach - Kaynan Duarte":"https://bjjfanatics.com/products/front-head-lock-control-submissions-and-transitions-by-kaynan-duarte",
        "Butterfly - Giancarlo":"https://bjjfanatics.com/collections/instructional-videos/products/efficiently-executing-from-butterfly-guard-by-giancarlo-bodoni",
        "Leg-lock defense - Giancarlo":"https://bjjfanatics.com/collections/instructional-videos/products/leg-lock-defense-survive-and-escape-by-giancarlo-bodoni",
        "Pin Escapes Gordon Ryan": "https://bjjfanatics.com/collections/instructional-videos/products/the-pillars-of-defense-pin-escapes-defensive-to-offensive-cycles-by-gordon-ryan",
        "Head lock escapes":"https://bjjfanatics.com/collections/instructional-videos/products/the-foundation-of-defense-turtle-front-headlock-escapes-by-gordon-ryan",
        "Guillotine Attack - Gordon Ryan":"https://bjjfanatics.com/collections/instructional-videos/products/systematically-attacking-the-guillotine-by-gordon-ryan",
        "Attacking Half Guard - Gordon Ryan": "https://bjjfanatics.com/collections/instructional-videos/products/systematically-attacking-the-guard-half-guard-passing-by-gordon-ryan",
        "Open Guard Seated - Gordon Ryan": "https://bjjfanatics.com/collections/instructional-videos/products/systematically-attacking-from-open-guard-seated-position-by-gordon-ryan",
        "Open Guard Supine - Gordon Ryan": "https://bjjfanatics.com/collections/instructional-videos/products/systematically-attacking-from-open-guard-supine-position-by-gordon-ryan",
        "Leglock Escapes and Counter Locks - Gordon Ryan":"https://bjjfanatics.com/collections/instructional-videos/products/the-pillars-of-defense-leg-lock-escapes-and-counter-locks-by-gordon-ryan",
        "Leglocks Escapes to guard passing - Gordon Ryan":"https://bjjfanatics.com/collections/instructional-videos/products/the-pillars-of-defense-leglocks-to-guard-passing-by-gordon-ryan",
        "Leglocks Defense to back takes - Gordon Ryab" : "https://bjjfanatics.com/collections/instructional-videos/products/pillars-of-defense-leg-locks-to-back-takes-by-gordon-ryan"
        
    }
    
    full_report = "Here are your daily prices:\n\n"
    
    for name, url in items.items():
        price = get_price(url)
        full_report += f"{name}: {price} Click:{url}\n\n"
    
    # print(full_report)
    send_email(full_report)
  
