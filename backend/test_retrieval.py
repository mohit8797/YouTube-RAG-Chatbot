import pickle
import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = "data/faiss.index"
META_FILE = "data/chunks.pkl"


def main():
    print("Loading index...")
    index = faiss.read_index(INDEX_FILE)

    print("Loading chunks...")
    with open(META_FILE, "rb") as f:
        chunks = pickle.load(f)

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    while True:
        query = input("\nAsk a question (or type exit): ")

        if query.lower() == "exit":
            break

        q_emb = model.encode([query])
        D, I = index.search(q_emb, k=3)

        print("\nTop matches:\n")
        for idx in I[0]:
            print("-" * 50)
            print(chunks[idx][:500])


if __name__ == "__main__":
    main()
