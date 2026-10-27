// ============================================================
// ARQUIVO: App.jsx
// O QUE FAZ: a tela do site com 3 seções:
//   - Consultar por SKU
//   - Inserir Item
//   - Validar Árvore RB
// ============================================================

import { useState } from "react";
import axios from "axios";

// Endereço da API (o backend Flask que está rodando)
const API = "http://localhost:5000/api";

export default function App() {
  // Estados: guardam o que o usuário digita
  const [sku, setSku] = useState("");
  const [produto, setProduto] = useState(null);
  const [valida, setValida] = useState(null);
  const [form, setForm] = useState({
    sku: "", nome: "", categoria: "", unidade_medida: "UN",
    quantidade: 0, estoque_minimo: 0,
  });

  // Busca um produto na API
  const buscar = async () => {
    try {
      const r = await axios.get(`${API}/itens/${sku}`);
      setProduto(r.data);
    } catch {
      setProduto({ erro: "não encontrado" });
    }
  };

  // Envia um novo produto para a API
  const inserir = async () => {
    await axios.post(`${API}/itens`, form);
    alert("Inserido!");
  };

  // Pede à API para validar a árvore
  const validar = async () => {
    const r = await axios.get(`${API}/arvore/validar`);
    setValida(r.data);
  };

  return (
    <div style={{ padding: 24, fontFamily: "sans-serif", maxWidth: 800, margin: "auto" }}>
      <h1>Gestão de Estoque — Árvore Rubro-Negra</h1>

      <section>
        <h2>Consultar por SKU</h2>
        <input value={sku} onChange={(e) => setSku(e.target.value)} placeholder="SKU" />
        <button onClick={buscar}>Buscar</button>
        {produto && <pre>{JSON.stringify(produto, null, 2)}</pre>}
      </section>

      <section>
        <h2>Inserir Item</h2>
        {Object.keys(form).map((k) => (
          <div key={k}>
            <label>{k}: </label>
            <input
              value={form[k]}
              onChange={(e) => setForm({ ...form, [k]: e.target.value })}
            />
          </div>
        ))}
        <button onClick={inserir}>Inserir</button>
      </section>

      <section>
        <h2>Validar Árvore RB</h2>
        <button onClick={validar}>Validar</button>
        {valida && <pre>{JSON.stringify(valida, null, 2)}</pre>}
      </section>
    </div>
  );
}