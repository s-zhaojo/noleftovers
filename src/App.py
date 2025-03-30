from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
import logging
from firebase_init import db  # Import the initialized Firestore client

# Local imports
from auth import verify_token, login_user
from database import (
    get_user_data, 
    create_user_object, 
    add_meal, 
    get_user_meals, 
    get_meals_by_date
)

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
             "https://noleftovers6890.vercel.app",  # Current Vercel deployment
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

@app.route('/update-points', methods=['POST'])
def update_points():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        points = data.get('points')
        password = data.get('password')

        if not all([user_id, points, password]):
            return jsonify({'message': 'Missing required fields'}), 400

        # Verify teacher password
        if password != 'nsd417':
            return jsonify({'message': 'Invalid teacher password'}), 401

        # Update user points in database using the initialized client
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({'message': 'User not found'}), 404

        # Get current points from the document data
        user_data = user_doc.to_dict()
        current_points = user_data.get('points', 0)
        new_points = current_points + points

        user_ref.update({
            'points': new_points
        })

        return jsonify({
            'message': 'Points updated successfully',
            'new_points': new_points
        }), 200

    except Exception as e:
        print(f"Error updating points: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/redeem-points', methods=['POST'])
def redeem_points():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        points = data.get('points')

        if not all([user_id, points]):
            return jsonify({'message': 'Missing required fields'}), 400

        # Get user's current points
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({'message': 'User not found'}), 404

        user_data = user_doc.to_dict()
        current_points = user_data.get('points', 0)

        # Check if user has enough points
        if current_points + points < 0:
            return jsonify({'message': 'Insufficient points'}), 400

        # Update points
        user_ref.update({
            'points': current_points + points
        })

        return jsonify({
            'message': 'Points updated successfully',
            'new_points': current_points + points
        }), 200

    except Exception as e:
        print(f"Error redeeming points: {str(e)}")
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"Starting server on https://noleftovers-backend.onrender.com/")
    app.run(host='0.0.0.0', debug=True, port=port)
