import './App.css'
import About from './components/layout/About'
import Hero from './components/layout/Hero'
import ScrollContext from './context/ScrollContext'

function App() {

  return (
    <ScrollContext>
      <Hero />
      <About />
    </ScrollContext>
  )
}

export default App
