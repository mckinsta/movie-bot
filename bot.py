import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

CHANNEL_ID = -1003950636326

if os.path.exists("movies.json"):
    with open("movies.json", "r") as f:
        movies = json.load(f)
else:
    movies = []

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    for movie in movies:
        if user_text in movie["name"].lower():

            await update.message.reply_text("Sending movie... 🎬")

            await context.bot.forward_message(
                chat_id=update.effective_chat.id,
                from_chat_id=CHANNEL_ID,
                message_id=movie["message_id"]
            )
            return

    await update.message.reply_text("Movie nahi sapadli bhau 😅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, search_movie))

print("Bot started 🚀")
app.run_polling()
from db import add_movie, search_movie
if msg.document:
    name = msg.document.file_name
    file_id = msg.document.file_id
    add_movie(name, file_id) 
result = search_movie(user_text)

if result:
    await update.message.reply_document(result[1])
