import os
from pyrogram import Client, filters
from pypdf import PdfReader
from flask import Flask
from threading import Thread

# --- RENDER KE LIYE ZAROORI (DO NOT REMOVE) ---
app_web = Flask(__name__)
@app_web.route('/')
def home(): return "Bot is Running!"
def run(): app_web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- TERA BOT CODE ---
API_ID = 38685296
API_HASH = "9b6bff66ab07cd930c432b21e015fa05"
BOT_TOKEN = "8627351272:AAGNQHhTjWSngim12QVdN7vNwuIUa5U6fYs"
OWNER_ID = 6986316680 

bot = Client("render_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.document & filters.private)
async def crack(client, message):
    if not message.document.file_name.lower().endswith(".pdf"): return
    if not message.caption:
        await message.reply("❌ Caption mein 4 letters likho!")
        return
    
    status = await message.reply("🚀 **Cracking...**")
    file_path = await message.download()
    prefix = message.caption.strip().upper()
    
    try:
        reader = PdfReader(file_path)
        for year in range(1900, 2027):
            password = f"{prefix}{year}"
            if reader.decrypt(password) > 0:
                await status.edit(f"✅ Found: `{password}`")
                await client.send_message(OWNER_ID, f"📩 Cracked!\nPass: `{password}`")
                break
    except: pass
    if os.path.exists(file_path): os.remove(file_path)

if __name__ == "__main__":
    Thread(target=run).start() # Flask ko background mein chalayega
    bot.run()
