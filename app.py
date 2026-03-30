import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# விபரங்கள்
GEMINI_API_KEY = "AIzaSyCh8COUy-iRfaR45FrkJoYT6x215KlmM84"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com"
APP_PASSWORD = "guwf pshu zzgt fgrj"
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com"

def generate_and_send():
    try:
        # நேரடி API அழைப்பு (Direct API Call) - இது வெர்ஷன் பிரச்சனையைத் தீர்க்கும்
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{"parts":[{"text": "மாணவர்களுக்கான ஒரு பொது அறிவுத் தகவலை தமிழில் சுருக்கமாக எழுதவும்."}]}]
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # கன்டென்ட் எடுக்கும் முறை
        content = result['candidates'][0]['content']['parts'][0]['text']
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = "KSSM AI Education Post"
        msg.attach(MIMEText(content, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return "Success"
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    status = generate_and_send()
    if status == "Success":
        return "<h1>வெற்றி!</h1> பிளாக்கரைச் செக் பண்ணுங்க ப்ரோ!"
    else:
        return f"<h1>தோல்வி!</h1> எரர்: {status}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
