from clients.api_client import (
    get_marcas,
    get_modelos,
    get_anos,
    get_cambios,
    get_combustiveis,
    get_direcoes,
    get_previsao,
)


def listar_marcas() -> list[str]:
    return get_marcas()


def listar_modelos(marca: str) -> list[str]:
    return get_modelos(marca)


def listar_anos(marca: str, modelo: str) -> list[int]:
    return get_anos(marca, modelo)


def listar_cambios(marca: str, modelo: str, ano: int) -> list[str]:
    return get_cambios(marca, modelo, ano)


def listar_combustiveis(marca: str, modelo: str, ano: int) -> list[str]:
    return get_combustiveis(marca, modelo, ano)


def listar_direcoes(marca: str, modelo: str, ano: int) -> list[str]:
    return get_direcoes(marca, modelo, ano)


def prever_preco(
    marca: str,
    modelo: str,
    ano: int,
    cambio: str,
    combustivel: str,
    direcao: str,
    quilometragem: float,
) -> dict:
    return get_previsao(marca, modelo, ano, cambio, combustivel, direcao, quilometragem)
