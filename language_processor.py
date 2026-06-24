# =========================================================
# 🌍 LANGUAGE PROCESSOR (ASTRA v2)
# =========================================================

LANG_MODE = "auto"   # auto / hindi / english

# 🔥 CLEAN TEXT
def clean_text(text):
    text = text.lower()

    fillers = ["bhai", "yaar", "please", "jara", "zara", "bhaiya"]
    for f in fillers:
        text = text.replace(f, "")

    return text.strip()

# 🔥 REMOVE USELESS WORDS
# 🔥 STRONG CLEAN (FINAL)
def remove_noise_words(text):
    noise = [
        "per", "pe", "par",
        "karo", "kar", "kardo", "kar do",
        "do", "de", "dijiye",
        "please", "bhai", "yaar",
        "nova", "innova", "novaa", "nov",
        "astra", "hey astra"
    ]

    words = text.split()
    words = [w for w in words if w not in noise]

    return " ".join(words)

def remove_duplicates(text):
    words = text.split()
    seen = []
    
    for w in words:
        if w not in seen:
            seen.append(w)

    return " ".join(seen)


def ensure_song_keyword(text):
    keywords = ["song", "gaana", "gana"]

    if any(k in text for k in keywords):
        return text

    return text


# 🔥 HINGLISH NORMALIZATION
def normalize_text(text):
    replacements = {
        "chalao": "play",
        "chala do": "play",
        "gaana": "song",
        "gana": "song",
        "suno": "play",
        "openo": "open",       
        "opena": "open", 
        "vedar": "weather",   
        "brouser": "browser",  
        "brouzer": "browser",   
        "bowser": "browser",   
        "veder": "weather",
        "mausam": "weather",
        "khol": "open",
        "kholo": "open",
        "band karo": "close",  
        "band kar": "close",   
        "band": "close",
        "browser close": "close browser", 
        "youtube close": "close youtube", 
        "chrome close": "close chrome",    
        "chalana": "play",
         "gaane": "song",
         "gane": "song",
        "songs": "song"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


# 🔥 LANGUAGE DETECT
def detect_language(text):
    hindi_words = ["kya", "kaise", "hai", "mausam", "chalao"]

    for w in hindi_words:
        if w in text:
            return "hindi"

    return "english"


# 🔥 MAIN PROCESS
def process_text(text):
    text = clean_text(text)
    text = remove_noise_words(text)
    text = normalize_text(text)
    text = remove_duplicates(text)   # 🔥 NEW LINE
    lang = detect_language(text)
    return text, lang