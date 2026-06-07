import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7890690659

db = sqlite3.connect("movies.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    file_id TEXT
)
""")
db.commit()

waiting_for_title = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Movies", callback_data="movies")]
    ]

    await update.message.reply_text(
        "Welcome to Movie Bot",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def addmovie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    waiting_for_title[update.effective_user.id] = True

    await update.message.reply_text(
        "ভিডিও পাঠাও এবং Caption-এ Movie Name লিখো"
    )

async def save_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.video:
        title = update.message.caption or "Untitled Movie"
        file_id = update.message.video.file_id

        cursor.execute(
            "INSERT INTO movies(title,file_id) VALUES(?,?)",
            (title, file_id)
        )
        db.commit()

        await update.message.reply_text(
            f"✅ Saved: {title}"
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "movies":
        cursor.execute("SELECT id,title FROM movies")
        movies = cursor.fetchall()

        keyboard = []

        for movie in movies:
            keyboard.append([
                InlineKeyboardButton(
                    movie[1],
                    callback_data=f"movie_{movie[0]}"
                )
            ])

        await query.message.reply_text(
            "🎬 Movie Library",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("movie_"):
        movie_id = int(query.data.split("_")[1])

        cursor.execute(
            "SELECT title,file_id FROM movies WHERE id=?",
            (movie_id,)
        )

        movie = cursor.fetchone()

        if movie:
            await context.bot.send_video(
                chat_id=query.from_user.id,
                video=movie[1],
                caption=f"🎬 {movie[0]}"
            )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addmovie", addmovie))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.VIDEO, save_video))

app.run_polling()
