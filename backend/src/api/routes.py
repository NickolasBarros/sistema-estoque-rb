# ============================================================
# ARQUIVO: routes.py
# O QUE FAZ: define as "portas" (rotas) da API.
# Cada @bp.xxx é um tipo de pedido que o site pode fazer:
#   GET    = pedir informação
#   POST   = criar algo novo
#   DELETE = apagar algo
# ============================================================

# Blueprint = caderno de rotas
# request = pega dados que o site enviou
# jsonify = transforma resposta em JSON
from flask import Blueprint, request, jsonify

# Importa o serviço (o gerente)
from services.estoque_service import EstoqueService

# Cria o caderno de rotas
bp = Blueprint("api", __name__)

# Instância única do serviço (usada em todas as rotas)
service = EstoqueService()


@bp.post("/itens")
def inserir():
    """POST /api/itens → insere um novo produto."""
    # Pega o JSON que o site enviou
    d = request.json

    # Chama o serviço passando os campos
    return jsonify(service.inserir_item(
        d["sku"], d["nome"], d["categoria"], d["unidade_medida"],
        d["quantidade"], d.get("estoque_minimo", 0)
    )), 201


@bp.delete("/itens/<sku>")
def remover(sku):
    """DELETE /api/itens/{sku} → remove ou decrementa."""
    # Pega 'quantidade' da URL (opcional)
    qtd = request.args.get("quantidade", type=int)
    return jsonify(service.remover_item(sku, qtd))


@bp.get("/itens/<sku>")
def consultar(sku):
    """GET /api/itens/{sku} → consulta disponibilidade."""
    r = service.consultar(sku)
    if r:
        return jsonify(r)
    return {"erro": "não encontrado"}, 404


@bp.get("/movimentacoes")
def movs():
    """GET /api/movimentacoes?inicio&fim → relatório."""
    ini = request.args.get("inicio", "0000")
    fim = request.args.get("fim", "9999")
    return jsonify(service.relatorio_movimentacoes(ini, fim))


@bp.get("/arvore/validar")
def validar():
    """GET /api/arvore/validar → confere as regras RB."""
    ok, msg = service.validar_arvore()
    return jsonify({"valida": ok, "mensagem": msg})