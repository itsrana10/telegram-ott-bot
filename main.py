import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ভিডিও আমাকে পাঠাও, আমি FILE_ID দেখাব।"
    )

async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        await update.message.reply_text(
            f"FILE_ID:\n{update.message.video.file_id}"
        )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, get_video))

app.run_polling()
