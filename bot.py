import json
import os
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = os.getenv("BOT_TOKEN")

with open("movies.json", "r") as f:
    movies = json.load(f)

def search_movie(update, context):
    user_text = update.message.text.lower()

    for movie in movies:
        if user_text in movie["name"].lower():
            update.message.reply_text(
                f"{movie['name']} ({movie['year']})\nWatch: {movie['link']}"
            )
            return

    update.message.reply_text("Movie nahi sapadli bhau 😅")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text, search_movie))

updater.start_polling()
updater.idle()
