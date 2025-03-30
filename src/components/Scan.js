import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Scan.css';

const Scan = ({ user }) => {
  const navigate = useNavigate();

  const handleAddMeal = async () => {
    try {
      const response = await fetch('https://noleftovers-backend.onrender.com/add-meal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          user_id: user.id,
          date_taken: new Date().toISOString().split('T')[0],
          pts: 10  // Test points value
        })
      });

      if (!response.ok) throw new Error('Failed to add meal');
      alert('Meal added successfully!');
    } catch (err) {
      alert('Error adding meal: ' + err.message);
    }
  };

  return (
    <div>
      <div className="add-meal">
        <h1>Add Meal</h1>
        <button onClick={handleAddMeal} className="add-meal-button">
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
