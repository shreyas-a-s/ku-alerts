import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { TablePage } from "./components";
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/:category/:course" element={<TablePage />} />
        <Route path="*" element={<Navigate to="/notifications/all" />} />
      </Routes>
    </Router>
  );
}

export default App;
