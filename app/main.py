import logging
from datetime import datetime, timezone, timedelta

from fastapi import FastAPI

from app.config import init_firebase
from app.services.firestore_service import get_all_active_users, get_eligible_users
from app.services.line_service import build_exercise_flex_message, send_push_message

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


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/send-line-notifications")
def send_line_notifications():

    now_bangkok = datetime.now(BANGKOK_TZ)
    current_hour = now_bangkok.hour

    logger.info(
        "Cron triggered — Bangkok time: %s, current_hour: %d",
        now_bangkok.isoformat(),
        current_hour,
    )

    try:
        eligible_users = get_eligible_users(current_hour)
    except Exception:
        logger.exception("Failed to fetch eligible users from Firestore")
        return {"success": False, "error": "Failed to read user settings"}

    sent = 0
    failed = 0

    for user in eligible_users:
        user_id = user["user_id"]
        ok = send_push_message(user_id, [build_exercise_flex_message()])
        if ok:
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
    now_bangkok = datetime.now(BANGKOK_TZ)

    logger.info("Force send triggered — Bangkok time: %s", now_bangkok.isoformat())

    try:
        active_users = get_all_active_users()
    except Exception:
        logger.exception("Failed to fetch active users from Firestore")
        return {"success": False, "error": "Failed to read user settings"}

    sent = 0
    failed = 0

    for user in active_users:
        user_id = user["user_id"]
        ok = send_push_message(user_id, [build_exercise_flex_message()])
        if ok:
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
