# =========================================================
# IMPORTS
# =========================================================

import re
from ai_chat import ask_ai
from worldmonitor import get_live_search
from providers.flipkart_search import flipkart_search


# =========================================================
# HELPERS
# =========================================================

def extract_budget(query):

    match = re.search(r'(\d{4,6})', query)

    if match:
        return int(match.group())

    return None


def get_phone_type(query):

    query = query.lower()

    if "gaming" in query:
        return "gaming"

    if "camera" in query:
        return "camera"

    if "battery" in query:
        return "battery"

    if "performance" in query:
        return "performance"

    return "general"

def get_phone_intent(query):

    query = query.lower()

    PRICE_WORDS = [
        "price",
        "cost",
        "rate",
        "kitne ka",
        "price of",
        "how much",
        "current price"
    ]

    SPEC_WORDS = [
        "spec",
        "specification",
        "ram",
        "processor",
        "battery",
        "camera"
    ]

    COMPARE_WORDS = [
        "compare",
        "vs",
        "versus"
    ]

    for word in PRICE_WORDS:
        if word in query:
            return "price"

    for word in SPEC_WORDS:
        if word in query:
            return "specs"

    for word in COMPARE_WORDS:
        if word in query:
            return "comparison"

    return "recommendation"

def get_laptop_type(query):

    query = query.lower()

    if "gaming" in query:
        return "gaming"

    if "coding" in query:
        return "coding"

    if "student" in query:
        return "student"

    if "graphic" in query or "editing" in query:
        return "creator"

    return "general"

def get_camera_type(query):

    query = query.lower()

    if "youtube" in query:
        return "youtube"

    if "vlog" in query:
        return "vlogging"

    if "photography" in query:
        return "photography"

    return "general"


# =========================================================
# PRODUCT KEYWORDS
# =========================================================

PHONE_WORDS = [
    "phone",
    "smartphone",
    "mobile",
    "iphone",
    "camera phone",
    "gaming phone"
]

LAPTOP_WORDS = [
    "laptop",
    "notebook",
    "macbook"
]

CAMERA_WORDS = [
    "camera",
    "dslr",
    "mirrorless"
]

AUDIO_WORDS = [
    "earbuds",
    "earphone",
    "headphone",
    "headset",
    "neckband"
]

WATCH_WORDS = [
    "smartwatch",
    "watch"
]


# =========================================================
# PHONE SEARCH
# =========================================================

def search_phone(query):

    print("PHONE ROUTER HIT:", query)

    intent = get_phone_intent(query)

    print("PHONE INTENT:", intent)

    # =====================================
    # PRICE QUERY
    # =====================================

    if intent == "price":

        results = flipkart_search(query)

        if results:

            top = results[0]

            price = top["price"]

            price_num = (
                price.replace("₹", "")
                .replace(",", "")
            )

            return (
                f"{top['title']} "
                f"is currently available on Flipkart "
                f"for {price_num} rupees."
            )

        return (
            "Sorry, I could not find the "
            "current Flipkart price."
        )

    # =====================================
    # SPECS QUERY
    # =====================================

    if intent == "specs":

        results = get_live_search(
            f"{query} specifications"
        )

        print("LIVE RESULTS:")
        print(results)

        return ask_ai(
            f"""
            Based ONLY on these latest search results.

            Search Results:
            {results}

            Tell the important specifications.

            Mention:
            Processor
            Display
            Battery
            Camera

            No numbering.
            No bullet points.

            Keep answer under 4 sentences.
            """
        )

    # =====================================
    # COMPARISON QUERY
    # =====================================

    if intent == "comparison":

        results = get_live_search(
            f"{query} comparison"
        )

        print("LIVE RESULTS:")
        print(results)

        return ask_ai(
            f"""
            Based ONLY on these latest search results.

            Search Results:
            {results}

            Compare both phones.

            Mention:
            Performance
            Camera
            Battery
            Value for money

            No numbering.
            No bullet points.

            Keep answer under 4 sentences.
            """
        )

    # =====================================
    # RECOMMENDATION QUERY
    # =====================================

    budget = extract_budget(query)

    if budget is None:
        return (
            "Please tell me your budget. "
            "For example, gaming phone under 30000."
        )

    print("BUDGET:", budget)

    phone_type = get_phone_type(query)

    print("PHONE TYPE:", phone_type)

    search_query = (
        f"best {phone_type} smartphone under "
        f"{budget} India 2026 review"
    )

    results = get_live_search(
        search_query
    )

    print("LIVE RESULTS:")
    print(results)

    return ask_ai(
        f"""
        Based ONLY on these latest search results.

        Search Results:
        {results}

        User Budget:
        {budget}

        Phone Type:
        {phone_type}

        Recommend the best phones.

        Recommend only products mentioned
        in the search results.

        Do not invent phone models.

        Do not recommend products
        older than 2 years.

        Prefer phones launched
        in 2025 or 2026.

        Mention approximate prices.

        Recommend only the top 2 phones.

        No numbering.
        No bullet points.

        Keep answer under 4 sentences.
        """
    )


