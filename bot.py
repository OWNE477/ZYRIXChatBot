import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ZYRIXChatBot is running")


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\nمن ZYRIXChatBot هستم 🤖\nپیامت رو بفرست."
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if client is None:
        await update.message.reply_text(
