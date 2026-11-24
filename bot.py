import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DASHBOARD = "https://mwas748.github.io/aviator-intel/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Welcome to AVIATOR INTEL!\n\n"
        "📊 Historical statistics dashboard\n\n"
        "/dashboard - Open dashboard\n"
        "/stats - Historical statistics\n"
        "/history - Recorded results\n"
        "/help - Available commands\n\n"
        "Past results cannot predict future outcomes."
    )


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 AVIATOR INTEL DASHBOARD\n\n" + DASHBOARD
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "View your historical statistics here:\n" + DASHBOARD
    )


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "View your recorded results here:\n" + DASHBOARD
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("help", start))

    app.run_polling()


if __name__ == "__main__":
    main()
