import streamlit as st

from services.carro_service import calcular_media_preco, prever_preco


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

        media = calcular_media_preco(
            filtros["marca"], filtros["modelo"], filtros["ano"],
            filtros["cambio"], filtros["combustivel"], filtros["direcao"],
            km_min=filtros.get("km_min", 0),
            km_max=filtros.get("km_max"),
        )
        resultado["media_anuncios"] = media.get("media")
        resultado["desvio_anuncios"] = media.get("desvio")
        resultado["total_anuncios"] = media.get("total", 0)
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

    cols = st.columns(2)
    cols[0].metric(escolha, f"R$ {resultado[chave]:,.0f}")

    media = resultado.get("media_anuncios")
    desvio = resultado.get("desvio_anuncios")
    total = resultado.get("total_anuncios", 0)
    if media is not None:
        cols[1].metric(
            f"Média dos anúncios ({total} encontrados)",
            f"R$ {media:,.0f}",
            delta=f"σ R$ {desvio:,.0f}" if desvio is not None else None,
            delta_color="off",
        )
        if desvio is not None and abs(resultado[chave] - media) > 1.5 * desvio:
            st.caption(
                f"⚠️ A estimativa está fora do desvio padrão dos anúncios "
                f"(desvio: R$ {desvio:,.0f}). Use com cautela."
            )
    else:
        cols[1].caption("Nenhum anúncio encontrado com esses filtros.")

    return resultado
