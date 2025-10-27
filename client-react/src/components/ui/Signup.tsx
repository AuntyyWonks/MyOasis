import React, { useState } from 'react';

const apiUrl = import.meta.env.VITE_API_URL;

const Signup = ({ setToken, setShowSignup }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();
    const regResponse = await fetch(`${apiUrl}/api/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (regResponse.ok) {
      const loginResponse = await fetch(`${apiUrl}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (loginResponse.ok) {
        const data = await loginResponse.json();
        setToken(data.token);
        setShowSignup(false);
      } else {
        alert('Login failed after signup. Please try logging in manually.');
      }
    } else {
      const data = await regResponse.json();
      alert(data.message);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-gray-900 p-8 rounded-lg shadow-lg">
        <h2 className="text-white text-2xl mb-4">Sign Up</h2>
        <form onSubmit={handleSignup}>
          <div className="mb-4">
            <label className="block text-gray-400 mb-2" htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-2 rounded bg-gray-700 text-white"
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-400 mb-2" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-2 rounded bg-gray-700 text-white"
            />
          </div>
          <div className="flex justify-end gap-4">
            <button type="button" onClick={() => setShowSignup(false)} className="bg-gray-600 text-white p-2 rounded">Cancel</button>
            <button type="submit" className="bg-blue-500 text-white p-2 rounded">Sign Up</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Signup;
