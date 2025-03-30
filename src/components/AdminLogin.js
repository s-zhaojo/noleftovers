import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const AdminLogin = () => {
  const [adminId, setAdminId] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('https://noleftovers-backend.onrender.com/admin/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ admin_id: adminId }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to login as admin');
      }

      // Store admin data in localStorage
      localStorage.setItem('adminData', JSON.stringify(data));
      
      // Navigate to admin dashboard
      navigate('/admin/dashboard');
    } catch (error) {
      console.error('Admin login error:', error);
      setError(error.message || 'Failed to login as admin');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Admin Login</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleAdminLogin}>
          <div className="form-group">
            <label>Admin ID:</label>
            <input
              type="text"
              value={adminId}
              onChange={(e) => setAdminId(e.target.value)}
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