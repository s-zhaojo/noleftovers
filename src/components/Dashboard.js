import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const [points, setPoints] = useState(() => {
    // Try getting the points from localStorage first
    const savedPoints = localStorage.getItem('points');
    return savedPoints ? parseInt(savedPoints, 10) : user.pts || 0;
  });
  const navigate = useNavigate();

  useEffect(() => {
    // Save points to localStorage whenever it changes
    localStorage.setItem('points', points);
  }, [points]);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user.name || 'User'}!</h1>
        <p>Track your food waste reduction progress</p>
      </div>
      
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Total Points</h3>
          <div className="stat-value">{points}</div>
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
          Scan 
        </button>
        <button className="action-button" onClick={() => navigate('/history')}>
          View History
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
