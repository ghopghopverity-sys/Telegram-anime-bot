import os
import asyncio
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_URL = "https://pollinations.ai"

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    await update.message.reply_text("✨ Cloud servers are generating your anime artwork...")
    
    # Auto-inject quality prompts so your phone text turns into crisp art
    sanitized = requests.utils.quote(user_prompt)
    anime_tags = "masterpiece, highly detailed anime style, vivid colors, flawless expression, "
    
    image_url = f"{API_URL}{requests.utils.quote(anime_tags)}{sanitized}?enhance=true&nologo=true&private=true"
    await update.message.reply_photo(photo=image_url)

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))
    print("Telegram Bot is listening...")
    app.run_polling(close_loop=False)

# Dummy web server to pass Render's free tier port health checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot Server Online")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

if __name__ == '__main__':
    # Start bot thread
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    # Start web container service
    run_health_server()
