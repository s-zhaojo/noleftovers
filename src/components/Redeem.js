import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Redeem.css';

const Redeem = ({ user }) => {
  const [error, setError] = useState('');
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [selectedReward, setSelectedReward] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { setPoints } = location.state || {};

  const rewards = [
    {
      id: 'free_lunch',
      name: 'Free Lunch',
      points: 1000,
      description: 'Redeem for a free lunch'
    },
    {
      id: 'free_snack',
      name: '$1 Snack',
      points: 500,
      description: 'Redeem for a $1 snack'
    }
  ];

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }
  }, [user, navigate]);

  const handleRedeem = async (reward) => {
    try {
      const response = await fetch('https://noleftovers-backend.onrender.com/redeem-points', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.id,
          points: -reward.points // Negative value to deduct points
        })
      });

      if (!response.ok) {
        throw new Error('Failed to redeem points');
      }

      // Update local points
      if (setPoints) {
        setPoints(prev => prev - reward.points);
      } else {
        const currentPoints = parseInt(localStorage.getItem('points'), 10) || 0;
        localStorage.setItem('points', currentPoints - reward.points);
      }

      // Show success message and redirect
      alert(`Successfully redeemed ${reward.name}!`);
      navigate('/dashboard');
    } catch (error) {
      console.error('Error redeeming points:', error);
      setError('Failed to redeem points. Please try again.');
    }
  };

  const handleRewardClick = (reward) => {
    setSelectedReward(reward);
    setShowConfirmation(true);
  };

  const handleConfirmRedeem = () => {
    handleRedeem(selectedReward);
    setShowConfirmation(false);
  };

  const handleCancelRedeem = () => {
    setShowConfirmation(false);
    setSelectedReward(null);
  };

  return (
    <div className="redeem-container">
      <h2>Redeem Points</h2>
      {error && <div className="error-message">{error}</div>}
      
      <div className="rewards-grid">
        {rewards.map(reward => (
          <div 
            key={reward.id} 
            className={`reward-card ${user.points < reward.points ? 'disabled' : ''}`}
            onClick={() => user.points >= reward.points && handleRewardClick(reward)}
          >
            <h3>{reward.name}</h3>
            <p className="points-required">{reward.points} points</p>
            <p className="description">{reward.description}</p>
            {user.points < reward.points && (
              <p className="insufficient-points">
                Need {reward.points - user.points} more points
              </p>
            )}
          </div>
        ))}
      </div>

      {showConfirmation && selectedReward && (
        <div className="confirmation-modal">
          <div className="confirmation-content">
            <h3>Confirm Redemption</h3>
            <p>Are you sure you want to redeem {selectedReward.points} points for {selectedReward.name}?</p>
            <div className="confirmation-buttons">
              <button onClick={handleConfirmRedeem} className="confirm-button">
                Yes, Redeem
              </button>
              <button onClick={handleCancelRedeem} className="cancel-button">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="redeem-buttons">
        <button onClick={() => navigate('/dashboard')} className="nav-button">
          Back to Dashboard
        </button>
      </div>
    </div>
  );
};

export default Redeem;
