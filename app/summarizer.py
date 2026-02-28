import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_summary(transcript_text):
    # 🔥 Limit transcript size for speed (important)
    transcript_text = transcript_text[:4000]

    prompt = f"""
You are an AI research assistant.

Generate a clean, structured summary.

Format strictly like this:

🎥 Video Title:
(If not available, write: Not mentioned)

📌 5 Key Points:
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

⏱ Important Moments:
- Timestamp – Topic
- Timestamp – Topic

🧠 Core Takeaway:
(2-3 lines conclusion)

Transcript:
{transcript_text}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
               "model": "phi3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120  # ⏳ prevent infinite waiting
        )

        response.raise_for_status()

        return response.json().get("response", "⚠️ No response from model.")

    except requests.exceptions.RequestException as e:
        return f"⚠️ Ollama connection error: {str(e)}"