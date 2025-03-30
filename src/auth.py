from firebase_admin import auth
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def verify_token(request):
    """Verify Firebase ID token from request header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning('No token provided')
        return None, jsonify({'error': 'Authorization header missing or invalid'}), 401
    
    token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid'], None, None
    except auth.InvalidIdTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        return None, jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None, jsonify({'error': 'Authentication failed'}), 401

def login_user(email, password):
    """Authenticate user with email and password"""
    try:
        if not email or not password:
            return None, jsonify({'error': 'Email and password are required'}), 400

        # Sign in with email and password using Firebase Admin SDK
        user = auth.get_user_by_email(email)
        
        return {
            'userId': user.uid,
            'email': user.email
        }, None, None

    except auth.UserNotFoundError:
        return None, jsonify({'error': 'User not found'}), 404
    except auth.InvalidPasswordError:
        return None, jsonify({'error': 'Invalid password'}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return None, jsonify({'error': 'Authentication failed'}), 401 