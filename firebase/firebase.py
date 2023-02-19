import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def initialize_db():
    cred = credentials.Certificate("firebase/firebase_account_key.json")
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

