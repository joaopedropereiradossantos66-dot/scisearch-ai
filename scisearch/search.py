import requests
from urllib.parse import quote
from datetime import datetime

HEADERS = {"User-Agent": "SciSearchAI/0.1 (academic literature discovery)"}

def _year(value):
    try:
        return int(value) if value else None
    except (TypeError, ValueError):
        return None

def search_openalex(query, year_from, year_to, limit, only_oa):
    params = {"search": query, "per-page": limit,
              "filter": f"from_publication_date:{year_from}-01-01,to_publication_date:{year_to}-12-31"}
    if only_oa:
        params["filter"] += ",is_oa:true"
    r = requests.get("https://api.openalex.org/works", params=params, headers=HEADERS, timeout=25)
    r.raise_for_status()
    data = r.json()
    out = []
    for w in data.get("results", []):
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        authors = ", ".join(a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])[:8])
        abstract = ""
        inv = w.get("abstract_inverted_index") or {}
        if inv:
            words = []
            for word, positions in inv.items():
                for p in positions:
                    words.append((p, word))
            abstract = " ".join(word for _, word in sorted(words))
        out.append({
            "title": w.get("title"), "year": _year(w.get("publication_year")),
            "authors": authors, "venue": (w.get("primary_location") or {}).get("source", {}).get("display_name"),
            "doi": doi, "url": w.get("doi") or w.get("id"), "abstract": abstract,
            "source": "OpenAlex", "open_access": (w.get("open_access") or {}).get("is_oa", False),
            "citations": w.get("cited_by_count", 0)
        })
    return out

def search_crossref(query, year_from, year_to, limit):
    params = {"query": query, "rows": limit,
              "filter": f"from-pub-date:{year_from},until-pub-date:{year_to}",
              "select": "DOI,title,author,published,container-title,URL,type"}
    r = requests.get("https://api.crossref.org/works", params=params, headers=HEADERS, timeout=25)
    r.raise_for_status()
    out = []
    for w in r.json().get("message", {}).get("items", []):
        date_parts = ((w.get("published") or {}).get("date-parts") or [[None]])[0]
        year = _year(date_parts[0] if date_parts else None)
        authors = ", ".join(" ".join(filter(None, [a.get("given"), a.get("family")])) for a in w.get("author", [])[:8])
        title = (w.get("title") or [None])[0]
        venue = (w.get("container-title") or [None])[0]
        doi = w.get("DOI")
        out.append({"title": title, "year": year, "authors": authors, "venue": venue,
                    "doi": doi, "url": f"https://doi.org/{doi}" if doi else w.get("URL"),
                    "abstract": "", "source": "Crossref", "open_access": None, "citations": None})
    return out

def search_all(query, sources, year_from, year_to, limit, only_oa=False):
    results, errors = [], []
    for source in sources:
        try:
            if source == "OpenAlex":
                results.extend(search_openalex(query, year_from, year_to, limit, only_oa))
            elif source == "Crossref":
                results.extend(search_crossref(query, year_from, year_to, limit))
        except requests.RequestException as e:
            errors.append(f"Falha ao consultar {source}: {e}")
        except Exception as e:
            errors.append(f"Erro em {source}: {e}")
    # Deduplicação por DOI; na ausência dele, por título normalizado.
    unique = {}
    for item in results:
        key = ("doi:" + item["doi"].lower()) if item.get("doi") else ("title:" + (item.get("title") or "").strip().lower())
        if key not in unique or (not unique[key].get("abstract") and item.get("abstract")):
            unique[key] = item
    return sorted(unique.values(), key=lambda x: (x.get("year") or 0, x.get("citations") or 0), reverse=True), errors
