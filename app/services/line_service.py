import logging
import random
from typing import Any

import requests

from app.config import LINE_CHANNEL_ACCESS_TOKEN
from app.messages import (
    EXERCISE_IMAGES,
    get_speaker_config,
    get_time_emoji,
    get_time_greeting,
    pick_random_greeting,
    pick_random_phrase,
)

logger = logging.getLogger(__name__)

LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
KAYA_MINIAPP_URL = "https://miniapp.line.me/2008680520-UNJtwcRg"


# ---------------------------------------------------------------------------
# 5 flex layout builders (one picked randomly per notification)
# ---------------------------------------------------------------------------


def _flex_layout_hero_image(
    cfg: dict, nickname: str, greeting: str, time_greeting: str, time_emoji: str, sub_text: str,
) -> dict[str, Any]:
    """Layout 1: Hero image on top, gradient header overlay."""
    return {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": random.choice(EXERCISE_IMAGES),
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": cfg["emoji"], "size": "lg", "flex": 0},
                        {
                            "type": "text",
                            "text": f"{time_greeting}ค่ะ/ครับ {nickname}!",
                            "size": "lg",
                            "weight": "bold",
                            "wrap": True,
                            "flex": 5,
                            "color": "#1A1A1A",
                        },
                    ],
                    "alignItems": "center",
                    "spacing": "sm",
                },
                {
                    "type": "text",
                    "text": greeting,
                    "size": "sm",
                    "color": "#888888",
                    "wrap": True,
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "paddingAll": "12px",
                    "cornerRadius": "10px",
                    "backgroundColor": cfg["bg_light"],
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": sub_text,
                            "size": "xs",
                            "color": cfg["color"],
                            "wrap": True,
                            "style": "italic",
                        }
                    ],
                },
            ],
            "paddingAll": "20px",
        },
        "footer": _footer_box(cfg),
        "styles": {"footer": {"separator": False}},
    }


def _flex_layout_gradient_top(
    cfg: dict, nickname: str, greeting: str, time_greeting: str, time_emoji: str, sub_text: str,
) -> dict[str, Any]:
    """Layout 2: Gradient header with name, body with message."""
    return {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{time_emoji} {time_greeting}",
                    "color": "#FFFFFF",
                    "size": "sm",
                },
                {
                    "type": "text",
                    "text": f"{nickname}!",
                    "color": "#FFFFFF",
                    "size": "xxl",
                    "weight": "bold",
                    "margin": "sm",
                },
            ],
            "paddingAll": "20px",
            "background": {
                "type": "linearGradient",
                "angle": "135deg",
                "startColor": cfg["gradient_start"],
                "endColor": cfg["gradient_end"],
            },
            "height": "100px",
            "justifyContent": "center",
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": greeting,
                    "size": "md",
                    "weight": "bold",
                    "wrap": True,
                    "color": "#1A1A1A",
                },
                {"type": "separator", "color": "#F0F0F0", "margin": "md"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "spacing": "sm",
                    "contents": [
                        {"type": "text", "text": "🏋️", "size": "md", "flex": 0},
                        {
                            "type": "text",
                            "text": "AI วางแผนออกกำลังกายให้คุณ",
                            "size": "xs",
                            "color": "#666666",
                            "wrap": True,
                        },
                    ],
                    "alignItems": "center",
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {"type": "text", "text": "⏱️", "size": "md", "flex": 0},
                        {
                            "type": "text",
                            "text": "ใช้เวลาแค่ 15 นาที",
                            "size": "xs",
                            "color": "#666666",
                            "wrap": True,
                        },
                    ],
                    "alignItems": "center",
                },
            ],
            "paddingAll": "20px",
        },
        "footer": _footer_box(cfg),
        "styles": {"footer": {"separator": False}},
    }


def _flex_layout_minimal(
    cfg: dict, nickname: str, greeting: str, time_greeting: str, time_emoji: str, sub_text: str,
) -> dict[str, Any]:
    """Layout 3: Clean minimal card."""
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": f"{time_emoji} KAYA AI",
                    "size": "sm",
                    "color": cfg["color"],
                    "weight": "bold",
                },
                {
                    "type": "text",
                    "text": f"{time_greeting} {nickname}!",
                    "size": "xl",
                    "weight": "bold",
                    "color": "#1A1A1A",
                    "wrap": True,
                },
                {
                    "type": "text",
                    "text": greeting,
                    "size": "md",
                    "color": "#555555",
                    "wrap": True,
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "paddingAll": "14px",
                    "cornerRadius": "12px",
                    "backgroundColor": cfg["bg_light"],
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{cfg['emoji']} {sub_text}",
                            "size": "sm",
                            "color": cfg["color"],
                            "wrap": True,
                        },
                    ],
                },
            ],
            "paddingAll": "20px",
        },
        "footer": _footer_box(cfg),
        "styles": {"footer": {"separator": False}},
    }


