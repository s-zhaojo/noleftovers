from firebase_admin import firestore
from models import User
from datetime import datetime
import logging
from firebase_init import db

logger = logging.getLogger(__name__)

def get_user_data(user_id):
    """Get user data from Firestore"""
    try:
        # Use the correct structure: nsd417 -> users -> [user_id]
        user_doc = db.collection('nsd417').collection('users').document(user_id).get()
        
        if user_doc.exists:
            print(f"User data found for: {user_id}")
            print(user_doc.to_dict())
            return user_doc.to_dict(), None, None
        else:
            print(f"Creating new user document for: {user_id}")
            default_user_data = {
                'name': '',
                'no_lunches_today': 0,
                'no_of_submissions_today': 0,
                'pts': 0
            }
            
            db.collection('nsd417').collection('users').document(user_id).set(default_user_data)
            return default_user_data, None, None
    except Exception as e:
        logger.error(f"Error getting user data: {str(e)}")
        return None, {'error': 'Failed to get user data'}, 500

def update_user_data(user_id, data):
    """Update user data in Firestore"""
    try:
        user_ref = db.collection('nsd417').collection('users').document(user_id)
        
        update_data = {
            **data,
            'lastUpdated': datetime.now().isoformat()
        }
        
        user_ref.update(update_data)
        logger.info(f"Successfully updated user data for: {user_id}")
        
        # Return updated user data
        updated_doc = user_ref.get()
        return updated_doc.to_dict(), None, None
    except Exception as e:
        logger.error(f"Error updating user data: {str(e)}")
        return None, {'error': 'Failed to update user data'}, 500

def create_user_object(user_id, user_data):
    """Create a User object from Firestore data"""
    try:
        # Map Firestore data to User object fields with correct field names
        user = User(
            uuid=user_id,
            name=user_data.get('name', ''),
            points=user_data.get('pts', 0),
            no_of_lunches_today=user_data.get('no_lunches_today', 0),
            no_of_submissions_today=user_data.get('no_of_submissions_today', 0)
        )
        print(user.to_dict())
        return user.to_dict(), None, None
    except Exception as e:
        logger.error(f"Error creating user object: {str(e)}")
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
        db.collection('nsd417').collection('meals').add(meal_data)
        
        # Update user's points and lunch count
        user_ref = db.collection('nsd417').collection('users').document(user_id)
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
        meals = db.collection('nsd417').collection('meals').where('userId', '==', user_id).get()
        
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
        meals = db.collection('nsd417').collection('meals').where('userId', '==', user_id)\
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