import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai


INDEX_FILE = "data/faiss.index"
META_FILE = "data/chunks.pkl"


def load_vector_db():
    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def retrieve_context(query, embed_model, index, chunks, k=4):
    q_emb = embed_model.encode([query])
    _, I = index.search(q_emb, k)

    results = []
    for idx in I[0]:
        results.append(chunks[idx])

    return "\n\n".join(results)


def build_prompt(context, question):
    return f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""


def main():
    print("Loading environment...")
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    # ✅ NEW Gemini Client
    client = genai.Client(api_key=api_key)

    print("Loading embedding model...")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Loading vector database...")
    index, chunks = load_vector_db()

    print("\nRAG Chatbot Ready! Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        context = retrieve_context(question, embed_model, index, chunks)
        prompt = build_prompt(context, question)

        # ✅ Gemini 3 Flash Preview
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        print("\nBot:", response.text)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()