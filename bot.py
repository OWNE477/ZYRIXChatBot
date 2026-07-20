import os
from openai import OpenAI

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)

# گرفتن کلیدها از Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# اتصال OpenAI
client = None

if OPENAI_KEY:
    client = OpenAI(api_key=OPENAI_KEY)


async def ask_ai(message):
    if client is None:
        return "❌ کلید هوش مصنوعی تنظیم نشده است."

    try:
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "تو دستیار هوش مصنوعی ZYRIX هستی. پاسخ‌ها را فارسی و دوستانه بده."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return result.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", e)
        return "❌ خطا در اتصال هوش مصنوعی"


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    await update.message.chat.send_action("typing")

    answer = await ask_ai(text)

    await update.message.reply_text(answer)


def main():

    if not BOT_TOKEN:
        print("BOT_TOKEN پیدا نشد")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("ZYRIXChatBot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
