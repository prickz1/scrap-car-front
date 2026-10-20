import requests

_BASE = "http://localhost:8000/api/v1"


def get_marcas() -> list[str]:
    try:
        r = requests.get(f"{_BASE}/ml/marcas").json()
        return r if isinstance(r, list) else []
    except Exception:
        return []


def get_modelos(marca: str) -> list[str]:
    try:
        r = requests.get(f"{_BASE}/ml/modelos", params={"marca": marca}).json()
        return r if isinstance(r, list) else []
    except Exception:
        return []


def get_anos(marca: str, modelo: str) -> list[int]:
    try:
        r = requests.get(f"{_BASE}/ml/anos", params={"marca": marca, "modelo": modelo}).json()
        return r if isinstance(r, list) else []
    except Exception:
        return []


def get_cambios(marca: str, modelo: str, ano: int) -> list[str]:
    try:
        r = requests.get(f"{_BASE}/ml/cambios", params={"marca": marca, "modelo": modelo, "ano": ano}).json()
        return r if isinstance(r, list) else []
    except Exception:
        return []


def get_combustiveis(marca: str, modelo: str, ano: int) -> list[str]:
    try:
        r = requests.get(f"{_BASE}/ml/combustiveis", params={"marca": marca, "modelo": modelo, "ano": ano}).json()
        return r if isinstance(r, list) else []
    except Exception:
        return []


def get_direcoes(marca: str, modelo: str, ano: int) -> list[str]:
    try:
        r = requests.get(f"{_BASE}/ml/direcoes", params={"marca": marca, "modelo": modelo, "ano": ano}).json()
        return r if isinstance(r, list) else []
    except Exception:
        return []


def get_previsao(
    marca: str,
    modelo: str,
    ano: int,
    cambio: str,
    combustivel: str,
    direcao: str,
    quilometragem: float,
) -> dict:
    try:
        r = requests.get(f"{_BASE}/ml/prever", params={
            "marca": marca,
            "modelo": modelo,
            "ano": ano,
            "cambio": cambio,
            "combustivel": combustivel,
            "direcao": direcao,
            "quilometragem": quilometragem,
        }).json()
        return r if isinstance(r, dict) else {}
    except Exception:
        return {}
