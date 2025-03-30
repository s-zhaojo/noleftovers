import { db } from '../firebase';
import { 
  doc, 
  getDoc, 
  setDoc, 
  updateDoc, 
  collection,
  query,
  where,
  getDocs,
  enableNetwork,
  disableNetwork
} from 'firebase/firestore';

// Ensure we're online before making Firestore calls
const ensureOnline = async () => {
  try {
    await enableNetwork(db);
  } catch (error) {
    console.error('Error enabling network:', error);
  }
};

// Get user data
export const getUserData = async (userId) => {
  try {
    console.log('Attempting to get user data for:', userId);
    const userDoc = await getDoc(doc(db, 'users', userId));
    
    if (userDoc.exists()) {
      console.log('User data found:', userDoc.data());
      return userDoc.data();
    } else {
      console.log('Creating new user document for:', userId);
      // If user doesn't exist, create a new user document
      const defaultUserData = {
        email: '',
        points: 0,
        lunchesBought: 0,
        photosSubmitted: 0,
        createdAt: new Date().toISOString(),
        lastUpdated: new Date().toISOString()
      };
      
      await setDoc(doc(db, 'users', userId), defaultUserData);
      console.log('Created new user document with default data');
      return defaultUserData;
    }
  } catch (error) {
    console.error('Error in getUserData:', error);
    console.error('Error code:', error.code);
    console.error('Error message:', error.message);
    throw error;
  }
};

// Update user data
export const updateUserData = async (userId, data) => {
  try {
    console.log('Attempting to update user data for:', userId);
    const userRef = doc(db, 'users', userId);
    await updateDoc(userRef, {
      ...data,
      lastUpdated: new Date().toISOString()
    });
    console.log('Successfully updated user data');
    return await getUserData(userId);
  } catch (error) {
    console.error('Error in updateUserData:', error);
    console.error('Error code:', error.code);
    console.error('Error message:', error.message);
    throw error;
  }
};

// Get user by email
export const getUserByEmail = async (email) => {
  try {
    console.log('Attempting to get user by email:', email);
    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('email', '==', email));
    const querySnapshot = await getDocs(q);
    
    if (!querySnapshot.empty) {
      const userDoc = querySnapshot.docs[0];
      console.log('Found user by email:', userDoc.data());
      return { id: userDoc.id, ...userDoc.data() };
    }
    console.log('No user found with email:', email);
    return null;
  } catch (error) {
    console.error('Error in getUserByEmail:', error);
    console.error('Error code:', error.code);
    console.error('Error message:', error.message);
    throw error;
  }
}; 