import json
import re
from urllib.parse import urlparse

import requests

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

urls = []


def ReadJSON(file):
    try:
        with open(file, "r") as file:
            data = json.load(file)
            for i, data in enumerate(data["urls"]):
                url = data["url"]
                if data.get("value"):
                    value = data["value"]
                    return {"url": url, "value": value}
                else:
                    keyword = data["keyword"]
                    return {"url": url, "keyword": keyword}
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
        return r.text
