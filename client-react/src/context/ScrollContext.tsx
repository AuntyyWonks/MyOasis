'use client';
import React, { useState, useEffect, createContext, useContext } from 'react'
import Lenis from 'lenis';

const SmoothScrollContext = createContext<Lenis | null>(null);

export const useSmoothScroll = () => useContext(SmoothScrollContext);

type ScrollContextProps = {
  children: React.ReactNode;
}

function ScrollContext({ children }: ScrollContextProps) {
  const [lenisRef, setLenis] = useState<null | Lenis>(null);
  const [rafState, setRaf] = useState<number>(0);

  useEffect(() => {
    const scroller = new Lenis();

    function raf(time: number) {
      scroller.raf(time);
      requestAnimationFrame(raf);
    }

    const rf = requestAnimationFrame(raf);
    setRaf(rf);
    setLenis(scroller);

    return () => {
      if (lenisRef) {
        cancelAnimationFrame(rafState)
        lenisRef.destroy();
      }
    };
  }, []);



  return (
    <SmoothScrollContext.Provider value={lenisRef}>
      {children}
    </SmoothScrollContext.Provider>
  )
}

export default ScrollContext