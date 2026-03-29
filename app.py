import google.generativeai as genai
import requests
import schedule
import time
import datetime

# --- 1. உங்களது விபரங்களை இங்கே கொடுக்கவும் ---
GEMINI_API_KEY = "gen-lang-client-0562297962"
BLOGGER_API_KEY = "AIzaSyDiLs0zT0cn_5LlRIXIqUUAjdpdqmBoAaI"
BLOGGER_ID = "1288039139605091785"

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_educational_content():
    print(f"[{datetime.datetime.now()}] Generating content...")
    
    # AI-யிடம் இருந்து கல்வி சார்ந்த தலைப்பு மற்றும் கட்டுரையை பெறுதல்
    prompt = "Write a detailed educational blog post in Tamil about a useful study tip or a scientific fact. Include a catchy title and structured points. Format it in HTML."
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # தலைப்பை மட்டும் தனியாக எடுக்க ஒரு சின்ன லாஜிக் (AI பெரும்பாலும் முதல் வரியை தலைப்பாக தரும்)
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
    
    params = {
        "key": BLOGGER_API_KEY
    }

    try:
        response = requests.post(url, json=payload, params=params)
        if response.status_code == 200:
            print(f"Successfully posted: {title}")
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

# --- 2. ஆட்டோமேஷன் செட்டிங்ஸ் ---
# தினமும் காலை 10:00 மணிக்கு போஸ்ட் செய்ய (நேரத்தை நீங்கள் மாற்றிக்கொள்ளலாம்)
schedule.every().day.at("10:00").do(job)

# ஒருமுறை உடனே டெஸ்ட் செய்ய (முதல்முறை மட்டும்)
job()

print("Automation script is running...")

while True:
    schedule.run_pending()
    time.sleep(60) # ஒரு நிமிடம் இடைவெளியில் செக் செய்யும்
