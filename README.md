# Calculator

## Telegram bot для связи с создателем

Файл `telegram_contact_bot.py` содержит пример бота, который пересылает сообщения
от пользователей создателю и позволяет отвечать им через команду `/send`.

### Запуск

1. Установите зависимости:
   ```bash
   python -m pip install python-telegram-bot==21.6
   ```
2. Создайте бота через [@BotFather](https://t.me/BotFather) и получите токен.
3. Узнайте свой `chat_id` (например, через `@userinfobot`) — это будет
   `CREATOR_CHAT_ID`.
4. Запустите:
   ```bash
   export BOT_TOKEN="ваш_токен"
   export CREATOR_CHAT_ID="ваш_chat_id"
   python telegram_contact_bot.py
   ```
