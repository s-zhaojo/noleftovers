from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from auth import verify_token, login_user
from database import get_user_data, update_user_data, create_user_object

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes with more permissive settings
CORS(app, 
     resources={r"/*": {
         "origins": [
             "https://noleftovers-krng.vercel.app",  # Current Vercel deployment
             "http://localhost:3000"  # Local development
         ],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type", "Authorization"]
     }})

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user_data_endpoint(user_id):
    user_id, error_response, error_code = verify_token(request)
    if error_response:
        return error_response, error_code

    user_data, error_response, error_code = get_user_data(user_id)
    if error_response:
        return jsonify(error_response), error_code

    return jsonify(user_data)

@app.route('/api/edit-users/<user_id>', methods=['PUT'])
def update_user_data_endpoint(user_id):
    user_id, error_response, error_code = verify_token(request)
    if error_response:
        return error_response, error_code

    data = request.get_json()
    updated_data, error_response, error_code = update_user_data(user_id, data)
    if error_response:
        return jsonify(error_response), error_code

    return jsonify(updated_data)

@app.route('/verify-token', methods=['POST'])
def verify_token_endpoint():
    user_id, error_response, error_code = verify_token(request)
    if error_response:
        return error_response, error_code

    user_data, error_response, error_code = get_user_data(user_id)
    if error_response:
        return jsonify(error_response), error_code

    user_dict, error_response, error_code = create_user_object(user_id, user_data)
    if error_response:
        return jsonify(error_response), error_code

    return jsonify(user_dict)

@app.route('/login', methods=['POST'])
def login_endpoint():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_data, error_response, error_code = login_user(email, password)
    if error_response:
        return error_response, error_code

    return jsonify(user_data)

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

