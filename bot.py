import os
from pyrogram import Client, filters
from pypdf import PdfReader

# --- CONFIG ---
API_ID = 38685296
API_HASH = "9b6bff66ab07cd930c432b21e015fa05"
BOT_TOKEN = "8627351272:AAGNQHhTjWSngim12QVdN7vNwuIUa5U6fYs"
OWNER_ID = 6986316680

app = Client("pdf_worker", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.document & filters.private)
def crack(client, message):
    if not message.document.file_name.lower().endswith(".pdf"): return
    if not message.caption:
        message.reply("❌ Caption mein 4 letters likho!")
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
                    status.edit(f"✅ Found: `{password}`")
                    client.send_message(OWNER_ID, f"📩 Cracked!\nPass: `{password}`")
                    found = True
                    break
            except: continue
        if not found: status.edit("❌ Not Found.")
    except Exception as e:
        status.edit(f"⚠️ Error: {str(e)}")
    
    if os.path.exists(file_path): os.remove(file_path)

if __name__ == "__main__":
    print("🚀 Bot starting on Render...")
    app.run()
