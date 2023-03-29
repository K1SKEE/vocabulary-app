import './App.css';
import React, { useContext } from 'react'
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Header from './components/Header';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import { AuthContext } from './context/AuthContext';
import AddWords from './components/AddWords';
import Vocabulary from './components/Vocabulary';
import Repetition from './components/Repetition';


function App() {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          {isAuthenticated ?
            <>
              <Route path="/" element={<Navigate to='/add' replace={true} />} />
              <Route path="/add" element={<AddWords />} />
              <Route path="/vocabulary" element={<Vocabulary />} />
              <Route path="/repetition" element={<Repetition />} />
            </>
            :
            <>
              <Route path="/" element={<Navigate to='/login' replace={true} />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
            </>
          }
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
