import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Redeem.css';

const Redeem = () => {
  const navigate = useNavigate();

  return (
    <div className="redeem-container">
      <h1>Redeem Points</h1>
      <button onClick={() => navigate('/dashboard')} className="back-button">
        Back to Dashboard
      </button>
    </div>
  );
};

export default Redeem; 