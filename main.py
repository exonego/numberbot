import requests
import time

from tokeninfo import bot_token

API_URL = "https://api.telegram.org/bot"
API_NUMBERS_URL = "http://numbersapi.com/42"
BOT_TOKEN = bot_token
ERROR_TEXT = "Тут должен был быть случайный факт о числе 42."

offset = -2
counter = 0
numbers_response: requests.Response
number_text: str


while counter < 100:
    print("attempt =", counter)
    updates = requests.get(
        f"{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}"
    ).json()

    if updates["result"]:
        for result in updates["result"]:
            offset = result["update_id"]
            chat_id = result["message"]["from"]["id"]
            numbers_response = requests.get(API_NUMBERS_URL)
            if numbers_response.status_code == 200:
                number_text = numbers_response.text
                requests.get(
                    f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={number_text}"
                )
            else:
                requests.get(
                    f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}"
                )

    time.sleep(1)
    counter += 1
