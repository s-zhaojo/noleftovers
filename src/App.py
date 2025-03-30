from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
from auth import verify_token, login_user
from database import get_user_data, create_user_object, add_meal, get_user_meals, get_meals_by_date, get_admin_data, update_admin_data, get_all_users, generate_qr_code, verify_admin
import logging
from io import BytesIO
from werkzeug.utils import secure_filename
from PIL import Image
import io
import numpy as np
from yolov5.detect import run_detection

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

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/admin/users', methods=['GET'])
def get_users_endpoint():
    """Get all users (admin only)"""
    # Verify admin token
    user_id, error_response, error_code = verify_token(request)
    if error_response:
        return error_response, error_code
        
    # Get user data to check if admin
    user_data, error_response, error_code = get_user_data(user_id)
    if error_response:
        return error_response, error_code
        
    # Check if user is admin (you'll need to add an is_admin field to your user documents)
    if not user_data.get('is_admin', False):
        return jsonify({'error': 'Unauthorized - Admin access required'}), 403
        
    # Get all users
    users, error_response, error_code = get_all_users()
    if error_response:
        return error_response, error_code
        
    return jsonify(users)

@app.route('/qr-code/<user_id>', methods=['GET'])
def get_qr_code_endpoint(user_id):
    """Get QR code for a user"""
    # Verify token
    requesting_user_id, error_response, error_code = verify_token(request)
    if error_response:
        return error_response, error_code
        
    # Get user data to check if admin or requesting their own QR code
    user_data, error_response, error_code = get_user_data(requesting_user_id)
    if error_response:
        return error_response, error_code
        
    # Allow access if user is admin or requesting their own QR code
    if not user_data.get('is_admin', False) and requesting_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    # Generate QR code
    qr_code, error_response, error_code = generate_qr_code(user_id)
    if error_response:
        return error_response, error_code
        
    # Return QR code as PNG image
    return send_file(
        BytesIO(qr_code),
        mimetype='image/png',
        as_attachment=True,
        download_name=f'qr_code_{user_id}.png'
    )

@app.route('/admin/login', methods=['POST'])
def admin_login_endpoint():
    """Admin login endpoint"""
    data = request.get_json()
    admin_id = data.get('admin_id')

    logger.debug(f"Admin login attempt with ID: {admin_id}")

    # Verify admin ID
    admin_data, error_response, error_code = verify_admin(admin_id)
    if error_response:
        logger.error(f"Admin login failed: {error_response}")
        return error_response, error_code

    logger.debug(f"Admin login successful: {admin_data}")
    return jsonify(admin_data)

@app.route('/analyze-food', methods=['POST'])
def analyze_food_endpoint():
    """Analyze food image using ML model"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        try:
            # Read the image
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Run ML model detection
            volume = run_detection(image)
            
            # Calculate points based on volume
            if volume == 0:
                points = 50
            elif volume < 0.3:
                points = -10
            elif volume < 0.6:
                points = -25
            else:
                points = -40
                
            return jsonify({
                'volume': volume,
                'points': points
            })
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            return jsonify({'error': 'Failed to analyze image'}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/')
def home():
    return jsonify({'message': 'Flask server is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"Starting server on https://noleftovers-backend.onrender.com/")
    app.run(host='0.0.0.0', debug=True, port=port)
