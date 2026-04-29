import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8703680242:AAGgbzLIrx2rEMT4VDdZbru-E7jpt-Ss_Tc")
CHANNEL_USERNAME = "https://t.me/+XLcp59H_lOw0NmZl"   # <-- tuza channel username

with open("movies.json", "r") as f:
    movies = json.load(f)

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    for movie in movies:
        if user_text in movie["name"].lower():

            await update.message.reply_text("Sending movie... 🎬")

            await context.bot.forward_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_USERNAME,
                message_id=movie["message_id"]
            )
            return

    await update.message.reply_text("Movie nahi sapadli bhau 😅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, search_movie))

print("Bot started 🚀")
app.run_polling()
