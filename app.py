import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# ---------- உங்கள் விபரங்கள் (ChatGPT API சேர்க்கப்பட்டுள்ளது) ----------
OPENAI_API_KEY = "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"

SENDER_EMAIL = "ttnswamidayananda1947@gmail.com"
APP_PASSWORD = "guwf pshu zzgt fgrj"
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com"

def generate_and_send():
    try:
        # ChatGPT API Endpoint
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        data = {
            "model": "gpt-4o-mini",  # இது வேகமாகவும் விலை குறைவாகவும் இருக்கும்
            "messages": [
                {"role": "system", "content": "You are a helpful educational assistant writing in Tamil."},
                {"role": "user", "content": "மாணவர்களுக்கான ஒரு முக்கியமான கல்வித் தகவலை அல்லது பொது அறிவுச் செய்தியை தமிழில் 150 வார்த்தைகளில் சுருக்கமாக எழுதவும்."}
            ]
        }
        
        # ChatGPT-யிடம் இருந்து கன்டென்ட் வாங்குதல்
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if 'choices' in result:
            content = result['choices'][0]['message']['content']
            
            # மெயில் அனுப்பும் பகுதி
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = BLOGGER_EMAIL
            msg['Subject'] = "KSSM AI Special Update (Powered by ChatGPT)"
            
            # தமிழ் எழுத்துக்கள் சரியாக வர utf-8
            msg.attach(MIMEText(content, "plain", "utf-8"))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
            server.quit()
            return "Success"
        else:
            return f"ChatGPT Error: {str(result)}"
            
    except Exception as e:
        return f"System Error: {str(e)}"

@app.route('/')
def home():
    status = generate_and_send()
    if status == "Success":
        return "<h1>✅ வெற்றி!</h1><p>ChatGPT மூலம் உங்கள் பிளாக்கருக்கு போஸ்ட் அனுப்பப்பட்டுவிட்டது!</p>"
    else:
        return f"<h1>தோல்வி!</h1><p>காரணம்: {status}</p>"

if __name__ == "__main__":
    # Render போர்ட் செட்டிங்ஸ்
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
