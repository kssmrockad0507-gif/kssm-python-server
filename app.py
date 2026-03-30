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

# Flask setup for Render (To keep it live)
app = Flask(__name__)

@app.route('/')
def home():
    return "KSSM AI Blogger Bot is active!"

# --- உங்களது விபரங்கள் ---
GEMINI_API_KEY = "AIzaSyD4UOXQM5rFNPONUwXLMv4vp5So0btGsBM"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com" 
APP_PASSWORD = "ajju sqbw awev vtof" 
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com" # 'kssm' இடத்தில நீங்க செட் பண்ண வார்த்தையை போடவும்

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_and_send():
    print(f"[{datetime.datetime.now()}] AI content தயார் செய்கிறது...")
    try:
        prompt = "Write an interesting educational or technology fact in Tamil for students. Use a catchy title and clear points. Format it nicely."
        response = model.generate_content(prompt)
        full_text = response.text
        
        # முதல் வரியை தலைப்பாக எடுக்கிறோம்
        lines = full_text.split('\n')
        title = lines[0].replace('#', '').strip()
        body = "\n".join(lines[1:])

        # மெயில் செட்டப்
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = title
        msg.attach(MIMEText(full_text, 'plain'))

        # மெயில் அனுப்புதல் (SMTP)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"வெற்றி! பிளாக்கருக்கு போஸ்ட் அனுப்பப்பட்டது: {title}")
        
    except Exception as e:
        print(f"Error: {e}")

def run_scheduler():
    # ஸ்டார்ட் பண்ண உடனே ஒரு போஸ்ட் போட
    generate_and_send()
    # தினமும் காலை 10:00 மணிக்கு (UTC நேரத்தை கவனித்துக்கொள்ளவும்)
    schedule.every().day.at("04:30").do(generate_and_send)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # ஷெட்யூலரை தனி த்ரெட்டில் ரன் செய்ய
    threading.Thread(target=run_scheduler, daemon=True).start()
    
    # Render Port Fix
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
