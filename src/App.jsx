import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { TablePage } from "./components";
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="*" element={<Navigate to="/notifications/all" />} />
        <Route path="/:category/:course" element={<TablePage />} />
      </Routes>
    </Router>
  );
}

export default App;
