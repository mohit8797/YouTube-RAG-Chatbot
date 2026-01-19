import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = "data/chunks.txt"
INDEX_FILE = "data/faiss.index"
META_FILE = "data/chunks.pkl"


def load_chunks():
    chunks = []
    current = []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("--- CHUNK"):
                if current:
                    chunks.append(" ".join(current).strip())
                    current = []
            else:
                current.append(line.strip())

        if current:
            chunks.append(" ".join(current).strip())

    return chunks


def main():
    print("Loading chunks...")
    chunks = load_chunks()
    print(f"Total chunks: {len(chunks)}")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    dim = embeddings.shape[1]
    print("Embedding dimension:", dim)

    print("Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print("Saving FAISS index...")
    faiss.write_index(index, INDEX_FILE)

    print("Saving chunk metadata...")
    with open(META_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print("Vector DB build complete!")


if __name__ == "__main__":
    main()
