from playwright.sync_api import sync_playwright


def smartprix_search(query):

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                f"https://www.smartprix.com/products/?q={query}",
                timeout=60000
            )

            page.wait_for_timeout(5000)

            html = page.content()

            browser.close()

            return html[:5000]

    except Exception as e:

        print(
            "SMARTPRIX ERROR:",
            e
        )

        return ""