import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = ({ user }) => {
  const navigate = useNavigate();

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user.name || 'User'}!</h1>
        <p>Track your food waste reduction progress</p>
      </div>
      
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Total Points</h3>
          <div className="stat-value">{user.points || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Lunches Bought Today</h3>
          <div className="stat-value">{user.lunchesBought || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Photos Submitted Today</h3>
          <div className="stat-value">{user.photosSubmitted || 0}</div>
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
      </div>
    </div>
  );
};

export default Dashboard; 