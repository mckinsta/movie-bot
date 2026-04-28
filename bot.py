import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

with open("movies.json", "r") as f:
    movies = json.load(f)

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    results = []

    for movie in movies:
        if user_text in movie["name"].lower():
            results.append(movie)

    if results:
        for movie in results[:3]:
            await update.message.reply_text(
                f"{movie['name']} ({movie['year']})\nWatch: {movie['link']}"
            )
    else:
        await update.message.reply_text("Movie nahi sapadli bhau 😅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, search_movie))

app.run_polling()
