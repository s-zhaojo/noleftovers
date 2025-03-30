from firebase_admin import firestore
from models import User
from datetime import datetime
import logging
from firebase_init import db

logger = logging.getLogger(__name__)

def get_user_data(user_id):
    """Get user data from Firestore"""
    try:
        user_doc = db.collection('users').document(user_id).get()
        
        if user_doc.exists:
            logger.info(f"User data found for: {user_id}")
            return user_doc.to_dict(), None, None
        else:
            logger.info(f"Creating new user document for: {user_id}")
            default_user_data = {
                'email': '',
                'points': 0,
                'lunchesBought': 0,
                'photosSubmitted': 0,
                'createdAt': datetime.now().isoformat(),
                'lastUpdated': datetime.now().isoformat()
            }
            
            db.collection('users').document(user_id).set(default_user_data)
            return default_user_data, None, None
    except Exception as e:
        logger.error(f"Error getting user data: {str(e)}")
        return None, {'error': 'Failed to get user data'}, 500

def update_user_data(user_id, data):
    """Update user data in Firestore"""
    try:
        user_ref = db.collection('users').document(user_id)
        
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
        # Map Firestore data to User object fields
        user = User(
            uuid=user_id,
            name=user_data.get('name', ''),
            points=user_data.get('points', 0),
            no_of_lunches_today=user_data.get('lunchesBought', 0),
            no_of_submissions_today=user_data.get('photosSubmitted', 0)
        )
        return user.to_dict(), None, None
    except Exception as e:
        logger.error(f"Error creating user object: {str(e)}")
        return None, {'error': 'Failed to create user object'}, 500 