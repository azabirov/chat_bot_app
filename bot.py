import requests
import os
import telegram
import time

def main():
    bot = telegram.Bot(token=os.getenv("telegram_token"))
    headers = {
                'Authorization': f'Token {os.environ["token"]}'
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
                    bot.send_message(text=f'''
                    У вас проверили работу
                    "{last_response["lesson_title"]}"\n\n
                    К сожалению в работе нашли ошибки.\n
                    Ссылка на урок: {last_response["lesson_url"]}
                    ''', chat_id=os.environ["chat_id"])
                else:
                    bot.send_message(text=f'''
                    У вас проверили работу
                    "{last_response["lesson_title"]}"\n\n
                    Преподавателю все понравилось!
                    Можно приступать к следующему уроку.''', chat_id=os.environ["chat_id"])
            if attempts["status"] == 'timeout':
                timestamp = response["timestamp_to_request"]

        except requests.exceptions.ReadTimeout:
            pass
        except ConnectionError:
            time.sleep(20)

if __name__ == "__main__":
    main()