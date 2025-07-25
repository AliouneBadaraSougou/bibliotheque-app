// src/index.js
import React from "react";
import ReactDOM from "react-dom/client"; // Importez ReactDOM depuis 'react-dom/client'
import App from "./App";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root")); // Créez une racine
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

