from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
from auth import verify_token, login_user
from database import get_user_data, create_user_object, add_meal, get_user_meals, get_meals_by_date
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes with more permissive settings
CORS(app, 
     resources={r"/*": {
         "origins": [
             "https://noleftovers-rho.vercel.app",  # Current Vercel deployment
             "http://localhost:3000"  # Local development
         ],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
         "supports_credentials": True,
         "expose_headers": ["Content-Type", "Authorization"]
     }})


@app.route('/add-meal', methods=['POST'])
def add_meal_endpoint():
    data = request.get_json()
    user_id = data.get('user_id')
    date_taken = data.get('date_taken')
    pts = data.get('pts')
    
    print(f"Received meal data: user_id={user_id}, date_taken={date_taken}, pts={pts}")  # Debug log
    
    try:
        date_taken = datetime.strptime(date_taken, '%Y-%m-%d')
        result, error_response, error_code = add_meal(user_id, date_taken, pts)
        if error_response:
            return jsonify(error_response), error_code
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        print(f"Date parsing error: {str(e)}")  # Debug log
        return jsonify({'error': 'Invalid date format'}), 400

@app.route('/verify-token', methods=['POST'])
def verify_token_endpoint():
    user_id, error_response, error_code = verify_token(request)
    if error_response:
        return error_response, error_code

    user_data, error_response, error_code = get_user_data(user_id)
    print(f"User data retrieved for {user_id}:", user_data)
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

    logger.debug(f"Login attempt for email: {email}")

    user_data, error_response, error_code = login_user(email, password)
    if error_response:
        logger.error(f"Login failed: {error_response}")
        return error_response, error_code

    logger.debug(f"Login successful, user data: {user_data}")

    # Get the user's data from Firestore
    user_id = user_data['userId']
    logger.debug(f"Fetching Firestore data for user_id: {user_id}")
    
    user_data, error_response, error_code = get_user_data(user_id)
    if error_response:
        logger.error(f"Failed to get user data: {error_response}")
        return error_response, error_code

    logger.debug(f"Retrieved user data from Firestore: {user_data}")

    # Create a proper user object
    user_dict, error_response, error_code = create_user_object(user_id, user_data)
    if error_response:
        logger.error(f"Failed to create user object: {error_response}")
        return error_response, error_code

    logger.debug(f"Successfully created user object: {user_dict}")
    return jsonify(user_dict)

@app.route('/dashboard', methods=['GET'])
def dashboard_endpoint():
    user_id = request.args.get('user_id')

    user_data, error_response, error_code = get_user_data(user_id)
    if error_response:
        return error_response, error_code
        
    user_dict, error_response, error_code = create_user_object(user_id, user_data)
    if error_response:
        return error_response, error_code

    return jsonify(user_dict)

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

