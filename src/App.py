from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

CORS(app, resources={
    r"/verify-token": {
        "origins": ["https://your-frontend-domain.com"],
        "methods": ["POST"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
})

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

@app.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            app.logger.warning('No token provided')
            return jsonify({'error': 'Authorization header missing or invalid'}), 401
        
        token = auth_header.split('Bearer ')[1]
        decoded_token = auth.verify_id_token(token)
        
        app.logger.info(f"Successfully verified token for user: {decoded_token['uid']}")
        return jsonify({
            'success': True,
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email', '')
        })
    except auth.InvalidIdTokenError as e:
        app.logger.error(f"Invalid token: {str(e)}")
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        app.logger.error(f"Authentication error: {str(e)}")
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

