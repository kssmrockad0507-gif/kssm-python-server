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

# 1. Flask setup (Render போர்ட் கனெக்ஷனுக்காக)
app = Flask(__name__)

@app.route('/')
def home():
    return "KSSM AI Blogger Bot is Running Successfully!"

# --- 2. உங்களது சரியான விபரங்கள் ---
GEMINI_API_KEY = "AIzaSyD4UOXQM5rFNPONUwXLMv4vp5So0btGsBM"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com" 
# புதிய App Password இங்கே இணைக்கப்பட்டுள்ளது
APP_PASSWORD = "guwf pshu zzgt fgrj" 
# பிளாக்கர் மெயில் ஐடி (கடைசியில் ரகசிய வார்த்தையைச் சரியாகச் சேர்க்கவும்)
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com" 

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_and_send():
    print(f"[{datetime.datetime.now()}] AI Content தயாரிப்பு தொடங்குகிறது...")
    try:
        # AI மூலம் போஸ்ட் தயார் செய்தல்
        prompt = "Write a detailed and interesting educational blog post in Tamil for students. Include a catchy title and structured points. Format it in HTML."
        response = model.generate_content(prompt)
        content = response.text
        
        # முதல் வரியைத் தலைப்பாக எடுக்கிறோம்
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip()
        body = "".join(lines[1:])

        # ஈமெயில் மெசேஜ் செட்டப்
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = title
        msg.attach(MIMEText(content, 'html')) # HTML ஃபார்மேட்டில் அனுப்புகிறோம்

        # மெயில் அனுப்புதல் (Gmail SMTP)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"வெற்றி! பிளாக்கருக்கு போஸ்ட் அனுப்பப்பட்டது: {title}")
        
    except Exception as e:
        print(f"தவறு நடந்துள்ளது: {e}")

# --- 3. ஆட்டோமேஷன் செட்டிங்ஸ் ---
def run_scheduler():
    # பாட் ரன் ஆன உடனே ஒரு போஸ்ட் போட
    generate_and_send()
    # தினமும் காலை 10:00 மணிக்கு போஸ்ட் செய்ய (இந்திய நேரப்படி)
    # Render-ன் UTC நேரத்தைக் கணக்கிட்டு '04:30' என வைத்துள்ளேன்
    schedule.every().day.at("04:30").do(generate_and_send)
    while True:
        schedule.run_pending()
        time.sleep(60)

# --- 4. மெயின் பங்க்ஷன் ---
if __name__ == "__main__":
    # ஷெட்யூலரைத் தனி த்ரெட்டில் ரன் செய்ய
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    # Render-க்கான போர்ட் செட்டிங்
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
