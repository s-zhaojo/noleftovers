import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Scan.css';

const Scan = ({ user }) => {
  const [points, setPoints] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { setPoints: setParentPoints } = location.state || {};

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    try {
      const response = await fetch('https://noleftovers-backend.onrender.com/update-points', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          points: parseInt(points),
          password: password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to update points');
      }

      setSuccess('Points updated successfully!');
      setPoints('');
      setPassword('');
      
      // Update points in parent component if available
      if (setParentPoints) {
        setParentPoints(data.new_points);
      } else {
        // Update localStorage if parent component is not available
        localStorage.setItem('points', data.new_points);
      }
      
    } catch (err) {
      console.error('Error updating points:', err);
      setError(err.message || 'Failed to update points. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="scan-container">
      <h2>Award Points</h2>
      <div className="scan-content">
        <form onSubmit={handleSubmit} className="points-form">
          <div className="form-group">
            <label>Number of Points:</label>
            <input
              type="number"
              value={points}
              onChange={(e) => setPoints(e.target.value)}
              required
              min="0"
              placeholder="Enter points to award"
            />
          </div>
          <div className="form-group">
            <label>Teacher Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter teacher password"
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}
          <button 
            type="submit" 
            className="submit-button"
            disabled={isLoading}
          >
            {isLoading ? 'Updating...' : 'Award Points'}
          </button>
        </form>
        <div className="button-container">
          <button onClick={() => navigate('/dashboard')} className="nav-button">
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
};

export default Scan; 
