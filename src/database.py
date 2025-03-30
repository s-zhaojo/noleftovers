from firebase_admin import firestore
from models.User import User
from datetime import datetime
import logging
from firebase_init import db

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