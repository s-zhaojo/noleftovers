import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Redeem from './components/Redeem';
import Scan from './components/Scan';
import ViewHistory from './components/ViewHistory';
import AddMeal from './components/AddMeal';
import './App.css';

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
        <div className="title-container">
          <img 
            src="https://no-leftovers.com/assets/logos/NLO-Main-Logo-300.png" 
            alt="No Leftovers Logo" 
            className="title-image" 
          />
        </div>

        <Routes>
          <Route path="/" element={<Login onLogin={handleLogin} />} />
          <Route 
            path="/add-meal" 
            element={<AddMeal user={user} />} 
          />
          <Route 
            path="/dashboard" 
            element={user ? <Dashboard user={user} /> : <Navigate to="/" />} 
          />
          <Route 
            path="/redeem" 
            element={user ? <Redeem /> : <Navigate to="/" />} 
          />
          <Route 
            path="/scan" 
            element={user ? <Scan user={user} /> : <Navigate to="/" />} 
          />
          <Route 
            path="/history" 
            element={user ? <ViewHistory /> : <Navigate to="/" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
