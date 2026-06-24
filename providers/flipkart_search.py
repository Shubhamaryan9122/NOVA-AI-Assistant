
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9"
}

BAD_WORDS = [
    "cover",
    "case",
    "charger",
    "cable",
    "adapter",
    "tempered",
    "glass",
    "back cover",
    "skin",
    "protector",
    "earbuds",
    "headphone",
    "neckband",
    "speaker",
    "power bank"
]


def clean_title(text):

    text = text.replace(
        "Currently unavailable",
        ""
    )

    text = text.replace(
        "Add to Compare",
        ""
    )

    price_match = re.search(
        r"₹\s?[\d,]+",
        text
    )

    if price_match:
        text = text[:price_match.start()]

    rating_match = re.search(
        r"\d\.\d\s+\d[\d,]*\s+Ratings",
        text
    )

    if rating_match:
        text = text[:rating_match.start()]

    return " ".join(
        text.split()
    ).strip()


def extract_price(text):

    match = re.search(
        r"₹\s?[\d,]+",
        text
    )

    if match:
        return match.group()

    return "Price not found"


def flipkart_search(query):

    url = (
        "https://www.flipkart.com/search?q="
        + quote(query)
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        print(
            "FLIPKART STATUS:",
            response.status_code
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        products = []
        seen = set()

        for a in soup.find_all(
            "a",
            href=True
        ):

            href = a.get(
                "href",
                ""
            )

            text = a.get_text(
                " ",
                strip=True
            )

            if "/p/" not in href:
                continue

            if "₹" not in text:
                continue

            title = clean_title(text)

            if not title:
                continue

            title_lower = title.lower()

            if any(
                word in title_lower
                for word in BAD_WORDS
            ):
                continue

            if title in seen:
                continue

            seen.add(title)

            products.append(
                {
                    "title": title,
                    "price": extract_price(text),
                    "url": (
                        "https://www.flipkart.com"
                        + href
                    )
                }
            )

        return products[:10]

    except Exception as e:

        print(
            "FLIPKART ERROR:",
            e
        )

        return []

