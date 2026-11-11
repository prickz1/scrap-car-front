import streamlit as st

from components.filtros import render_filtros
from components.estimativa import render_estimativa
from components.anuncios import render_anuncios

st.set_page_config(page_title="Scrap Carros", layout="wide")
st.title("Estimativa de Preço Justo")

filtros = render_filtros()
if filtros is None:
    st.stop()

# reseta resultado e anúncios ao mudar qualquer filtro
filtro_key = "|".join(str(filtros[k]) for k in ["marca", "modelo", "ano", "cambio", "combustivel", "direcao", "faixa_km", "modelo_escolhido"])
if st.session_state.get("filtro_key") != filtro_key:
    st.session_state["filtro_key"] = filtro_key
    st.session_state["resultado"] = None
    st.session_state["anuncios"] = None

st.divider()

resultado = render_estimativa(filtros)
if resultado is None:
    st.stop()

st.divider()

chave = "geral" if filtros["modelo_escolhido"] == "Modelo Geral" else "popular"
render_anuncios(filtros, resultado.get(chave))
