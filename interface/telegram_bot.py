from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from core.lyrics import get_lyrics

import os


# Token should come from environment variables (especially important for deployment)
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")


user_states = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command and initialize user state"""
    user_id = update.effective_user.id
    user_states[user_id] = {"step": "artist"}
    await update.message.reply_text("🎤 Please send the artist name")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages based on current user step"""
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_states:
        await update.message.reply_text("Please send /start first")
        return

    step = user_states[user_id]["step"]

    if step == "artist":
        user_states[user_id]["artist"] = text
        user_states[user_id]["step"] = "song"
        await update.message.reply_text("🎵 Now send the song name")

    elif step == "song":
        artist = user_states[user_id]["artist"]
        song = text

        await update.message.reply_text("⏳ Searching...")

        try:
            lyrics = get_lyrics(artist, song)

            # Telegram message limit is ~4096 characters
            max_length = 4000

            if len(lyrics) > max_length:
                for i in range(0, len(lyrics), max_length):
                    chunk = lyrics[i : i + max_length]
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(lyrics or "Lyrics not found 😔")

        except Exception as e:
            await update.message.reply_text(f"An error occurred: {str(e)}")

        # Reset to artist step for next search
        user_states[user_id]["step"] = "artist"


def run_bot():
    """Build and run the bot application (polling mode - for local/testing)"""
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running... (polling mode)")
    app.run_polling(
        drop_pending_updates=True,  # ignore old messages when bot starts
        allowed_updates=["message"],  # only process message updates
    )
