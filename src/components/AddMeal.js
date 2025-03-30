import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './AddMeal.css';

const AddMeal = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { setPoints } = location.state || {};  // Access setPoints passed from Dashboard
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePointAddition = (pointsToAdd) => {
    if (setPoints) {
      // Add points and update Dashboard through the setPoints function
      setPoints((prevPoints) => prevPoints + pointsToAdd);
    } else {
      // If setPoints is not available, use localStorage to persist the points
      const currentPoints = parseInt(localStorage.getItem('points'), 10) || 0;
      const newPoints = currentPoints + pointsToAdd;
      localStorage.setItem('points', newPoints);
    }
  };

  const handleAddMeal = async () => {
    setLoading(true);
    setError(null);

    const testData = {
      // Data structure similar to what you'd send to the backend
      user_id: "123",  // Replace with actual user ID
      date_taken: new Date().toISOString().split('T')[0],
      pts: 10,  // Adding 10 points
    };

    console.log('Sending test data:', testData);  // Debug log

    try {
      const response = await fetch('https://noleftovers-backend.onrender.com/add-meal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(testData)
      });

      const data = await response.json();
      console.log('Response data:', data);  // Debug log

      if (!response.ok) throw new Error(data.error || 'Failed to add meal');
      
      alert('Meal added successfully!');
      handlePointAddition(10);  // Add 10 points to the user after adding meal
      navigate('/dashboard');
    } catch (err) {
      console.error('Error:', err);  // Debug log
      setError(err.message);
      alert('Error adding meal: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-meal-container">
      <h1>Add Meal</h1>
      <div className="meal-info">
        <p>User ID: 123</p>
        <p>Date: {new Date().toISOString().split('T')[0]}</p>
        <p>Points to add: 10</p>
      </div>
      {error && <div className="error-message">{error}</div>}
      <button 
        onClick={handleAddMeal} 
        className="submit-button"
        disabled={loading}
      >
        {loading ? 'Adding Meal...' : 'Add Meal'}
      </button>
      <button onClick={() => navigate('/dashboard')} className="back-button">
        Back to Dashboard
      </button>
    </div>
  );
};

export default AddMeal;
