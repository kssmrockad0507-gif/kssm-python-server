import google.generativeai as genai
import smtplib
import schedule
import time
import datetime
import os
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "KSSM AI Blogger Bot is Running Successfully!"

# --- உங்களது புதிய விபரங்கள் ---
GEMINI_API_KEY = "AIzaSyCh8COUy-iRfaR45FrkJoYT6x215KlmM84"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com" 
APP_PASSWORD = "guwf pshu zzgt fgrj" 
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com" 

# Gemini லேட்டஸ்ட் செட்டப்
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_and_send():
    print(f"[{datetime.datetime.now()}] AI Content தயார் செய்கிறது...")
    try:
        # மாணவர்களுக்கான பயனுள்ள தகவல்
        prompt = "Write an interesting and helpful educational fact or study tip in Tamil for students. Provide a clear title and bullet points. Format it clearly."
        response = model.generate_content(prompt)
        content = response.text
        
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip()
        if not title:
            title = "Daily Education Update"

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = title
        msg.attach(MIMEText(content, 'plain'))

        # மெயில் அனுப்புதல்
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"வெற்றி! பிளாக்கருக்கு போஸ்ட் அனுப்பப்பட்டது: {title}")
        
    except Exception as e:
        print(f"Error occurred: {e}")

def run_scheduler():
    # ஸ்டார்ட் ஆன உடனே ஒரு போஸ்ட் போட
    generate_and_send()
    # தினமும் ஒருமுறை இந்திய நேரப்படி அதிகாலை 4:30 மணிக்கு
    schedule.every().day.at("04:30").do(generate_and_send)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # பாட் வேலை செய்கிறதா என உடனே செக் செய்ய
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    # Render போர்ட் செட்டிங்ஸ்
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
