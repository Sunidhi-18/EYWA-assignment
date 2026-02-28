import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"

# Embedding model name (for reference)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"