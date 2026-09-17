from ingest import add_entry
from pattern_detector import detect_pattern
from reflection_generator import generate_reflection
from safety_check import is_crisis, CRISIS_RESOURCES

def process_entry(text: str):
    if is_crisis(text):
        return {
            "type": "crisis",
            "message": CRISIS_RESOURCES
        }

    entry_id = add_entry(text)
    pattern = detect_pattern(entry_id, text)

    if pattern["pattern_found"]:
        reflection = generate_reflection(text, pattern)
        return {
            "type": "pattern",
            "message": reflection,
            "matches": pattern["matches"]
        }

    return {
        "type": "logged",
        "message": "Entry saved."
    }