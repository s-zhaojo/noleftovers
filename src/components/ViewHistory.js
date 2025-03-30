import React from 'react';
import { useNavigate } from 'react-router-dom';
import './ViewHistory.css';

const ViewHistory = () => {
  const navigate = useNavigate();

  return (
    <div className="history-container">
      <h1>View History</h1>
      <button onClick={() => navigate('/dashboard')} className="back-button">
        Back to Dashboard
      </button>
    </div>
  );
};

export default ViewHistory; 