import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is admin
    const adminData = JSON.parse(localStorage.getItem('adminData'));
    if (!adminData) {
      navigate('/admin/login');
      return;
    }

    fetchUsers();
  }, [navigate]);

  const fetchUsers = async () => {
    try {
      const adminData = JSON.parse(localStorage.getItem('adminData'));
      const response = await fetch('https://noleftovers-backend.onrender.com/admin/users', {
        headers: {
          'Authorization': `Bearer ${adminData.id}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }

      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('adminData');
    navigate('/admin/login');
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="admin-dashboard">
      <header className="admin-header">
        <h1>Admin Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>

      <div className="admin-content">
        <section className="users-section">
          <h2>Users</h2>
          <div className="users-table">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Points</th>
                  <th>Lunches Today</th>
                  <th>Submissions Today</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id}>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.pts}</td>
                    <td>{user.no_lunches_today}</td>
                    <td>{user.no_of_submissions_today}</td>
                    <td>
                      <button 
                        onClick={() => window.open(`https://noleftovers-backend.onrender.com/qr-code/${user.id}`, '_blank')}
                        className="qr-button"
                      >
                        Get QR Code
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
};

export default AdminDashboard; 