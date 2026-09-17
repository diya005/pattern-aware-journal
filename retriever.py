import chromadb
from embedder import embed

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection("journal_entries")

def find_similar(text: str, exclude_id: str = None, top_k: int = 5):
    query_vector = embed(text)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k + 1  # +1 in case the entry itself is in the DB
    )

    similar = []
    for i, entry_id in enumerate(results["ids"][0]):
        if entry_id == exclude_id:
            continue
        similar.append({
            "id": entry_id,
            "text": results["documents"][0][i],
            "distance": results["distances"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return similar[:top_k]