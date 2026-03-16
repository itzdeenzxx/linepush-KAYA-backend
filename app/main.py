import logging
from datetime import datetime, timezone, timedelta

from fastapi import FastAPI

from app.config import init_firebase
from app.messages import pick_random_phrase
from app.services.firestore_service import get_all_active_users, get_eligible_users
from app.services.line_service import (
    build_audio_message,
    build_personalized_flex,
    send_push_message,
)
from app.services.voice_service import generate_audio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="LINE Push Notification Service")

BANGKOK_TZ = timezone(timedelta(hours=7))


@app.on_event("startup")
def on_startup() -> None:
    init_firebase()
    logger.info("Application started")


@app.get("/")
def health_check():
    return {"status": "ok"}


def _send_to_user(user: dict, current_hour: int) -> bool:
    """Build personalized flex + voice and send to one user."""
    user_id = user["user_id"]
    nickname = user["nickname"]
    speaker = user["speaker"]

    # 1) Build flex message
    flex_msg = build_personalized_flex(nickname, speaker, current_hour)

    # 2) Generate voice
    voice_text = pick_random_phrase(speaker, nickname)
    audio_url = generate_audio(voice_text, speaker)

    # 3) Assemble messages
    messages = [flex_msg]
    if audio_url:
        messages.append(build_audio_message(audio_url))

    # 4) Send
    return send_push_message(user_id, messages)


@app.get("/send-line-notifications")
def send_line_notifications():
    """Cron endpoint: send to users whose notifyHour matches current Bangkok hour."""
    now_bangkok = datetime.now(BANGKOK_TZ)
    current_hour = now_bangkok.hour

    logger.info("Cron triggered — Bangkok time: %s, hour: %d", now_bangkok.isoformat(), current_hour)

    try:
        eligible_users = get_eligible_users(current_hour)
    except Exception:
        logger.exception("Failed to fetch eligible users")
        return {"success": False, "error": "Failed to read user settings"}

    sent = 0
    failed = 0

    for user in eligible_users:
        if _send_to_user(user, current_hour):
            sent += 1
        else:
            failed += 1

    result = {
        "success": True,
        "bangkok_time": now_bangkok.isoformat(),
        "current_hour": current_hour,
        "eligible": len(eligible_users),
        "sent": sent,
        "failed": failed,
    }
    logger.info("Result: %s", result)
    return result


@app.get("/force-send")
def force_send():
    """Force send to ALL active users immediately (ignores notifyHour)."""
    now_bangkok = datetime.now(BANGKOK_TZ)
    current_hour = now_bangkok.hour

    logger.info("Force send triggered — Bangkok time: %s", now_bangkok.isoformat())

    try:
        active_users = get_all_active_users()
    except Exception:
        logger.exception("Failed to fetch active users")
        return {"success": False, "error": "Failed to read user settings"}

    sent = 0
    failed = 0

    for user in active_users:
        if _send_to_user(user, current_hour):
            sent += 1
        else:
            failed += 1

    result = {
        "success": True,
        "bangkok_time": now_bangkok.isoformat(),
        "total_active": len(active_users),
        "sent": sent,
        "failed": failed,
    }
    logger.info("Force send result: %s", result)
    return result
