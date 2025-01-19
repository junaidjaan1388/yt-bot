from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("7547355316:AAF2XAkqpYYBGJ2DXoh4RhdTxeZVmpN94wY")

def download_youtube_video(url: str) -> str:
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  
            'format': 'mp4',  
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  
            file_path = ydl.prepare_filename(info_dict)  
        return file_path
    except Exception as e:
        return f"Error: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a YouTube video link, and I'll download it for you!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("Downloading the YouTube video... Please wait.")
        file_path = download_youtube_video(url)

        if file_path and os.path.exists(file_path):
            await update.message.reply_text("Download complete! Sending the video...")
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video)
            os.remove(file_path) 
        else:
            await update.message.reply_text("Failed to download the video. Please check the link and try again.")
    else:
        await update.message.reply_text("This bot only supports YouTube video links!")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    main()
