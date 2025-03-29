import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <div className="title-container">
          <img 
            src="https://no-leftovers.com/assets/logos/NLO-Main-Logo-300.png" 
            alt="No Leftovers Logo" 
            className="title-image" 
          />
          <h1 className="title">No Leftovers</h1>
          <link rel="stylesheet" href="https://supportrenewalshelp.oracle.com/app/answers/detail/a_id/1246/~/pending-page?">
          <div class="card">
          <img src="https://t3.ftcdn.net/jpg/00/77/71/12/360_F_77711294_BA5QTjtgGPmLKCXGdtbAgZciL4kEwCnx.jpg" alt="John" style="width:100%">
          <h1>John Doe</h1>
          <p class="title">CEO & Founder, Example</p>
          <p>Harvard University</p>
          <a href="#"><i class="fa fa-dribbble"></i></a>
          <a href="#"><i class="fa fa-twitter"></i></a>
          <a href="#"><i class="fa fa-linkedin"></i></a>
          <a href="#"><i class="fa fa-facebook"></i></a>
          <p><button>Contact</button></p>
</div>
        </div>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
          {/* Add more routes as needed */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
