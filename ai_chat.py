from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file!")

client = Groq(api_key=api_key)


conversation_history = []

MAX_HISTORY = 10


def ask_ai(prompt):
    try:
        # 🔥 User ka message history mein add karo
        conversation_history.append({"role": "user", "content": prompt})

        # 🔥 Sirf last MAX_HISTORY messages bhejo (memory save)
        recent = conversation_history[-MAX_HISTORY:]

        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are NOVA, an intelligent voice assistant.
                    Speak naturally like a real assistant.
                    Never use numbered lists.
                    Never use bullet points.
                    Use conversational English.
                    Keep answers under 4 sentences.
                    Do not mention knowledge cutoffs unless absolutely necessary.
                    If live search results are provided, use them to answer the user.
                    Prefer concise, voice-friendly responses.
                    """,
                },
                *recent,
            ],
        )

        output = res.choices[0].message.content

        if not output:
            return "AI did not respond properly"

        # 🔥 AI ka reply bhi history mein save karo
        conversation_history.append({"role": "assistant", "content": output})

        return output

    except Exception as e:
        print("AI ERROR:", e)
        return "AI system error"


# 🔥 History clear karne ka function (optional)
def clear_history():
    conversation_history.clear()
    print("Conversation history cleared")
