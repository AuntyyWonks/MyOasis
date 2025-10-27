import { useState } from 'react';
import './App.css';
import About from './components/layout/About';
import Hero from './components/layout/Hero';
import ScrollContext from './context/ScrollContext';

function App() {
  const [token, setToken] = useState(null);

  return (
    <ScrollContext>
      <Hero token={token} setToken={setToken} />
      <About />
    </ScrollContext>
  );
}

export default App;
