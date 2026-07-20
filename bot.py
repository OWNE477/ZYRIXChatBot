
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ZYRIXChatBot هستم 🤖")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("پیامت دریافت شد ✅")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("ZYRIXChatBot is ready!")

app.run_polling()
