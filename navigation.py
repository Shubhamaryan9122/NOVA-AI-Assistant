# =========================================================
# navigation.py
# =========================================================

from urllib.parse import quote
from browser import safe_driver

# =========================================================
# MEMORY
# =========================================================

LAST_DESTINATION = None


def set_last_destination(destination):

    global LAST_DESTINATION

    LAST_DESTINATION = destination


def get_last_destination():

    return LAST_DESTINATION


# =========================================================
# OPEN MAPS
# =========================================================


def open_maps(location):

    d = safe_driver()

    if not d:
        return "Browser not available."

    url = "https://www.google.com/maps/search/" f"{quote(location)}"

    d.get(url)

    return f"Opening map for {location}"


# =========================================================
# NAVIGATE TO DESTINATION
# =========================================================


def navigate_to(destination):

    destination = destination.strip()

    if not destination:
        return "No destination provided."

    set_last_destination(destination)

    d = safe_driver()

    if not d:
        return "Browser not available."

    url = (
        "https://www.google.com/maps/dir/?api=1"
        f"&destination={quote(destination)}"
        "&travelmode=driving"
    )

    print("NAVIGATION URL:", url)

    d.get(url)

    return f"Starting navigation to {destination}"


# =========================================================
# NAVIGATE SOURCE -> DESTINATION
# =========================================================


def navigate_route(source, destination):

    source = source.strip()
    destination = destination.strip()

    if not source or not destination:
        return "Invalid route."

    set_last_destination(destination)

    d = safe_driver()

    if not d:
        return "Browser not available."

    url = "https://www.google.com/maps/dir/" f"{quote(source)}/" f"{quote(destination)}"

    print("ROUTE URL:", url)

    d.get(url)

    return f"Navigating from " f"{source} to {destination}"


# =========================================================
# GET URL ONLY
# =========================================================


def get_navigation_url(destination):

    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&destination={quote(destination)}"
        "&travelmode=driving"
    )


# =========================================================
# SMART DESTINATION EXTRACTOR
# =========================================================


def extract_destination(cmd):

    cmd = cmd.lower().strip()

    # follow-up commands

    if cmd in [
        "navigate there",
        "take me there",
        "go there",
        "route there",
        "directions there",
    ]:

        return get_last_destination()

    patterns = [
        "navigate to",
        "take me to",
        "directions to",
        "route to",
        "go to",
        "travel to",
        "how can i visit",
        "how do i reach",
        "show route to",
        "best route to",
        "visit",
        "reach",
    ]

    for p in patterns:

        if p in cmd:

            destination = cmd.split(p, 1)[1].strip()

            if destination:

                set_last_destination(destination)

                return destination

    return ""


# =========================================================
# CHECK NAVIGATION QUERY
# =========================================================


def is_navigation_query(cmd):

    cmd = cmd.lower()

    patterns = [
        "navigate to",
        "take me to",
        "directions to",
        "route to",
        "go to",
        "travel to",
        "visit",
        "reach",
        "how can i visit",
        "how do i reach",
        "show route to",
        "best route to",
        # follow-ups
        "navigate there",
        "take me there",
        "go there",
        "route there",
        "directions there",
    ]

    return any(p in cmd for p in patterns)


# =========================================================
# SEARCH NEARBY
# =========================================================


def search_nearby(place):

    d = safe_driver()

    if not d:
        return False

    set_last_destination(place)

    url = "https://www.google.com/maps/search/" + place.replace(" ", "+") + "+near+me"

    print("SEARCH URL:", url)

    d.get(url)

    return True
