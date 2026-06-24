import webbrowser
import feedparser
import time
import os

from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor


# =========================================================
# NEWS SOURCES
# =========================================================

NEWS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
    "https://www.reutersagency.com/feed/?best-topics=world&post_type=best"
    "https://apnews.com/hub/ap-top-news?output=rss"
]

CRYPTO_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://cryptopotato.com/feed/"
]


# =========================================================
# CACHE
# =========================================================

NEWS_CACHE = ""
CACHE_TIME = 0
CACHE_DURATION = 60  # 1 min


# =========================================================
# FETCH SINGLE FEED
# =========================================================

def fetch_feed(url):

    headlines = []

    try:

        feed = feedparser.parse(url)

        for item in feed.entries[:3]:

            headlines.append(
                item.title
            )

    except Exception as e:

        print(
            "Feed Error:",
            e
        )

    return headlines


# =========================================================
# WORLD NEWS
# =========================================================

def get_world_news():

    global NEWS_CACHE
    global CACHE_TIME

    # Cache hit
    if (
        NEWS_CACHE
        and time.time() - CACHE_TIME
        < CACHE_DURATION
    ):
        return NEWS_CACHE

    headlines = []

    try:

        with ThreadPoolExecutor(
            max_workers=5
        ) as executor:

            results = executor.map(
                fetch_feed,
                NEWS_FEEDS
            )

            for items in results:
                headlines.extend(items)

    except Exception as e:

        print(
            "World News Error:",
            e
        )

    if not headlines:
        return "Unable to fetch world news."

    result = "\n".join(
        headlines[:5]
    )

    NEWS_CACHE = result
    CACHE_TIME = time.time()

    return result


# =========================================================
# CRYPTO NEWS
# =========================================================

def get_crypto_news():

    headlines = []

    try:

        with ThreadPoolExecutor(
            max_workers=2
        ) as executor:

            results = executor.map(
                fetch_feed,
                CRYPTO_FEEDS
            )

            for items in results:
                headlines.extend(items)

    except Exception as e:

        print(
            "Crypto Error:",
            e
        )

    if not headlines:
        return "Unable to fetch crypto news."

    return "\n".join(
        headlines[:5]
    )


# =========================================================
# LIVE GOOGLE NEWS SEARCH
# =========================================================

def get_live_search(query):

    try:

        encoded_query = quote(query)

        url = (
            "https://news.google.com/rss/search?"
            f"q={encoded_query}"
            "&hl=en-US"
            "&gl=US"
            "&ceid=US:en"
        )

        feed = feedparser.parse(url)

        headlines = []

        for item in feed.entries[:10]:

            headlines.append(
                item.title
            )

        if not headlines:
            return "No news found."

        return "\n".join(
            headlines
        )

    except Exception as e:

        print(
            "Live Search Error:",
            e
        )

        return "Unable to search news."


# =========================================================
# OPEN WORLDMONITOR IN CHROME
# =========================================================

def open_world_monitor():

    chrome_paths = [

        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        )
    ]

    try:

        chrome = None

        for path in chrome_paths:

            if os.path.exists(path):

                chrome = path
                break

        if chrome:

            webbrowser.register(
                "chrome",
                None,
                webbrowser.BackgroundBrowser(
                    chrome
                )
            )

            webbrowser.get(
                "chrome"
            ).open_new_tab(
                "https://www.worldmonitor.app/"
            )

        else:

            webbrowser.open(
                "https://www.worldmonitor.app/"
            )

    except Exception as e:

        print(
            "WorldMonitor Error:",
            e
        )

        webbrowser.open(
            "https://www.worldmonitor.app/"
        )

    return "Opening World Monitor"