from firebase_admin import firestore
from models.User import User
from models.Admin import Admin
from datetime import datetime
import logging
from firebase_init import db
import requests

logger = logging.getLogger(__name__)

def get_user_data(user_id):
    """Get user data from Firestore"""
    try:
        logger.debug(f"Attempting to get user data for user_id: {user_id}")
        
        # Log the collection and document path
        collection_ref = db.collection('users')
        doc_ref = collection_ref.document(user_id)
        logger.debug(f"Accessing Firestore path: users/{user_id}")
        
        # Get the document
        user_doc = doc_ref.get()
        logger.debug(f"Firestore query completed for user_id: {user_id}")

        if user_doc.exists:
            logger.debug(f"User data found for: {user_id}")
            user_data = user_doc.to_dict()
            logger.debug(f"Raw user data from Firestore: {user_data}")
            
            # Log all fields in the document
            for field, value in user_data.items():
                logger.debug(f"Field '{field}': {value}")
            
            # Return the raw data without modification
            return user_data, None, None
        else:
            logger.debug(f"No document found for user_id: {user_id}")
            return None, {'error': 'User document not found'}, 404
            
    except Exception as e:
        logger.error(f"Error getting user data for {user_id}: {str(e)}")
        return None, {'error': 'Failed to get user data'}, 500

def create_user_object(user_id, user_data):
    """Create a User object from Firestore data"""
    try:
        logger.debug(f"Creating user object with data: user_id={user_id}, user_data={user_data}")
        
        # Map Firestore data to User object fields
        user = User(
            uuid=user_id,
            name=user_data.get('name', ''),  # Get name from Firestore
            points=user_data.get('pts', 0),
            no_of_lunches_today=user_data.get('no_lunches_today', 0),
            no_of_submissions_today=user_data.get('no_of_submissions_today', 0)
        )
        
        user_dict = user.to_dict()
        logger.debug(f"Created user object: {user_dict}")
        return user_dict, None, None
    except Exception as e:
        logger.error(f"Error creating user object: {str(e)}")
        logger.error(f"User data that caused error: {user_data}")
        return None, {'error': 'Failed to create user object'}, 500

def add_meal(user_id, points):
    """Add a new meal record and update user's points"""
    try:
        # Create new meal record
        meal_data = {
            'date_taken': datetime.now(),
            'pts': points,
            'userId': user_id
        }
        
        # Add to meals collection
        db.collection('meals').add(meal_data)
        
        # Update user's points and lunch count
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            current_data = user_doc.to_dict()
            new_pts = current_data.get('pts', 0) + points
            new_lunches = current_data.get('no_lunches_today', 0) + 1
            
            user_ref.update({
                'pts': new_pts,
                'no_lunches_today': new_lunches
            })
            
            return {'success': True, 'new_points': new_pts, 'new_lunches': new_lunches}, None, None
        else:
            return None, {'error': 'User not found'}, 404
            
    except Exception as e:
        logger.error(f"Error adding meal: {str(e)}")
        return None, {'error': 'Failed to add meal'}, 500

def get_user_meals(user_id):
    """Get all meals for a specific user"""
    try:
        # Query meals collection for user's meals
        meals = db.collection('meals').where('userId', '==', user_id).get()
        
        # Convert to list of dictionaries
        meals_list = []
        for meal in meals:
            meal_data = meal.to_dict()
            meal_data['id'] = meal.id
            meals_list.append(meal_data)
            
        return meals_list, None, None
    except Exception as e:
        logger.error(f"Error getting user meals: {str(e)}")
        return None, {'error': 'Failed to get user meals'}, 500

def get_meals_by_date(user_id, date):
    """Get meals for a specific user on a specific date"""
    try:
        # Convert date to datetime range
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        
        # Query meals collection for user's meals on the specified date
        meals = db.collection('meals').where('userId', '==', user_id)\
            .where('date_taken', '>=', start_of_day)\
            .where('date_taken', '<=', end_of_day)\
            .get()
        
        # Convert to list of dictionaries
        meals_list = []
        for meal in meals:
            meal_data = meal.to_dict()
            meal_data['id'] = meal.id
            meals_list.append(meal_data)
            
        return meals_list, None, None
    except Exception as e:
        logger.error(f"Error getting meals by date: {str(e)}")
        return None, {'error': 'Failed to get meals by date'}, 500

