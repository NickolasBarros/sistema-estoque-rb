"""Regras de negócio do controle de estoque da mercearia."""

from datetime import datetime, timezone

from data_structures.arvore_rb import ArvoreRB
from models.movimentacao import Movimentacao
from models.produto import Produto


class EstoqueService:
    """Coordena produtos, movimentações e a árvore de busca."""

    def __init__(self, carregar_exemplos=False):
        # A árvore indexa produtos pelo SKU para encontrar itens rapidamente.
        self.arvore = ArvoreRB()
        self.movimentacoes = []
        if carregar_exemplos:
            self._carregar_produtos_de_exemplo()

    def _carregar_produtos_de_exemplo(self):
        """Prepara um catálogo inicial para facilitar a demonstração acadêmica."""
        produtos = [
            ("MER-001", "Arroz tipo 1 · 5 kg", "Mercearia", "PCT", 18, 8),
            ("MER-002", "Feijão carioca · 1 kg", "Mercearia", "PCT", 4, 8),
            ("MER-003", "Café torrado · 500 g", "Mercearia", "PCT", 3, 5),
            ("BEB-001", "Leite integral · 1 L", "Bebidas", "UN", 24, 10),
            ("BEB-002", "Óleo de soja · 900 ml", "Bebidas", "UN", 2, 6),
            ("HOR-001", "Banana prata · kg", "Hortifruti", "KG", 9, 5),
            ("LIM-001", "Detergente neutro · 500 ml", "Limpeza", "UN", 12, 5),
        ]
        for produto in produtos:
            self.inserir_item(*produto)

    def inserir_item(self, sku, nome, categoria, unidade, qtd, minimo=0):
        """Cadastra um produto ou registra uma reposição."""
        sku = self._texto_obrigatorio(sku, "SKU").upper()
        nome = self._texto_obrigatorio(nome, "Nome")
        categoria = self._texto_obrigatorio(categoria, "Categoria")
        unidade = self._texto_obrigatorio(unidade, "Unidade de medida")
        qtd = self._quantidade_valida(qtd, "Quantidade")
        minimo = self._quantidade_valida(minimo, "Estoque mínimo")

        existente = self.arvore.buscar(sku)

        if existente:
            existente.valor.quantidade += qtd
            produto = existente.valor
        else:
            produto = Produto(sku, nome, categoria, unidade, qtd, minimo)
            self.arvore.inserir(sku, produto)

        if qtd:
            self._registrar(sku, "ENTRADA", qtd, "Fornecedor")
        return produto.para_dict()

    def remover_item(self, sku, qtd=None):
        """Registra uma saída; sem quantidade, remove todo o saldo."""
        sku = self._texto_obrigatorio(sku, "SKU").upper()
        no = self.arvore.buscar(sku)
        if not no:
            return {"erro": "SKU não encontrado"}

        if qtd is None:
            qtd = no.valor.quantidade
            self.arvore.remover(sku)
        else:
            qtd = self._quantidade_valida(qtd, "Quantidade", permitir_zero=False)
            if qtd > no.valor.quantidade:
                raise ValueError("A saída não pode ser maior que o estoque disponível.")

        if qtd == no.valor.quantidade and self.arvore.buscar(sku):
            self.arvore.remover(sku)
        elif self.arvore.buscar(sku):
            no.valor.quantidade -= qtd

        if qtd:
            self._registrar(sku, "SAIDA", qtd, "Cliente")
        return {"removido": True, "sku": sku, "quantidade": qtd}

    def consultar(self, sku):
        """Devolve os dados do produto, ou None se não existir."""
        no = self.arvore.buscar(sku.upper())
        return no.valor.para_dict() if no else None

    def listar_itens(self):
        """Lista o catálogo em ordem alfabética de SKU."""
        return [produto.para_dict() for produto in self.arvore.valores_em_ordem()]

    def resumo(self):
        """Calcula os indicadores apresentados no painel principal."""
        produtos = self.arvore.valores_em_ordem()
        baixo_estoque = [
            produto.para_dict()
            for produto in produtos
            if produto.quantidade <= produto.estoque_minimo
        ]
        return {
            "total_produtos": len(produtos),
            "unidades_em_estoque": sum(p.quantidade for p in produtos),
            "itens_baixo_estoque": len(baixo_estoque),
            "baixo_estoque": baixo_estoque,
        }

    def _registrar(self, sku, tipo, qtd, origem):
        """Adiciona ao histórico uma movimentação com horário UTC."""
        movimentacao = Movimentacao(
            id=len(self.movimentacoes) + 1,
            data_hora=datetime.now(timezone.utc).isoformat(),
            tipo=tipo,
            quantidade=qtd,
            origem_destino=origem,
            sku_produto=sku,
        )
        self.movimentacoes.append(movimentacao)

    def relatorio_movimentacoes(self, inicio, fim):
        """Filtra movimentações entre duas datas."""
        return [
            m.para_dict() for m in self.movimentacoes
            if inicio <= m.data_hora <= fim
        ]

    def validar_arvore(self):
        """Verifica se a árvore continua respeitando as regras RB."""
        return self.arvore.validar()

    @staticmethod
    def _texto_obrigatorio(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} é obrigatório.")
        if campo == "SKU" and len(valor.strip()) > 50:
            raise ValueError("SKU deve ter no máximo 50 caracteres.")
        return valor.strip()

    @staticmethod
    def _quantidade_valida(valor, campo, permitir_zero=True):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError(f"{campo} deve ser um número inteiro.")
        if valor < 0 or (not permitir_zero and valor == 0):
            complemento = "maior que zero" if not permitir_zero else "zero ou maior"
            raise ValueError(f"{campo} deve ser {complemento}.")
        return valor