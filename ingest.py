import uuid
from datetime import datetime
import chromadb
from db import init_db
from tagger import tag_entry
from embedder import embed

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection("journal_entries")

def add_entry(text: str):
    entry_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    tags = tag_entry(text)
    vector = embed(text)

    conn = init_db()
    conn.execute(
        "INSERT INTO entries VALUES (?, ?, ?, ?, ?, ?, ?)",
        (entry_id, text, timestamp, tags["emotion"], tags["intensity"], ",".join(tags["themes"]), tags["summary"])
    )
    conn.commit()

    collection.add(
        ids=[entry_id],
        embeddings=[vector],
        metadatas=[{"timestamp": timestamp, "emotion": tags["emotion"]}],
        documents=[text]
    )

    print(f"Stored entry {entry_id}: {tags}")
    return entry_id

if __name__ == "__main__":
    add_entry("Work has been crushing me all week, barely slept.")