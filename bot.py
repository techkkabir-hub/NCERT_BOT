import os
import json
import random
import re
import asyncio
import urllib.request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://techkkabir-hub.github.io/NCERT-QUIZ")

user_states = {}

SUBJECTS = {
    "history": "⚔️ इतिहास",
    "geography": "🌍 भूगोल",
    "economics": "📈 अर्थशास्त्र",
    "polity": "🏛️ राजनीतिशास्त्र",
    "mixed": "🎲 मिश्रित"
}

SUBJECT_NAMES = {
    "history": "इतिहास",
    "geography": "भूगोल",
    "economics": "अर्थशास्त्र",
    "polity": "राजनीतिशास्त्र",
    "mixed": "इतिहास, भूगोल, अर्थशास्त्र, राजनीतिशास्त्र"
}

def generate_mcq(subject, class_level):
    class_text = f"कक्षा {class_level}" if class_level != "all" else "कक्षा 6 से 12"
    subject_name = SUBJECT_NAMES.get(subject, "इतिहास")
    seed = random.randint(1000, 9999)
    prompt = f"""You are NCERT expert. Create 1 MCQ from NCERT {subject_name} {class_text} asked in UPSC/SSC/Railway exam.
Return ONLY valid JSON no extra text:
{{
  "class": "कक्षा 9",
  "exam_tag": "SSC 2022",
  "q_hi": "हिंदी प्रश्न",
  "q_en": "English question",
  "options": [
    {{"letter": "A", "hi": "विकल्प A", "en": "Option A"}},
    {{"letter": "B", "hi": "विकल्प B", "en": "Option B"}},
    {{"letter": "C", "hi": "विकल्प C", "en": "Option C"}},
    {{"letter": "D", "hi": "विकल्प D", "en": "Option D"}}
  ],
  "correct": "B",
  "exp_hi": "व्याख्या",
  "exp_en": "Explanation"
}}
Seed:{seed}"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    data = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 1000}
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    match = re.search(r'\{[\s\S]*\}', text)
    if not match:
        raise ValueError("JSON not found")
    return json.loads(match.group())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {"subject": "history", "class": "all", "score": 0, "total": 0, "streak": 0}
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
        "🎓 कक्षा 6 से 12 | UPSC SSC Railway CTET\n\n"
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
        user_states[user_id] = {"subject": "history", "class": "all", "score": 0, "total": 0, "streak": 0}
    state = user_states[user_id]

    if data.startswith("sub_"):
        state["subject"] = data[4:]
        keyboard = [
            [InlineKeyboardButton("सभी", callback_data="cls_all"),
             InlineKeyboardButton("6th", callback_data="cls_6"),
             InlineKeyboardButton("7th", callback_data="cls_7"),
             InlineKeyboardButton("8th", callback_data="cls_8")],
            [InlineKeyboardButton("9th", callback_data="cls_9"),
             InlineKeyboardButton("10th", callback_data="cls_10"),
             InlineKeyboardButton("11th", callback_data="cls_11"),
             InlineKeyboardButton("12th", callback_data="cls_12")],
            [InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")]
        ]
        await query.edit_message_text(
            f"✅ विषय: *{SUBJECTS.get(state['subject'])}*\nकक्षा चुनें 👇",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data.startswith("cls_"):
        state["class"] = data[4:]
        await query.edit_message_text(
            f"✅ तैयार!\nविषय: *{SUBJECTS.get(state['subject'])}*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 शुरू!", callback_data="start_quiz")]])
        )
    elif data == "start_quiz":
        await query.edit_message_text("⏳ प्रश्न तैयार हो रहा है...")
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
        exp_text = f"\n\n💡 *व्याख्या:*\n{exp.get('hi', '')}\n_{exp.get('en', '')}_" if exp else ""
        keyboard = [
            [InlineKeyboardButton("➡️ अगला प्रश्न", callback_data="next_q")],
            [InlineKeyboardButton("📊 Score", callback_data="show_score"),
             InlineKeyboardButton("🔄 विषय बदलें", callback_data="change_sub")]
        ]
        await query.edit_message_text(
            f"{result}{exp_text}", parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif data == "next_q":
        await query.edit_message_text("⏳ अगला प्रश्न...")
        await send_question(query.message.chat_id, context, user_id)
    elif data == "show_score":
        total = state.get("total", 0)
        score = state.get("score", 0)
        pct = round((score / total) * 100) if total > 0 else 0
        emoji = "🏆" if pct >= 80 else "👍" if pct >= 60 else "📚"
        await query.edit_message_text(
            f"{emoji} *Score*\n✅ {score}/{total}\n📊 {pct}%\n🔥 {state.get('streak', 0)}",
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
    state = user_states.get(user_id, {"subject": "history", "class": "all"})
    try:
        q = await asyncio.get_event_loop().run_in_executor(
            None, lambda: generate_mcq(state["subject"], state["class"])
        )
        context.user_data[f"{user_id}_exp"] = {"hi": q.get("exp_hi", ""), "en": q.get("exp_en", "")}
        correct = q.get("correct", "A")
        keyboard = []
        for opt in q.get("options", []):
            letter = opt["letter"]
            text = f"{letter}. {opt['hi']}"[:60]
            keyboard.append([InlineKeyboardButton(text, callback_data=f"ans_{letter}_{correct}")])
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📌 *{q.get('class', '')} | {SUBJECTS.get(state['subject'])}*\n"
                 f"🏷️ _{q.get('exam_tag', '')}_\n\n"
                 f"❓ *{q.get('q_hi', '')}*\n\n_{q.get('q_en', '')}_\n\nउत्तर चुनें 👇",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(f"Error: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ प्रश्न लाने में समस्या। फिर try करें।",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Try Again", callback_data="next_q")]])
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
