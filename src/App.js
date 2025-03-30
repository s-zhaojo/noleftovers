import { BrowserRouter as Router, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import Login from './Login'; // Make sure you have a Login component
import Dashboard from './Dashboard'; // Make sure you have a Dashboard component
import Submit from './Submit'; // Make sure you have a Submit component
import History from './History'; // Make sure you have a History component
import Redeem from './Redeem'; // Make sure you have a Redeem component

function App() {
  const location = useLocation();

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
        </div>
        
        {/* Define your routes */}
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/submit" element={<Submit />} />
          <Route path="/history" element={<History />} />
          <Route path="/redeem" element={<Redeem />} />
          {/* Redirect to login if the path doesn't match any of the above */}
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>

        {/* Profile in the top right, conditionally render on all routes except /login */}
        {location.pathname !== '/login' && (
          <div className="profile-card">
            <img 
              src="https://t3.ftcdn.net/jpg/00/77/71/12/360_F_77711294_BA5QTjtgGPmLKCXGdtbAgZciL4kEwCnx.jpg" 
              alt="John" 
              className="profile-img"
            />
            <h1>John Doe</h1>
            <p className="title">1766546</p>
            <p>Points: 400</p>
            <p>Number of times bought lunch: 14</p>
            <p>Number of times submitted photo: 14</p>
            <div className="social-links">
              <a href="#"><i className="fa fa-dribbble"></i></a>
              <a href="#"><i className="fa fa-twitter"></i></a>
              <a href="#"><i className="fa fa-linkedin"></i></a>
              <a href="#"><i className="fa fa-facebook"></i></a>
            </div>
            <p><button>Contact</button></p>
          </div>
        )}
      </div>
    </Router>
  );
}

export default App;
