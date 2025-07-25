// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Accueil from "./components/Accueil";
import DetailsLivre from "./components/DetailsLivre";
import Connexion from "./components/Connexion";
import Profil from "./components/Profil";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Accueil />} />
        <Route path="/livre/:id" element={<DetailsLivre />} />
        <Route path="/connexion" element={<Connexion />} />
        <Route path="/profil" element={<Profil />} />
      </Routes>
    </Router>
  );
}

export default App;
