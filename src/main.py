import json
import os
from urllib.parse import urlparse

import requests

TELEGRAM_BOT_TOKEN = os.environ("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ("CHAT_ID")

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


def ReadJSON(file):
    try:
        with open(file, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: The file 'urls.json' was not found.")


def scraper(url):
    website = urlparse(url).netloc

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Scraping", website, "failed.")
        return None
    else:
        print("Scraping", website, "Passed.")
        return r.text  # type:str


def Trigger(url_data):  # data -> url, keyword?value
    for data in url_data["urls"]:
        url = data["url"]
        fetch_info = scraper(url)
        desciption = data["description"]

        if fetch_info is not None:
            if data.get("value"):
                value = data["value"]
                # return f"{desciption}\n{url}"
            else:
                keyword = data["keyword"]
                if keyword.lower() in fetch_info.lower():
                    yield f"{desciption}\n{url}"


def TelegramBot(msg):
    api_https = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}

    requests.post(api_https, data=payload)


if __name__ == "__main__":
    data = ReadJSON("urls.json")
    msgs = Trigger(data)
    for msg in msgs:
        TelegramBot(msg)
