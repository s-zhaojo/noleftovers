import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    console.log('Attempting login with:', { email });

    try {
      console.log('Sending request to backend...');
      const response = await fetch('https://noleftovers-backend.onrender.com/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        mode: 'cors',
        credentials: 'include'
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Full response data:', JSON.stringify(data, null, 2));

      if (!response.ok) {
        throw new Error(data.message || 'Login failed');
      }

      // Transform the response data into the expected user object structure
      const userData = {
        id: data.uuid,
        name: data.name || email.split('@')[0],
        points: data.points || 0,
        no_lunches_today: data.no_of_lunches_today || 0,
        no_of_submissions_today: data.no_of_submissions_today || 0
      };

      // Store the token (if provided)
      if (data.token) {
        localStorage.setItem('token', data.token);
        console.log('Token stored in localStorage');
      }
      
      // Call the onLogin callback with user data
      console.log('Calling onLogin with user data:', userData);
      onLogin(userData);
      
      // Navigate to dashboard
      console.log('Navigating to dashboard...');
      navigate('/dashboard');
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Welcome Back</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login; 