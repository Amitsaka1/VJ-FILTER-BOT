
import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command("yt") & filters.private)
async def youtube_download(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a YouTube link.\nUsage: /yt <youtube link>", quote=True)

    url = message.text.split(None, 1)[1]
    buttons = [
        [
            InlineKeyboardButton("🎥 Video 720p", callback_data=f"yt_video_720|{url}"),
            InlineKeyboardButton("🎥 Video 360p", callback_data=f"yt_video_360|{url}")
        ],
        [
            InlineKeyboardButton("🎧 Audio MP3", callback_data=f"yt_audio|{url}")
        ]
    ]

    await message.reply("🔍 Select the format you want to download:",
                        reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("yt_"))
async def yt_format_handler(client, callback_query):
    data = callback_query.data
    format_type, url = data.split("|", 1)

    await callback_query.message.edit("⬇️ Downloading...")

    try:
        if format_type == "yt_audio":
            out_file = f"downloads/{callback_query.from_user.id}_audio.mp3"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': out_file,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
                'quiet': True,
            }
        else:
            quality = '18' if "360" in format_type else '22'
            out_file = f"downloads/{callback_query.from_user.id}_video.mp4"
            ydl_opts = {
                'format': quality,
                'outtmpl': out_file,
                'quiet': True,
            }

        os.makedirs("downloads", exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await client.send_document(
            chat_id=callback_query.message.chat.id,
            document=out_file,
            caption="✅ Download complete."
        )
        os.remove(out_file)

        await callback_query.message.delete()

    except Exception as e:
        await callback_query.message.edit(f"❌ Error: {str(e)}")
