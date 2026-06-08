import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

VIDEO1 = "BAACAgQAAyEFAASsX1-0AAMQaiUugm7SJt-edUnbvW-7UxHoDhoAAkseAAL3PwFRowNLEaf6ZNI7BA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) > 0:

        if context.args[0] == "movie1":
            await context.bot.send_video(
                chat_id=update.effective_user.id,
                video=VIDEO1,
                caption="🎬 Movie 1"
            )
            return

    await update.message.reply_text(
        "🎬 Welcome to CineBox BD"
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
