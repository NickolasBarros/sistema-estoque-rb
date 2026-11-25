import pytest

from services.estoque_service import EstoqueService


def test_cadastro_gera_resumo_e_catalogo_ordenado():
    service = EstoqueService()
    service.inserir_item("mer-002", "Leite", "Bebidas", "UN", 3, 2)
    service.inserir_item("mer-001", "Cafe", "Mercearia", "PCT", 1, 2)

    assert [item["sku"] for item in service.listar_itens()] == ["MER-001", "MER-002"]
    assert service.resumo() == {
        "total_produtos": 2,
        "unidades_em_estoque": 4,
        "itens_baixo_estoque": 1,
        "baixo_estoque": [
            {
                "sku": "MER-001",
                "nome": "Cafe",
                "categoria": "Mercearia",
                "unidade_medida": "PCT",
                "quantidade": 1,
                "estoque_minimo": 2,
            }
        ],
    }


def test_reposicao_e_saida_atualizam_produto_e_historico():
    service = EstoqueService()
    service.inserir_item("MER-010", "Arroz", "Mercearia", "PCT", 5, 2)
    service.inserir_item("MER-010", "Arroz", "Mercearia", "PCT", 3, 2)

    resultado = service.remover_item("MER-010", 2)

    assert service.consultar("MER-010")["quantidade"] == 6
    assert resultado == {"removido": True, "sku": "MER-010", "quantidade": 2}
    assert [mov["tipo"] for mov in service.relatorio_movimentacoes("0000", "9999")] == [
        "ENTRADA",
        "ENTRADA",
        "SAIDA",
    ]


def test_saida_nao_permite_quantidade_maior_que_o_saldo():
    service = EstoqueService()
    service.inserir_item("MER-020", "Feijao", "Mercearia", "PCT", 2, 1)

    with pytest.raises(ValueError, match="maior que o estoque"):
        service.remover_item("MER-020", 3)

    assert service.consultar("MER-020")["quantidade"] == 2
    assert service.validar_arvore()[0]


def test_quantidades_negativas_e_dados_obrigatorios_sao_rejeitados():
    service = EstoqueService()

    with pytest.raises(ValueError, match="Nome é obrigatório"):
        service.inserir_item("MER-030", " ", "Mercearia", "UN", 1, 0)

    with pytest.raises(ValueError, match="zero ou maior"):
        service.inserir_item("MER-030", "Macarrao", "Mercearia", "PCT", -1, 0)
