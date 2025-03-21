from flask import Flask, render_template, request, jsonify, session
import requests
from flask_session import Session  # Server-side session အတွက်

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Hugging Face API အတွက်
API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"  # ဥပမာ model

def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route('/')
def index():
    if 'messages' not in session:
        session['messages'] = [
            {"type": "bot", "text": "မင်္ဂလာပါ။ PPH AI စကားပြောစက်မှ ကြိုဆိုပါတယ်။ ဘာကူညီပေးရမလဲ?"}
        ]
    return render_template('index.html', messages=session['messages'])

@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.form['chatInput'].strip()
    
    # User message ကို session ထဲ ထည့်မယ်
    session['messages'].append({"type": "user", "text": user_message})
    
    # Hugging Face API ကနေ AI response ယူမယ်
    payload = {"inputs": user_message}
    response = query_huggingface(payload)
    
    # API response ကနေ text ထုတ်ယူမယ် (model ပေါ်မူတည်ပြီး structure ကွဲပြားနိုင်တယ်)
    bot_response = response[0]['generated_text'] if response and isinstance(response, list) else "တောင်းပန်ပါတယ်၊ ပြဿနာတစ်ခုရှိနေပါတယ်။"
    
    # Bot response ကို session ထဲ ထည့်မယ်
    session['messages'].append({"type": "bot", "text": bot_response})
    session.modified = True  # Session ပြောင်းလဲမှု သိမ်းဖို့
    
    return jsonify({"messages": session['messages']})

if __name__ == '__main__':
    app.run(debug=True)

from gtts import gTTS
import os

@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.form['chatInput'].strip()
    session['messages'].append({"type": "user", "text": user_message})
    
    # AI response
    payload = {"inputs": user_message}
    response = query_huggingface(payload)
    bot_response = response[0]['generated_text'] if response and isinstance(response, list) else "တောင်းပန်ပါတယ်၊ ပြဿနာတစ်ခုရှိနေပါတယ်။"
    session['messages'].append({"type": "bot", "text": bot_response})
    
    # Text-to-Speech
    tts = gTTS(text=bot_response, lang='my')  # 'my' for Myanmar (support မရှိရင် 'en' သုံးပါ)
    audio_file = "static/response.mp3"
    tts.save(audio_file)
    
    session.modified = True
    return jsonify({"messages": session['messages'], "audio": audio_file})

