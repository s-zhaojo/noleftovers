import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Redeem.css';

const Redeem = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { setPoints } = location.state || {};  // Access setPoints passed from Dashboard
  
  const handlePointDeduction = (pointsToDeduct) => {
    if (setPoints) {
      setPoints((prevPoints) => prevPoints - pointsToDeduct);  // Deduct points and update Dashboard
    }
  };

  return (
    <div className="redeem-container">
      <h1>Redeem Points</h1>
      <button onClick={() => navigate('/dashboard')} className="back-button">
        Back to Dashboard
      </button>
      
      <div className="redeem-items">
        <div className="redeem-item">
          <button className="action-button" onClick={() => navigate('/dashboard')}>
            <img 
              src="https://m.media-amazon.com/images/I/71zK01gJfML.jpg" 
              alt="Fruit Snack" 
              className="redeem-image" 
            />
          </button>
          <p className="points-tag">500 Points</p>
        </div>
        <div className="redeem-item">
          <button className="action-button" onClick={() => navigate('/dashboard')}>
            <img 
              src="https://live.staticflickr.com/65535/52765596162_1bee372f32_h.jpg" 
              alt="Lunch Tray" 
              className="redeem-image" 
            />
          </button>
          <p className="points-tag">1000 Points</p>
        </div>
      </div>
    </div>
  );
};

export default Redeem;
