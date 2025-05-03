import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime
import streamlit as st

# Load Firebase credentials from Streamlit secrets
cred_json = st.secrets["firebase-credentials"]

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_json)
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def store_result(edited):
    # Get the current date and time
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add data to Firestore
    doc_ref = db.collection("weights").add({
        "weight": edited,
        "date": current_date
    })
