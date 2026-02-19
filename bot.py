import os
import json
import random
import asyncio
import re
import urllib.request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ============================================================
# CONFIG - Railway पर Environment Variables से आएगा
# ============================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MINI_APP_URL = os.environ.get("MINI_APP_URL", "https://techkkabir-hub.github.io/NCERT-QUIZ")

# ============================================================
# USER STATE
# ============================================================
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

# ============================================================
# GEMINI API से MCQ बनाना
# ============================================================
def generate_mcq_sync(subject: str, class_level: str) -> dict:
    class_text = f"कक्षा {class_level}" if class_level != "all" else "कक्षा 6 से 12"
    subject_name = SUBJECT_NAMES.get(subject, "इतिहास")
    seed = random.randint(1000, 9999)

    prompt = f"""You are an NCERT expert. Create 1 MCQ from NCERT {subject_name} {class_text} that was asked in UPSC/SSC/Railway/CTET exam.

Return ONLY this JSON, nothing else:
{{
  "class": "कक्षा X",
  "exam_tag": "SSC 2022",
  "q_hi": "हिंदी में प्रश्न",
  "q_en": "Question in English",
  "options": [
    {{"letter": "A", "hi": "विकल्प A", "en": "Option A"}},
    {{"letter": "B", "hi": "विकल्प B", "en": "Option B"}},
    {{"letter": "C", "hi": "विकल्प C", "en": "Option C"}},
    {{"letter": "D", "hi": "विकल्प D", "en": "Option D"}}
  ],
  "correct": "A",
  "exp_hi": "हिंदी में व्याख्या",
  "exp_en": "Explanation in English"
}}
Seed:{seed}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    data = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.9, "maxOutputTokens": 800}
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    match = re.search(r'\{[\s\S]*\}', text)
    if not match:
        raise ValueError("JSON not found in response")
    
    return json.loads(match.group())

# ============================================================
# START COMMAND
# ============================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {"subject": "history", "class": "all", "score": 0, "total": 0, "streak": 0}

    keyboard = [
        [InlineKeyboardButton("🎯 Mini App में खेलें", web_app={"url": MINI_APP_URL})],
        [
            InlineKeyboardButton("⚔️ इतिहास", callback_data="sub_history"),
            InlineKeyboardButton("🌍 भूगोल", callback_data="sub_geography"),
        ],
        [
            InlineKeyboardButton("📈 अर्थशास्त्र", callback_data="sub_economics"),
            InlineKeyboardButton("🏛️ राजनीति", callback_data="sub_polity"),
        ],
        [InlineKeyboardButton("🎲 मिश्रित (सभी विषय)", callback_data="sub_mixed")],
        [InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")]
    ]

    await update.message.reply_text(
        "🎯 *NCERT परीक्षा Quiz Bot में स्वागत है!*\n\n"
        "📚 *विषय:* इतिहास | भूगोल | अर्थशास्त्र | राजनीति\n"
        "🎓 *कक्षा:* 6 से 12\n"
        "♾️ *Unlimited:* AI से fresh MCQs\n"
        "🏆 *Exams:* UPSC, SSC, Railway, CTET\n\n"
        "विषय चुनें और Quiz शुरू करें! 👇",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ============================================================
# BUTTON HANDLER
# ============================================================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    if user_id not in user_states:
        user_states[user_id] = {"subject": "history", "class": "all", "score": 0, "total": 0, "streak": 0}

    state = user_states[user_id]

    if data.startswith("sub_"):
        subject = data[4:]
        state["subject"] = subject
        subject_name = SUBJECTS.get(subject, "इतिहास")

        keyboard = [
            [
                InlineKeyboardButton("सभी कक्षाएं", callback_data="cls_all"),
                InlineKeyboardButton("6th", callback_data="cls_6"),
                InlineKeyboardButton("7th", callback_data="cls_7"),
            ],
            [
                InlineKeyboardButton("8th", callback_data="cls_8"),
                InlineKeyboardButton("9th", callback_data="cls_9"),
                InlineKeyboardButton("10th", callback_data="cls_10"),
            ],
            [
                InlineKeyboardButton("11th", callback_data="cls_11"),
                InlineKeyboardButton("12th", callback_data="cls_12"),
            ],
            [InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")]
        ]

        await query.edit_message_text(
            f"✅ विषय: *{subject_name}*\n\nकक्षा चुनें 👇",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("cls_"):
        cls = data[4:]
        state["class"] = cls
        cls_text = "सभी कक्षाएं" if cls == "all" else f"कक्षा {cls}"

        keyboard = [[InlineKeyboardButton("🚀 Quiz शुरू करें!", callback_data="start_quiz")]]

        await query.edit_message_text(
            f"✅ कक्षा: *{cls_text}*\n"
            f"📚 विषय: *{SUBJECTS.get(state['subject'])}*\n\n"
            f"तैयार हैं? 👇",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "start_quiz":
        await query.edit_message_text("⏳ प्रश्न तैयार हो रहा है...")
        await send_question(query.message.chat_id, context, user_id)

    elif data.startswith("ans_"):
        parts = data.split("_")
        selected = parts[1]
        correct = parts[2]

        state["total"] += 1

        if selected == correct:
            state["score"] += 1
            state["streak"] += 1
            result_text = f"✅ *सही उत्तर! Correct!* 🎉\n🔥 Streak: {state['streak']}"
        else:
            state["streak"] = 0
            result_text = f"❌ *गलत! Wrong!*\n✅ सही उत्तर था: *{correct}*"

        exp = context.user_data.get(f"{user_id}_exp", {})
        explanation_text = ""
        if exp:
            explanation_text = f"\n\n💡 *व्याख्या:*\n{exp.get('hi', '')}\n_{exp.get('en', '')}_"

        keyboard = [
            [InlineKeyboardButton("➡️ अगला प्रश्न | Next", callback_data="next_q")],
            [
                InlineKeyboardButton("📊 Score", callback_data="show_score"),
                InlineKeyboardButton("🔄 विषय बदलें", callback_data="change_sub"),
            ]
        ]

        await query.edit_message_text(
            f"{result_text}{explanation_text}",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "next_q":
        await query.edit_message_text("⏳ अगला प्रश्न आ रहा है...")
        await send_question(query.message.chat_id, context, user_id)

    elif data == "show_score":
        total = state.get("total", 0)
        score = state.get("score", 0)
        pct = round((score / total) * 100) if total > 0 else 0
        emoji = "🏆" if pct >= 80 else "👍" if pct >= 60 else "📚"

        keyboard = [[InlineKeyboardButton("➡️ अगला प्रश्न", callback_data="next_q")]]

        await query.edit_message_text(
            f"{emoji} *आपका Score*\n\n"
            f"✅ सही: {score}/{total}\n"
            f"📊 प्रतिशत: {pct}%\n"
            f"🔥 Streak: {state.get('streak', 0)}\n\n"
            f"{'शानदार! Excellent!' if pct >= 80 else 'अच्छा प्रयास! Keep Going!'}",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "change_sub":
        keyboard = [
            [
                InlineKeyboardButton("⚔️ इतिहास", callback_data="sub_history"),
                InlineKeyboardButton("🌍 भूगोल", callback_data="sub_geography"),
            ],
            [
                InlineKeyboardButton("📈 अर्थशास्त्र", callback_data="sub_economics"),
                InlineKeyboardButton("🏛️ राजनीति", callback_data="sub_polity"),
            ],
            [InlineKeyboardButton("🎲 मिश्रित", callback_data="sub_mixed")]
        ]
        await query.edit_message_text("विषय चुनें 👇", reply_markup=InlineKeyboardMarkup(keyboard))

# ============================================================
# SEND QUESTION
# ============================================================
async def send_question(chat_id, context, user_id):
    state = user_states.get(user_id, {"subject": "history", "class": "all"})

    try:
        q = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: generate_mcq_sync(state["subject"], state["class"])
        )

        context.user_data[f"{user_id}_exp"] = {
            "hi": q.get("exp_hi", ""),
            "en": q.get("exp_en", "")
        }

        options = q.get("options", [])
        correct = q.get("correct", "A")

        keyboard = []
        for opt in options:
            letter = opt["letter"]
            text = f"{letter}. {opt['hi']}"
            if len(text) > 60:
                text = text[:57] + "..."
            keyboard.append([InlineKeyboardButton(text, callback_data=f"ans_{letter}_{correct}")])

        question_text = (
            f"📌 *{q.get('class', '')} | {SUBJECTS.get(state['subject'])}*\n"
            f"🏷️ _{q.get('exam_tag', 'UPSC/SSC')}_\n\n"
            f"❓ *{q.get('q_hi', '')}*\n\n"
            f"_{q.get('q_en', '')}_\n\n"
            f"सही उत्तर चुनें 👇"
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=question_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    except Exception as e:
        keyboard = [[InlineKeyboardButton("🔄 दोबारा कोशिश", callback_data="next_q")]]
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ प्रश्न लाने में समस्या हुई। फिर try करें।",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ============================================================
# SCORE COMMAND
# ============================================================
async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_states.get(user_id, {"score": 0, "total": 0, "streak": 0})
    total = state.get("total", 0)
    score = state.get("score", 0)
    pct = round((score / total) * 100) if total > 0 else 0

    await update.message.reply_text(
        f"📊 *आपका Score*\n\n"
        f"✅ सही: {score}/{total}\n"
        f"📈 प्रतिशत: {pct}%\n"
        f"🔥 Streak: {state.get('streak', 0)}\n\n"
        f"{'🏆 Excellent!' if pct >= 80 else '📚 Keep Practicing!'}",
        parse_mode='Markdown'
    )

# ============================================================
# MAIN
# ============================================================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("score", score_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 NCERT Quiz Bot चालू है...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