# =========================================================
# LAPTOP SEARCH
# =========================================================

def search_laptop(query):

    print("LAPTOP ROUTER HIT:", query)

    budget = extract_budget(query)

    if budget is None:
        return (
            "Please tell me your budget. "
            "For example, laptop under 60000."
        )

    print("BUDGET:", budget)

    laptop_type = get_laptop_type(query)

    print("LAPTOP TYPE:", laptop_type)

    results = get_live_search(
        f"best {laptop_type} laptop under {budget} India 2026 review"
    )

    print("LIVE RESULTS:")
    print(results)

    return ask_ai(
        f"""
        Based ONLY on these latest search results.

        Search Results:
        {results}

        User Budget:
        {budget}

        Laptop Type:
        {laptop_type}

        Recommend the best laptops matching the laptop type and budget.

        Recommend only products mentioned in the search results.

        Do not invent laptop models.

        Do not recommend products older than 2 years.

        Prefer products launched in 2025 or 2026.

        Mention approximate prices.

        Recommend only the top 2 products.

        No numbering.
        No bullet points.

        Keep answer under 4 sentences.
        """
    )
# =========================================================
# CAMERA SEARCH
# =========================================================

def search_camera(query):

    print("CAMERA ROUTER HIT:", query)

    budget = extract_budget(query)

    if budget is None:
        return (
            "Please tell me your budget. "
            "For example, camera under 50000."
        )

    print("BUDGET:", budget)

    camera_type = get_camera_type(query)

    print("CAMERA TYPE:", camera_type)

    results = get_live_search(
        f"best {camera_type} camera under {budget} India 2026 review"
    )

    print("LIVE RESULTS:")
    print(results)

    return ask_ai(
        f"""
        Based ONLY on these latest search results.

        Search Results:
        {results}

        User Budget:
        {budget}

        Camera Type:
        {camera_type}

        Recommend the best cameras matching the camera type and budget.

        Recommend only products mentioned in the search results.

        Do not invent camera models.

        Do not recommend products older than 2 years.

        Prefer products launched in 2025 or 2026.

        Mention approximate prices.

        Recommend only the top 2 products.

        No numbering.
        No bullet points.

        Keep answer under 4 sentences.
        """
    )


# =========================================================
# AUDIO SEARCH
# =========================================================

def search_audio(query):

    print("AUDIO ROUTER HIT:", query)

    budget = extract_budget(query)

    if budget is None:
        return (
            "Please tell me your budget. "
            "For example, earbuds under 3000."
        )

    print("BUDGET:", budget)

    results = get_live_search(
        f"best earbuds under {budget} India 2026 review"
    )

    print("LIVE RESULTS:")
    print(results)

    return ask_ai(
        f"""
        Based ONLY on these latest search results.

        Search Results:
        {results}

        User Budget:
        {budget}

        Recommend the best earbuds or headphones.
        Recommend only products mentioned in the search results.
        Do not recommend products older than 2 years.
        Prefer products launched in 2025 or 2026.

        Do not invent product models.

        Mention approximate prices.

        No numbering.
        No bullet points.

        Keep answer under 4 sentences.
        """
    )


# =========================================================
# SMARTWATCH SEARCH
# =========================================================

def search_watch(query):

    print("WATCH ROUTER HIT:", query)

    budget = extract_budget(query)

    if budget is None:
        return (
            "Please tell me your budget. "
            "For example, smartwatch under 5000."
        )

    print("BUDGET:", budget)

    results = get_live_search(
        f"best smartwatch under {budget} India 2026 review"
    )

    print("LIVE RESULTS:")
    print(results)

    return ask_ai(
        f"""
        Based ONLY on these latest search results.

        Search Results:
        {results}

        User Budget:
        {budget}

        Recommend the best smartwatches.
        Recommend only products mentioned in the search results.
        Do not recommend products older than 2 years.
        Prefer products launched in 2025 or 2026.

        Do not invent smartwatch models.

        Mention approximate prices.

        No numbering.
        No bullet points.

        Keep answer under 4 sentences.
        """
    )


# =========================================================
# MASTER ROUTER
# =========================================================

def product_search(query):

    query_lower = query.lower()

    # PHONE DETECTION

    if (
        any(word in query_lower for word in PHONE_WORDS)
        or "samsung" in query_lower
        or "iqoo" in query_lower
        or "oneplus" in query_lower
        or "realme" in query_lower
        or "vivo" in query_lower
        or "oppo" in query_lower
        or "xiaomi" in query_lower
        or "redmi" in query_lower
        or "poco" in query_lower
        or "motorola" in query_lower
        or "nothing" in query_lower
    ):
        return search_phone(query)

    if any(word in query_lower for word in LAPTOP_WORDS):
        return search_laptop(query)

    if any(word in query_lower for word in CAMERA_WORDS):
        return search_camera(query)

    if any(word in query_lower for word in AUDIO_WORDS):
        return search_audio(query)

    if any(word in query_lower for word in WATCH_WORDS):
        return search_watch(query)

    return None