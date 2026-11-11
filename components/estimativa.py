import streamlit as st

from services.carro_service import prever_preco


def render_estimativa(filtros: dict) -> dict | None:
    if st.button("Estimar Preço Justo"):
        with st.spinner(""):
            resultado = prever_preco(
                filtros["marca"], filtros["modelo"], filtros["ano"],
                filtros["cambio"], filtros["combustivel"], filtros["direcao"],
                filtros["quilometragem"],
            )
        if not resultado:
            st.warning("Modelo ainda carregando. Aguarde alguns instantes e tente novamente.")
            return None
        st.session_state["resultado"] = resultado

    resultado = st.session_state.get("resultado")
    if not resultado:
        return None

    st.subheader("Estimativa de Preço Justo")
    modelos_resultado = []
    if "geral" in resultado:
        modelos_resultado.append(("Modelo Geral", resultado["geral"], None))
    if "popular" in resultado:
        modelos_resultado.append(("Modelo Popular", resultado["popular"], None))
    if "faixas" in resultado:
        faixas = resultado["faixas"]
        label = f"Modelo por Faixa ({faixas['faixa']})"
        modelos_resultado.append((label, faixas["preco"], None))

    colunas = st.columns(len(modelos_resultado))
    for col, (label, preco, _) in zip(colunas, modelos_resultado):
        col.metric(label, f"R$ {preco:,.0f}")

    return resultado
