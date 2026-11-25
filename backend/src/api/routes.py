"""Endpoints HTTP do sistema de estoque."""

from flask import Blueprint, jsonify, request

from services.estoque_service import EstoqueService

bp = Blueprint("api", __name__)
# Dados fictícios permitem explorar o painel logo ao iniciar a demonstração.
service = EstoqueService(carregar_exemplos=True)


@bp.post("/itens")
def inserir():
    """Cadastra um produto ou registra uma entrada para SKU existente."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados do produto em formato JSON."}), 400
    try:
        produto = service.inserir_item(
            dados.get("sku"),
            dados.get("nome"),
            dados.get("categoria"),
            dados.get("unidade_medida"),
            dados.get("quantidade"),
            dados.get("estoque_minimo", 0),
        )
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    return jsonify(produto), 201


@bp.delete("/itens/<sku>")
def remover(sku):
    """Registra uma saída ou remove todo o saldo se não houver quantidade."""
    quantidade = request.args.get("quantidade")
    try:
        qtd = int(quantidade) if quantidade is not None else None
    except ValueError:
        return jsonify({"erro": "Quantidade deve ser um número inteiro."}), 400
    try:
        resultado = service.remover_item(sku, qtd)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    if "erro" in resultado:
        return jsonify(resultado), 404
    return jsonify(resultado)


@bp.get("/itens/<sku>")
def consultar(sku):
    """Consulta um produto pelo SKU."""
    produto = service.consultar(sku)
    if produto:
        return jsonify(produto)
    return jsonify({"erro": "SKU não encontrado."}), 404


@bp.get("/itens")
def listar_itens():
    """Lista todos os produtos em ordem de SKU."""
    return jsonify(service.listar_itens())


@bp.get("/resumo")
def resumo():
    """Fornece os indicadores do painel de estoque."""
    return jsonify(service.resumo())


@bp.get("/movimentacoes")
def movs():
    """Lista movimentações; aceita limites ISO em inicio e fim."""
    inicio = request.args.get("inicio", "0000")
    fim = request.args.get("fim", "9999")
    return jsonify(service.relatorio_movimentacoes(inicio, fim))


@bp.get("/arvore/validar")
def validar():
    """Confere se a árvore respeita as propriedades rubro-negras."""
    ok, mensagem = service.validar_arvore()
    return jsonify({"valida": ok, "mensagem": mensagem})
