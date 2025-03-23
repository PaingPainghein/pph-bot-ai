from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os
from datetime import datetime

app = Flask(__name__)

# ဘာသာပြန်အတွက် dictionary
def translate_to_english(text):
    translations = {
        "မင်္ဂလာပါ": "Hello",
        "နေကောင်းလား": "Are you well?",
        "ကျေးဇူးပါ": "Thank you",
        "ဘာလုပ်လို့ရလဲ": "What can you do?",
        "ဘယ်ကလာလဲ": "Where are you from?",
        "အခုဘယ်နာရီလဲ": "What time is it now?",
        "ဒီနေ့ ရာသီဥတု ဘယ်လိုလဲ": "How's the weather today?",
        "ဘာစားရမလဲ": "What should I eat?",
        "ဘယ်မှာလဲ": "Where are you?",
        "ဘယ်လိုလဲ": "How are you?",
        "အိပ်ချင်တယ်": "I'm sleepy",
        "ပျော်တယ်": "I'm happy",
        "ဘာလုပ်နေလဲ": "What are you doing?",
        "ဘယ်လောက်ကျလဲ": "How much does it cost?",
        "ဘယ်သူလဲ": "Who are you?",
        "ဘာလိုချင်လဲ": "What do you want?",
        "ဘယ်နေ့လဲ": "What day is it?",
        # အသစ်ထည့်ထားတဲ့ စာလုံးများ
        "ဘာလဲ": "What?",
        "ဘာလုပ်ရမလဲ": "What should I do?",
        "ဘယ်လောက်လှလဲ": "How beautiful is it?"
    }
    return translations.get(text.strip(), "ဒီစာကို ဘာသာမပြန်နိုင်သေးပါဘူး။ တခြား စာကြောင်း ပြောပြပါ။")

# ရာသီဥတု အချက်အလက်
def get_weather(city):
    weather_data = {
        "ရန်ကုန်": "ဒီနေ့ ရန်ကုန်မှာ မိုးအနည်းငယ် ရွာနိုင်ပါတယ်။ အပူချိန် ၃၀ ဒီဂရီရှိပါတယ်။",
        "မန္တလေး": "ဒီနေ့ မန္တလေးမှာ နေပူပြီး အပူချိန် ၃၅ ဒီဂရီရှိပါတယ်။",
        "နေပြည်တော်": "ဒီနေ့ နေပြည်တော်မှာ တိမ်အနည်းငယ်ရှိပြီး အပူချိန် ၃၂ ဒီဂရီရှိပါတယ်။",
        # အခြား မြို့တွေ အရင်ကအတိုင်း ထားထားတယ်
    }
    return weather_data.get(city.strip(), "ဒီမြို့ရဲ့ ရာသီဥတုကို မသိသေးပါဘူး။ မြို့အမည်ကို ပြောပြပါ။")

# မြန်မာနိုင်ငံ အချက်အလက် (အရင်ကအတိုင်း ထားထားတယ်)
def get_myanmar_info(place):
    myanmar_data = {
        "ရန်ကုန်တိုင်းဒေသကြီး": "မြို့တော်က ရန်ကုန်မြို့ပါ။ လူဦးရေ ၇ သန်းကျော်ရှိပြီး မြန်မာနိုင်ငံရဲ့ စီးပွားရေး ဗဟိုချက်ပါ။",
        "မန္တလေးတိုင်းဒေသကြီး": "မြို့တော်က မန္တလေးမြို့ပါ။ လူဦးရေ ၆ သန်းကျော်ရှိပြီး ယဉ်ကျေးမှု အမွေအနှစ်တွေ ကြွယ်ဝပါတယ်။",
        # အခြား တိုင်းနဲ့ ပြည်နယ်တွေ အရင်ကအတိုင်း
    }
    return myanmar_data.get(place.strip(), "ဒီနေရာကို မသိသေးပါဘူး။ ပြည်နယ် ဒါမှမဟုတ် တိုင်းဒေသကြီး အမည်ကို ပြောပြပါ။")

