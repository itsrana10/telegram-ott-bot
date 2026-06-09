import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from fastapi import FastAPI
import uvicorn
import threading

from database import init, add_movie, get_movie, get_movies

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7890690659

init()

# ---------------- BOT ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args:
        movie = get_movie(args[0])
        if movie:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=movie["file_id"],
                caption=movie["title"]
            )
            return

    await update.message.reply_text("🎬 CineBox BD")

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data["file_id"] = update.message.video.file_id
    await update.message.reply_text("🎬 Movie Name পাঠাও")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    file_id = context.user_data.get("file_id")
    title = update.message.text

    if not file_id:
        return

    movie_id = f"movie{len(get_movies())+1}"

    add_movie(movie_id, title, file_id)

    await update.message.reply_text(f"✅ Saved: {movie_id}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, video_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

# ---------------- FASTAPI ----------------

api = FastAPI()

@api.get("/movies")
def movies():
    return get_movies()

# ---------------- RUN BOTH ----------------

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000)

threading.Thread(target=run_api).start()

app.run_polling()
