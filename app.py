import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# ---------- உங்களுடைய சரியான விபரங்கள் இங்கே ----------
GEMINI_API_KEY = "AIzaSyA7dYLknwTxKbYntHgXeYURQ8lR2fO-45s"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com"
APP_PASSWORD = "guwf pshu zzgt fgrj"
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com"

# ---------- AI கன்டென்ட் தயார் செய்யும் பகுதி ----------
def generate_content():
    # v1beta வெர்ஷன் நேரடி URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{
                "text": "மாணவர்களுக்கு உதவும் கல்வி தகவலை தமிழில் 150 வார்த்தைகளில் எழுதவும்."
            }]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        # எரர் செக்
        if "candidates" not in result:
            return None, str(result)

        content = result["candidates"][0]["content"]["parts"][0]["text"]
        return content, None
    except Exception as e:
        return None, str(e)

# ---------- பிளாக்கருக்கு மெயில் அனுப்பும் பகுதி ----------
def send_to_blogger(content):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = BLOGGER_EMAIL
    msg['Subject'] = "KSSM ROCK TAMIL - AI Auto Post"

    # தமிழில் எழுத்துக்கள் சரியாக வர utf-8 பயன்படுத்தப்பட்டுள்ளது
    msg.attach(MIMEText(content, "plain", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

# ---------- சர்வர் ரூட் (URL கிளிக் செய்தால் இது நடக்கும்) ----------
@app.route("/")
def home():
    content, error = generate_content()

    if error:
        return f"<h2>Gemini API Error</h2><pre>{error}</pre>"

    if content:
        try:
            send_to_blogger(content)
            return "<h1>✅ Blogger Auto Post Success!</h1><p>உங்க பிளாக்கரை செக் பண்ணுங்க ப்ரோ!</p>"
        except Exception as e:
            return f"<h2>Email Error</h2><pre>{str(e)}</pre>"
    
    return "<h2>Unknown Error Occurred</h2>"

# ---------- சர்வர் ஸ்டார்ட் ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
