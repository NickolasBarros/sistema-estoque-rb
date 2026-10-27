-- ============================================================
-- ARQUIVO: schema.sql
-- O QUE FAZ: cria as tabelas do banco PostgreSQL.
-- Execute depois, se quiser usar persistência.
-- ============================================================

-- Tipos especiais (como "listas de opções")
CREATE TYPE tipo_mov AS ENUM ('ENTRADA', 'SAIDA');
CREATE TYPE cor_no AS ENUM ('VERMELHO', 'PRETO');

-- Tabela de produtos
CREATE TABLE produto (
    sku VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    categoria VARCHAR(100),
    unidade_medida VARCHAR(20),
    estoque_minimo INTEGER DEFAULT 0
);

-- Tabela de movimentações (entradas e saídas)
CREATE TABLE movimentacao (
    id_movimentacao SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL DEFAULT NOW(),
    tipo tipo_mov NOT NULL,
    quantidade INTEGER NOT NULL,
    origem_destino VARCHAR(200),
    sku_produto VARCHAR(50) REFERENCES produto(sku) ON DELETE CASCADE
);

-- Índice para acelerar consultas por período
CREATE INDEX idx_mov_data ON movimentacao(data_hora);

-- Tabela que espelha a estrutura da árvore rubro-negra
CREATE TABLE no_arvore (
    sku VARCHAR(50) PRIMARY KEY REFERENCES produto(sku) ON DELETE CASCADE,
    cor cor_no NOT NULL,
    sku_pai VARCHAR(50) REFERENCES no_arvore(sku),
    sku_filho_esq VARCHAR(50) REFERENCES no_arvore(sku),
    sku_filho_dir VARCHAR(50) REFERENCES no_arvore(sku)
);