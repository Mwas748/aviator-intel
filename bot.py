
import os
import asyncio
import json
import urllib.request

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

DASHBOARD = "https://mwas748.github.io/aviator-intel/"


def fetch_results(limit=100):
    url = (
        SUPABASE_URL.rstrip("/")
        + "/rest/v1/aviator_results"
        + f"?select=multiplier,created_at"
        + f"&order=id.desc&limit={limit}"
    )

    headers = {"apikey": SUPABASE_KEY}

    if not SUPABASE_KEY.startswith("sb_"):
        headers["Authorization"] = f"Bearer {SUPABASE_KEY}"

    request = urllib.request.Request(
        url, headers=headers
    )

    with urllib.request.urlopen(
        request, timeout=15
    ) as response:
        return json.loads(response.read())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✈️ Welcome to AVIATOR INTEL!\n\n"
        "📊 Historical statistics dashboard\n\n"
        "/dashboard - Open dashboard\n"
        "/stats - Historical statistics\n"
        "/history - Recorded results\n"
        "/status - Database connection\n"
        "/help - Available commands\n\n"
        "Past results cannot predict future outcomes."
    )


async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 AVIATOR INTEL DASHBOARD\n\n" + DASHBOARD
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await asyncio.to_thread(fetch_results, 1)
        await update.message.reply_text(
            "✅ Supabase connection successful."
        )
    except Exception:
        await update.message.reply_text(
            "❌ Database connection failed. "
            "Check Railway variables and permissions."
        )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        results = await asyncio.to_thread(
            fetch_results, 100
        )

        values = [
            float(row["multiplier"])
            for row in results
        ]

        if not values:
            await update.message.reply_text(
                "No recorded results yet."
            )
            return

        await update.message.reply_text(
            "📊 HISTORICAL STATISTICS\n\n"
            f"Recorded sample: {len(values)}\n"
            f"Average: {sum(values)/len(values):.2f}x\n"
            f"Highest: {max(values):.2f}x\n"
            f"Lowest: {min(values):.2f}x\n\n"
            "Historical data only. "
            "Not a prediction."
        )

    except Exception:
        await update.message.reply_text(
            "Unable to retrieve statistics."
        )


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        results = await asyncio.to_thread(
            fetch_results, 10
        )

        if not results:
            await update.message.reply_text(
                "No recorded results yet."
            )
            return

        lines = [
            f"{i}. {float(row['multiplier']):.2f}x"
            for i, row in enumerate(results, 1)
        ]

        await update.message.reply_text(
            "📋 LAST 10 RECORDED RESULTS\n\n"
            + "\n".join(lines)
        )

    except Exception:
        await update.message.reply_text(
            "Unable to retrieve results."
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dashboard", dashboard))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("help", start))

    app.run_polling()


if __name__ == "__main__":
    main()
