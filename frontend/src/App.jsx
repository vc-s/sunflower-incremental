import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [ score, setScore ] = useState(0);
  const [ tier, setTier ] = useState(0);
  const [ worth, setWorth ] = useState(1);
  const [ board, setBoard ] = useState([[]]);
  const [ temp, setTemp ] = useState('');
  
  const initBoard = () => {
    fetch(`http://127.0.0.1:8000/init`, { method: 'POST' })
    .then(resp => resp.json())
  }
  
  const getBoard = () => {
    fetch(`http://127.0.0.1:8000/show-board`)
    .then(resp => resp.json())
    .then(data => {
      setBoard(data.board)
      setScore(data.score)
      setTier(data.tier)
      setWorth(data.worth)
    })
  }
  
  useEffect(() => {
    initBoard()
    getBoard()
  }, [])
  
  const collectFlower = (r, c) => {
    fetch(`http://127.0.0.1:8000/collect-flower?row=${r}&col=${c}`, { method: 'PUT' })
    .then(resp => resp.json())
    .then(data => {
      setTemp(data)
      getBoard()
    })
  }
  
  const upgradeTier = () => {
    fetch(`http://127.0.0.1:8000/upgrade`, { method: 'PUT' })
    .then(resp => resp.json())
    .then(data => {
      setTemp(data)
      getBoard()
    })
  }

  return (
    <div>
      <h1>Sunflower Incremental</h1>
      <h3>Welcome to Sunflower Incremental !</h3>
      <p>Score: {score}</p>
      <p>Tier: {tier}</p>
      <p>Worth: {worth}</p>
      <table className="board">
        <tbody>
          {board.map((row, r) => (
            <tr key={r}>
              {row.map((cell, c) => (
                <td key={c} className={cell === "F" ? "flower" : "empty"}>
                  <button onClick={() => collectFlower(r, c)}>{cell === "F" ? "🌻" : ""}</button>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={upgradeTier}>Upgrade Tier</button>
      <p>{temp}</p>
    </div>
  )
}

export default App