def _flex_layout_image_side(
    cfg: dict, nickname: str, greeting: str, time_greeting: str, time_emoji: str, sub_text: str,
) -> dict[str, Any]:
    """Layout 4: Image + text side by side (compact)."""
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "lg",
                    "contents": [
                        {
                            "type": "image",
                            "url": random.choice(EXERCISE_IMAGES),
                            "size": "full",
                            "aspectRatio": "1:1",
                            "aspectMode": "cover",
                            "flex": 2,
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "flex": 3,
                            "spacing": "sm",
                            "justifyContent": "center",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"{time_emoji} {time_greeting}",
                                    "size": "xs",
                                    "color": cfg["color"],
                                },
                                {
                                    "type": "text",
                                    "text": f"{nickname}!",
                                    "size": "xl",
                                    "weight": "bold",
                                    "color": "#1A1A1A",
                                },
                                {
                                    "type": "text",
                                    "text": greeting,
                                    "size": "xs",
                                    "color": "#888888",
                                    "wrap": True,
                                },
                            ],
                        },
                    ],
                },
            ],
            "paddingAll": "16px",
        },
        "footer": _footer_box(cfg),
        "styles": {"footer": {"separator": False}},
    }


def _flex_layout_bold_quote(
    cfg: dict, nickname: str, greeting: str, time_greeting: str, time_emoji: str, sub_text: str,
) -> dict[str, Any]:
    """Layout 5: Big motivational quote style."""
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": f"{time_emoji} {time_greeting} {nickname}",
                    "size": "sm",
                    "color": "#AAAAAA",
                },
                {
                    "type": "text",
                    "text": f"💬 \"{greeting}\"",
                    "size": "lg",
                    "weight": "bold",
                    "wrap": True,
                    "color": cfg["color"],
                    "margin": "md",
                },
                {"type": "separator", "margin": "lg", "color": "#F0F0F0"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "lg",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "cornerRadius": "999px",
                            "width": "8px",
                            "height": "40px",
                            "backgroundColor": cfg["color"],
                            "contents": [],
                        },
                        {
                            "type": "text",
                            "text": sub_text,
                            "size": "sm",
                            "color": "#555555",
                            "wrap": True,
                        },
                    ],
                    "alignItems": "center",
                },
            ],
            "paddingAll": "20px",
            "background": {
                "type": "linearGradient",
                "angle": "180deg",
                "startColor": "#FFFFFF",
                "endColor": cfg["bg_light"],
            },
        },
        "footer": _footer_box(cfg),
        "styles": {"footer": {"separator": False}},
    }


# ---------------------------------------------------------------------------
# Shared footer
# ---------------------------------------------------------------------------

def _footer_box(cfg: dict) -> dict[str, Any]:
    return {
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
                "color": cfg["color"],
                "height": "md",
            },
        ],
        "paddingAll": "16px",
    }


# ---------------------------------------------------------------------------
# All 5 layouts
# ---------------------------------------------------------------------------

_FLEX_LAYOUTS = [
    _flex_layout_hero_image,
    _flex_layout_gradient_top,
    _flex_layout_minimal,
    _flex_layout_image_side,
    _flex_layout_bold_quote,
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

MOTIVATIONAL_SUBS = [
    "ทุกก้าวเล็กๆ คือจุดเริ่มต้นของการเปลี่ยนแปลงครั้งใหญ่",
    "ร่างกายที่แข็งแรงคือของขวัญที่ดีที่สุดที่คุณให้ตัวเอง",
    "วันนี้คุณเลือกที่จะแข็งแรงขึ้น",
    "แค่เริ่มก็ชนะครึ่งนึงแล้ว",
    "สุขภาพดีไม่ได้มาจากโชค แต่มาจากความตั้งใจ",
]


def build_personalized_flex(
    nickname: str, speaker_id: str, current_hour: int,
) -> dict[str, Any]:
    """Build a random personalized flex message for a user."""
    cfg = get_speaker_config(speaker_id)
    time_greeting = get_time_greeting(current_hour)
    time_emoji = get_time_emoji(current_hour)
    greeting = pick_random_greeting(speaker_id)
    sub_text = random.choice(MOTIVATIONAL_SUBS)

    layout_fn = random.choice(_FLEX_LAYOUTS)
    bubble = layout_fn(cfg, nickname, greeting, time_greeting, time_emoji, sub_text)

    return {
        "type": "flex",
        "altText": f"{time_greeting} {nickname}! มาออกกำลังกายกับ KAYA AI กันเถอะ 💪",
        "contents": bubble,
    }


def build_audio_message(audio_url: str) -> dict[str, Any]:
    """Build a LINE audio message."""
    return {
        "type": "audio",
        "originalContentUrl": audio_url,
        "duration": 10000,
    }


def send_push_message(user_id: str, messages: list[dict[str, Any]]) -> bool:
    """Send LINE push messages to a single user."""
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": user_id,
        "messages": messages,
    }

    try:
        response = requests.post(LINE_PUSH_URL, headers=headers, json=payload, timeout=15)
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
