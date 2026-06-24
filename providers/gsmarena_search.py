import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

def gsmarena_search(query):

    url = (
        "https://www.gsmarena.com/results.php3?"
        f"sQuickSearch=yes&sName={quote(query)}"
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        print("GSMARENA STATUS:", response.status_code)
        print(response.text[:1000])

        with open(
            "gsmarena_debug.html",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(response.text)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        phones = []

        for li in soup.find_all("li"):

            text = li.get_text(
                " ",
                strip=True
            )

            if len(text) > 10:
                phones.append(text)

        return phones[:10]

    except Exception as e:

        print(
            "GSMARENA ERROR:",
            e
        )

        return []