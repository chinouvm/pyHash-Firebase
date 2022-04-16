import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

try:
    cred = credentials.Certificate("./key.json")
except ValueError:
    print("Database connection failed: Invalid key.json file")
except IOError:
    print("Database connection failed: Invalid key.json file")

firebase_admin.initialize_app(cred)

db = firestore.client()
