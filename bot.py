import os
from pyrogram import Client, filters
from pypdf import PdfReader
from flask import Flask
from threading import Thread

# --- FAKE WEBSITE FOR RENDER ---
web_app = Flask(__name__)
@web_app.route('/')
def home(): return "Bot is Online"

def run_web():
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- BOT CONFIG ---
API_ID = 38685296
API_HASH = "9b6bff66ab07cd930c432b21e015fa05"
BOT_TOKEN = "8627351272:AAGNQHhTjWSngim12QVdN7vNwuIUa5U6fYs"
OWNER_ID = 6986316680

app = Client("final_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document & filters.private)
def crack_pdf(client, message):
    if not message.document.file_name.lower().endswith(".pdf"): return
    if not message.caption:
        message.reply("❌ **Caption mein 4 letters likho!**")
        return
    
    status = message.reply("🚀 **Cracking...**")
    file_path = message.download()
    prefix = message.caption.strip().upper()
    
    try:
        reader = PdfReader(file_path)
        found = False
        for year in range(1900, 2027):
            password = f"{prefix}{year}"
            try:
                if reader.decrypt(password) > 0:
                    status.edit(f"✅ **MIL GAYA!**\n🔑 Pass: `{password}`")
                    client.send_message(OWNER_ID, f"📩 Cracked!\n👤 {message.from_user.first_name}\n🔑 `{password}`")
                    found = True
                    break
            except: continue
        if not found: status.edit("❌ Password nahi mila.")
    except Exception as e: status.edit(f"⚠️ Error: {str(e)}")
    
    if os.path.exists(file_path): os.remove(file_path)

# --- STARTING LOGIC ---
if __name__ == "__main__":
    # Start fake web server in background
    Thread(target=run_web).start()
    print("🚀 Bot is Starting...")
    # Start bot in main thread (No asyncio jhanjhat)
    app.run()
