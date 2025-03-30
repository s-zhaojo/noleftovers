import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const [user, setUser] = useState({
    pts: 0,
    name: 'User'
  });

  const navigate = useNavigate();

  useEffect(() => {
    // Fetch user data on component mount
    const fetchUserData = async () => {
      try {
        const response = await fetch('https://noleftovers-backend.onrender.com/get-user', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          }
        });
        const data = await response.json();
        if (data.success) {
          setUser(data.user);
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, []);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user.name || 'User'}!</h1>
        <p>Track your food waste reduction progress</p>
      </div>
      
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Total Points</h3>
          <div className="stat-value">{user.pts || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Lunches Bought Today</h3>
          <div className="stat-value">{user.no_lunches_today || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Photos Submitted Today</h3>
          <div className="stat-value">{user.no_of_submissions_today || 0}</div>
        </div>
      </div>

      <div className="dashboard-actions">
        <button className="action-button" onClick={() => navigate('/redeem')}>
          Redeem Points
        </button>
        <button className="action-button" onClick={() => navigate('/scan')}>
          Scan QR Code
        </button>
        <button className="action-button" onClick={() => navigate('/history')}>
          View History
        </button>
        <button className="action-button" onClick={() => navigate('/add-meal', { state: { setPoints } })}>
          Add Meal
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
