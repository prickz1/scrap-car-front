import streamlit as st

from services.carro_service import listar_anuncios


def render_anuncios(filtros: dict, preco_justo: float | None, desvio: float | None = None) -> None:

    if st.button("Mostrar Anúncios"):
        with st.spinner(""):
            anuncios = listar_anuncios(
                filtros["marca"], filtros["modelo"], filtros["ano"],
                filtros["cambio"], filtros["combustivel"], filtros["direcao"],
                km_min=filtros.get("km_min", 0),
                km_max=filtros.get("km_max"),
            )
        st.session_state["anuncios"] = anuncios

    anuncios = st.session_state.get("anuncios")
    if anuncios is None:
        return

    if not anuncios:
        st.info("Nenhum anúncio encontrado com esses filtros.")
        return

    st.subheader(f"{len(anuncios)} anúncio(s) encontrado(s)")
    for a in anuncios:
        km = f"{int(a['quilometragem']):,} km" if a.get("quilometragem") else "km não informado"
        cor = a.get("cor") or "—"
        local = f"{a.get('cidade') or ''}{'/' + a['estado'] if a.get('estado') else ''}".strip("/")
        titulo = a.get("titulo") or f"{filtros['marca']} {filtros['modelo']} {filtros['ano']}"
        url = a.get("url_anuncio") or "#"
        preco_real = a["preco"]

        with st.container(border=True):
            escolha = filtros.get("modelo_escolhido", "Modelo Geral")
            cols = st.columns(3)

            with cols[0]:
                st.markdown(f"**{titulo}**")
                st.caption(f"{km} · {cor} · {local}")
            with cols[1]:
                st.metric("Preço anunciado", f"R$ {preco_real:,.0f}")

            if preco_justo is not None:
                diff = preco_justo - preco_real
                label = f"R$ {abs(diff):,.0f} {'abaixo' if diff > 0 else 'acima'} do justo"
                cols[2].metric(escolha, f"R$ {preco_justo:,.0f}", delta=label, delta_color="normal" if diff > 0 else "inverse")
                if desvio is not None and abs(diff) > 1.5 * desvio:
                    cols[2].caption("⚠️ Fora do desvio padrão de mercado")

            st.markdown(f'<a href="{url}" target="_blank">Ver anúncio →</a>', unsafe_allow_html=True)
