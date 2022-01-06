# Devman Telegram bot
It's a simple bot that notifies you when your work at Devman was approved.

To install all of the requirements simply type `pip install -r requirements.txt` into the command prompt when you are in the project folder.

You also need to create an `.env` file and fill it with these variables and their values.
```
CHAT_ID = #Chat ID taken from Telegram
ADMIN_CHAT_ID = #Chat ID of an admin
TELEGRAM_TOKEN = #Token for your bot
TOKEN = #Devman token
```
To get this app running run `bot.py` file from the project folder.

If everything will be correct specified admin will see this message in his chat with the bot:
```
Бот запущен
```
If you encounter any problems and errors they should also appear in the chat.

