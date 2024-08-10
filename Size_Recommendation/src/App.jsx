import { useState } from 'react'
import './App.css'
import TshirtSize from './components/TshirtSize'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <TshirtSize/>
    </>

  )
}

export default App
