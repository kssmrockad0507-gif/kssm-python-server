import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# -------- SETTINGS --------
GEMINI_API_KEY = "PUT_NEW_API_KEY_HERE"
SENDER_EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "gmail_app_password"
BLOGGER_EMAIL = "yourblog@blogger.com"


# -------- GENERATE CONTENT --------
def generate_content():

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{
                "text": "மாணவர்களுக்கான ஒரு கல்வி தகவலை தமிழில் 150 வார்த்தைகளில் எழுதவும்."
            }]
        }]
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    # SAFE RESPONSE CHECK
    if "candidates" not in result:
        return None, str(result)

    content = result["candidates"][0]["content"]["parts"][0]["text"]

    return content, None


# -------- SEND TO BLOGGER --------
def send_to_blogger(content):

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = BLOGGER_EMAIL
    msg['Subject'] = "KSSM ROCK TAMIL - AI Post"

    msg.attach(MIMEText(content, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()


# -------- MAIN ROUTE --------
@app.route("/")
def home():

    content, error = generate_content()

    if error:
        return f"<h1>Gemini Error</h1><pre>{error}</pre>"

    send_to_blogger(content)

    return "<h1>✅ Post Sent to Blogger Successfully!</h1>"


# -------- SERVER START --------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
