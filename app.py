import google.generativeai as genai
import requests
import schedule
import time
import datetime
import os
import threading
from flask import Flask

# 1. Flask App setup (Render "Port Timeout" எரர் வராமல் இருக்க)
app = Flask(__name__)

@app.route('/')
def home():
    return "KSSM AI Bot is Running Successfully!"

# --- 2. உங்கள் விபரங்கள் ---
API_KEY = "AIzaSyD4UOXQM5rFNPONUwXLMv4vp5So0btGsBM"
BLOGGER_ID = "1288039139605091785"

# Gemini AI Setup
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_educational_content():
    print(f"[{datetime.datetime.now()}] Generating content...")
    # கல்வி சார்ந்த தலைப்பு - Prompt
    prompt = "Write a detailed educational blog post in Tamil about a useful study tip or a scientific fact. Include a catchy title and structured points. Format it in HTML."
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # தலைப்பு மற்றும் கட்டுரையை பிரித்தல்
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip()
        body = "".join(lines[1:])
        
        return title, body
    except Exception as e:
        print(f"Error generating content: {e}")
        return None, None

def post_to_blogger(title, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_ID}/posts/"
    payload = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    params = {"key": API_KEY}

    try:
        response = requests.post(url, json=payload, params=params)
        if response.status_code == 200:
            print(f"Successfully posted to Blogger: {title}")
        else:
            print(f"Failed to post. Status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error posting to Blogger: {e}")

def job():
    print("Starting automated task...")
    title, content = generate_educational_content()
    if title and content:
        post_to_blogger(title, content)

# --- 3. ஆட்டோமேஷன் செட்டிங்ஸ் ---
def run_scheduler():
    # சர்வர் ரன் ஆன உடனே டெஸ்ட்டிற்காக ஒரு போஸ்ட் போட
    job()
    # தினமும் காலை 10:00 மணிக்கு போஸ்ட் செய்ய (நேரத்தை மாற்றிக்கொள்ளலாம்)
    schedule.every().day.at("10:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)

# --- 4. மெயின் பங்க்ஷன் (Render Fix) ---
if __name__ == "__main__":
    # ஷெட்யூலரை தனி த்ரெட்டில் ரன் செய்ய (Background Task)
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Render-க்கு தேவையான போர்ட் செட்டிங்ஸ்
    # இது மிக முக்கியம்: host='0.0.0.0' மற்றும் port=10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
