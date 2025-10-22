import React from 'react'

function Header() {
  const navItems = ['Home', 'About', 'Why it matters']

  return (
    <header className='w-lg h-14 rounded-2xl bg-black/15 border border-white/35 backdrop-blur-[1.5px]'>
      <nav className='h-full'>
        <ul className='w-full h-full inline-flex text-2xl justify-evenly items-center'>
          {navItems.map((item) => (
            <li>{item}</li>
          ))}
        </ul>
      </nav>
    </header>
  )
}

export default Header