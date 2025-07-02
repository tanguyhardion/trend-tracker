import firebase_admin
from firebase_admin import credentials, firestore
import os

FIREBASE_CRED_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'firebase_creds.json')

firebase_app = None
db = None

def init_firebase():
    global firebase_app, db
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CRED_PATH)
        firebase_app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
