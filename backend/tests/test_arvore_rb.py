# ============================================================
# ARQUIVO: test_arvore_rb.py
# O QUE FAZ: testa a árvore automaticamente.
# Rodar com: pytest tests -v (dentro de backend, com venv ativo)
# ============================================================

# Importa a árvore
from data_structures.arvore_rb import ArvoreRB


def test_insercao_e_busca():
    """Insere 6 números e verifica busca + validação."""
    t = ArvoreRB()

    # Insere fora de ordem (força rotações)
    for k in [10, 20, 30, 15, 25, 5]:
        t.inserir(k, {"v": k})

    # A busca deve encontrar o 15
    assert t.buscar(15).valor["v"] == 15

    # A árvore deve continuar válida
    assert t.validar()[0] is True


def test_remocao():
    """Insere 50 números, remove os ímpares, valida."""
    t = ArvoreRB()
    for k in range(1, 51):
        t.inserir(k)

    # Remove 1, 3, 5, ..., 49
    for k in range(1, 51, 2):
        t.remover(k)

    # Continua válida
    assert t.validar()[0] is True