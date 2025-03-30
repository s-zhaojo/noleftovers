import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Redeem.css';

const Redeem = () => {
  const [qrCodeUrl, setQrCodeUrl] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { setPoints } = location.state || {};  // Access setPoints passed from Dashboard
  const user = JSON.parse(localStorage.getItem('user'));
  
  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    fetchQrCode();
  }, [user, navigate]);

  const fetchQrCode = async () => {
    try {
      const response = await fetch(`https://noleftovers-backend.onrender.com/qr-code/${user.id}`, {
        headers: {
          'Authorization': `Bearer ${user.id}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch QR code');
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setQrCodeUrl(url);
    } catch (error) {
      console.error('Error fetching QR code:', error);
      setError('Failed to load QR code');
    }
  };

  // Function to update points
  const handlePointDeduction = (pointsToDeduct) => {
    if (setPoints) {
      setPoints((prevPoints) => prevPoints - pointsToDeduct);  // Deduct points and update Dashboard
    } else {
      // Update localStorage directly if setPoints is not available
      const currentPoints = parseInt(localStorage.getItem('points'), 10) || 0;
      const newPoints = currentPoints - pointsToDeduct;
      localStorage.setItem('points', newPoints);
      navigate('/dashboard');  // Navigate back to the dashboard after deduction
    }
  };

  const handleRedeemPoints = () => {
    // Your existing redeem points logic
  };

  const handleViewHistory = () => {
    navigate('/view-history');
  };

  return (
    <div className="redeem-container">
      <h2>Redeem Points</h2>
      {error && <div className="error-message">{error}</div>}
      
      {/* QR Code Section */}
      <div className="qr-code-section">
        <h3>Your QR Code</h3>
        {qrCodeUrl && (
          <img src={qrCodeUrl} alt="Your QR Code" className="qr-code-image" />
        )}
        <p className="qr-code-info">Show this QR code to redeem your points</p>
      </div>

      {/* Existing Buttons */}
      <div className="redeem-buttons">
        <button onClick={handleRedeemPoints} className="redeem-button">
          Redeem Points
        </button>
        <button onClick={handleViewHistory} className="history-button">
          View History
        </button>
      </div>
    </div>
  );
};

export default Redeem;
