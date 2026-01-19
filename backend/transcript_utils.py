# import re
# from youtube_transcript_api import YouTubeTranscriptApi


# def extract_video_id(url: str) -> str:
#     if "youtu.be" in url:
#         return url.split("/")[-1]
#     if "watch?v=" in url:
#         return url.split("watch?v=")[-1].split("&")[0]
#     raise ValueError("Invalid YouTube URL")


# def get_transcript(url: str) -> str:
#     video_id = extract_video_id(url)
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#     full_text = " ".join([item["text"] for item in transcript_list])
#     return full_text


# def clean_text(text: str) -> str:
#     text = text.lower()
#     text = re.sub(r"\[.*?\]", "", text)
#     text = re.sub(r"\s+", " ", text)
#     return text.strip()


# def chunk_text(text: str, chunk_size=500, overlap=100):
#     words = text.split()
#     chunks = []

#     start = 0
#     while start < len(words):
#         end = start + chunk_size
#         chunk = " ".join(words[start:end])
#         chunks.append(chunk)
#         start = end - overlap

#     return chunks


# from urllib.parse import urlparse, parse_qs

# def extract_video_id(url: str) -> str:
#     """
#     Extracts the YouTube video ID from various URL formats:
#     - https://www.youtube.com/watch?v=VIDEOID
#     - https://youtu.be/VIDEOID
#     - https://m.youtube.com/watch?v=VIDEOID&t=10s
#     """

#     url = url.strip()

#     # Short link: youtu.be/VIDEOID
#     if "youtu.be" in url:
#         return url.split("/")[-1].split("?")[0]

#     # Full YouTube link: watch?v=VIDEOID
#     parsed = urlparse(url)
#     query = parse_qs(parsed.query)
#     if "v" in query:
#         return query["v"][0]

#     # Fallback: extract from path (rare edge cases)
#     path_parts = parsed.path.split("/")
#     if len(path_parts) > 1:
#         return path_parts[-1]

#     raise ValueError("Invalid YouTube URL. Make sure it is a proper YouTube link.")


from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from various URL formats.
    """
    url = url.strip()

    # Short link: youtu.be/VIDEOID
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]

    # Full YouTube link: watch?v=VIDEOID
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    if "v" in query:
        return query["v"][0]

    # Fallback: extract from path (rare edge cases)
    path_parts = parsed.path.split("/")
    if len(path_parts) > 1:
        return path_parts[-1]

    raise ValueError("Invalid YouTube URL. Make sure it is a proper YouTube link.")


def get_transcript(video_id: str) -> str:
    """
    Fetches the transcript for a YouTube video.
    Returns the full transcript as a single string.
    """

    # Use the latest FetchedTranscript API style
    ytt_api = YouTubeTranscriptApi()

    try:
        fetched_transcript = ytt_api.fetch(video_id, languages=["en"])
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {str(e)}")

    # Join all snippet texts
    transcript_text = " ".join([snippet.text for snippet in fetched_transcript])
    return transcript_text


def clean_text(text: str) -> str:
    import re
    # lowercase, remove brackets, extra spaces
    text = text.lower()
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap if end - overlap > 0 else end

    return chunks