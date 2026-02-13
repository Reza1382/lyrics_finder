from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from core.lyrics import get_lyrics


TOKEN = "8251636783:AAFURdfwQRlvgVsT8ZjyxuZ4drksWewArDA"


user_states = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_states[update.effective_user.id] = {"step": "artist"}
    await update.message.reply_text("🎤 Send artist name")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_states:
        await update.message.reply_text("Send /start first")
        return

    step = user_states[user_id]["step"]

    if step == "artist":
        user_states[user_id]["artist"] = text
        user_states[user_id]["step"] = "song"
        await update.message.reply_text("🎵 Now send song name")

    elif step == "song":

        artist = user_states[user_id]["artist"]
        song = text

        await update.message.reply_text("⏳ Searching...")

        lyrics = get_lyrics(artist, song)

        # محدودیت تلگرام: 4096 کاراکتر
        max_length = 4000

        if len(lyrics) > max_length:
            for i in range(0, len(lyrics), max_length):
                await update.message.reply_text(lyrics[i : i + max_length])
        else:
            await update.message.reply_text(lyrics)

        user_states[user_id]["step"] = "artist"


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot is running...")
    app.run_polling()
