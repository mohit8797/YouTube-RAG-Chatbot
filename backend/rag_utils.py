import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai


INDEX_FILE = "data/faiss.index"
META_FILE = "data/chunks.pkl"

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# ✅ New Gemini client
client = genai.Client(api_key=API_KEY)

# Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


def build_vector_db(chunks):
    embeddings = embed_model.encode(chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs("data", exist_ok=True)
    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump(chunks, f)


def load_vector_db():
    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks


def retrieve_context(question, index, chunks, k=4):
    q_emb = embed_model.encode([question])
    _, I = index.search(q_emb, k)

    return "\n\n".join(chunks[i] for i in I[0])


def ask_gemini(context, question):
    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not present, say "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

    # ✅ Gemini 3 Flash Preview
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text