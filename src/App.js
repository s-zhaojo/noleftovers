import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import './App.css';

// Login Component (Simple Example)
const Login = ({ onLogin }) => {
  const handleLogin = () => {
    const userData = {
      name: 'John Doe',
      id: '1766546',
      points: 400,
      lunchCount: 14,
      photoCount: 14
    };
    // Simulate login and store user data in the app state
    onLogin(userData);
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <button onClick={handleLogin}>Login as John Doe</button>
    </div>
  );
};

// Dashboard Component
const Dashboard = ({ user }) => {
  return (
    <div className="dashboard-container">
      {/* Title and logo */}
      <div className="title-container">
        <img 
          src="https://no-leftovers.com/assets/logos/NLO-Main-Logo-300.png" 
          alt="No Leftovers Logo" 
          className="title-image" 
        />
        <h1 className="title">No Leftovers</h1>
      </div>

      {/* Profile card */}
      <div className="profile-card">
        <img 
          src="https://t3.ftcdn.net/jpg/00/77/71/12/360_F_77711294_BA5QTjtgGPmLKCXGdtbAgZciL4kEwCnx.jpg" 
          alt="John" 
          className="profile-img"
        />
        <h1>{user.name}</h1>
        <p className="title">{user.id}</p>
        <p>Points: {user.points}</p>
        <p>Number of times bought lunch: {user.lunchCount}</p>
        <p>Number of times submitted photo: {user.photoCount}</p>
        <div className="social-links">
          <button className="social-button"><i className="fa fa-dribbble"></i></button>
          <button className="social-button"><i className="fa fa-twitter"></i></button>
          <button className="social-button"><i className="fa fa-linkedin"></i></button>
          <button className="social-button"><i className="fa fa-facebook"></i></button>
        </div>
        <p><button>Contact</button></p>
      </div>

      {/* Buttons section */}
      <div className="button-container">
        <Link to="/history">
          <button className="nav-button">View History</button>
        </Link>
        <Link to="/scan">
          <button className="nav-button">Scan</button>
        </Link>
        <Link to="/redeem">
          <button className="nav-button">Redeem</button>
        </Link>
      </div>
    </div>
  );
};

const Redeem = () => <div>Redeem Page</div>;
const Scan = () => <div>Scan Page</div>;
const ViewHistory = () => <div>History Page</div>;

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check for existing token on app load
    const token = localStorage.getItem('token');
    if (token) {
      console.log('Found existing token, verifying...');
      verifyToken(token);
    }
  }, []);

  const verifyToken = async (token) => {
    try {
      const response = await fetch('https://noleftovers-backend.onrender.com/verify-token', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Token verified, setting user:', data);
        setUser(data);
      } else {
        console.log('Token verification failed');
        localStorage.removeItem('token');
      }
    } catch (error) {
      console.error('Token verification error:', error);
      localStorage.removeItem('token');
    }
  };

  const handleLogin = (userData) => {
    console.log('App: handleLogin called with:', userData);
    setUser(userData);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route 
            path="/dashboard" 
            element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/redeem" 
            element={user ? <Redeem /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/scan" 
            element={user ? <Scan /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/history" 
            element={user ? <ViewHistory /> : <Navigate to="/login" />} 
          />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
