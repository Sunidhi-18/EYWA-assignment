# Telegram YouTube Summarizer & Q&A Bot

Eywa SDE Intern Assignment

## Overview

This project is a Telegram-based assistant that helps users understand long YouTube videos quickly.

The bot accepts a YouTube link, fetches its transcript, generates a structured summary, and allows users to ask contextual follow-up questions. It supports English by default and Hindi on request.

The goal was to build a practical AI research assistant that improves how users consume long-form video content.

---

## Features

### 1. Structured Video Summary

When a user sends a YouTube link, the bot:

* Fetches the transcript
* Generates a structured summary
* Returns:

  * Video title (if available)
  * 5 key points
  * Important timestamps
  * Core takeaway

The summary is concise and organized, not a simple paragraph dump.

---

### 2. Contextual Question & Answer

After the summary, users can ask follow-up questions about the video.

The system:

* Retrieves relevant parts of the transcript
* Generates answers grounded only in that context
* Avoids hallucinations
* Clearly states when a topic is not covered in the video

Multiple follow-up questions are supported within the same session.

---

### 3. Multi-language Support

* English (default)
* Hindi (on request)

Users can write:

* “Explain in Hindi”
* “Summarize in Hindi”

Language control is handled during generation rather than by translating after the fact. This ensures cleaner and more natural responses.

---

## Architecture

The system follows a Retrieval Augmented Generation (RAG) approach.

### High-Level Flow

1. User sends a YouTube link.
2. Transcript is fetched using `youtube-transcript-api`.
3. Transcript is chunked into smaller segments.
4. Chunks are stored in a lightweight vector store.
5. For Q&A:

   * Relevant chunks are retrieved.
   * Context is sent to a local LLM.
   * The answer is generated strictly based on retrieved content.

### Components

* `transcript.py` – Handles transcript extraction and error management
* `summarizer.py` – Generates structured summaries
* `qa_engine.py` – Implements retrieval and grounded answer generation
* `vector_store.py` – Stores and retrieves transcript chunks
* `telegram_bot.py` – Manages user interaction and session handling
* `config.py` – Configuration and environment setup

The architecture is modular so that each component can be improved independently.

---

## Design Decisions

### Local LLM (Ollama)

The project uses a locally hosted model via Ollama. This avoids external API dependency, keeps costs zero, and allows full control over the system.

### RAG for Q&A

Instead of sending the entire transcript to the model for each question, the system retrieves only relevant chunks. This improves:

* Accuracy
* Efficiency
* Grounded responses

### Session Handling

Each Telegram user session is handled independently to support multiple users simultaneously.

---

## Edge Cases Handled

* Invalid YouTube URLs
* Missing transcripts
* Subtitles disabled
* Very long transcripts
* Ollama connection errors
* Timeouts
* Questions asked before sending a link

The bot fails gracefully with meaningful error messages.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd <repo-name>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Run Ollama

Install Ollama locally.

Pull the model:

```bash
ollama pull phi3
```

Start Ollama:

```bash
ollama run phi3
```

(You can exit after it loads — the server will keep running.)

---

### 5. Create Telegram Bot

* Open Telegram
* Search for BotFather
* Create a new bot
* Copy the token

Create a `.env` file:

```
BOT_TOKEN=your_token_here
```

---

### 6. Run the Bot

```bash
python app/main.py
```

You should see:

```
Telegram Bot is running...
```

---

The implementation satisfies:

* End-to-end functionality
* Structured summary generation
* Contextual and grounded Q&A
* Multi-language support (English + Hindi)
* Clean modular architecture
* Proper error handling

---


Future Improvements:

Add transcript caching for performance

Support videos without subtitles using speech-to-text

Persist session data across restarts

Cloud deployment

## Development Timeline

Completed within the expected 3–4 day timeframe.

## Sample outputs
![alt text](<Screenshot 2026-02-28 200109.png>)
![alt text](<Screenshot 2026-02-28 200131.png>)