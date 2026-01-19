import re
import os
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Supports:
    - https://www.youtube.com/watch?v=VIDEOID
    - https://youtu.be/VIDEOID
    """
    if "youtu.be" in url:
        return url.split("/")[-1]
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    raise ValueError("Invalid YouTube URL")


def get_transcript(video_id: str) -> str:
    """
    Fetch transcript using latest youtube-transcript-api
    """
    ytt_api = YouTubeTranscriptApi()

    try:
        fetched_transcript = ytt_api.fetch(video_id, languages=["en"])
    except Exception:
        # fallback if English is not explicitly available
        fetched_transcript = ytt_api.fetch(video_id)

    full_text = " ".join(snippet.text for snippet in fetched_transcript)
    return full_text


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\[.*?\]", "", text)   # remove [music], [applause]
    text = re.sub(r"\s+", " ", text)      # normalize spaces
    return text.strip()


def chunk_text(text: str, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks


def main():
    url = input("Enter YouTube URL: ").strip()

    print("Extracting video id...")
    video_id = extract_video_id(url)

    print("Downloading transcript...")
    text = get_transcript(video_id)

    print("Cleaning text...")
    clean = clean_text(text)

    print("Chunking text...")
    chunks = chunk_text(clean)

    print(f"Total chunks: {len(chunks)}")

    # ensure data folder exists
    os.makedirs("data", exist_ok=True)

    with open("data/chunks.txt", "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"--- CHUNK {i + 1} ---\n")
            f.write(chunk + "\n\n")

    print("Saved to data/chunks.txt")


if __name__ == "__main__":
    main()