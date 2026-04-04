import os
import asyncio
from pyrogram import Client, filters, idle
from pypdf import PdfReader
from flask import Flask
from threading import Thread

# --- RENDER FAKE WEB SERVER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Bot is Alive and Running!"

def run_web():
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- CONFIG ---
API_ID = 38685296
API_HASH = "9b6bff66ab07cd930c432b21e015fa05"
BOT_TOKEN = "8627351272:AAGNQHhTjWSngim12QVdN7vNwuIUa5U6fYs"
OWNER_ID = 6986316680

app = Client("pdf_cracker_render", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
                    await status.edit(f"✅ **MIL GAYA!**\n🔑 Pass: `{password}`")
                    await client.send_message(OWNER_ID, f"📩 Cracked!\n🔑 `{password}`")
                    found = True
                    break
            except: continue
        if not found: await status.edit("❌ Password nahi mila.")
    except Exception as e: await status.edit(f"⚠️ Error: {str(e)}")
    
    if os.path.exists(file_path): os.remove(file_path)

# --- THE ULTIMATE RENDER STARTUP ---
async def main():
    # Start Web Server in background
    Thread(target=run_web).start()
    print("🚀 Web server started...")
    
    # Start Bot
    await app.start()
    print("✅ Bot is Online!")
    
    # Keep bot running
    await idle()
    
    # Stop Bot safely
    await app.stop()

if __name__ == "__main__":
    # Manual loop creation to fix "No current event loop"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
