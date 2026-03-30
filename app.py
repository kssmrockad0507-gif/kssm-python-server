import google.generativeai as genai
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# விபரங்கள் (நேரடியாகவும் இருக்கலாம் அல்லது Environment Variables-லும் இருக்கலாம்)
GEMINI_API_KEY = "AIzaSyCh8COUy-iRfaR45FrkJoYT6x215KlmM84"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com"
APP_PASSWORD = "guwf pshu zzgt fgrj"
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com"

# --- மிக முக்கியமான மாற்றம் இங்கே ---
# பழைய v1beta-வுக்குப் பதில் லேட்டஸ்ட் செட்டிங்ஸ்
genai.configure(api_key=GEMINI_API_KEY)
# இங்கே மாடல் பெயரைச் சரியாகக் குறிப்பிடுகிறோம்
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_and_send():
    print("AI Content தயார் செய்கிறது...")
    try:
        # சிம்பிள் பிராம்ப்ட்
        response = model.generate_content("மாணவர்களுக்கான ஒரு பொது அறிவுத் தகவலை தமிழில் சுருக்கமாக எழுதவும்.")
        content = response.text
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = "KSSM AI Daily Update"
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
