import json
import os

MEMORY_FILE = "memory.json"


# ==========================================
# LOAD MEMORY
# ==========================================


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# ==========================================
# SAVE MEMORY
# ==========================================


def save_memory(data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("Memory save error:", e)


# ==========================================
# BASIC MEMORY
# ==========================================


def remember(key, value):
    data = load_memory()
    data[key] = value
    save_memory(data)


def recall(key, default=None):
    data = load_memory()
    return data.get(key, default)


# ==========================================
# LAST QUESTION / ANSWER
# ==========================================


def save_chat(question, answer):
    data = load_memory()

    data["last_question"] = question
    data["last_answer"] = answer

    save_memory(data)


# ==========================================
# CONTEXT MEMORY
# ==========================================


def save_context(context_type, query, results):

    data = load_memory()

    data["conversation_context"] = {
        "type": context_type,
        "query": query,
        "results": results,
    }

    save_memory(data)


def get_context():

    data = load_memory()

    return data.get(
        "conversation_context", {"type": None, "query": None, "results": []}
    )


def clear_context():

    data = load_memory()

    data["conversation_context"] = {"type": None, "query": None, "results": []}

    save_memory(data)


# ==========================================
# BEST RESULT
# ==========================================


def get_best_result():

    context = get_context()

    results = context.get("results", [])

    if not results:
        return None

    try:
        return max(results, key=lambda x: float(x.get("rating", 0)))
    except:
        return results[0]


# ==========================================
# SAVE USER INFO
# ==========================================


def save_user_info(name=None, age=None):

    data = load_memory()

    if name:
        data["name"] = name

    if age:
        data["age"] = age

    save_memory(data)


# ==========================================
# GET USER INFO
# ==========================================


def get_user_info():

    data = load_memory()

    return {"name": data.get("name"), "age": data.get("age")}
