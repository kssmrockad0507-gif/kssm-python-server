import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# விபரங்கள் (சரியாக உள்ளன)
GEMINI_API_KEY = "AIzaSyA7dYLknwTxKbYntHgXeYURQ8lR2fO-45s"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com"
APP_PASSWORD = "guwf pshu zzgt fgrj"
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com"

def generate_and_send():
    try:
        # மாடல் பெயரில் 'latest' சேர்க்கப்பட்டுள்ளது - இதுதான் 404 எரரைத் தீர்க்கும்
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts":[{"text": "மாணவர்களுக்கான ஒரு பொது அறிவுத் தகவலை தமிழில் சுருக்கமாக எழுதவும்."}]}]
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if 'candidates' in result:
            content = result['candidates'][0]['content']['parts'][0]['text']
            
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = BLOGGER_EMAIL
            msg['Subject'] = "KSSM AI Special Update"
            msg.attach(MIMEText(content, "plain", "utf-8"))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
            server.quit()
            return "Success"
        else:
            return f"Google Reply: {str(result)}"
            
    except Exception as e:
        return f"System Error: {str(e)}"

@app.route('/')
def home():
    status = generate_and_send()
    if status == "Success":
        return "<h1>✅ வெற்றி!</h1> பிளாக்கரை செக் பண்ணுங்க ப்ரோ!"
    else:
        return f"<h1>தோல்வி!</h1> காரணம்: {status}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
