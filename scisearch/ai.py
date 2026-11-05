import os
from openai import OpenAI

def summarize_articles(topic, articles):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Para ativar a análise por IA, configure OPENAI_API_KEY no arquivo .env. A busca científica funciona sem essa chave.")
    client = OpenAI(api_key=api_key)
    compact = []
    for a in articles:
        compact.append({
            "title": a.get("title"), "year": a.get("year"), "authors": a.get("authors"),
            "abstract": (a.get("abstract") or "")[:3500], "doi": a.get("doi"), "source": a.get("source")
        })
    prompt = f"""
Tema solicitado: {topic}
Analise os metadados e resumos abaixo. Não invente resultados nem complete informações ausentes.
Entregue: (1) síntese temática; (2) convergências e divergências identificáveis;
(3) limitações da evidência disponível; (4) perguntas para aprofundamento.
Diferencie claramente o que está explícito nos resumos do que é interpretação.
Se não houver resumo, informe que não há dados suficientes para avaliar o conteúdo.
Registros: {compact}
"""
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
        instructions="Você é um assistente de pesquisa científica rigoroso. Nunca invente referências, DOI, métodos ou resultados.",
        input=prompt
    )
    return response.output_text
