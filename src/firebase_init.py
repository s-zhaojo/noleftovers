import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def initialize_firebase():
    try:
        # Check if Firebase is already initialized
        app = firebase_admin.get_app()
        logger.debug("Firebase app already initialized")
    except ValueError:
        logger.debug("Initializing Firebase app...")
        # Initialize Firebase Admin
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").strip('"').replace("\\n", "\n"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
        })
        
        # Initialize the app
        app = firebase_admin.initialize_app(cred)
        logger.debug("Firebase app initialized successfully")

    # Get Firestore client
    logger.debug("Getting Firestore client...")
    db = firestore.client()
    logger.debug("Firestore client initialized successfully")

    # Test the connection
    try:
        # Try to access the root collections
        collections = db.collections()
        logger.debug(f"Successfully connected to Firestore. Available collections: {[c.id for c in collections]}")
        return db
    except Exception as e:
        logger.error(f"Failed to connect to Firestore: {str(e)}")
        raise

# Initialize Firebase and get the Firestore client
db = initialize_firebase() 