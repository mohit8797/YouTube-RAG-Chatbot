# from fastapi import FastAPI
# from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .transcript_utils import get_transcript, clean_text, chunk_text
from .rag_utils import build_vector_db, load_vector_db, retrieve_context, ask_gemini
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# app = FastAPI()


# class VideoRequest(BaseModel):
#     url: str


# class ChatRequest(BaseModel):
#     question: str


# @app.post("/process_video")
# def process_video(req: VideoRequest):
#     text = get_transcript(req.url)
#     clean = clean_text(text)
#     chunks = chunk_text(clean)

#     build_vector_db(chunks)

#     return {"status": "success", "chunks": len(chunks)}


# @app.post("/chat")
# def chat(req: ChatRequest):
#     index, chunks = load_vector_db()
#     context = retrieve_context(req.question, index, chunks)
#     answer = ask_gemini(context, req.question)

#     return {"answer": answer}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ✅ Relative imports (VERY IMPORTANT)
from .transcript_utils import (
    extract_video_id,
    get_transcript,
    clean_text,
    chunk_text,
)
from .rag_utils import (
    build_vector_db,
    load_vector_db,
    retrieve_context,
    ask_gemini,
)

app = FastAPI(title="YouTube RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

class VideoRequest(BaseModel):
    url: str


class ChatRequest(BaseModel):
    question: str


@app.post("/process_video")
def process_video(req: VideoRequest):
    try:
        video_id = extract_video_id(req.url)

        text = get_transcript(video_id)
        clean = clean_text(text)
        chunks = chunk_text(clean)

        build_vector_db(chunks)

        return {
            "status": "success",
            "video_id": video_id,
            "total_chunks": len(chunks),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/ask")
def chat(req: ChatRequest):
    try:
        index, chunks = load_vector_db()
        context = retrieve_context(req.question, index, chunks)
        answer = ask_gemini(context, req.question)

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def serve_index():
    return FileResponse("backend/static/index.html")


@app.get("/chat")
def serve_chat():
    return FileResponse("backend/static/chat.html")
