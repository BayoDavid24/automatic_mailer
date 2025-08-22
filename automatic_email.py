from dotenv import load_dotenv
load_dotenv()
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import os   # NEW: for environment variables

now = datetime.datetime.now()

content = ''


def extract_news(url):
    print('Extracting Nairaland News Stories...')
    cnt = '<b>NL TOP STORIES:</b><br>' + '-'*50 + '<br/>'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')

    # Grab only the top story links
    for i, tag in enumerate(soup.select('a[href^="https://www.nairaland.com/"]')[:10]):  
        text = tag.get_text(" ", strip=True)   # combines inner <b> text nicely
        link = tag['href']
        if text:
            cnt += f"{i}. <a href='{link}'>{text}</a><br>"
    return cnt


cnt = extract_news('https://www.nairaland.com/')
content += cnt
content += ('<br>------------<br>')
content += ('<br><br> End of Message') 

print('Composing Email...')

# ✅ Read from environment variables instead of hardcoding
SERVER = 'smtp.gmail.com'
PORT = 587
FROM_EMAIL: ${{ secrets.FROM_EMAIL }}
TO_EMAIL:   ${{ secrets.TO_EMAIL }}
EMAIL_PASS: ${{ secrets.EMAIL_PASS }}


Once these secrets are set, re-run the workflow and it should proceed without this error.

if not FROM or not TO or not PASS:
    raise ValueError("⚠️ Missing email credentials. Please set FROM_EMAIL, TO_EMAIL, and EMAIL_PASS.")

msg = MIMEMultipart()
msg['Subject'] = f'Top News Stories NL [Automated Email] {now.day}-{now.month}-{now.year}'
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()

server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent...')
server.quit()
