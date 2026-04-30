import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from db import add_movie, get_parts, get_movie_by_part

TOKEN = "8703680242:AAGgbzLIrx2rEMT4VDdZbru-E7jpt-Ss_Tc"


# 📥 SAVE MOVIE
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    file_id = None
    file_name = "movie"

    if msg.document:
        file_id = msg.document.file_id
        file_name = msg.document.file_name or "movie"

    elif msg.video:
        file_id = msg.video.file_id
        file_name = msg.video.file_name or "movie"

    if not file_id:
        await msg.reply_text("❌ File_id मिळाला नाही bhau")
        return

    file_name = file_name.lower().replace(".mp4", "").strip()

    if "_" in file_name:
        movie_name, part = file_name.rsplit("_", 1)
        try:
            part = int(part)
        except:
            part = 1
    else:
        movie_name = file_name
        part = 1

    movie_name = movie_name.strip().lower()

    add_movie(movie_name, part, file_id)

    await msg.reply_text(f"✔️ Saved: {movie_name} Part {part}")

# 🔍 SEARCH MOVIE
async def search_movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower().replace(".mp4", "").strip()

    parts = get_parts(query)

    if not parts:
        await update.message.reply_text("❌ Movie नाही सापडली bhau 😅")
        return

    buttons = []
    for p in parts:
        buttons.append([
            InlineKeyboardButton(
                f"🎬 Part {p}",
                callback_data=f"{query}|{p}"
            )
        ])

    await update.message.reply_text(
        f"🎬 {query.upper()} - Choose Part",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 🎯 BUTTON CLICK → SEND MOVIE
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        name, part = query.data.split("|")
        part = int(part)

        name = name.strip().lower()

        file_id = get_movie_by_part(name, part)

        if not file_id:
            await query.message.reply_text("❌ Movie file सापडली नाही")
            return

        try:
            await query.message.reply_video(
                video=file_id,
                caption=f"🎬 {name.upper()} - Part {part} 🍿"
            )
        except:
            await query.message.reply_document(
                document=file_id,
                caption=f"🎬 {name.upper()} - Part {part} 🍿"
            )

    except Exception as e:
        await query.message.reply_text("⚠️ Error आली bhau")


# 🚀 APP SETUP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO, save_movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie_handler))
app.add_handler(CallbackQueryHandler(button_handler))

print("🚀 Bot Started")
app.run_polling()
