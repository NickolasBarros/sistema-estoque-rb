import pytest

from api import routes
from main import app
from services.estoque_service import EstoqueService


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(routes, "service", EstoqueService())
    return app.test_client()


def test_api_cadastra_lista_e_resume_produtos(client):
    resposta = client.post(
        "/api/itens",
        json={
            "sku": "mer-001",
            "nome": "Arroz",
            "categoria": "Mercearia",
            "unidade_medida": "PCT",
            "quantidade": 4,
            "estoque_minimo": 5,
        },
    )

    assert resposta.status_code == 201
    assert client.get("/api/itens").get_json()[0]["sku"] == "MER-001"
    assert client.get("/api/resumo").get_json()["itens_baixo_estoque"] == 1


def test_api_rejeita_saida_invalida_sem_alterar_o_saldo(client):
    client.post(
        "/api/itens",
        json={
            "sku": "MER-002",
            "nome": "Leite",
            "categoria": "Bebidas",
            "unidade_medida": "UN",
            "quantidade": 3,
        },
    )

    resposta = client.delete("/api/itens/MER-002?quantidade=abc")

    assert resposta.status_code == 400
    assert client.get("/api/itens/MER-002").get_json()["quantidade"] == 3
