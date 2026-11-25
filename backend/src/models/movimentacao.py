"""Modelo de domínio para entradas e saídas do estoque."""

from dataclasses import asdict, dataclass


@dataclass
class Movimentacao:
    """Registra uma alteração de quantidade de um produto."""

    id: int
    data_hora: str
    tipo: str
    quantidade: int
    origem_destino: str
    sku_produto: str

    def para_dict(self):
        """Converte o objeto para o formato JSON usado pela API."""
        return asdict(self)
