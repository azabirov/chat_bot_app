import logging
import requests
import os
import telegram
import time
from dotenv import load_dotenv


class TelegramBotHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(text=log_entry, chat_id=self.chat_id)


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.environ.get("telegram_token"))
    logger = logging.getLogger('Logger')
    logger.addHandler(TelegramBotHandler(bot, chat_id=os.environ["admin_chat_id"]))
    try:
        logger.warning('Бот запущен')
        headers = {
                    'Authorization': f'Token {os.environ.get("token")}'
        }
        timestamp = ""
        while True:
            try:
                response = requests.get("https://dvmn.org/api/long_polling/",
                                        timeout=5, headers=headers, params={"timestamp":timestamp})
                response.raise_for_status()
                attempts = response.json()
                if attempts["status"] == 'found':
                    last_response = attempts['new_attempts'][0]
                    timestamp = attempts["last_attempt_timestamp"]
                    if last_response["is_negative"]:
                        bot.send_message(text=f''' У вас проверили работу "{last_response["lesson_title"]}"
                        \nК сожалению в работе нашли ошибки.
                        \nСсылка на урок: {last_response["lesson_url"]}
                        ''', chat_id=os.environ["chat_id"])
                    else:
                        bot.send_message(text=f'''У вас проверили работу "{last_response["lesson_title"]}"
                        \nПреподавателю все понравилось!
                        \nМожно приступать к следующему уроку.
                        ''', chat_id=os.environ["chat_id"])
                if attempts["status"] == 'timeout':
                    timestamp = response["timestamp_to_request"]

            except requests.exceptions.ReadTimeout:
                pass
            except ConnectionError:
                time.sleep(20)
    except Exception as e:
        logger.error("В работе бота возникла ошибка:")
        logger.exception(e)


if __name__ == "__main__":
    main()
