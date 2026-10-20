import streamlit as st

from services.carro_service import (
    listar_marcas,
    listar_modelos,
    listar_anos,
    listar_cambios,
    listar_combustiveis,
    listar_direcoes,
    prever_preco,
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


st.set_page_config(page_title="Scrap Carros", layout="wide")
st.title("Estimativa de Preço Justo")

# --- Marca ---
marca = st.selectbox("Marca", ["Selecione..."] + _marcas())
if marca == "Selecione...":
    st.stop()

# --- Modelo ---
modelo = st.selectbox("Modelo", ["Selecione..."] + _modelos(marca), key=f"m_{marca}")
if modelo == "Selecione...":
    st.stop()

# --- Ano ---
anos = _anos(marca, modelo)
if not anos:
    st.info("Nenhum dado encontrado para esse modelo.")
    st.stop()
ano = st.selectbox("Ano", anos, key=f"a_{marca}_{modelo}")

# --- Câmbio ---
cambios = _cambios(marca, modelo, ano)
if not cambios:
    st.info("Nenhum dado de câmbio encontrado.")
    st.stop()
cambio = st.selectbox("Câmbio", cambios, key=f"cb_{marca}_{modelo}_{ano}")

# --- Combustível ---
combustiveis = _combustiveis(marca, modelo, ano)
if not combustiveis:
    st.info("Nenhum dado de combustível encontrado.")
    st.stop()
combustivel = st.selectbox("Combustível", combustiveis, key=f"co_{marca}_{modelo}_{ano}")

# --- Direção ---
direcoes = _direcoes(marca, modelo, ano)
if not direcoes:
    st.info("Nenhum dado de direção encontrado.")
    st.stop()
direcao = st.selectbox("Direção", direcoes, key=f"d_{marca}_{modelo}_{ano}")

# --- Quilometragem ---
faixa_km = st.selectbox("Quilometragem", list(FAIXAS_KM.keys()), key=f"km_{marca}_{modelo}_{ano}")
quilometragem = FAIXAS_KM[faixa_km]

# --- Avaliar ---
if st.button("Estimar Preço Justo"):
    with st.spinner(""):
        resultado = prever_preco(marca, modelo, ano, cambio, combustivel, direcao, quilometragem)

    if not resultado:
        st.warning("Modelo ainda carregando. Aguarde alguns instantes e tente novamente.")
        st.stop()

    st.subheader("Estimativa de Preço Justo")

    modelos_resultado = []
    if "geral" in resultado:
        modelos_resultado.append(("Modelo Geral", resultado["geral"]))
    if "popular" in resultado:
        modelos_resultado.append(("Modelo Popular", resultado["popular"]))

    colunas = st.columns(len(modelos_resultado))
    for col, (label, preco) in zip(colunas, modelos_resultado):
        col.metric(label, f"R$ {preco:,.0f}")
