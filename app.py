from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "KSSM AI Running"

@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.json
    command = data["command"].lower()

    if "time" in command:
        reply = str(datetime.datetime.now())

    elif "hello" in command:
        reply = "Hello Santhosh! I am your assistant."

    else:
        reply = "Command not understood"

    return jsonify({"reply": reply})
