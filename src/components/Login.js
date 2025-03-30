import React, { useState } from 'react';
import { auth } from '../firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';
import { getUserData } from '../services/userService';
import './Login.css';

// Log environment variables
console.log('Environment variables:', {
  REACT_APP_BACKEND_URL: process.env.REACT_APP_BACKEND_URL,
  NODE_ENV: process.env.NODE_ENV
});

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      // First authenticate with Firebase
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const token = await userCredential.user.getIdToken();
      console.log('Firebase auth successful, got token');

      // Temporarily hardcode the backend URL for testing
      const backendUrl = 'https://noleftovers-backend.onrender.com';
      console.log('Using backend URL:', backendUrl);
      
      // Send token to backend for verification
      const response = await fetch(`${backendUrl}/verify-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json'
        },
        mode: 'cors',
        credentials: 'include'
      });

      console.log('Backend response status:', response.status);
      console.log('Backend response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Backend error response:', errorData);
        throw new Error(errorData.error || 'Authentication failed');
      }

      const data = await response.json();
      console.log('Login successful:', data);
      
      // Get user data from Firestore
      const userData = await getUserData(data.uid);
      
      // Store user data in localStorage
      localStorage.setItem('user', JSON.stringify({
        ...data,
        ...userData
      }));
      
      // Navigate to dashboard
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      if (error.code === 'auth/user-not-found' || error.code === 'auth/wrong-password') {
        setError('Invalid email or password');
      } else if (error.message === 'Failed to fetch') {
        console.error('Network error details:', error);
        setError('Unable to connect to server. Please check your internet connection.');
      } else {
        setError(error.message || 'An error occurred during login');
      }
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin} className="login-form">
        <h2>Login</h2>
        {error && <p className="error">{error}</p>}
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="Enter your email"
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Enter your password"
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login; 