def get_admin_data():
    """Get admin data from Firestore"""
    try:
        logger.debug("Attempting to get admin data")
        admin_doc = db.collection('admin').document('settings').get()
        
        if admin_doc.exists:
            logger.debug("Admin data found")
            admin_data = admin_doc.to_dict()
            logger.debug(f"Admin data: {admin_data}")
            return admin_data, None, None
        else:
            logger.debug("No admin data found, creating default settings")
            default_admin_data = {
                'lunch_tray_height': 0,
                'lunch_tray_length': 0
            }
            db.collection('admin').document('settings').set(default_admin_data)
            return default_admin_data, None, None
    except Exception as e:
        logger.error(f"Error getting admin data: {str(e)}")
        return None, {'error': 'Failed to get admin data'}, 500

def update_admin_data(lunch_tray_height, lunch_tray_length):
    """Update admin settings in Firestore"""
    try:
        logger.debug(f"Updating admin settings: height={lunch_tray_height}, length={lunch_tray_length}")
        admin_ref = db.collection('admin').document('settings')
        
        admin_ref.update({
            'lunch_tray_height': lunch_tray_height,
            'lunch_tray_length': lunch_tray_length
        })
        
        logger.debug("Admin settings updated successfully")
        return {'success': True}, None, None
    except Exception as e:
        logger.error(f"Error updating admin data: {str(e)}")
        return None, {'error': 'Failed to update admin data'}, 500

def get_all_users():
    """Get all users from Firestore"""
    try:
        logger.debug("Attempting to get all users")
        users_ref = db.collection('users')
        users = users_ref.get()
        
        users_list = []
        for user in users:
            user_data = user.to_dict()
            user_data['id'] = user.id
            users_list.append(user_data)
            
        logger.debug(f"Successfully retrieved {len(users_list)} users")
        return users_list, None, None
    except Exception as e:
        logger.error(f"Error getting all users: {str(e)}")
        return None, {'error': 'Failed to get users'}, 500

def generate_qr_code(user_id):
    """Generate QR code for a user using api.qrserver.com"""
    try:
        logger.debug(f"Generating QR code for user_id: {user_id}")
        
        # Create the URL that will be encoded in the QR code
        # This should be the URL where users can redeem their points
        redeem_url = f"https://noleftovers-rho.vercel.app/redeem/{user_id}"
        
        # Call the QR code API
        qr_api_url = "https://api.qrserver.com/v1/create-qr-code/"
        params = {
            'size': '200x200',  # QR code size
            'data': redeem_url,  # URL to encode
            'format': 'png'     # Output format
        }
        
        response = requests.get(qr_api_url, params=params)
        
        if response.status_code == 200:
            logger.debug("QR code generated successfully")
            return response.content, None, None
        else:
            logger.error(f"Failed to generate QR code: {response.status_code}")
            return None, {'error': 'Failed to generate QR code'}, 500
            
    except Exception as e:
        logger.error(f"Error generating QR code: {str(e)}")
        return None, {'error': 'Failed to generate QR code'}, 500

def verify_admin(admin_id):
    """Verify admin credentials using admin ID"""
    try:
        logger.debug(f"Verifying admin ID: {admin_id}")
        
        # Check if the admin ID matches the expected value
        if admin_id != 'nsd417':
            logger.debug("Invalid admin ID")
            return None, {'error': 'Invalid admin ID'}, 401
            
        # Return admin data without sensitive information
        admin_data = {
            'id': admin_id,
            'role': 'admin'
        }
        
        logger.debug("Admin ID verified successfully")
        return admin_data, None, None
        
    except Exception as e:
        logger.error(f"Error verifying admin ID: {str(e)}")
        return None, {'error': 'Failed to verify admin ID'}, 500 