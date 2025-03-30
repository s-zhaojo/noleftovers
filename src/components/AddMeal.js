import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AddMeal.css';

const AddMeal = ({ user }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAddMeal = async () => {
    setLoading(true);
    setError(null);
    
    const testData = {
      user_id: user.id,
      date_taken: new Date().toISOString().split('T')[0],
      pts: 10
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
      <h1>Add Test Meal</h1>
      <div className="meal-info">
        <p>User ID: {user.id}</p>
        <p>Date: {new Date().toISOString().split('T')[0]}</p>
        <p>Points to add: 10</p>
      </div>
      {error && <div className="error-message">{error}</div>}
      <button 
        onClick={handleAddMeal} 
        className="submit-button"
        disabled={loading}
      >
        {loading ? 'Adding Meal...' : 'Add Test Meal'}
      </button>
      <button onClick={() => navigate('/dashboard')} className="back-button">
        Back to Dashboard
      </button>
    </div>
  );
};

export default AddMeal;

