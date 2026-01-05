import asyncio
import json
import time
from os import getenv
from urllib.parse import urlparse

import aiohttp
import requests
from dotenv import load_dotenv

load_dotenv()

# Reads ENV from .env file
TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = getenv("CHAT_ID")

# Header mimic the Browser request
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


# Scrape the html from url
def scraper(url):
    website = urlparse(url).netloc

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Scraping", website, "failed.")
        return None
    else:
        print("Scraping", website, "Passed.")
        return r.text  # type:str


# Checks wheather conditions are met
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


# Send msg to Telegram bot, if conditions are met
def TelegramBot(msg):
    api_https = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}

    response = requests.post(api_https, data=payload)
    if response:
        print("Notification sent!")


async def fetch(session, url):
    website = urlparse(url).netloc
    async with session.get(url, headers=headers) as response:
        html = return await response.text()  # Scrapped html


async def main():
    url_data = ReadJSON("urls.json")
    tasks = []

    async with aiohttp.ClientSession() as session:
        for info in url_data:
            url = info["url"]
            tasks.append(fetch(session, url))

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

