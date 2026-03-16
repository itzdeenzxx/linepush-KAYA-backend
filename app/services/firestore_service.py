import logging
from typing import Any

from app.config import get_firestore_client

logger = logging.getLogger(__name__)


def get_eligible_users(current_hour: int) -> list[dict[str, Any]]:
    db = get_firestore_client()
    docs = db.collection("userSettings").stream()

    eligible: list[dict[str, Any]] = []

    for doc in docs:
        user_id = doc.id
        data = doc.to_dict()

        line_notification = data.get("lineNotification")
        if not isinstance(line_notification, dict):
            logger.debug("user=%s: missing lineNotification field, skipping", user_id)
            continue

        accepted = line_notification.get("accepted", False)
        enabled = line_notification.get("enabled", False)
        notify_hour = line_notification.get("notifyHour")

        if not accepted:
            logger.debug("user=%s: not accepted, skipping", user_id)
            continue

        if not enabled:
            logger.debug("user=%s: not enabled, skipping", user_id)
            continue

        if notify_hour != current_hour:
            logger.debug(
                "user=%s: notifyHour=%s != current_hour=%s, skipping",
                user_id,
                notify_hour,
                current_hour,
            )
            continue

        eligible.append({"user_id": user_id, "notify_hour": notify_hour})
        logger.info("user=%s: eligible for notification", user_id)

    logger.info("Found %d eligible user(s) for hour %d", len(eligible), current_hour)
    return eligible


def get_all_active_users() -> list[dict[str, Any]]:
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

        active.append({"user_id": user_id})

    logger.info("Found %d active user(s) for force send", len(active))
    return active
