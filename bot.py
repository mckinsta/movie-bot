import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from db import add_movie, get_parts, get_movie_by_part

TOKEN = "YOUR_TOKEN"

# 📥 Save movie (with part support)
async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.document or msg.video:
        if msg.document:
            name = msg.document.file_name
            file_id = msg.document.file_id
        else:
            name = msg.video.file_name if msg.video.file_name else "movie"
            file_id = msg.video.file_id

        # 👉 name format: kgf_1, kgf_2 asa thev
        if "_" in name:
            movie_name, part = name.lower().split("_")
            part = int(part)
        else:
            movie_name = name.lower()
            part = 1

        add_movie(movie_name, part, file_id)

        await msg.reply_text(f"Saved ✔️ {movie_name} Part {part}")


# 🔍 Search → show parts buttons
async def search_movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()

    parts = get_parts(query)

    if parts:
        buttons = []

        for p in parts:
            buttons.append([InlineKeyboardButton(f"🎬 Part {p}", callback_data=f"{query}|{p}")])

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.reply_text(
            f"🎬 {query.upper()} – Choose Part",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("❌ Movie nahi sapadli bhau 😅")


# 🎯 Button click → send correct part WITH caption
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")
    name = data[0]
    part = int(data[1])

    result = get_movie_by_part(name, part)

    if result:
        file_id = result

        try:
            await query.message.reply_video(
                file_id,
                caption=f"🎬 {name.upper()} - Part {part} 🍿"
            )
        except:
            await query.message.reply_document(
                file_id,
                caption=f"🎬 {name.upper()} - Part {part} 🍿"
            )


# 🚀 App setup
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO, save_movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie_handler))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot started 🚀")
app.run_polling()
