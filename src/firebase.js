import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore, connectFirestoreEmulator } from 'firebase/firestore';

// Your web app's Firebase configuration
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
export const auth = getAuth(app);
export const db = getFirestore(app);

// Log successful initialization
console.log('Firebase initialized successfully');
console.log('Project ID:', firebaseConfig.projectId);

export default app; 