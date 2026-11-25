"""Modelo de domínio para os produtos da mercearia."""

from dataclasses import asdict, dataclass


@dataclass
class Produto:
    """Representa um item comercializado e controlado pelo estoque."""

    sku: str
    nome: str
    categoria: str
    unidade_medida: str
    quantidade: int
    estoque_minimo: int

    def para_dict(self):
        """Converte o objeto para o formato JSON usado pela API."""
        return asdict(self)
