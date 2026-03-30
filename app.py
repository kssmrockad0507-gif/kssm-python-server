import google.generativeai as genai
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask

app = Flask(__name__)

# விபரங்கள் (மாத்தாதீங்க)
GEMINI_API_KEY = "AIzaSyCh8COUy-iRfaR45FrkJoYT6x215KlmM84"
SENDER_EMAIL = "ttnswamidayananda1947@gmail.com"
APP_PASSWORD = "guwf pshu zzgt fgrj"
BLOGGER_EMAIL = "ttnswamidayananda1947.kssm@blogger.com"

# --- புதுப்பிக்கப்பட்ட செட்டிங்ஸ் ---
genai.configure(api_key=GEMINI_API_KEY)

def generate_and_send():
    try:
        # v1beta-வுக்குப் பதில் நேரடி மாடல் தேர்வு
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("மாணவர்களுக்கான ஒரு பொது அறிவுத் தகவலை தமிழில் சுருக்கமாக எழுதவும்.")
        content = response.text
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = "KSSM AI Special Update"
        msg.attach(MIMEText(content, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return "Success"
    except Exception as e:
        # எரர் மெசேஜில் v1beta சம்பந்தப்பட்ட பழைய விஷயங்களைத் தவிர்க்க
        return str(e)

@app.route('/')
def home():
    status = generate_and_send()
    if status == "Success":
        return "<h1>வெற்றி!</h1> பிளாக்கரைச் செக் பண்ணுங்க ப்ரோ!"
    else:
        # இங்கதான் எரர் வரும்போது தெளிவா காட்டும்
        return f"<h1>தோல்வி!</h1> எரர்: {status}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
