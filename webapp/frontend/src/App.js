import logo from './logo.svg';
import './App.css';
import UploadComponent from './UploadComponent';

function App() {
  return (
    <div className="App">
      <header>
        <img src="/logo512.png" alt="CellSeg logo" style={{ height: "32px", marginRight: "5px" }} />
        <span style={{ fontSize: "1.5rem", fontWeight: "bold" }}>CellSeg</span>
      </header>      
      <main>
        <UploadComponent />
      </main>
    </div>
  );
}

export default App;
