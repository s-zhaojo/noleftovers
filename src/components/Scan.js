import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Scan.css';

const Scan = () => {
  const navigate = useNavigate();

  return (
    <div className="scan-container">
      <h1>Scan QR Code</h1>
      <button onClick={() => navigate('/dashboard')} className="back-button">
        Back to Dashboard
      </button>
    </div>
  );
};

export default Scan; 