import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

VIDEO_FILE_ID = "BAACAgQAAyEFAASsX1-0AAMQaiUugm7SJt-edUnbvW-7UxHoDhoAAkseAAL3PwFRowNLEaf6ZNI7BA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("▶ Watch Now", callback_data="movie1")]
    ]

    await update.message.reply_photo(
        photo="https://picsum.photos/800/450",
        caption="""
🎬 Movie 1

⭐ Rating: 8.5/10
🎭 Category: Action
📝 Description:
Best action movie collection.

👇 Click Watch Now
""",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "movie1":
        await context.bot.send_video(
            chat_id=query.from_user.id,
            video=VIDEO_FILE_ID,
            caption="🎬 Movie 1"
        )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
