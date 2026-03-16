import logging

import requests

logger = logging.getLogger(__name__)

BOTNOI_BASE_URL = "https://api-voice.botnoi.ai"
BOTNOI_TOKEN = "2XtOvwLar6vW5Pu2uGNQ1qZEVH72ZMad"


def generate_audio(text: str, speaker: str) -> str | None:
    """Generate audio via Botnoi TTS API.

    Returns the audio URL on success, None on failure.
    """
    url = f"{BOTNOI_BASE_URL}/openapi/v1/generate_audio"
    headers = {
        "botnoi-token": BOTNOI_TOKEN,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "speaker": str(speaker),
        "volume": 1,
        "speed": 1,
        "type_media": "mp3",
        "save_file": "true",
        "language": "th",
        "page": "user",
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if not response.ok:
            logger.error(
                "Botnoi TTS failed status=%d body=%s",
                response.status_code,
                response.text,
            )
            return None

        data = response.json()
        audio_url = data.get("audio_url")
        if not audio_url:
            logger.error("Botnoi TTS response missing audio_url: %s", data)
            return None

        logger.info("Botnoi TTS generated audio: %s", audio_url)
        return audio_url

    except requests.RequestException:
        logger.exception("Botnoi TTS request error")
        return None
