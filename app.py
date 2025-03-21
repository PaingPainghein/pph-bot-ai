from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os
from datetime import datetime

app = Flask(__name__)

# ရိုးရှင်းတဲ့ ဘာသာပြန်ခြင်း (dummy translation)
def translate_to_english(text):
    translations = {
        "မင်္ဂလာပါ": "Hello",
        "နေကောင်းလား": "Are you well?",
        "ကျေးဇူးပါ": "Thank you",
        "ဘာလုပ်လို့ရလဲ": "What can you do?",
        "ဘယ်ကလာလဲ": "Where are you from?",
        "အခုဘယ်နာရီလဲ": "What time is it now?",
        "ဒီနေ့ ရာသီဥတု ဘယ်လိုလဲ": "How's the weather today?"
    }
    return translations.get(text, "I can't translate that yet.")

# ရိုးရှင်းတဲ့ ရာသီဥတု (dummy weather)
def get_weather(city):
    weather_data = {
        "ရန်ကုန်": "ဒီနေ့ ရန်ကုန်မှာ မိုးအနည်းငယ် ရွာနိုင်ပါတယ်။ အပူချိန် ၃၀ ဒီဂရီရှိပါတယ်။",
        "မန္တလေး": "ဒီနေ့ မန္တလေးမှာ နေပူပြီး အပူချိန် ၃၅ ဒီဂရီရှိပါတယ်။",
        "နေပြည်တော်": "ဒီနေ့ နေပြည်တော်မှာ တိမ်အနည်းငယ်ရှိပြီး အပူချိန် ၃၂ ဒီဂရီရှိပါတယ်။"
    }
    return weather_data.get(city, "ဒီမြို့ရဲ့ ရာသီဥတုကို မသိသေးပါဘူး။ မြို့အမည်ကို ပြောပြပါ။")

# Custom response function
def get_custom_response(message):
    message = message.strip().lower()
    
    # အချိန်မေးရင်
    if "အခုဘယ်နာရီလဲ" in message or "အချိန်" in message:
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"အခုအချိန်က {current_time} ပါ။"
    
    # ရာသီဥတု မေးရင်
    if "ရာသီဥတု" in message:
        city = message.replace("ဒီနေ့", "").replace("ရာသီဥတု", "").replace("ဘယ်လိုလဲ", "").strip()
        if city:
            return get_weather(city)
        return "ဘယ်မြို့ရဲ့ ရာသီဥတုကို သိချင်လဲ ပြောပြပါ။"
    
    # ဘာသာပြန်ရင်
    if "အင်္ဂလိပ်လို ပြန်ပေး" in message or "ဘာသာပြန်" in message:
        text_to_translate = message.replace("အင်္ဂလိပ်လို ပြန်ပေး", "").replace("ဘာသာပြန်", "").strip()
        if text_to_translate:
            return translate_to_english(text_to_translate)
        return "ဘာကို ဘာသာပြန်ပေးရမလဲ ပြောပြပါ။"

    # ပုံမှန် တုံ့ပြန်မှု
    responses = {
        "မင်္ဂလာပါ": "မင်္ဂလာပါ။ PPH AI မှ ကြိုဆိုပါတယ်။ ဘာကူညီပေးရမလဲ?",
        "ဟိုင်း": "ဟိုင်း။ PPH AI က ဘာလဲလို့ မေးကြည့်လိုက်မယ်?",
        "နေကောင်းလား": "ကျွန်တော် နေကောင်းပါတယ်။ သင်ရော နေကောင်းလား?",
        "ကျေးဇူးပါ": "ရပါတယ်။ PPH AI က နောက်ထပ် ဘာကူညီပေးရမလဲ?",
        "ဘာမှမသိဘူး": "စိတ်မပူပါနဲ့။ သင်သိချင်တာ ဘာလဲဆိုတာ ပြောပြရင် PPH AI က ရှင်းပြပေးမယ်။",
        "သွားတော့မယ်": "အိုကေ။ နောက်တစ်ခါ PPH AI နဲ့ ပြန်တွေ့မယ်နော်။ ဂရုစိုက်ပါ။",
        "ဂွတ်ဘိုင်": "ဂွတ်ဘိုင်။ PPH AI နဲ့ နောက်မှ ထပ်ဆုံကြမယ်။",
        "ဘယ်သူလဲ": "ကျွန်တော်က PPH AI စကားပြောစက်ပါ။ သင့်ကို ကူညီဖို့ ဖန်တီးထားတာပါ။",
        "ဘာလုပ်လို့ရလဲ": "PPH AI က မေးခွန်းတွေ ဖြေပေးနိုင်တယ်၊ စကားပြောနိုင်တယ်၊ အချက်အလက် ရှာပေးနိုင်တယ်၊ ဘာသာပြန်ပေးနိုင်တယ်၊ ရာသီဥတု ပြောပြပေးနိုင်တယ်။ ဘာလုပ်ချင်လဲ?",
        "ဘယ်ကလာလဲ": "ကျွန်တော်က ဒစ်ဂျစ်တယ် ကမ္ဘာက လာတာပါ။ PPH AI လို နေရာမျိုးက ဖန်တီးထားတာပါ။",
        "ဘယ်လောက်သိလဲ": "PPH AI က အများကြီး သိအောင် လေ့ကျင့်ထားပါတယ်။ သင်မေးတာကို ဖြေကြည့်လို့ရပါတယ်။"
    }
    return responses.get(message, "သင်ပြောတာကို နားမလည်ဘူး။ PPH AI ကို နောက်တစ်ခါ ပြန်ပြောပြပါ။ ဘာကူညီပေးရမလဲ?")

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    response = get_custom_response(text)
    try:
        tts = gTTS(text=response, lang='my', slow=False)
        audio_file = "static/response.mp3"
        tts.save(audio_file)
        return send_file(audio_file, mimetype="audio/mp3")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/response', methods=['POST'])
def response():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    response_text = get_custom_response(text)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True, host='0.0.0.0', port=5000)
