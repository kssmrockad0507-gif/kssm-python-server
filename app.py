import google.generativeai as genai
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# --- விபரங்களை சிஸ்டம் மூலம் எடுக்க ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
APP_PASSWORD = os.environ.get("APP_PASSWORD")
BLOGGER_EMAIL = os.environ.get("BLOGGER_EMAIL")

# Gemini செட்டப்
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_and_send():
    print("AI Content தயார் செய்கிறது...")
    try:
        prompt = "Write an interesting and helpful educational fact or study tip in Tamil for students. Provide a clear title and bullet points."
        response = model.generate_content(prompt)
        content = response.text
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = "Daily Student Update from KSSM AI"
        msg.attach(MIMEText(content, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("வெற்றி! பிளாக்கருக்கு போஸ்ட் அனுப்பப்பட்டது.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/')
def home():
    # யாராவது வெப்சைட்டைத் திறந்தால் உடனே ஒரு போஸ்ட் போட
    status = generate_and_send()
    if status:
        return "KSSM AI Bot is Active! Post Sent to Blogger."
    else:
        return "Bot is Active, but failed to send post. Check Logs."

if __name__ == "__main__":
    # சர்வர் ஸ்டார்ட் ஆகும்போதே ஒருமுறை ரன் செய்ய
    generate_and_send()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
