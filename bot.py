import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = None
if OPENAI_KEY:
    client = OpenAI(api_key=OPENAI_KEY)


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
    keyboard = [
        [
            InlineKeyboardButton("🤖 درباره ربات", callback_data="about"),
            InlineKeyboardButton("📚 راهنما", callback_data="help")
        ]
    ]

    await update.message.reply_text(
        "سلام 👋\nمن ZYRIXChatBot هستم 🤖\nپیامت رو بفرست.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.message.reply_text(
            "🤖 ZYRIXChatBot\nربات هوشمند گفتگو"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "💬 سوالت رو بفرست."
        )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text(
            "⚠️ هوش مصنوعی هنوز وصل نشده."
        )
        return

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=update.message.text
        )

        await update.message.reply_text(
            response.output_text
        )

    except Exception:
        await update.message.reply_text(
            "❌ خطا در اتصال به هوش مصنوعی"
        )


threading.Thread(target=run_server, daemon=True).start()


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("ZYRIXChatBot is ready!")

app.run_polling()
