import re

import requests

urls = [
    "https://www.myntra.com/shirts/wrogn/wrogn-men-navy-blue-slim-fit-striped-casual-shirt/13673098/buy",
    "https://www.ajio.com/shein-shein-full-length-fly-with-button-closure-mid-wash-jeans/p/443381647_charcoal?",
]

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


def crawl(url):
    website = re.search(r"https:\/\/www\.(.*?)\.com\/", url)

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(website.group(1), "Crawl failed.")
    else:
        print(website.group(1), "Crawl Passed !.")


for url in urls:
    crawl(url)