# စိတ်ကြိုက် အဖြေထုတ်တဲ့ function (ပိုထက်မြက်အောင် ပြင်ထားတယ်)
def get_custom_response(message):
    message = message.strip().lower()

    # အချိန်နဲ့ ရက်စွဲ
    if "အခုဘယ်နာရီလဲ" in message or "အချိန်" in message:
        current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format ပြောင်းထားတယ်
        return f"အခုအချိန်က {current_time} ပါ။"
    if "ဒီနေ့ ဘယ်နေ့လဲ" in message or "ရက်စွဲ" in message:
        current_date = datetime.now().strftime("%Y-%m-%d, %A")  # ရက်နာမည် ထည့်ထားတယ်
        return f"ဒီနေ့က {current_date} ပါ။"

    # ရာသီဥတု
    if "ရာသီဥတု" in message:
        city = message.replace("ဒီနေ့", "").replace("ရာသီဥတု", "").replace("ဘယ်လိုလဲ", "").strip()
        return get_weather(city) if city else "ဘယ်မြို့ရဲ့ ရာသီဥတုကို သိချင်လဲ ပြောပြပါ။"

    # ဘာသာပြန်
    if "အင်္ဂလိပ်လို ပြန်ပေး" in message or "ဘာသာပြန်" in message:
        text_to_translate = message.replace("အင်္ဂလိပ်လို ပြန်ပေး", "").replace("ဘာသာပြန်", "").strip()
        return translate_to_english(text_to_translate) if text_to_translate else "ဘာကို ဘာသာပြန်ပေးရမလဲ ပြောပြပါ။"

    # မြန်မာနိုင်ငံ အချက်အလက်
    if "မြန်မာနိုင်ငံ" in message and ("ပြည်နယ်" in message or "တိုင်း" in message):
        place = message.replace("မြန်မာနိုင်ငံ", "").replace("အကြောင်း", "").replace("ပြောပြပါ", "").strip()
        return get_myanmar_info(place) if place else "မြန်မာနိုင်ငံအကြောင်း ဘာသိချင်လဲ? ပြည်နယ် ဒါမှမဟုတ် တိုင်းတစ်ခုကို ပြောပြပါ။"

    # နေ့စဉ်သုံး စကားပြောများ (ပိုကွဲပြားအောင် ထည့်ထားတယ်)
    responses = {
        "မင်္ဂလာပါ": "မင်္ဂလာပါ။ PPH AI ကနေ ကြိုဆိုပါတယ်။ ဘာလုပ်ပေးရမလဲ?",
        "ဟိုင်း": "ဟိုင်း။ ဒီနေ့ ဘာလုပ်ချင်လဲ?",
        "နေကောင်းလား": "ကျွန်တော် ကောင်းပါတယ်။ သင်ရော ဘယ်လိုလဲ?",
        "ကျေးဇူးပါ": "ရပါတယ်။ နောက်ဘာလုပ်ပေးရမလဲ?",
        "ဘာလုပ်လို့ရလဲ": "ကျွန်တော်က စကားပြောတာ၊ ဘာသာပြန်တာ၊ ရာသီဥတု ပြောပြတာ၊ အချက်အလက် ရှာပေးတာ လုပ်နိုင်တယ်။ ဘာစမ်းကြည့်ချင်လဲ?",
        "ဘာစားရမလဲ": "ဒီနေ့ ထမင်းနဲ့ အမဲသားကြော် စားကြည့်ပါလား။ သင်ဘာကြိုက်လဲ ပြောပြပါ။",
        "ဘယ်သူလဲ": "ကျွန်တော်က PPH AI ပါ။ သင့်ကို ကူညီဖို့ ဒီမှာ ရှိတယ်။",
        "အိပ်ချင်တယ်": "အိပ်ချင်ရင် အိပ်လိုက်ပါ။ အိပ်မက်လှလှ မက်ပါစေ။",
        "ဘာလုပ်နေလဲ": "ကျွန်တော်က သင်နဲ့ စကားပြောဖို့ စောင့်နေတာပါ။ သင်ရော?",
        # အသစ်ထည့်ထားတဲ့ အဖြေများ
        "ဘာလုပ်ရမလဲ": "ဘာလုပ်ချင်လဲ ပေါ်မူတည်တယ်။ အနားယူချင်ရင် အိပ်လိုက်၊ ပျော်ချင်ရင် သီချင်းနားထောင်ကြည့်ပါ။",
        "ဘာဖြစ်လဲ": "ကျွန်တော်က ဘာမှ မဖြစ်ပါဘူး။ သင်ဘာဖြစ်လို့လဲ?",
        "ပိုက်ဆံမရှိဘူး": "စိတ်မပူပါနဲ့။ ကျွန်တော်က အခမဲ့ ကူညီပေးမှာပါ။"
    }
    return responses.get(message, "သင်ပြောတာကို နားမလည်သေးဘူး။ ဘာကို ဆိုလိုတာလဲ ထပ်ရှင်းပြပေးပါ။")

# Root endpoint
@app.route('/')
def index():
    if os.path.exists('index.html'):
        return send_file('index.html')
    return jsonify({"error": "HTML file not found"}), 404  # HTML ဖိုင်မရှိရင် အမှား ပြပါတယ်

# Speak endpoint (ပိုမြန်အောင် ပြင်ထားတယ်)
@app.route('/speak', methods=['POST'])
def speak():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "စာသား ထည့်မထားပါဘူး"}), 400

    response = get_custom_response(text)
    audio_file = "static/response.mp3"

    # ဖိုင်အဟောင်း ဖျက်ပြီး အသစ်ထုတ်တယ်
    if os.path.exists(audio_file):
        os.remove(audio_file)

    try:
        tts = gTTS(text=response, lang='my', slow=False)
        tts.save(audio_file)
        return send_file(audio_file, mimetype="audio/mp3")
    except Exception as e:
        return jsonify({"error": f"အသံဖိုင် ထုတ်မရဘူး: {str(e)}"}), 500

# Response endpoint
@app.route('/response', methods=['POST'])
def response():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "စာသား ထည့်မထားပါဘူး"}), 400
    response_text = get_custom_response(text)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    # Static folder ရှိမရှိ သေချာအောင် စစ်တယ်
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(host='0.0.0.0', port=5000, debug=True)