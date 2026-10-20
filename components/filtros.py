import streamlit as st

from services.carro_service import (
    listar_marcas,
    listar_modelos,
    listar_anos,
    listar_cambios,
    listar_combustiveis,
    listar_direcoes,
)

FAIXAS_KM = {
    "Até 20.000 km":        10_000,
    "20.000 – 40.000 km":   30_000,
    "40.000 – 60.000 km":   50_000,
    "60.000 – 80.000 km":   70_000,
    "80.000 – 100.000 km":  90_000,
    "100.000 – 150.000 km": 125_000,
    "Acima de 150.000 km":  175_000,
}


@st.cache_data(show_spinner=False)
def _marcas():
    return listar_marcas()


@st.cache_data(show_spinner=False)
def _modelos(marca):
    return listar_modelos(marca)


@st.cache_data(show_spinner=False)
def _anos(marca, modelo):
    return listar_anos(marca, modelo)


@st.cache_data(show_spinner=False)
def _cambios(marca, modelo, ano):
    return listar_cambios(marca, modelo, ano)


@st.cache_data(show_spinner=False)
def _combustiveis(marca, modelo, ano):
    return listar_combustiveis(marca, modelo, ano)


@st.cache_data(show_spinner=False)
def _direcoes(marca, modelo, ano):
    return listar_direcoes(marca, modelo, ano)


def render_filtros() -> dict | None:
    """Renderiza os filtros em cascata. Retorna dict com os valores ou None se incompleto."""

    marca = st.selectbox("Marca", ["Selecione..."] + _marcas())
    if marca == "Selecione...":
        return None

    modelo = st.selectbox("Modelo", ["Selecione..."] + _modelos(marca), key=f"m_{marca}")
    if modelo == "Selecione...":
        return None

    anos = _anos(marca, modelo)
    if not anos:
        st.info("Nenhum dado encontrado para esse modelo.")
        return None
    ano = st.selectbox("Ano", anos, key=f"a_{marca}_{modelo}")

    cambios = _cambios(marca, modelo, ano)
    if not cambios:
        st.info("Nenhum dado de câmbio encontrado.")
        return None
    cambio = st.selectbox("Câmbio", cambios, key=f"cb_{marca}_{modelo}_{ano}")

    combustiveis = _combustiveis(marca, modelo, ano)
    if not combustiveis:
        st.info("Nenhum dado de combustível encontrado.")
        return None
    combustivel = st.selectbox("Combustível", combustiveis, key=f"co_{marca}_{modelo}_{ano}")

    direcoes = _direcoes(marca, modelo, ano)
    if not direcoes:
        st.info("Nenhum dado de direção encontrado.")
        return None
    direcao = st.selectbox("Direção", direcoes, key=f"d_{marca}_{modelo}_{ano}")

    faixa_km = st.selectbox("Quilometragem", list(FAIXAS_KM.keys()), key=f"km_{marca}_{modelo}_{ano}")

    return {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "cambio": cambio,
        "combustivel": combustivel,
        "direcao": direcao,
        "faixa_km": faixa_km,
        "quilometragem": FAIXAS_KM[faixa_km],
    }
