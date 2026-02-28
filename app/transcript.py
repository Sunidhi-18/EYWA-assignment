from youtube_transcript_api import YouTubeTranscriptApi
import re


def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")


def get_transcript(url):
    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()

    try:
        # Try English first
        transcript = api.fetch(video_id, languages=["en"])
    except:
        # If English not available, fetch whatever is available
        transcript = api.fetch(video_id)

    return [{"text": item.text} for item in transcript]