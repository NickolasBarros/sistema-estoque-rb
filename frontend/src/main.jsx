// ============================================================
// ARQUIVO: main.jsx
// O QUE FAZ: liga o React ao <div id="root"> do HTML.
// ============================================================

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(<App />);