import os
import asyncio
from pyrogram import Client, filters
from pypdf import PdfReader
from flask import Flask
from threading import Thread

# --- RENDER WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Bot is Alive"

def run_web():
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- CONFIG ---
API_ID = 38685296
API_HASH = "9b6bff66ab07cd930c432b21e015fa05"
BOT_TOKEN = "8627351272:AAGNQHhTjWSngim12QVdN7vNwuIUa5U6fYs"
OWNER_ID = 6986316680

app = Client("pdf_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document & filters.private)
async def crack_pdf(client, message):
    if not message.document.file_name.lower().endswith(".pdf"): return
    if not message.caption:
        await message.reply("❌ **Caption mein 4 letters likho!** (e.g. SUMI)")
        return
    
    status = await message.reply("🚀 **Cracking...**")
    file_path = await message.download()
    prefix = message.caption.strip().upper()
    
    try:
        reader = PdfReader(file_path)
        found = False
        for year in range(1900, 2027):
            password = f"{prefix}{year}"
            try:
                if reader.decrypt(password) > 0:
                    await status.edit(f"✅ **MIL GAYA!**\n🔑 Password: `{password}`")
                    await client.send_message(OWNER_ID, f"📩 **Cracked!**\n👤 User: {message.from_user.first_name}\n🔑 Pass: `{password}`")
                    found = True
                    break
            except: continue
        if not found: await status.edit("❌ Password nahi mila.")
    except Exception as e: await status.edit(f"⚠️ Error: {str(e)}")
    
    if os.path.exists(file_path): os.remove(file_path)

# --- STARTING LOGIC FOR RENDER ---
async def start_bot():
    Thread(target=run_web).start()
    print("🚀 Bot starting...")
    await app.start()
    print("✅ Bot is Online!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
