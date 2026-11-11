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

    escolha = filtros["modelo_escolhido"]
    chave = "geral" if escolha == "Modelo Geral" else "popular"

    if chave not in resultado:
        st.warning(f"{escolha} não disponível para essa marca. Tente o Modelo Geral.")
        return None

    st.metric(escolha, f"R$ {resultado[chave]:,.0f}")
    return resultado
