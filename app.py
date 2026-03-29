import google.generativeai as genai
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- 1. உங்களது விபரங்கள் ---
GEMINI_API_KEY = "AIzaSyD4UOXQM5rFNPONUwXLMv4vp5So0btGsBM"
SENDER_EMAIL = "உங்க_ஜிமெயில்_ஐடி@gmail.com" 
APP_PASSWORD = "உங்க_ஜிமெயில்_ஆப்_பாஸ்வேர்டு" # Gmail -> Security -> 2FA -> App Passwords
BLOGGER_EMAIL = "ttnswamidayananda1947.ரகசிய_வார்த்தை@blogger.com"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_and_send():
    print("AI content தயார் செய்கிறது...")
    try:
        prompt = "Write an educational blog post in Tamil with a catchy title. Format it nicely."
        response = model.generate_content(prompt)
        content = response.text
        
        # தலைப்பை எடுக்கிறோம்
        title = content.split('\n')[0].replace('#', '').strip()

        # மெயில் அனுப்புதல்
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = title # இதுதான் பிளாக்கர் போஸ்ட் தலைப்பு
        msg.attach(MIMEText(content, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"வெற்றி! போஸ்ட் அனுப்பப்பட்டது: {title}")
        
    except Exception as e:
        print(f"Error: {e}")

# உடனே ஒருமுறை டெஸ்ட் செய்ய
generate_and_send()

# தினமும் ஷெட்யூல் செய்ய
schedule.every().day.at("10:00").do(generate_and_send)

while True:
    schedule.run_pending()
    time.sleep(60)
    
