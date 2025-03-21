from flask import Flask, render_template, request, jsonify, session
import requests
from flask_session import Session
import os
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# GitHub raw URL ကနေ responses ယူမယ်
GITHUB_RAW_URL = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/pphaibot/main/responses.json"

# Azure TTS အတွက် (သင့် Azure credentials ထည့်ပါ)
AZURE_SPEECH_KEY = "YOUR_AZURE_SPEECH_KEY"
AZURE_REGION = "YOUR_AZURE_REGION"
AUDIO_OUTPUT_PATH = "static/response.wav"

def get_github_responses():
    try:
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching GitHub responses: {e}")
        return {"တောင်းပန်ပါတယ်": "တစ်ခုခု မှားနေပါတယ်။"}

def text_to_speech_azure(text):
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
    speech_config.speech_synthesis_voice_name = "my-MM-ThiriNeural"  # Myanmar voice
    audio_config = speechsdk.audio.AudioOutputConfig(filename=AUDIO_OUTPUT_PATH)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return AUDIO_OUTPUT_PATH
    return None

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
    
    # User message ထည့်မယ်
    session['messages'].append({"type": "user", "text": user_message})
    
    # GitHub ကနေ response ယူမယ်
    responses = get_github_responses()
    bot_response = responses.get(user_message, "မသိပါဘူး။ တစ်ခြား ဘာမေးချင်လဲ?")
    
    # Bot response ထည့်မယ်
    session['messages'].append({"type": "bot", "text": bot_response})
    
    # Azure TTS နဲ့ Myanmar အသံထုတ်မယ်
    audio_file = text_to_speech_azure(bot_response)
    
    session.modified = True
    return jsonify({"messages": session['messages'], "audio": audio_file if audio_file else ""})

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=5000, debug=True)