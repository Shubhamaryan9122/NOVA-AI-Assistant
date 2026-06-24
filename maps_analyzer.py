from selenium.webdriver.common.by import By
from browser import safe_driver
import time
import re
import math


def get_best_place():

    d = safe_driver()

    print("DEBUG driver:", d)

    if not d:
        return None

    try:

        # Maps load hone do
        time.sleep(8)

        print("=" * 50)
        print("TITLE:", d.title)
        print("URL:", d.current_url)
        print("=" * 50)

        places = d.find_elements(By.CSS_SELECTOR, "div[role='article']")

        print("ARTICLES FOUND:", len(places))

        best_name = None
        best_rating = 0.0
        best_reviews = 0
        best_score = -1
        best_index = -1

        all_results = []

        for idx, p in enumerate(places[:10]):

            try:

                text = p.text.strip()

                if not text:
                    continue

                print("ITEM:")
                print(text)
                print("-" * 50)

                all_results.append(text)

                lines = text.split("\n")

                if not lines:
                    continue

                name = lines[0]

                # Rating extract
                rating_match = re.search(r"(\d\.\d)", text)

                if not rating_match:
                    continue

                rating = float(rating_match.group(1))

                # Reviews extract
                review_match = re.search(r"\(([\d,]+)\)", text)

                reviews = 0

                if review_match:

                    reviews = int(review_match.group(1).replace(",", ""))

                # Smart score
                if reviews > 0:

                    score = rating * math.log10(reviews + 1)

                else:

                    # fallback if reviews hidden
                    score = rating

                print(
                    f"FOUND: {name} | "
                    f"Rating={rating} | "
                    f"Reviews={reviews} | "
                    f"Score={score:.2f}"
                )

                if score > best_score:

                    best_score = score
                    best_name = name
                    best_rating = rating
                    best_reviews = reviews
                    best_index = idx

            except Exception as e:

                print("ITEM ERROR:", e)

        print("=" * 50)
        print("BEST PLACE:", best_name)
        print("BEST RATING:", best_rating)
        print("BEST REVIEWS:", best_reviews)
        print("BEST SCORE:", best_score)
        print("BEST INDEX:", best_index)
        print("=" * 50)

        if best_name is None:

            return None

        return {
            "name": best_name,
            "rating": best_rating,
            "reviews": best_reviews,
            "score": round(best_score, 2),
            "index": best_index,
            "results": all_results,
        }

    except Exception as e:

        print("MAPS ANALYZER ERROR:", e)

        return None
