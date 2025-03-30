import { db } from '../firebase';
import { 
  doc, 
  getDoc, 
  setDoc, 
  updateDoc, 
  collection,
  query,
  where,
  getDocs
} from 'firebase/firestore';

// Get user data
export const getUserData = async (userId) => {
  try {
    const userDoc = await getDoc(doc(db, 'users', userId));
    
    if (userDoc.exists()) {
      return userDoc.data();
    } else {
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
      return defaultUserData;
    }
  } catch (error) {
    console.error('Error getting user data:', error);
    throw error;
  }
};

// Update user data
export const updateUserData = async (userId, data) => {
  try {
    const userRef = doc(db, 'users', userId);
    await updateDoc(userRef, {
      ...data,
      lastUpdated: new Date().toISOString()
    });
    return await getUserData(userId);
  } catch (error) {
    console.error('Error updating user data:', error);
    throw error;
  }
};

// Get user by email
export const getUserByEmail = async (email) => {
  try {
    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('email', '==', email));
    const querySnapshot = await getDocs(q);
    
    if (!querySnapshot.empty) {
      const userDoc = querySnapshot.docs[0];
      return { id: userDoc.id, ...userDoc.data() };
    }
    return null;
  } catch (error) {
    console.error('Error getting user by email:', error);
    throw error;
  }
}; 