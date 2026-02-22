import os
import json
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://techkkabir-hub.github.io/NCERT-QUIZ")

user_states = {}

# Ready MCQs - No API needed!
QUESTIONS = [
    {"subject": "history", "q_hi": "सिंधु घाटी सभ्यता की खोज किसने की?", "q_en": "Who discovered the Indus Valley Civilization?", "options": [{"letter": "A", "hi": "जॉन मार्शल", "en": "John Marshall"}, {"letter": "B", "hi": "दयाराम साहनी", "en": "Dayaram Sahni"}, {"letter": "C", "hi": "आर.डी. बनर्जी", "en": "R.D. Banerjee"}, {"letter": "D", "hi": "मोर्टिमर व्हीलर", "en": "Mortimer Wheeler"}], "correct": "B", "exp_hi": "हड़प्पा की खोज 1921 में दयाराम साहनी ने की थी।", "exp_en": "Harappa was discovered by Dayaram Sahni in 1921.", "exam_tag": "UPSC 2018", "class": "कक्षा 6"},
    {"subject": "history", "q_hi": "बौद्ध धर्म के संस्थापक कौन थे?", "q_en": "Who founded Buddhism?", "options": [{"letter": "A", "hi": "महावीर", "en": "Mahavira"}, {"letter": "B", "hi": "गौतम बुद्ध", "en": "Gautam Buddha"}, {"letter": "C", "hi": "आदि शंकराचार्य", "en": "Adi Shankaracharya"}, {"letter": "D", "hi": "चाणक्य", "en": "Chanakya"}], "correct": "B", "exp_hi": "गौतम बुद्ध ने 6वीं सदी ईसा पूर्व में बौद्ध धर्म की स्थापना की।", "exp_en": "Gautam Buddha founded Buddhism in the 6th century BCE.", "exam_tag": "SSC 2019", "class": "कक्षा 6"},
    {"subject": "history", "q_hi": "अकबर का दरबारी संगीतकार कौन था?", "q_en": "Who was the court musician of Akbar?", "options": [{"letter": "A", "hi": "तानसेन", "en": "Tansen"}, {"letter": "B", "hi": "बैजू बावरा", "en": "Baiju Bawra"}, {"letter": "C", "hi": "अमीर खुसरो", "en": "Amir Khusro"}, {"letter": "D", "hi": "मियां की मल्हार", "en": "Miyan ki Malhar"}], "correct": "A", "exp_hi": "तानसेन अकबर के नवरत्नों में से एक थे।", "exp_en": "Tansen was one of the nine gems of Akbar's court.", "exam_tag": "UPSC 2020", "class": "कक्षा 7"},
    {"subject": "history", "q_hi": "1857 की क्रांति का तात्कालिक कारण क्या था?", "q_en": "What was the immediate cause of the 1857 revolt?", "options": [{"letter": "A", "hi": "भारी कर", "en": "Heavy taxation"}, {"letter": "B", "hi": "चर्बी वाले कारतूस", "en": "Greased cartridges"}, {"letter": "C", "hi": "अंग्रेजी शिक्षा", "en": "English education"}, {"letter": "D", "hi": "डलहौजी की नीति", "en": "Dalhousie's policy"}], "correct": "B", "exp_hi": "एनफील्ड राइफल में चर्बी लगे कारतूस ने 1857 की क्रांति को जन्म दिया।", "exp_en": "Greased cartridges of Enfield rifle triggered the 1857 revolt.", "exam_tag": "SSC 2021", "class": "कक्षा 8"},
    {"subject": "history", "q_hi": "भारतीय राष्ट्रीय कांग्रेस की स्थापना कब हुई?", "q_en": "When was Indian National Congress founded?", "options": [{"letter": "A", "hi": "1885", "en": "1885"}, {"letter": "B", "hi": "1890", "en": "1890"}, {"letter": "C", "hi": "1905", "en": "1905"}, {"letter": "D", "hi": "1857", "en": "1857"}], "correct": "A", "exp_hi": "INC की स्थापना 1885 में A.O. Hume ने की थी।", "exp_en": "INC was founded in 1885 by A.O. Hume.", "exam_tag": "Railway 2019", "class": "कक्षा 8"},
    {"subject": "history", "q_hi": "गांधीजी ने दांडी मार्च कब किया?", "q_en": "When did Gandhiji conduct the Dandi March?", "options": [{"letter": "A", "hi": "1920", "en": "1920"}, {"letter": "B", "hi": "1930", "en": "1930"}, {"letter": "C", "hi", "1942", "en": "1942"}, {"letter": "D", "hi": "1915", "en": "1915"}], "correct": "B", "exp_hi": "1930 में गांधीजी ने नमक सत्याग्रह के तहत दांडी मार्च किया।", "exp_en": "Gandhiji conducted Dandi March in 1930 as part of Salt Satyagraha.", "exam_tag": "UPSC 2017", "class": "कक्षा 10"},
    {"subject": "geography", "q_hi": "भारत की सबसे लंबी नदी कौन सी है?", "q_en": "Which is the longest river in India?", "options": [{"letter": "A", "hi": "गंगा", "en": "Ganga"}, {"letter": "B", "hi": "गोदावरी", "en": "Godavari"}, {"letter": "C", "hi": "यमुना", "en": "Yamuna"}, {"letter": "D", "hi": "सिंधु", "en": "Indus"}], "correct": "A", "exp_hi": "गंगा भारत की सबसे लंबी नदी है जिसकी लंबाई 2525 km है।", "exp_en": "Ganga is India's longest river with a length of 2525 km.", "exam_tag": "SSC 2020", "class": "कक्षा 6"},
    {"subject": "geography", "q_hi": "भारत का सबसे बड़ा राज्य (क्षेत्रफल) कौन सा है?", "q_en": "Which is the largest state of India by area?", "options": [{"letter": "A", "hi": "मध्य प्रदेश", "en": "Madhya Pradesh"}, {"letter": "B", "hi": "महाराष्ट्र", "en": "Maharashtra"}, {"letter": "C", "hi": "राजस्थान", "en": "Rajasthan"}, {"letter": "D", "hi": "उत्तर प्रदेश", "en": "Uttar Pradesh"}], "correct": "C", "exp_hi": "राजस्थान 342,239 वर्ग किमी के साथ भारत का सबसे बड़ा राज्य है।", "exp_en": "Rajasthan is India's largest state with 342,239 sq km.", "exam_tag": "Railway 2020", "class": "कक्षा 6"},
    {"subject": "geography", "q_hi": "विश्व का सबसे ऊँचा पर्वत कौन सा है?", "q_en": "Which is the highest mountain in the world?", "options": [{"letter": "A", "hi": "K2", "en": "K2"}, {"letter": "B", "hi": "माउंट एवरेस्ट", "en": "Mount Everest"}, {"letter": "C", "hi": "कंचनजंगा", "en": "Kanchenjunga"}, {"letter": "D", "hi": "नंगा पर्बत", "en": "Nanga Parbat"}], "correct": "B", "exp_hi": "माउंट एवरेस्ट 8848 मीटर ऊँचाई के साथ विश्व का सबसे ऊँचा पर्वत है।", "exp_en": "Mount Everest at 8848m is the world's highest mountain.", "exam_tag": "CTET 2019", "class": "कक्षा 7"},
    {"subject": "geography", "q_hi": "भारत में सबसे अधिक वर्षा कहाँ होती है?", "q_en": "Where does the highest rainfall occur in India?", "options": [{"letter": "A", "hi": "चेरापूंजी", "en": "Cherrapunji"}, {"letter": "B", "hi": "मासिनराम", "en": "Mawsynram"}, {"letter": "C", "hi": "मुंबई", "en": "Mumbai"}, {"letter": "D", "hi": "कोलकाता", "en": "Kolkata"}], "correct": "B", "exp_hi": "मासिनराम (मेघालय) विश्व में सर्वाधिक वर्षा वाला स्थान है।", "exp_en": "Mawsynram (Meghalaya) receives the highest rainfall in the world.", "exam_tag": "SSC 2018", "class": "कक्षा 7"},
    {"subject": "economics", "q_hi": "भारत का केंद्रीय बैंक कौन सा है?", "q_en": "Which is the central bank of India?", "options": [{"letter": "A", "hi": "SBI", "en": "SBI"}, {"letter": "B", "hi": "RBI", "en": "RBI"}, {"letter": "C", "hi": "NABARD", "en": "NABARD"}, {"letter": "D", "hi": "SEBI", "en": "SEBI"}], "correct": "B", "exp_hi": "RBI (भारतीय रिजर्व बैंक) की स्थापना 1935 में हुई।", "exp_en": "RBI (Reserve Bank of India) was established in 1935.", "exam_tag": "SSC 2021", "class": "कक्षा 10"},
    {"subject": "economics", "q_hi": "GDP का पूरा नाम क्या है?", "q_en": "What is the full form of GDP?", "options": [{"letter": "A", "hi": "Gross Domestic Product", "en": "Gross Domestic Product"}, {"letter": "B", "hi": "General Domestic Product", "en": "General Domestic Product"}, {"letter": "C", "hi": "Gross Development Product", "en": "Gross Development Product"}, {"letter": "D", "hi": "Global Domestic Product", "en": "Global Domestic Product"}], "correct": "A", "exp_hi": "GDP यानी सकल घरेलू उत्पाद एक वर्ष में देश में उत्पादित सभी वस्तुओं और सेवाओं का मूल्य है।", "exp_en": "GDP (Gross Domestic Product) is the total value of goods and services produced in a country in a year.", "exam_tag": "Railway 2021", "class": "कक्षा 10"},
    {"subject": "polity", "q_hi": "भारत का संविधान कब लागू हुआ?", "q_en": "When did the Indian Constitution come into effect?", "options": [{"letter": "A", "hi": "15 अगस्त 1947", "en": "15 August 1947"}, {"letter": "B", "hi": "26 जनवरी 1950", "en": "26 January 1950"}, {"letter": "C", "hi": "26 नवंबर 1949", "en": "26 November 1949"}, {"letter": "D", "hi": "2 अक्टूबर 1950", "en": "2 October 1950"}], "correct": "B", "exp_hi": "भारत का संविधान 26 जनवरी 1950 को लागू हुआ।", "exp_en": "The Indian Constitution came into effect on 26 January 1950.", "exam_tag": "UPSC 2019", "class": "कक्षा 9"},
    {"subject": "polity", "q_hi": "भारत के प्रथम राष्ट्रपति कौन थे?", "q_en": "Who was the first President of India?", "options": [{"letter": "A", "hi": "जवाहरलाल नेहरू", "en": "Jawaharlal Nehru"}, {"letter": "B", "hi": "डॉ. राजेंद्र प्रसाद", "en": "Dr. Rajendra Prasad"}, {"letter": "C", "hi": "सरदार पटेल", "en": "Sardar Patel"}, {"letter": "D", "hi": "डॉ. अंबेडकर", "en": "Dr. Ambedkar"}], "correct": "B", "exp_hi": "डॉ. राजेंद्र प्रसाद भारत के प्रथम राष्ट्रपति थे।", "exp_en": "Dr. Rajendra Prasad was the first President of India.", "exam_tag": "SSC 2020", "class": "कक्षा 9"},
    {"subject": "polity", "q_hi": "लोकसभा में कुल कितनी सीटें हैं?", "q_en": "How many seats are there in Lok Sabha?", "options": [{"letter": "A", "hi": "542", "en": "542"}, {"letter": "B", "hi": "545", "en": "545"}, {"letter": "C", "hi": "543", "en": "543"}, {"letter": "D", "hi": "550", "en": "550"}], "correct": "C", "exp_hi": "लोकसभा में 543 निर्वाचित सीटें हैं।", "exp_en": "Lok Sabha has 543 elected seats.", "exam_tag": "Railway 2019", "class": "कक्षा 9"},
]

