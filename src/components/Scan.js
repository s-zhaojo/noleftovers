import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Scan.css';

const Scan = ({ user }) => {
  const navigate = useNavigate();

  return (
    <div>
      <div className="add-meal">
        <h1>Add Meal</h1>
        <button onClick={() => navigate('/add-meal')} className="add-meal-button">
          Add Test Meal
        </button>
      </div>

      <div className="return">
        <h1>Return To Dashboard</h1>
        <button onClick={() => navigate('/dashboard')} className="back-button">
          Back to Dashboard
        </button>
      </div>
    </div>
  );
};

export default Scan; 
