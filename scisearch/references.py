def to_abnt(item):
    authors = (item.get("authors") or "AUTORIA NÃO INFORMADA").upper()
    title = item.get("title") or "Título não informado"
    venue = item.get("venue") or "Periódico não informado"
    year = item.get("year") or "s.d."
    doi = item.get("doi")
    ref = f"{authors}. {title}. {venue}, {year}."
    if doi:
        ref += f" DOI: https://doi.org/{doi}."
    elif item.get("url"):
        ref += f" Disponível em: {item['url']}."
    return ref
