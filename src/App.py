from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Configure CORS to allow all origins during development
CORS(app, 
     resources={
         r"/*": {
             "origins": "*",  # Allow all origins
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "Accept", "Origin"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "max_age": 3600
         }
     })

# Initialize Firebase Admin
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
})

firebase_admin.initialize_app(cred)

@app.route('/login', methods=['POST'])
def login():
    return "Hello World"

@app.route('/verify-token', methods=['POST', 'OPTIONS'])
def verify_token():
    print("\n=== New Request ===")
    print("Request method:", request.method)
    print("Request headers:", dict(request.headers))
    print("Request origin:", request.headers.get('Origin'))
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        print("Handling OPTIONS request")
        response = jsonify({'message': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # Get the token from the Authorization header
    auth_header = request.headers.get('Authorization')
    print("Auth header:", auth_header)
    
    if not auth_header or not auth_header.startswith('Bearer '):
        print("No valid Authorization header found")
        response = jsonify({'error': 'No token provided'}), 401
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    token = auth_header.split('Bearer ')[1]
    print("Token received:", token[:20] + "...")  # Only print first 20 chars for security
    
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        print("Token verified successfully")
        print("Decoded token:", decoded_token)
        response = jsonify({
            'success': True,
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email', '')
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        response = jsonify({'error': str(e)}), 401
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"Starting server on http://localhost:{port}")
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

