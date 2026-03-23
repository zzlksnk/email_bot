import smtplib
import requests
from email.mime.text import MIMEText
from email.utils import formataddr

GIPHY_API_KEY = "GIPHY_API_KEY"
email = "EMAIL"
password = "PASSWORD"
to_email = "TO_EMAIL"

url = "https://api.giphy.com/v1/gifs/random"

params = {
    "api_key": GIPHY_API_KEY,
    "tag": "love you",
    "rating": "pg"
}

response = requests.get(url, params=params)
data = response.json()

gif_url = data["data"]["images"]["original"]["url"]

html = f"""
<html>
  <body>
    <img src="{gif_url}" width="300">
  </body>
</html>
"""

msg = MIMEText(html, "html")
msg["Subject"] = "❤️"
msg["From"] = formataddr(("Your pookie", email))
msg["To"] = to_email

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)
server.sendmail(email, to_email, msg.as_string())
server.quit()

print("Письмо отправлено")