import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from db import add_movie, search_movie

TOKEN = os.environ.get("BOT_TOKEN")

CHANNEL_ID = -1003950636326


# 📥 Save (forwarded/uploaded movies)
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.document or msg.video:
    if msg.document:
        name = msg.document.file_name
        file_id = msg.document.file_id
    else:
        name = msg.video.file_name or "movie"
        file_id = msg.video.file_id

    add_movie(name, file_id)
    await msg.reply_text("Saved ✔️")


# 🔍 Search
async def search_movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    result = search_movie(user_text)

    if result:
        await update.message.reply_document(result[1])
    else:
        await update.message.reply_text("Movie nahi sapadli bhau 😅")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.Document.ALL, save_movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie_handler))

print("Bot started 🚀")
app.run_polling()
