import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

REFLECTION_PROMPT = """You are a thoughtful journaling companion. You are NOT a therapist and must not give clinical advice or diagnoses.

The user just wrote this journal entry:
"{new_entry}"

You've noticed this connects to a recurring pattern. Here are similar past entries from their journal:
{past_entries}

The common emotion across these entries is: {common_emotion}

Write ONE short, warm, specific reflective question (2-3 sentences max) that:
- Gently points out the pattern you're noticing (reference specifics from the past entries, not vague generalities)
- Asks an open-ended question to help them reflect, not gives advice
- Does NOT sound clinical, does NOT diagnose, does NOT lecture

Respond with ONLY the reflective question/message, nothing else."""

def generate_reflection(new_entry: str, pattern: dict) -> str:
    past_entries_text = "\n".join(
        f"- \"{m['text']}\"" for m in pattern["matches"]
    )

    prompt = REFLECTION_PROMPT.format(
        new_entry=new_entry,
        past_entries=past_entries_text,
        common_emotion=pattern["common_emotion"]
    )

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"].strip()