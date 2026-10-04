import smtplib
import requests
import os
from email.mime.text import MIMEText
from email.utils import formataddr

# Берём данные из Secrets
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
to_email = os.getenv("TO_EMAIL")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

# Проверяем, что все секреты есть
if not all([email, password, to_email, GIPHY_API_KEY]):
    raise ValueError("Один или несколько секретов не настроены! Проверьте EMAIL, PASSWORD, TO_EMAIL, GIPHY_API_KEY")

# Получаем случайную гифку с GIPHY
url = "https://api.giphy.com/v1/gifs/random"
params = {
    "api_key": GIPHY_API_KEY,
    "tag": "love you",
    "rating": "pg"
}

response = requests.get(url, params=params)
data = response.json()

# Проверяем, что API вернул данные
if "data" in data and data["data"]:
    gif_url = data["data"]["images"]["original"]["url"]
else:
    # запасная гифка
    gif_url = "https://media.giphy.com/media/14uQ3cOFteDaU/giphy.gif"

# Формируем HTML письмо
html = f"""
<html>
  <body>
    <img src="{gif_url}" width="300">
  </body>
</html>
"""

msg = MIMEText(html, "html")
msg["Subject"] = "❤️"
msg["From"] = formataddr(("Your Alex", email))
msg["To"] = to_email

# Отправляем письмо через Gmail
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(email, password)
server.sendmail(email, to_email, msg.as_string())
server.quit()

print("Письмо отправлено")
