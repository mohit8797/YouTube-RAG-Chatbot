# backend/__init__.py

# This file makes 'backend' a Python package

# Optional: expose main functions for easier imports
from .rag_utils import (
    build_vector_db,
    load_vector_db,
    retrieve_context,
    ask_gemini,
)

from .transcript_utils import (
    extract_video_id,
    get_transcript,
    clean_text,
    chunk_text,
)