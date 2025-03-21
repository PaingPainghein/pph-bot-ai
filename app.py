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