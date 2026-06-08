import os
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7890690659

MOVIES_FILE = "movies.json"

waiting_for_title = {}
pending_video = {}


def load_movies():
    try:
        with open(MOVIES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_movies(movies):
    with open(MOVIES_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"CineBox BD 🎬\n\nYour ID: {update.effective_user.id}"
    )


async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_movies()

    if not data:
        await update.message.reply_text("❌ No movies found.")
        return

    text = "🎬 Movie List:\n\n"

    for i, movie in enumerate(data, start=1):
        text += f"{i}. {movie['title']}\n"

    await update.message.reply_text(text)


async def receive_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    file_id = update.message.video.file_id

    pending_video[update.effective_user.id] = file_id
    waiting_for_title[update.effective_user.id] = True

    await update.message.reply_text(
        "🎬 Movie Name?"
    )


async def receive_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        return

    if user_id not in waiting_for_title:
        return

    title = update.message.text
    file_id = pending_video[user_id]

    data = load_movies()

    data.append({
        "title": title,
        "file_id": file_id
    })

    save_movies(data)

    del waiting_for_title[user_id]
    del pending_video[user_id]

    await update.message.reply_text(
        f"✅ Movie Added:\n\n{title}"
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movies", movies))

app.add_handler(MessageHandler(filters.VIDEO, receive_video))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title))

app.run_polling()
