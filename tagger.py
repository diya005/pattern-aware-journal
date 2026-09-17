import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

SCHEMA_PROMPT = """You must respond with ONLY valid JSON, no other text, matching this exact structure:
{{
  "emotion": "<primary emotion as one word, e.g. anxious, content, frustrated>",
  "intensity": <integer 1-10>,
  "themes": [<list of topic strings, e.g. "work", "sleep", "family">],
  "summary": "<one neutral sentence summarizing the entry>"
}}

Journal entry:
{entry}

JSON response:"""

def tag_entry(text: str) -> dict:
    prompt = SCHEMA_PROMPT.format(entry=text)

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "format": "json",
        "stream": False
    })

    raw = response.json()["response"]

    try:
        data = json.loads(raw)
        assert all(k in data for k in ["emotion", "intensity", "themes", "summary"])
        return data
    except (json.JSONDecodeError, AssertionError):
        print("Malformed response, got:", raw)
        return None