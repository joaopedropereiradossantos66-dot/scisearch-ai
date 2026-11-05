# SciSearch AI — protótipo funcional

Aplicação web em Streamlit para descoberta de literatura científica.

## O que já funciona
- Busca de publicações na API do OpenAlex e na API REST do Crossref.
- Filtro por intervalo de anos e opção de priorizar acesso aberto no OpenAlex.
- Deduplicação por DOI/título.
- Exibição de autores, periódico, ano, resumo, DOI e link.
- Exportação dos resultados em CSV.
- Geração de referência bibliográfica preliminar.
- Histórico local de pesquisas em SQLite.
- Links de pesquisa direta no Google Acadêmico e SciELO.
- Síntese assistida por IA opcional, com OpenAI API.

## Requisitos
Python 3.10 ou superior.

## Instalação local
1. Extraia o ZIP.
2. Abra o terminal dentro da pasta `scisearch_ai`.
3. Crie um ambiente virtual:
   - Windows: `py -m venv .venv` e `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` e `source .venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Inicie: `streamlit run app.py`

## Ativar a IA
A busca funciona sem chave de IA. Para habilitar a síntese:
1. Copie `.env.example` para `.env`.
2. Preencha `OPENAI_API_KEY` com sua chave da API.
3. No terminal, carregue as variáveis de ambiente (ou use `python-dotenv`/Secrets do Streamlit Cloud).
   Para simplificar, adicione no início de `app.py`:
   `from dotenv import load_dotenv; load_dotenv()`
4. Confira se sua conta da API tem acesso ao modelo configurado em `OPENAI_MODEL`.

**Segurança:** nunca publique sua chave, nunca a coloque no código-fonte e não envie o arquivo `.env` ao GitHub.

## Fontes e limitações
- OpenAlex: API pública de trabalhos acadêmicos. Consulte https://docs.openalex.org/ e https://help.openalex.org/api/
- Crossref: API REST de metadados DOI. Consulte https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Google Acadêmico: link de busca manual; não há API pública oficial para consulta automatizada.
- SciELO: link de pesquisa no portal. A integração automatizada específica deve ser validada conforme os serviços e políticas atuais da SciELO.
- O resultado depende dos metadados fornecidos pelas fontes. Resumo ausente não significa artigo sem conteúdo.
- A referência ABNT é preliminar e precisa de conferência editorial.
- A IA analisa somente os resumos e metadados recuperados, não o texto integral automaticamente.
- O protótipo não substitui protocolo de revisão sistemática, avaliação de risco de viés ou leitura dos textos completos.

## Próximas etapas recomendadas
Autenticação de usuários, banco de dados PostgreSQL, busca SciELO validada, importação de PDF com extração de texto, filtros PRISMA, exportação RIS/BibTeX/DOCX e implantação em nuvem.