SUBJECTS = {
    "history": "⚔️ इतिहास",
    "geography": "🌍 भूगोल",
    "economics": "📈 अर्थशास्त्र",
    "polity": "🏛️ राजनीतिशास्त्र",
    "mixed": "🎲 मिश्रित"
}

def get_question(subject):
    if subject == "mixed":
        return random.choice(QUESTIONS)
    filtered = [q for q in QUESTIONS if q["subject"] == subject]
    if not filtered:
        return random.choice(QUESTIONS)
    return random.choice(filtered)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {"subject": "history", "score": 0, "total": 0, "streak": 0}
    keyboard = [
        [InlineKeyboardButton("🎯 Mini App में खेलें", web_app={"url": MINI_APP_URL})],
        [InlineKeyboardButton("⚔️ इतिहास", callback_data="sub_history"),
         InlineKeyboardButton("🌍 भूगोल", callback_data="sub_geography")],
        [InlineKeyboardButton("📈 अर्थशास्त्र", callback_data="sub_economics"),
         InlineKeyboardButton("🏛️ राजनीति", callback_data="sub_polity")],
        [InlineKeyboardButton("🎲 मिश्रित", callback_data="sub_mixed")],
        [InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")]
    ]
    await update.message.reply_text(
        "🎯 *NCERT Quiz Bot में स्वागत है!*\n\n"
        "📚 इतिहास | भूगोल | अर्थशास्त्र | राजनीति\n"
        "🎓 UPSC | SSC | Railway | CTET\n\n"
        "विषय चुनें 👇",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    if user_id not in user_states:
        user_states[user_id] = {"subject": "history", "score": 0, "total": 0, "streak": 0}
    state = user_states[user_id]

    if data.startswith("sub_"):
        state["subject"] = data[4:]
        await query.edit_message_text(
            f"✅ विषय: *{SUBJECTS.get(state['subject'])}*\n\nतैयार हैं?",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")]])
        )
    elif data == "start_quiz":
        await send_question(query.message.chat_id, context, user_id)
    elif data.startswith("ans_"):
        parts = data.split("_")
        selected, correct = parts[1], parts[2]
        state["total"] += 1
        if selected == correct:
            state["score"] += 1
            state["streak"] += 1
            result = f"✅ *सही! Correct!* 🎉\n🔥 Streak: {state['streak']}"
        else:
            state["streak"] = 0
            result = f"❌ *गलत! Wrong!*\n✅ सही था: *{correct}*"
        exp = context.user_data.get(f"{user_id}_exp", {})
        exp_text = f"\n\n💡 *व्याख्या:*\n{exp.get('hi','')}\n_{exp.get('en','')}_" if exp else ""
        keyboard = [
            [InlineKeyboardButton("➡️ अगला प्रश्न", callback_data="next_q")],
            [InlineKeyboardButton("📊 Score", callback_data="show_score"),
             InlineKeyboardButton("🔄 विषय बदलें", callback_data="change_sub")]
        ]
        await query.edit_message_text(f"{result}{exp_text}", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "next_q":
        await send_question(query.message.chat_id, context, user_id)
    elif data == "show_score":
        total = state.get("total", 0)
        score = state.get("score", 0)
        pct = round((score/total)*100) if total > 0 else 0
        emoji = "🏆" if pct >= 80 else "👍" if pct >= 60 else "📚"
        await query.edit_message_text(
            f"{emoji} *Score*\n✅ {score}/{total}\n📊 {pct}%\n🔥 {state.get('streak',0)}",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ अगला", callback_data="next_q")]])
        )
    elif data == "change_sub":
        keyboard = [
            [InlineKeyboardButton("⚔️ इतिहास", callback_data="sub_history"),
             InlineKeyboardButton("🌍 भूगोल", callback_data="sub_geography")],
            [InlineKeyboardButton("📈 अर्थशास्त्र", callback_data="sub_economics"),
             InlineKeyboardButton("🏛️ राजनीति", callback_data="sub_polity")],
            [InlineKeyboardButton("🎲 मिश्रित", callback_data="sub_mixed")]
        ]
        await query.edit_message_text("विषय चुनें 👇", reply_markup=InlineKeyboardMarkup(keyboard))

async def send_question(chat_id, context, user_id):
    state = user_states.get(user_id, {"subject": "mixed"})
    q = get_question(state["subject"])
    context.user_data[f"{user_id}_exp"] = {"hi": q.get("exp_hi",""), "en": q.get("exp_en","")}
    correct = q.get("correct", "A")
    keyboard = []
    for opt in q.get("options", []):
        t = f"{opt['letter']}. {opt['hi']}"[:60]
        keyboard.append([InlineKeyboardButton(t, callback_data=f"ans_{opt['letter']}_{correct}")])
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"📌 *{q.get('class','')} | {SUBJECTS.get(state['subject'])}*\n"
             f"🏷️ _{q.get('exam_tag','')}_\n\n"
             f"❓ *{q.get('q_hi','')}*\n\n_{q.get('q_en','')}_\n\nउत्तर चुनें 👇",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    print("🤖 Bot शुरू हो रहा है...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ Bot चालू है!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
