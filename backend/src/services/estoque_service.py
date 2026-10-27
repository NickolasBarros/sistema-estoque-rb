# ============================================================
# ARQUIVO: estoque_service.py
# O QUE FAZ: é o "gerente da loja". Usa a árvore para
# guardar produtos e mantém histórico de movimentações.
# ============================================================

# Importa a função datetime para registrar a data e hora
# de cada movimentação de estoque
from datetime import datetime

# Importa a nossa árvore rubro-negra
# (o arquivo arvore_rb.py que criamos antes)
from data_structures.arvore_rb import ArvoreRB


class EstoqueService:
    """Classe que cuida de todas as operações do estoque."""

    def __init__(self):
        # Cria uma árvore vazia (que vai viver só na memória RAM)
        self.arvore = ArvoreRB()

        # Lista que guarda o histórico de entradas e saídas
        # (num sistema em produção isso iria para o PostgreSQL)
        self.movimentacoes = []

    def inserir_item(self, sku, nome, categoria, unidade, qtd, minimo):
        """Adiciona um produto. Se já existir, soma a quantidade."""
        # Procura o SKU na árvore
        existente = self.arvore.buscar(sku)

        if existente:
            # Já existe → só soma na quantidade atual
            existente.valor["quantidade"] += qtd
            produto = existente.valor
        else:
            # Não existe → cria um dicionário com os dados
            produto = {
                "sku": sku,
                "nome": nome,
                "categoria": categoria,
                "unidade_medida": unidade,
                "quantidade": qtd,
                "estoque_minimo": minimo,
            }
            # E insere na árvore (que se auto-organiza)
            self.arvore.inserir(sku, produto)

        # Registra no histórico
        self._registrar(sku, "ENTRADA", qtd, "Fornecedor")
        return produto

    def remover_item(self, sku, qtd=None):
        """Remove item. Se qtd for None, remove tudo."""
        # Procura o SKU
        no = self.arvore.buscar(sku)
        if not no:
            return {"erro": "SKU não encontrado"}

        # Se qtd não foi informada OU é maior que o estoque → remove tudo
        if qtd is None or qtd >= no.valor["quantidade"]:
            qtd = no.valor["quantidade"]
            self.arvore.remover(sku)   # tira da árvore (rebalanceia)
            self._registrar(sku, "SAIDA", qtd, "Cliente")
            return {"removido": True, "sku": sku, "quantidade": qtd}

        # Senão, só diminui a quantidade
        no.valor["quantidade"] -= qtd
        self._registrar(sku, "SAIDA", qtd, "Cliente")
        return no.valor

    def consultar(self, sku):
        """Devolve os dados do produto, ou None se não existir."""
        no = self.arvore.buscar(sku)
        return no.valor if no else None

    def _registrar(self, sku, tipo, qtd, origem):
        """Guarda uma movimentação no histórico."""
        self.movimentacoes.append({
            "id": len(self.movimentacoes) + 1,
            "data_hora": datetime.utcnow().isoformat(),
            "tipo": tipo,
            "quantidade": qtd,
            "origem_destino": origem,
            "sku_produto": sku,
        })

    def relatorio_movimentacoes(self, inicio, fim):
        """Filtra movimentações entre duas datas."""
        return [
            m for m in self.movimentacoes
            if inicio <= m["data_hora"] <= fim
        ]

    def validar_arvore(self):
        """Verifica se a árvore continua respeitando as regras RB."""
        return self.arvore.validar()