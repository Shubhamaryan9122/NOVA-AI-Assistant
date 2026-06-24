def rank_phone(spec_text):

    text = spec_text.lower()

    score = 0

    if "snapdragon 8" in text:
        score += 50

    if "dimensity 9400" in text:
        score += 50

    if "6000mah" in text:
        score += 20

    if "120hz" in text:
        score += 10

    if "144hz" in text:
        score += 15

    return score