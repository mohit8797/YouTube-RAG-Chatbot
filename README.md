🎥 YouTube RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about any YouTube video.
The system extracts video transcripts, builds a vector database using FAISS, and generates accurate answers using Google Gemini (gemini-3-flash-preview) via a FastAPI backend.

⸻

🚀 Features
	•	🔗 Accepts YouTube video URLs
	•	📝 Automatically extracts video transcripts
	•	🧹 Cleans and chunks transcript text
	•	📊 Builds a FAISS vector database for semantic search
	•	🔍 Retrieves the most relevant transcript context
	•	🤖 Answers user questions using Google Gemini
	•	⚡ FastAPI-based backend with REST endpoints

⸻

🧠 Tech Stack
	•	Backend: FastAPI
	•	Vector Database: FAISS
	•	Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
	•	LLM: Google Gemini (gemini-3-flash-preview)
	•	Language: Python
	•	API Integration: YouTube Transcript API

⸻

📂 Project Structure
youtube-rag-chatbot/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── rag_utils.py
│   ├── transcript_utils.py
├── data/
│   ├── faiss.index
│   ├── chunks.pkl
├── .env
├── .gitignore
├── requirements.txt
└── README.md

⸻

⚙️ Setup Instructions

1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/youtube-rag-chatbot.git
cd youtube-rag-chatbot

2️⃣ Create Virtual Environment

Recommended Python Version: 3.10
python3.10 -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Environment Variables

Create a .env file in the root directory:
GEMINI_API_KEY=your_gemini_api_key_here

▶️ Run the Application

Start the FastAPI server:
python -m uvicorn backend.main:app --reload

🔌 API Endpoints

📌 Process YouTube Video

POST /process_video
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}

💬 Chat with Video

POST /chat
{
  "question": "What is the main topic of this video?"
}

⸻

👨‍💻 Author
Mohit Redhu
B.Tech CSE | AI & GenAI Enthusiast
