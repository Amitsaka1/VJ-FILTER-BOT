from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dl import *  # This imports your download functions from yt_dl.py

@Client.on_message(filters.command(["yt", "youtube"]) & filters.private)
async def youtube_download_handler(client: Client, message: Message):
    url = message.text.split(maxsplit=1)[1] if len(message.command) > 1 else None
    if not url:
        return await message.reply("❌ Please send a YouTube link.\n\nExample:\n`/yt https://youtu.be/abcd1234`")

    try:
        msg = await message.reply("🔄 Downloading... Please wait.")
        # Assuming you have a function called 'download_youtube' in yt_dl.py
        file_path = await download_youtube(url)
        await client.send_document(chat_id=message.chat.id, document=file_path)
        await msg.delete()
    except Exception as e:
        await message.reply(f"❌ Failed to download video.\n**Error:** `{e}`")
