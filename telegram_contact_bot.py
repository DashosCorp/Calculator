"""Telegram bot that lets users contact the bot creator."""

from __future__ import annotations

import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def _get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Привет! Напишите сообщение, и я передам его создателю. "
            "Он сможет ответить через команду /send."
        )


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    creator_chat_id = context.bot_data["creator_chat_id"]
    user = update.message.from_user
    sender_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Неизвестный"
    header = "Новое сообщение для создателя:\n"
    header += f"Имя: {sender_name}\n"
    if user.username:
        header += f"Username: @{user.username}\n"
    header += f"User ID: {user.id}\n"

    await context.bot.send_message(chat_id=creator_chat_id, text=header)
    await update.message.copy(chat_id=creator_chat_id)
    await update.message.reply_text("Сообщение отправлено создателю.")


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    creator_chat_id = context.bot_data["creator_chat_id"]
    if update.message.from_user.id != creator_chat_id:
        await update.message.reply_text("Эта команда доступна только создателю.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Использование: /send <user_id> <текст>")
        return

    user_id = context.args[0]
    message_text = " ".join(context.args[1:])

    try:
        await context.bot.send_message(chat_id=int(user_id), text=message_text)
        await update.message.reply_text("Ответ отправлен.")
    except ValueError:
        await update.message.reply_text("Некорректный user_id.")


def main() -> None:
    token = _get_required_env("BOT_TOKEN")
    creator_chat_id = int(_get_required_env("CREATOR_CHAT_ID"))

    application = Application.builder().token(token).build()
    application.bot_data["creator_chat_id"] = creator_chat_id

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send", send))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    LOGGER.info("Bot started")
    application.run_polling()


if __name__ == "__main__":
    main()
