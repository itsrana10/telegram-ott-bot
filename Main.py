from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

VIDEO_FILE_ID = "VIDEO_FILE_ID_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎬 Movie 1", callback_data="movie1")]
    ]

    await update.message.reply_text(
        "Welcome to OTT Bot\n\nSelect a movie:",
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
