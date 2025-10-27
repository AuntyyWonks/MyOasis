import React from 'react';
import SignInButton from '../ui/SignInButton';

// Example nav items
const navItems = ['Home', 'About', 'Contact'];

const Header = () => {
  return (
    <header className="h-14 rounded-2xl bg-black/15 border border-white/35 backdrop-blur-[1.5px] px-6 text-white
    ">
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
      <SignInButton />
    </header>
  );
};

export default Header;