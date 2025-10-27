import React from 'react';

// Example nav items
const navItems = ['Home', 'About', 'Contact'];

const Header = ({ setShowLogin, setShowSignup, token, setToken }) => {
  const handleLogout = () => {
    setToken(null);
  };

  return (
    <header className="h-14 rounded-2xl bg-black/15 border border-white/35 backdrop-blur-[1.5px] px-6 text-white flex items-center justify-between w-full">
      <nav className='h-full'>
        <ul className='w-full h-full inline-flex text-xl items-center gap-x-8'>
          {navItems.map((item) => (
            <li key={item} className="relative h-7 overflow-hidden">
              <a href="#" className="block relative h-full group" aria-label={item}>
                <span className="h-full transition-transform duration-300 ease-in-out transform group-hover:-translate-y-full flex items-center">
                  {item}
                </span>
                <span className="absolute top-0 left-0 w-full h-full transition-transform duration-300 ease-in-out transform translate-y-full group-hover:translate-y-0 flex items-center">
                  {item}
                </span>
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <div className="flex items-center gap-4">
        {token ? (
          <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded">Logout</button>
        ) : (
          <>
            <button onClick={() => setShowLogin(true)} className="bg-blue-500 text-white px-4 py-2 rounded">Login</button>
            <button onClick={() => setShowSignup(true)} className="bg-green-500 text-white px-4 py-2 rounded">Sign Up</button>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;