import { useCallback, useEffect, useMemo, useState } from "react";
import axios from "axios";
import "./styles.css";

const API = "http://localhost:5000/api";

function Icon({ name, size = 20 }) {
  const paths = {
    grid: <><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></>,
    box: <><path d="m12 3 9 5-9 5-9-5 9-5Z" /><path d="m3 8 9 5 9-5M3 8v9l9 5 9-5V8M12 13v9" /></>,
    search: <><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>,
    alert: <><path d="m10.3 3.9-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3.1l-8-14a2 2 0 0 0-3.4 0Z" /><path d="M12 9v4m0 4h.01" /></>,
    chart: <><path d="M3 3v18h18" /><path d="m19 9-5 5-4-4-5 5" /></>,
    arrow: <><path d="M7 17 17 7M7 7h10v10" /></>,
    close: <><path d="m18 6-12 12M6 6l12 12" /></>,
    basket: <><path d="m5 10 2 10h10l2-10M3 10h18M9 10l3-6 3 6" /><path d="M9 14v2m6-2v2" /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>;
}

const numberFormat = new Intl.NumberFormat("pt-BR");
const diaDaSemana = new Intl.DateTimeFormat("pt-BR", { weekday: "long" }).format(new Date()).toLocaleUpperCase("pt-BR");

function App() {
  const [produtos, setProdutos] = useState([]);
  const [movimentacoes, setMovimentacoes] = useState([]);
  const [resumo, setResumo] = useState({ total_produtos: 0, unidades_em_estoque: 0, itens_baixo_estoque: 0, baixo_estoque: [] });
  const [consulta, setConsulta] = useState("");
  const [filtro, setFiltro] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [erro, setErro] = useState("");
  const [modalAberto, setModalAberto] = useState(false);
  const [carregando, setCarregando] = useState(true);
  const [arvoreValida, setArvoreValida] = useState(null);
  const [form, setForm] = useState({ sku: "", nome: "", categoria: "Mercearia", unidade_medida: "UN", quantidade: "", estoque_minimo: "" });

  const carregarDados = useCallback(async () => {
    setCarregando(true);
    try {
      const [itens, painel, historico] = await Promise.all([
        axios.get(`${API}/itens`),
        axios.get(`${API}/resumo`),
        axios.get(`${API}/movimentacoes`),
      ]);
      setProdutos(itens.data);
      setResumo(painel.data);
      setMovimentacoes(historico.data.slice(-6).reverse());
      setErro("");
    } catch {
      setErro("Não foi possível conectar à API. Verifique se o servidor Flask está em execução.");
    } finally {
      setCarregando(false);
    }
  }, []);

  useEffect(() => {
    carregarDados();
  }, [carregarDados]);

  const produtosFiltrados = useMemo(() => {
    const termo = filtro.trim().toLocaleLowerCase("pt-BR");
    if (!termo) return produtos;
    return produtos.filter((item) => `${item.nome} ${item.sku} ${item.categoria}`.toLocaleLowerCase("pt-BR").includes(termo));
  }, [filtro, produtos]);

  async function buscarProduto(event) {
    event.preventDefault();
    if (!consulta.trim()) {
      setFiltro("");
      setMensagem("");
      return;
    }
    try {
      const resposta = await axios.get(`${API}/itens/${encodeURIComponent(consulta.trim())}`);
      setFiltro(resposta.data.sku);
      setMensagem(`Produto encontrado: ${resposta.data.nome}.`);
      setErro("");
    } catch (requestError) {
      setMensagem("");
      setErro(requestError.response?.data?.erro || "Produto não encontrado.");
    }
  }

  async function cadastrarProduto(event) {
    event.preventDefault();
    try {
      await axios.post(`${API}/itens`, {
        ...form,
        quantidade: Number(form.quantidade),
        estoque_minimo: Number(form.estoque_minimo || 0),
      });
      setMensagem("Produto cadastrado e entrada registrada com sucesso.");
      setErro("");
      setModalAberto(false);
      setForm({ sku: "", nome: "", categoria: "Mercearia", unidade_medida: "UN", quantidade: "", estoque_minimo: "" });
      await carregarDados();
    } catch (requestError) {
      setErro(requestError.response?.data?.erro || "Não foi possível cadastrar o produto.");
      setMensagem("");
    }
  }

  async function registrarSaida(produto) {
    try {
      await axios.delete(`${API}/itens/${encodeURIComponent(produto.sku)}`, { params: { quantidade: 1 } });
      setMensagem(`Saída de 1 ${produto.unidade_medida} registrada para ${produto.nome}.`);
      setErro("");
      await carregarDados();
    } catch (requestError) {
      setErro(requestError.response?.data?.erro || "Não foi possível registrar a saída.");
      setMensagem("");
    }
  }

  async function validarArvore() {
    try {
      const resposta = await axios.get(`${API}/arvore/validar`);
      setArvoreValida(resposta.data.valida);
      setMensagem(resposta.data.valida ? "Árvore Rubro-Negra válida: as propriedades de balanceamento estão preservadas." : resposta.data.mensagem);
      setErro("");
    } catch {
      setErro("Não foi possível validar a árvore. Verifique se a API está em execução.");
      setMensagem("");
    }
  }

  function formatarData(valor) {
    return new Intl.DateTimeFormat("pt-BR", { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" }).format(new Date(valor));
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" aria-label="Mercearia Horizonte, página inicial">
          <span className="brand-mark"><Icon name="basket" size={23} /></span>
          <span><strong>horizonte</strong><small>mercearia de bairro</small></span>
        </a>
        <div className="side-label">GESTÃO</div>
        <nav className="navigation" aria-label="Navegação principal">
          <a className="nav-item active" href="#painel"><Icon name="grid" /><span>Painel geral</span></a>
          <a className="nav-item" href="#estoque"><Icon name="box" /><span>Estoque</span><span className="nav-count">{resumo.total_produtos}</span></a>
          <a className="nav-item" href="#movimentacoes"><Icon name="chart" /><span>Movimentações</span></a>
        </nav>
        <div className="sidebar-bottom">
          <div className="tree-note">
            <span className="tree-dot" />
            <div><strong>Busca eficiente</strong><small>Árvore Rubro-Negra ativa</small></div>
          </div>
          <button className="validate-tree-button" onClick={validarArvore}>
            <Icon name="chart" size={14} /> {arvoreValida === null ? "Validar estrutura RB" : arvoreValida ? "Estrutura RB válida" : "Verificar estrutura RB"}
          </button>
          <p>Projeto acadêmico · Estrutura de Dados</p>
        </div>
      </aside>

      <main className="main-content" id="painel">
        <header className="topbar">
          <div className="breadcrumb">Mercearia Horizonte <span>/</span> <strong>Painel geral</strong></div>
          <div className="store-status"><span /> Sistema operacional</div>
        </header>

        <section className="page-heading">
          <div>
            <p className="eyebrow">{diaDaSemana} · CONTROLE DE ESTOQUE</p>
            <h1>Bom dia, equipe<span>.</span></h1>
            <p className="heading-copy">Acompanhe os produtos e mantenha as prateleiras sempre abastecidas.</p>
          </div>
          <button className="primary-button" onClick={() => setModalAberto(true)}><Icon name="plus" size={18} /> Novo produto</button>
        </section>

        {(erro || mensagem) && <div className={`notice ${erro ? "notice-error" : "notice-success"}`} role="status">{erro || mensagem}<button onClick={() => { setErro(""); setMensagem(""); }} aria-label="Fechar mensagem"><Icon name="close" size={16} /></button></div>}

        <section className="metric-grid" aria-label="Indicadores do estoque">
          <article className="metric-card">
            <div className="metric-top"><span className="metric-icon icon-mint"><Icon name="box" /></span><span className="metric-tag">CATÁLOGO</span></div>
            <p className="metric-value">{numberFormat.format(resumo.total_produtos)}</p><p className="metric-label">Produtos cadastrados</p>
          </article>
          <article className="metric-card">
            <div className="metric-top"><span className="metric-icon icon-blue"><Icon name="basket" /></span><span className="metric-tag">DISPONÍVEL</span></div>
            <p className="metric-value">{numberFormat.format(resumo.unidades_em_estoque)}</p><p className="metric-label">Unidades em estoque</p>
          </article>
          <article className="metric-card metric-warning">
            <div className="metric-top"><span className="metric-icon icon-amber"><Icon name="alert" /></span><span className="metric-tag">ATENÇÃO</span></div>
            <p className="metric-value">{numberFormat.format(resumo.itens_baixo_estoque)}</p><p className="metric-label">Produtos para repor</p>
          </article>
        </section>

        <div className="dashboard-grid">
          <section className="panel inventory-panel" id="estoque">
            <div className="panel-heading">
              <div><h2>Estoque da loja</h2><p>Consulte os produtos e registre saídas do balcão.</p></div>
              <form className="search-box" onSubmit={buscarProduto}>
                <Icon name="search" size={18} /><input value={consulta} onChange={(event) => setConsulta(event.target.value)} placeholder="Buscar por SKU" aria-label="Buscar produto por SKU" /><button type="submit">Buscar</button>
              </form>
            </div>
            <div className="table-wrap">
              <table>
                <thead><tr><th>PRODUTO</th><th>CATEGORIA</th><th>QUANTIDADE</th><th>STATUS</th><th /></tr></thead>
                <tbody>
                  {carregando ? <tr><td className="empty-row" colSpan="5">Carregando produtos…</td></tr> : produtosFiltrados.length === 0 ? <tr><td className="empty-row" colSpan="5">{produtos.length ? "Nenhum produto corresponde à busca." : "Seu estoque está vazio. Cadastre o primeiro produto para começar."}</td></tr> : produtosFiltrados.map((produto) => {
                    const baixo = produto.quantidade <= produto.estoque_minimo;
                    return <tr key={produto.sku}>
                      <td><div className="product-cell"><span className="product-avatar">{produto.nome.slice(0, 1).toLocaleUpperCase("pt-BR")}</span><span><strong>{produto.nome}</strong><small>SKU {produto.sku}</small></span></div></td>
                      <td><span className="category-pill">{produto.categoria}</span></td>
                      <td><strong className="quantity">{numberFormat.format(produto.quantidade)}</strong><span className="unit"> {produto.unidade_medida}</span></td>
                      <td><span className={`status-pill ${baixo ? "status-low" : "status-ok"}`}><i />{baixo ? "Repor estoque" : "Disponível"}</span></td>
                      <td className="action-cell"><button className="text-button" disabled={!produto.quantidade} onClick={() => registrarSaida(produto)}>Registrar saída</button></td>
                    </tr>;
                  })}
                </tbody>
              </table>
            </div>
            <div className="table-footer"><span>Exibindo {produtosFiltrados.length} de {produtos.length} produtos</span><span>Ordenado por SKU <span className="sort-arrow">↕</span></span></div>
          </section>

          <div className="right-column">
            <section className="panel low-stock-panel">
              <div className="compact-heading"><div><span className="small-icon icon-amber"><Icon name="alert" size={17} /></span><h2>Precisa de reposição</h2></div><span className="counter">{resumo.itens_baixo_estoque}</span></div>
              <p className="panel-subtitle">Produtos no limite ou abaixo do mínimo definido.</p>
              {resumo.baixo_estoque?.length ? <ul className="low-stock-list">{resumo.baixo_estoque.slice(0, 4).map((produto) => <li key={produto.sku}><span className="mini-product-avatar">{produto.nome.slice(0, 1).toLocaleUpperCase("pt-BR")}</span><span className="low-product-name"><strong>{produto.nome}</strong><small>Mínimo: {produto.estoque_minimo} {produto.unidade_medida}</small></span><span className="low-quantity">{produto.quantidade}</span></li>)}</ul> : <div className="all-good"><span>✓</span><p>Tudo em dia! Nenhum produto precisa de reposição.</p></div>}
            </section>

            <section className="panel movements-panel" id="movimentacoes">
              <div className="compact-heading"><div><span className="small-icon icon-blue"><Icon name="chart" size={17} /></span><h2>Atividade recente</h2></div><a href="#movimentacoes" className="subtle-link">Últimas</a></div>
              {movimentacoes.length ? <ul className="movement-list">{movimentacoes.map((movimento) => {
                const produto = produtos.find((item) => item.sku === movimento.sku_produto);
                const entrada = movimento.tipo === "ENTRADA";
                return <li key={movimento.id}><span className={`movement-icon ${entrada ? "movement-in" : "movement-out"}`}>{entrada ? "↓" : "↑"}</span><span className="movement-copy"><strong>{entrada ? "Entrada recebida" : "Saída registrada"}</strong><small>{produto?.nome || `SKU ${movimento.sku_produto}`} · {formatarData(movimento.data_hora)}</small></span><span className={`movement-amount ${entrada ? "amount-in" : "amount-out"}`}>{entrada ? "+" : "−"}{movimento.quantidade}</span></li>;
              })}</ul> : <div className="empty-activity">As entradas e saídas registradas aparecerão aqui.</div>}
            </section>
          </div>
        </div>

        <footer className="page-footer"><span>Mercearia Horizonte <span>·</span> Projeto acadêmico</span><span><span className="footer-dot" /> Estrutura de busca: Árvore Rubro-Negra</span></footer>
      </main>

      {modalAberto && <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) setModalAberto(false); }}>
        <section className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          <div className="modal-heading"><div><p className="eyebrow">CATÁLOGO DA MERCEARIA</p><h2 id="modal-title">Cadastrar produto</h2><p>Adicione um item ou registre uma nova entrada no estoque.</p></div><button className="icon-button" onClick={() => setModalAberto(false)} aria-label="Fechar"><Icon name="close" /></button></div>
          <form onSubmit={cadastrarProduto}>
            <label>Nome do produto<input required maxLength="200" value={form.nome} onChange={(event) => setForm({ ...form, nome: event.target.value })} placeholder="Ex.: Café torrado 500 g" /></label>
            <div className="form-row">
              <label>SKU / código<input required maxLength="50" value={form.sku} onChange={(event) => setForm({ ...form, sku: event.target.value })} placeholder="Ex.: MER-001" /></label>
              <label>Categoria<select value={form.categoria} onChange={(event) => setForm({ ...form, categoria: event.target.value })}><option>Mercearia</option><option>Bebidas</option><option>Hortifruti</option><option>Limpeza</option><option>Higiene</option><option>Padaria</option><option>Outros</option></select></label>
            </div>
            <div className="form-row form-row-three">
              <label>Quantidade<input required type="number" min="0" step="1" value={form.quantidade} onChange={(event) => setForm({ ...form, quantidade: event.target.value })} placeholder="0" /></label>
              <label>Estoque mínimo<input type="number" min="0" step="1" value={form.estoque_minimo} onChange={(event) => setForm({ ...form, estoque_minimo: event.target.value })} placeholder="0" /></label>
              <label>Unidade<select value={form.unidade_medida} onChange={(event) => setForm({ ...form, unidade_medida: event.target.value })}><option>UN</option><option>KG</option><option>L</option><option>PCT</option><option>CX</option></select></label>
            </div>
            <div className="modal-actions"><button type="button" className="secondary-button" onClick={() => setModalAberto(false)}>Cancelar</button><button type="submit" className="primary-button"><Icon name="plus" size={17} /> Cadastrar produto</button></div>
          </form>
        </section>
      </div>}
    </div>
  );
}

export default App;
