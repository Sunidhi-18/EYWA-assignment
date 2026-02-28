from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN
from transcript import get_transcript
from summarizer import generate_summary
from qa_engine import chunk_transcript, answer_question
from vector_store import VectorStore

# Store user sessions separately
user_sessions = {}


# ✅ Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to YouTube AI Assistant!\n\n"
        "1️⃣ Send a YouTube link to get a structured summary.\n"
        "2️⃣ Then ask questions about the video.\n\n"
        "🌐 Default language: English\n"
        "🇮🇳 If you want Hindi, include 'in Hindi' in your question."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 How to use this bot:\n\n"
        "1️⃣ Send a YouTube link\n"
        "2️⃣ Get structured summary\n"
        "3️⃣ Ask questions about the video\n\n"
        "🌐 Default: English\n"
        "🇮🇳 Add 'in Hindi' for Hindi answers"
    )

# ✅ Main message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text.strip()
    lower_text = text.lower()

    # 🔹 STEP 1 — YouTube Link
    if "youtube.com" in lower_text or "youtu.be" in lower_text:
        try:
            await update.message.reply_text("⏳ Fetching transcript...")

            transcript = get_transcript(text)
            transcript_text = " ".join([t["text"] for t in transcript])

            await update.message.reply_text("🧠 Generating structured summary...")

            summary = generate_summary(transcript_text)

            # Build vector store for Q&A
            chunks = chunk_transcript(transcript)
            vs = VectorStore()
            vs.build_index(chunks)

            user_sessions[user_id] = vs

            await update.message.reply_text(summary)

        except ValueError:
            await update.message.reply_text(
                "❌ Invalid YouTube URL or subtitles not available."
            )
        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {str(e)}")

    # 🔹 STEP 2 — Q&A
    else:
        if user_id not in user_sessions:
            await update.message.reply_text(
                "📌 Please send a YouTube link first."
            )
            return

        vs = user_sessions[user_id]

        try:
            answer = answer_question(vs, text)
            await update.message.reply_text(answer)

        except Exception as e:
            await update.message.reply_text(f"⚠️ Error: {str(e)}")


# ✅ Bot starter
def start_bot():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing. Check your .env file.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))  # 👈 ADD THIS
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Telegram Bot is running...")
    app.run_polling()