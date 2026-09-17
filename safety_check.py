import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

SAFETY_PROMPT = """You are a safety classifier for a journaling app. Read the entry below and determine if it indicates the person may be at risk of self-harm, suicide, or a genuine mental health crisis requiring immediate professional support — as opposed to normal stress, sadness, or frustration.

Entry: "{entry}"

Respond with ONLY one word: "CRISIS" or "SAFE"."""

CRISIS_RESOURCES = (
    "It sounds like you're going through something really difficult right now. "
    "Please consider reaching out to a crisis line — in the US, you can call or text 988 "
    "(Suicide & Crisis Lifeline), available 24/7. If you're outside the US, please look up "
    "your local crisis line. You don't have to go through this alone."
)

def is_crisis(entry: str) -> bool:
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": SAFETY_PROMPT.format(entry=entry),
        "stream": False
    })
    result = response.json()["response"].strip().upper()
    return "CRISIS" in result