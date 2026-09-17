from retriever import find_similar
from collections import Counter

DISTANCE_THRESHOLD = 1.0
MIN_OCCURRENCES = 2

def detect_pattern(entry_id: str, text: str):
    matches = find_similar(text, exclude_id=entry_id, top_k=10)

    # Keep only genuinely close matches
    close_matches = [m for m in matches if m["distance"] < DISTANCE_THRESHOLD]

    if len(close_matches) < MIN_OCCURRENCES:
        return {"pattern_found": False, "matches": []}

    # Pull common emotion across the matches, as a signal of what the pattern "is"
    emotions = [m["metadata"]["emotion"] for m in close_matches]
    common_emotion = Counter(emotions).most_common(1)[0][0]

    return {
        "pattern_found": True,
        "match_count": len(close_matches),
        "common_emotion": common_emotion,
        "matches": close_matches
    }