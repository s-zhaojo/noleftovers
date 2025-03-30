from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore
from models.user import User
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes with more permissive settings
CORS(app, 
     resources={r"/*": {
         "origins": ["https://noleftovers.vercel.app", "http://localhost:3000"],  # Allow Vercel and local development
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type", "Authorization"]
     }})

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

firebase_admin.initialize_app(cred)
db = firestore.client()

def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        app.logger.warning('No token provided')
        return None, jsonify({'error': 'Authorization header missing or invalid'}), 401
    
    token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid'], None, None
    except auth.InvalidIdTokenError as e:
        app.logger.error(f"Invalid token: {str(e)}")
        return None, jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        app.logger.error(f"Authentication error: {str(e)}")
        return None, jsonify({'error': 'Authentication failed'}), 401

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user_data(user_id):
    user_id, error_response, error_code = verify_token()
    if error_response:
        return error_response, error_code

    try:
        user_doc = db.collection('users').document(user_id).get()
        
        if user_doc.exists:
            app.logger.info(f"User data found for: {user_id}")
            return jsonify(user_doc.to_dict())
        else:
            app.logger.info(f"Creating new user document for: {user_id}")
            default_user_data = {
                'email': '',
                'points': 0,
                'lunchesBought': 0,
                'photosSubmitted': 0,
                'createdAt': datetime.now().isoformat(),
                'lastUpdated': datetime.now().isoformat()
            }
            
            db.collection('users').document(user_id).set(default_user_data)
            return jsonify(default_user_data)
    except Exception as e:
        app.logger.error(f"Error getting user data: {str(e)}")
        return jsonify({'error': 'Failed to get user data'}), 500

@app.route('/api/edit-users/<user_id>', methods=['PUT'])
def update_user_data(user_id):
    user_id, error_response, error_code = verify_token()
    if error_response:
        return error_response, error_code

    try:
        data = request.get_json()
        user_ref = db.collection('users').document(user_id)
        
        update_data = {
            **data,
            'lastUpdated': datetime.now().isoformat()
        }
        
        user_ref.update(update_data)
        app.logger.info(f"Successfully updated user data for: {user_id}")
        
        # Return updated user data
        updated_doc = user_ref.get()
        return jsonify(updated_doc.to_dict())
    except Exception as e:
        app.logger.error(f"Error updating user data: {str(e)}")
        return jsonify({'error': 'Failed to update user data'}), 500

@app.route('/verify-token', methods=['POST'])
def verify_token_endpoint():
    user_id, error_response, error_code = verify_token()
    if error_response:
        return error_response, error_code

    try:
        app.logger.info(f"Successfully verified token for user: {user_id}")
        user_doc = db.collection('users').document(user_id).get()
        
        if not user_doc.exists:
            return jsonify({'error': 'User not found'}), 404
            
        user_data = user_doc.to_dict()
        
        # Create User object
        user = User(
            uuid=user_id,
            name=user_data.get('name', ''),
            points=user_data.get('points', 0),
            no_of_lunches_today=user_data.get('no_of_lunches_today', 0),
            no_of_submissions_today=user_data.get('no_of_submissions_today', 0)
        )
        
        return user.to_dict()
    except Exception as e:
        app.logger.error(f"Error in verify-token: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 401

@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"Starting server on https://noleftovers-backend.onrender.com/")
    app.run(host='0.0.0.0', debug=True, port=port)

"""

Paste this in the body tag at the bottom of the html file before the firebase services uses

    <script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.5.0/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyBhf5uVyxDHESysm6u1rfHFmVDBaeoRjB8",
    authDomain: "noleftovers-fe4a1.firebaseapp.com",
    projectId: "noleftovers-fe4a1",
    storageBucket: "noleftovers-fe4a1.firebasestorage.app",
    messagingSenderId: "681158133625",
    appId: "1:681158133625:web:05d45feb669ed4dbd6d1a8",
    measurementId: "G-7QL4Q2TZLB"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
</script>
"""

