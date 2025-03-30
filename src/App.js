import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
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
          <h1 className="title">No Leftovers</h1>
        </div>
        
        

        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route 
            path="/dashboard" 
            element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} 
          />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
        {/* Profile in the top right */}
        <div className="profile-card">
          <img 
            src="https://t3.ftcdn.net/jpg/00/77/71/12/360_F_77711294_BA5QTjtgGPmLKCXGdtbAgZciL4kEwCnx.jpg" 
            alt="John" 
            className="profile-img"
          />
          <h1>John Doe</h1>
          <p className="title">1766546</p>
          <p>Points: 400</p>
          <p>Number of times bought lunch: 14</p>
          <p>Number of times submitted photo: 14</p>
          <div className="social-links">
            <button className="social-button"><i className="fa fa-dribbble"></i></button>
            <button className="social-button"><i className="fa fa-twitter"></i></button>
            <button className="social-button"><i className="fa fa-linkedin"></i></button>
            <button className="social-button"><i className="fa fa-facebook"></i></button>
          </div>
          <p><button>Contact</button></p>
        </div>
      </div>
    </Router>
  );
}

export default App;
