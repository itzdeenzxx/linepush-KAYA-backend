import json
import os
import logging

from dotenv import load_dotenv

load_dotenv()

import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger(__name__)

LINE_CHANNEL_ACCESS_TOKEN: str = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

FIREBASE_CREDENTIALS_JSON: str = os.environ["FIREBASE_CREDENTIALS_JSON"]


def init_firebase() -> None:
    """Initialize the Firebase Admin SDK once."""
    if firebase_admin._apps:
        return

    cred_dict = json.loads(FIREBASE_CREDENTIALS_JSON)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    logger.info("Firebase initialized")


def get_firestore_client() -> firestore.firestore.Client:
    """Return the Firestore client, initializing Firebase if needed."""
    init_firebase()
    return firestore.client()
