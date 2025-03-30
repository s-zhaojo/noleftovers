import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAuth } from 'firebase/auth';
const auth = getAuth();
import { signInWithEmailAndPassword } from 'firebase/auth';
import { getFirestore, doc, getDoc } from 'firebase/firestore';
import './Login.css';

const AdminLogin = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const db = getFirestore();

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // Sign in with Firebase Auth
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      // Check if user is admin in Firestore
      const adminDoc = await getDoc(doc(db, 'admin', user.uid));
      
      if (!adminDoc.exists()) {
        setError('Unauthorized: Admin access required');
        return;
      }

      // Get admin data
      const adminData = adminDoc.data();
      
      // Store admin data in localStorage
      localStorage.setItem('adminData', JSON.stringify({
        id: user.uid,
        email: user.email,
        ...adminData
      }));

      // Navigate to admin dashboard
      navigate('/admin/dashboard');
    } catch (error) {
      console.error('Admin login error:', error);
      setError('Failed to login as admin');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Admin Login</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleAdminLogin}>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Login as Admin</button>
        </form>
      </div>
    </div>
  );
};

export default AdminLogin; 