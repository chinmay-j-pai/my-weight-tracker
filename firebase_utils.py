import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# Check if running on Streamlit Cloud or locally
if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
    # When deployed on Streamlit Cloud (or any environment with the correct environment variable)
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
else:
    # When running locally, use the local path to the firebase credentials file
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
