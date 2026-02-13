from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

from core.lyrics import get_lyrics

TOKEN = os.getenv("TELEGRAM_TOKEN")

user_states = {}

def start(update, context):
    user_id = update.message.from_user.id
    user_states[user_id] = {"step": "artist"}
    update.message.reply_text("🎤 Send artist name")

def handle_message(update, context):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_states:
        update.message.reply_text("Send /start first")
        return

    step = user_states[user_id]["step"]

    if step == "artist":
        user_states[user_id]["artist"] = text
        user_states[user_id]["step"] = "song"
        update.message.reply_text("🎵 Now send song name")

    elif step == "song":
        artist = user_states[user_id]["artist"]
        song = text

        update.message.reply_text("⏳ Searching...")

        lyrics = get_lyrics(artist, song)

        max_length = 4000
        if len(lyrics) > max_length:
            for i in range(0, len(lyrics), max_length):
                update.message.reply_text(lyrics[i : i + max_length])
        else:
            update.message.reply_text(lyrics)

        user_states[user_id]["step"] = "artist"

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()
