import requests
from urllib.parse import quote

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

def amazon_search(query):

    url = (
        "https://www.amazon.in/s?k="
        f"{quote(query)}"
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        print("AMAZON STATUS:", response.status_code)
        print(response.text[:1000])

        return response.text

    except Exception as e:

        print("AMAZON ERROR:", e)
        return ""