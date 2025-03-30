import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Scan.css';

const Scan = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [points, setPoints] = useState(null);
  const navigate = useNavigate();

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError('');
      setPoints(null);
    }
  };

  const calculatePoints = (volume) => {
    // Points calculation logic:
    // - If volume is 0 (empty plate): +50 points
    // - If volume is low (little food): -10 points
    // - If volume is medium (some food): -25 points
    // - If volume is high (lots of food): -40 points
    if (volume === 0) return 50;
    if (volume < 0.3) return -10;
    if (volume < 0.6) return -25;
    return -40;
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setIsAnalyzing(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('image', selectedImage);

      // Send image to ML model endpoint
      const response = await fetch('https://noleftovers-backend.onrender.com/analyze-food', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      setPoints(data.points);

      // Store the result in localStorage for the redeem page
      localStorage.setItem('scanResult', JSON.stringify({
        points: data.points,
        volume: data.volume,
        message: data.message,
        timestamp: new Date().toISOString()
      }));

    } catch (error) {
      console.error('Analysis error:', error);
      setError('Failed to analyze image. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRedeem = () => {
    if (points !== null) {
      navigate('/redeem');
    }
  };

  return (
    <div className="scan-container">
      <h2>Scan Your Plate</h2>
      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          className="file-input"
          id="image-upload"
        />
        <label htmlFor="image-upload" className="upload-button">
          Choose Image
        </label>
      </div>

      {previewUrl && (
        <div className="preview-section">
          <img src={previewUrl} alt="Preview" className="preview-image" />
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      <div className="action-buttons">
        <button
          onClick={handleAnalyze}
          disabled={!selectedImage || isAnalyzing}
          className="analyze-button"
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Plate'}
        </button>

        {points !== null && (
          <button onClick={handleRedeem} className="redeem-button">
            Redeem Points ({points})
          </button>
        )}
      </div>

      {points !== null && (
        <div className="result-section">
          <h3>Analysis Result</h3>
          <p>Points: {points}</p>
          <p className="points-explanation">
            {JSON.parse(localStorage.getItem('scanResult')).message}
          </p>
        </div>
      )}
    </div>
  );
};

export default Scan; 
