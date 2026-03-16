import logging
from typing import Any

from app.config import get_firestore_client

logger = logging.getLogger(__name__)


def _enrich_user(db, user_id: str, data: dict) -> dict[str, Any]:
    """Add nickname and speaker ID to a user dict."""
    # Get speaker from userSettings -> tts.speaker
    tts = data.get("tts")
    speaker = "5"  # default
    if isinstance(tts, dict):
        speaker = str(tts.get("speaker", "5"))

    # Get nickname from users collection
    nickname = "เพื่อน"
    try:
        user_doc = db.collection("users").document(user_id).get()
        if user_doc.exists:
            nickname = user_doc.to_dict().get("nickname", "เพื่อน") or "เพื่อน"
    except Exception:
        logger.exception("user=%s: failed to fetch nickname", user_id)

    return {
        "user_id": user_id,
        "nickname": nickname,
        "speaker": speaker,
    }


def get_eligible_users(current_hour: int) -> list[dict[str, Any]]:
    """Return users whose lineNotification matches the current hour."""
    db = get_firestore_client()
    docs = db.collection("userSettings").stream()

    eligible: list[dict[str, Any]] = []

    for doc in docs:
        user_id = doc.id
        data = doc.to_dict()

        line_notification = data.get("lineNotification")
        if not isinstance(line_notification, dict):
            continue

        if not line_notification.get("accepted", False):
            continue

        if not line_notification.get("enabled", False):
            continue

        if line_notification.get("notifyHour") != current_hour:
            continue

        user = _enrich_user(db, user_id, data)
        eligible.append(user)
        logger.info("user=%s nickname=%s speaker=%s: eligible", user_id, user["nickname"], user["speaker"])

    logger.info("Found %d eligible user(s) for hour %d", len(eligible), current_hour)
    return eligible


def get_all_active_users() -> list[dict[str, Any]]:
    """Return all users with accepted+enabled (ignore hour)."""
    db = get_firestore_client()
    docs = db.collection("userSettings").stream()

    active: list[dict[str, Any]] = []

    for doc in docs:
        user_id = doc.id
        data = doc.to_dict()

        line_notification = data.get("lineNotification")
        if not isinstance(line_notification, dict):
            continue

        if not line_notification.get("accepted", False):
            continue

        if not line_notification.get("enabled", False):
            continue

        user = _enrich_user(db, user_id, data)
        active.append(user)

    logger.info("Found %d active user(s) for force send", len(active))
    return active
