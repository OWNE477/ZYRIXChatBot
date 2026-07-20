import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")


# برای Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ZYRIXChatBot is running")


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton("🤖 درباره ربات", callback_data="about"),
            InlineKeyboardButton("📚 راهنما", callback_data="help")
        ]
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "سلام 👋\nمن ZYRIXChatBot هستم 🤖\n\nیک گزینه انتخاب کن:",
        reply_markup=keyboard
    )


# دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.message.reply_text(
            "🤖 ZYRIXChatBot\nربات هوشمند شما"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "📚 راهنما:\nپیامت رو ارسال کن."
        )


# پیام‌های معمولی
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "پیامت دریافت شد ✅"
    )


# اجرای سرور Render
threading.Thread(target=run_server, daemon=True).start()


if not TOKEN:
    print("BOT_TOKEN پیدا نشد!")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("ZYRIXChatBot is ready!")

app.run_polling()  
