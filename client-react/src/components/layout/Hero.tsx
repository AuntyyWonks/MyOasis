import React from 'react'
import Header from './Header'

function Hero() {
  return (
    <div className='hero w-full h-screen'>
      <div className='w-full h-full bg-black/20 flex flex-col items-center py-14'>
        <Header />
      </div>
    </div>
  )
}

export default Hero