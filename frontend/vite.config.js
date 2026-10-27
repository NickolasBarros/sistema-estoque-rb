// ============================================================
// ARQUIVO: vite.config.js
// O QUE FAZ: configura o Vite para compilar JSX "automaticamente",
// sem precisar colocar "import React" em todo arquivo.
// ============================================================

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [
    react({
      // "automatic" faz o Vite injetar o import do React sozinho
      jsxRuntime: "automatic",
    }),
  ],
});