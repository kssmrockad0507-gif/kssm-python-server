import google.generativeai as genai
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# --- விபரங்களை நேரடியாக இங்கே கொடுக்கவும் (Testing Purpose) ---
GEMINI_API_KEY = "AIzaSyCh8COUy-iRfaR45FrkJoYT6x215KlmM84"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com"
APP_PASSWORD = "guwf pshu zzgt fgrj" 
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_and_send():
    print("AI Content தயார் செய்கிறது...")
    try:
        response = model.generate_content("மாணவர்களுக்கான ஒரு பொது அறிவுத் தகவலை தமிழில் சுருக்கமாக எழுதவும்.")
        content = response.text
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = "Daily KSSM Education Post"
        msg.attach(MIMEText(content, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("வெற்றி! மெயில் அனுப்பப்பட்டது.")
        return "Success"
    except Exception as e:
        print(f"Error Detals: {e}")
        return str(e)

@app.route('/')
def home():
    status = generate_and_send()
    if status == "Success":
        return "<h1>வெற்றி!</h1> பிளாக்கர் செக் பண்ணுங்க ப்ரோ!"
    else:
        return f"<h1>தோல்வி!</h1> காரணம்: {status}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
