import React from 'react'
import Header from './Header'

function Hero() {
  return (
    <div className="w-full h-screen relative overflow-hidden">
      <video
        className="absolute top-0 left-0 w-full h-full object-cover z-0"
        autoPlay
        muted
        loop
      >
        <source src="/oasis-hero.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      /* Overlay and content */
      <div className="w-full h-full bg-black/30 flex flex-col items-center py-14 relative z-10">
        <div className="relative h-4/5 z-20 flex flex-col items-center justify-between">
          <Header />
          <div className="w-full flex flex-col gap-12 text-center">
            <div className='flex flex-col gap-4 text-white tracking-tighter'>
              <h1 className="text-6xl font-bold">Oasis</h1>
              <p className="text-lg px-12">Your AI farming assistant to help you plant, grow, and care for crops with confidence</p>
            </div>
          </div>
        </div>
      </div>
    </div>

  )
}

export default Hero