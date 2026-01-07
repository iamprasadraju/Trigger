import json
import os
from urllib.parse import urlparse

import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml",
    "Referer": "https://google.com",
}


# Read json file
def ReadJSON(file):
    try:
        with open(file, "r") as file:
            data = json.load(file)
            return data["urls"]
    except FileNotFoundError:
        print("Error: The file 'urls.json' was not found.")


# Send msg to Telegram bot, if conditions are met
def TelegramBot(msg):
    api_https = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}

    response = requests.post(api_https, data=payload)
    if response.status_code == 200:
        print("Notification sent!")


def fetch(data):
    url = data["url"]
    keyword = data.get("keyword")
    value = data.get("value")
    description = data.get("description", "")

    website = urlparse(url).netloc

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Scraping {website} failed")
        return

    html = response.text  # Scrapped html
    print(f"Scraping {website} passed")

    trigger = False

    if keyword:
        trigger = keyword.lower() in html.lower()

    if value:
        trigger = value in html

    if trigger:
        msg = f"{description}\n{url}"
        TelegramBot(msg)


def main():
    url_data = ReadJSON("urls.json")
    for data in url_data:
        fetch(data)


if __name__ == "__main__":
    main()
