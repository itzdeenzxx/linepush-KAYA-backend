import logging
from typing import Any

import requests

from app.config import LINE_CHANNEL_ACCESS_TOKEN

logger = logging.getLogger(__name__)

LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"

KAYA_MINIAPP_URL = "https://miniapp.line.me/2008680520-UNJtwcRg"


def build_exercise_flex_message() -> dict[str, Any]:
    return {
        "type": "flex",
        "altText": "ถึงเวลาออกกำลังกายแล้ว! มาออกกำลังกายกับ KAYA AI กันเถอะ 💪",
        "contents": {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "KAYA",
                                "color": "#FFFFFF",
                                "size": "3xl",
                                "weight": "bold",
                            },
                            {
                                "type": "text",
                                "text": "AI FITNESS",
                                "color": "#FFFFFF",
                                "size": "xs",
                                "offsetTop": "-4px",
                            },
                        ],
                    }
                ],
                "paddingAll": "20px",
                "background": {
                    "type": "linearGradient",
                    "angle": "135deg",
                    "startColor": "#FF6B00",
                    "endColor": "#FF9E44",
                },
                "height": "80px",
                "justifyContent": "center",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # --- Greeting ---
                    {
                        "type": "text",
                        "text": "ได้เวลาขยับร่างกายแล้ว! 💪",
                        "weight": "bold",
                        "size": "xl",
                        "wrap": True,
                        "color": "#1A1A1A",
                    },
                    {
                        "type": "text",
                        "text": "วันนี้คุณออกกำลังกายแล้วหรือยัง?",
                        "size": "sm",
                        "color": "#888888",
                        "margin": "sm",
                        "wrap": True,
                    },
                    # --- Separator ---
                    {
                        "type": "separator",
                        "margin": "xl",
                        "color": "#F0F0F0",
                    },
                    # --- Feature list ---
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xl",
                        "spacing": "md",
                        "contents": [
                            _feature_row("🏋️", "AI วางแผนออกกำลังกายให้คุณ"),
                            _feature_row("📊", "ติดตามพัฒนาการอย่างต่อเนื่อง"),
                            _feature_row("⏱️", "ใช้เวลาแค่ 15 นาทีต่อวัน"),
                        ],
                    },
                    # --- Motivational quote ---
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xl",
                        "paddingAll": "16px",
                        "cornerRadius": "12px",
                        "backgroundColor": "#FFF5EB",
                        "contents": [
                            {
                                "type": "text",
                                "text": "\"ทุกก้าวเล็ก ๆ คือจุดเริ่มต้นของการเปลี่ยนแปลงครั้งใหญ่\"",
                                "size": "sm",
                                "color": "#FF6B00",
                                "wrap": True,
                                "style": "italic",
                            },
                        ],
                    },
                ],
                "paddingAll": "20px",
                "spacing": "none",
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "เริ่มออกกำลังกายเลย!",
                            "uri": KAYA_MINIAPP_URL,
                        },
                        "style": "primary",
                        "color": "#FF6B00",
                        "height": "md",
                    },
                ],
                "paddingAll": "20px",
            },
            "styles": {
                "footer": {
                    "separator": False,
                },
            },
        },
    }


def _feature_row(icon: str, text: str) -> dict[str, Any]:
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": "md",
        "contents": [
            {
                "type": "text",
                "text": icon,
                "size": "lg",
                "flex": 0,
            },
            {
                "type": "text",
                "text": text,
                "size": "sm",
                "color": "#555555",
                "wrap": True,
                "flex": 5,
            },
        ],
        "alignItems": "center",
    }


def send_push_message(user_id: str, messages: list[dict[str, Any]]) -> bool:

    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": user_id,
        "messages": messages,
    }

    try:
        response = requests.post(LINE_PUSH_URL, headers=headers, json=payload, timeout=10)
        if response.ok:
            logger.info("user=%s: LINE push sent successfully", user_id)
            return True

        logger.error(
            "user=%s: LINE push failed status=%d body=%s",
            user_id,
            response.status_code,
            response.text,
        )
        return False

    except requests.RequestException:
        logger.exception("user=%s: LINE push request error", user_id)
        return False
