import asyncio
import json
import os
from urllib.parse import urlparse

import aiohttp

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
async def TelegramBot(session, msg):
    api_https = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}

    async with session.post(api_https, data=payload) as r:
        if r.status == 200:
            print("Notification sent!")


async def fetch(session, data):
    url = data["url"]
    keyword = data.get("keyword")
    value = data.get("value")
    description = data.get("description", "")

    website = urlparse(url).netloc

    try:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"Scraping {website} failed")
                return

            html = await response.text()  # Scrapped html
            print(f"Scraping {website} passed")

            trigger = False

            if keyword:
                trigger = keyword.lower() in html.lower()

            if value:
                trigger = value in html

            if trigger:
                msg = f"{description}\n{url}"
                await TelegramBot(session, msg)

    except asyncio.TimeoutError:
        print(f"Timeout while scraping {website}")

    except aiohttp.ClientError as e:
        print(f"Error scraping {website}: {e}")


async def main():
    url_data = ReadJSON("urls.json")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, data) for data in url_data]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
