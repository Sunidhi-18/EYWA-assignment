import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def chunk_transcript(transcript, chunk_size=700):
    """
    Break transcript into manageable chunks for vector storage.
    """
    chunks = []
    current_chunk = ""

    for entry in transcript:
        text = entry["text"]

        if len(current_chunk) + len(text) < chunk_size:
            current_chunk += " " + text
        else:
            chunks.append(current_chunk.strip())
            current_chunk = text

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def detect_language(question: str):
    """
    Detect if user explicitly wants Hindi.
    """
    question_lower = question.lower()

    hindi_triggers = [
        "in hindi",
        "hindi",
        "हिंदी",
        "हिन्दी"
    ]

    for trigger in hindi_triggers:
        if trigger in question_lower:
            return "Hindi"

    return "English"


def answer_question(vector_store, question):
    """
    Answer user question using RAG (retrieval + LLM).
    """

    # 🔹 Retrieve context
    context = vector_store.search(question)

    if not context:
        return "⚠️ I couldn't find relevant information in the video."

    # 🔹 Language detection
    language = detect_language(question)

    prompt = f"""
You are a helpful AI assistant.

Answer the question clearly and concisely
using ONLY the context provided below.

If the answer is not present in the context,
say: "The video does not mention this."

Respond strictly in {language}.

Context:
{context}

Question:
{question}

Answer:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3
                }
            },
            timeout=120  # prevent hanging
        )

        response.raise_for_status()

        answer = response.json().get("response", "").strip()

        if not answer:
            return "⚠️ Failed to generate an answer."

        return answer

    except requests.exceptions.Timeout:
        return "⏳ The model is taking too long to respond. Try again."

    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to Ollama. Make sure it is running."

    except requests.exceptions.HTTPError as e:
        return f"⚠️ Ollama error: {str(e)}"

    except Exception:
        return "⚠️ Unexpected error while generating answer."