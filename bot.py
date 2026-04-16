import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = os.environ["BOT_TOKEN"]

def download_video_sync(url: str) -> str:
    opts = {
        "format": "best[filesize<50M]/best",
        "outtmpl": "/tmp/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("Надішли мені посилання на відео 👇")
        return

    msg = await update.message.reply_text("⏳ Завантажую...")

    try:
        filepath = await asyncio.to_thread(download_video_sync, url)

        with open(filepath, "rb") as video:
            await update.message.reply_video(video)

        if os.path.exists(filepath):
            os.remove(filepath)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ Помилка: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущено!")
    app.run_polling()

if __name__ == "__main__":
    main()