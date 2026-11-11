import streamlit as st

from services.carro_service import (
    listar_marcas,
    listar_modelos,
    listar_anos,
    listar_cambios,
    listar_combustiveis,
    listar_direcoes,
)

MARCAS_POPULARES = {"Fiat", "VW", "Volkswagen", "Chevrolet", "Ford", "Hyundai", "Renault", "Toyota", "Honda", "Jeep"}

FAIXAS_KM = {
    "Todos (acima de 0 km)": 90_000,
    "Até 20.000 km":        10_000,
    "20.000 – 40.000 km":   30_000,
    "40.000 – 60.000 km":   50_000,
    "60.000 – 80.000 km":   70_000,
    "80.000 – 100.000 km":  90_000,
    "100.000 – 150.000 km": 125_000,
    "Acima de 150.000 km":  175_000,
}

FAIXAS_KM_RANGE = {
    "Todos (acima de 0 km)": (0,      None),
    "Até 20.000 km":        (0,       20_000),
    "20.000 – 40.000 km":   (20_000,  40_000),
    "40.000 – 60.000 km":   (40_000,  60_000),
    "60.000 – 80.000 km":   (60_000,  80_000),
    "80.000 – 100.000 km":  (80_000,  100_000),
    "100.000 – 150.000 km": (100_000, 150_000),
    "Acima de 150.000 km":  (150_000, None),
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


_INFO_GERAL = (
    "Treinado com todos os carros do banco (70.720 registros).\n"
    "• R² = 0.86 — erra em média R$ 8.453\n"
    "• Cobre todas as marcas e modelos disponíveis\n"
    "• Menor precisão por incluir carros de luxo e exóticos junto com populares"
)

_INFO_POPULAR = (
    "Treinado apenas com as 9 marcas mais vendidas no Brasil (58.735 registros).\n"
    "• R² = 0.95 — erra em média R$ 5.303\n"
    "• Marcas: Fiat, VW, Chevrolet, Ford, Hyundai, Renault, Toyota, Honda, Jeep\n"
    "• Mais preciso, porém limitado a essas marcas"
)


def render_filtros() -> dict | None:
    modelo_escolhido = st.radio(
        "Escolha o modelo de estimativa",
        options=["Modelo Geral", "Modelo Popular"],
        index=None,
        horizontal=True,
        captions=[
            "R²=0.86 · Todas as marcas",
            "R²=0.95 · 9 marcas populares",
        ],
    )

    if modelo_escolhido == "Modelo Geral":
        st.info(_INFO_GERAL, icon="ℹ️")
    elif modelo_escolhido == "Modelo Popular":
        st.info(_INFO_POPULAR, icon="ℹ️")
    else:
        return None

    st.divider()

    todas_marcas = _marcas()
    if modelo_escolhido == "Modelo Popular":
        todas_marcas = [m for m in todas_marcas if m in MARCAS_POPULARES]

    marca = st.selectbox("Marca", ["Selecione..."] + todas_marcas)
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

    if faixa_km == "Todos (acima de 0 km)":
        st.warning(
            "Selecione uma faixa específica para maior precisão.",
            icon="⚠️",
        )

    km_min, km_max = FAIXAS_KM_RANGE[faixa_km]
    return {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "cambio": cambio,
        "combustivel": combustivel,
        "direcao": direcao,
        "faixa_km": faixa_km,
        "quilometragem": FAIXAS_KM[faixa_km],
        "km_min": km_min,
        "km_max": km_max,
        "modelo_escolhido": modelo_escolhido,
    }
