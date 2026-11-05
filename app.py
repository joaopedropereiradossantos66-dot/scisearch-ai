from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import pandas as pd
from scisearch.search import search_all
from scisearch.ai import summarize_articles
from scisearch.storage import save_search, load_history
from scisearch.references import to_abnt

st.set_page_config(page_title="SciSearch AI", page_icon="🔬", layout="wide")
st.markdown("""
<style>
.main {background: #f7fafc;}
.block-container {padding-top: 1.5rem; max-width: 1250px;}
.hero {padding: 1.4rem 1.6rem; border-radius: 18px; background: linear-gradient(120deg,#102a43,#087f8c); color:white;}
.hero h1 {color:white; margin:0;}
.hero p {color:#d9f3f4; margin:.35rem 0 0;}
.small-muted {color:#64748b;font-size:.88rem}
</style>
<div class="hero">
<h1>🔬 SciSearch AI</h1>
<p>Pesquisa científica inteligente • Artigos • Análise • Referências</p>
</div>
""", unsafe_allow_html=True)

st.write("")
with st.sidebar:
    st.header("Configurações da busca")
    sources = st.multiselect("Fontes", ["OpenAlex", "Crossref"], default=["OpenAlex", "Crossref"])
    years = st.slider("Ano de publicação", 1990, 2026, (2021, 2026))
    limit = st.select_slider("Resultados por fonte", options=[10, 20, 30, 50], value=20)
    only_oa = st.checkbox("Priorizar artigos de acesso aberto", value=False)
    st.caption("Google Acadêmico e SciELO: atalhos oficiais de pesquisa. Não fazemos raspagem automatizada dessas plataformas.")

st.subheader("Encontre literatura científica")
query = st.text_input("Tema, pergunta ou palavras-chave", placeholder="Ex.: fisioterapia na prevenção de quedas em idosos")
col1, col2 = st.columns([1,1])
with col1:
    search_btn = st.button("🔎 Pesquisar artigos", type="primary", use_container_width=True)
with col2:
    st.link_button("Abrir Google Acadêmico", "https://scholar.google.com/", use_container_width=True)

if search_btn:
    if not query.strip():
        st.warning("Digite um tema para pesquisar.")
    elif not sources:
        st.warning("Selecione pelo menos uma fonte.")
    else:
        with st.spinner("Consultando bases científicas..."):
            results, errors = search_all(query, sources, years[0], years[1], limit, only_oa)
        st.session_state["results"] = results
        st.session_state["query"] = query
        save_search(query, len(results))
        if errors:
            for err in errors:
                st.warning(err)

results = st.session_state.get("results", [])
if results:
    st.success(f"{len(results)} registros encontrados para: {st.session_state.get('query','')}")
    df = pd.DataFrame(results)
    if "year" in df:
        df["year"] = df["year"].fillna("—")
    st.download_button("⬇️ Exportar resultados em CSV", df.to_csv(index=False).encode("utf-8-sig"),
                       file_name="scisearch_resultados.csv", mime="text/csv")
    for idx, item in enumerate(results):
        title = item.get("title") or "Título não informado"
        with st.expander(f"{idx+1}. {title} ({item.get('year') or 'ano não informado'})", expanded=(idx == 0)):
            st.write("**Autores:**", item.get("authors") or "Não informado")
            st.write("**Periódico/fonte:**", item.get("venue") or "Não informado")
            st.write("**DOI:**", item.get("doi") or "Não informado")
            st.write("**Resumo:**", item.get("abstract") or "Resumo não disponibilizado pela base.")
            if item.get("url"):
                st.markdown(f"[Abrir registro ou artigo]({item['url']})")
            st.code(to_abnt(item), language=None)
    st.divider()
    st.subheader("Análise assistida por IA")
    st.caption("A análise usa apenas os metadados e resumos recuperados. Não substitui a leitura crítica do texto completo.")
    if st.button("✨ Sintetizar os resultados com IA"):
        with st.spinner("Preparando síntese..."):
            try:
                st.markdown(summarize_articles(st.session_state.get("query", query), results[:15]))
            except Exception as e:
                st.error(str(e))
else:
    st.info("Faça uma busca para visualizar artigos, resumos, DOI e referências.")
    st.markdown("**Bases integradas:** OpenAlex e Crossref. **Complementos:** links de busca no Google Acadêmico e SciELO.")
    if query.strip():
        from urllib.parse import quote_plus
        q = quote_plus(query)
        c1, c2 = st.columns(2)
        c1.link_button("Pesquisar este tema no Google Acadêmico", f"https://scholar.google.com/scholar?q={q}", use_container_width=True)
        c2.link_button("Pesquisar este tema na SciELO", f"https://search.scielo.org/?q={q}&lang=pt", use_container_width=True)

with st.expander("Histórico de pesquisas"):
    hist = load_history()
    if hist:
        st.dataframe(pd.DataFrame(hist), use_container_width=True, hide_index=True)
    else:
        st.caption("As pesquisas feitas neste dispositivo aparecerão aqui.")
st.caption("SciSearch AI — protótipo inicial. Confirme sempre os dados bibliográficos na página original antes de citar.")
