import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    // Handle login logic here
    console.log('Login', username, password);
  };

  return (
    <Router>
      <div className="App">
        <div className="header">
          <img 
            src="https://no-leftovers.com/assets/logos/NLO-Main-Logo-300.png" 
            alt="No Leftovers Logo" 
            className="logo" 
          />
          <h1 className="title">No Leftovers</h1>
        </div>

        {/* Profile in the top right */}
        <div className="profile-card">
          <img 
            src="https://t3.ftcdn.net/jpg/00/77/71/12/360_F_77711294_BA5QTjtgGPmLKCXGdtbAgZciL4kEwCnx.jpg" 
            alt="John" 
            className="profile-img"
          />
          <h1>John Doe</h1>
          <p className="title">CEO & Founder, Example</p>
          <p>Harvard University</p>
          <div className="social-links">
            <a href="#"><i className="fa fa-dribbble"></i></a>
            <a href="#"><i className="fa fa-twitter"></i></a>
            <a href="#"><i className="fa fa-linkedin"></i></a>
            <a href="#"><i className="fa fa-facebook"></i></a>
          </div>
        </div>

        <div className="login-container">
          <form onSubmit={handleLogin} className="login-form">
            <h2>Sign In</h2>
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit" className="login-button">Log In</button>
            <div className="signup-link">
              <p>Don't have an account? <a href="#">Sign Up</a></p>
            </div>
          </form>
        </div>

        <Routes>
          {/* Add routes for login or other pages here */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
