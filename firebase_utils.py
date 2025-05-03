import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Use full path or relative path to your JSON file
cred_path = os.path.join(os.getcwd(), "firebase-credentials.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def store_result(edited):
    try:
        # Get the current date and time
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Add data to Firestore
        doc_ref = db.collection("weights").add({
            "weight": edited,
            "date": current_date
        })
        print(f"Document successfully added with ID: {doc_ref.id}")
    except Exception as e:
        print("Error adding document to Firestore:", e)
