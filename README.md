# Pattern-Aware Journal Companion

A journaling app that goes beyond simple mood tracking — it detects when new entries 
connect to recurring emotional patterns from your past writing, and generates a 
grounded, specific reflective question about it. Runs 100% locally and for free 
using open-source models — no data ever leaves your machine.

## Why this is different from a typical mood tracker
Most journaling AI tools just score sentiment on each entry in isolation. This 
project treats the journal as a whole: it embeds every entry into a semantic vector 
space, retrieves genuinely similar past entries (not just keyword matches), and 
flags when a cluster of similar entries indicates a recurring pattern — then uses 
that retrieved context to generate a specific, grounded reflection (RAG), rather 
than a generic AI response.

## Architecture
1. **Tagging** — Local LLM (Llama 3.1 8B via Ollama) extracts structured mood data 
   (emotion, intensity, themes) from each entry using constrained JSON generation.
2. **Embedding** — sentence-transformers (all-MiniLM-L6-v2) converts entries into 
   384-dim vectors, stored locally in a Chroma vector database.
3. **Retrieval** — Semantic similarity search finds past entries related to a new 
   one by meaning, not keywords.
4. **Pattern detection** — A distance-threshold + frequency method flags when 
   enough similar past entries exist to constitute a recurring pattern (threshold 
   tuned empirically against real journal data).
5. **Grounded generation (RAG)** — Retrieved entries are fed into the LLM's prompt 
   so the reflective question is specific and evidence-based, not generic.
6. **Safety layer** — A dedicated crisis-language classifier runs before anything 
   else; if triggered, it bypasses all other logic and surfaces real crisis 
   resources instead.

## Tech stack
Python, Ollama (Llama 3.1 8B), sentence-transformers, ChromaDB, SQLite, Streamlit

## Design decisions
- **Local-first, not cloud API**: zero cost, zero data leaves the user's machine — 
  important for a mental-health-adjacent tool.
- **Separated tagging (structured JSON) from reflection (free text)**: different 
  tasks need different output shapes; forcing JSON on a task meant for natural 
  reading text degrades quality.
- **Safety check runs first and can short-circuit the entire pipeline** — a 
  deliberate design choice so no "clever" feature can ever override a safety 
  concern.

## Possible extensions
- Replace threshold-based pattern detection with proper clustering (HDBSCAN)
- Weight pattern relevance by recency, not just similarity
- Multi-modal input (voice journaling)

## Demo
https://github.com/diya005/pattern-aware-journal/raw/main/demo(1).mp4
