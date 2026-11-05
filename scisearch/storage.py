import sqlite3
from pathlib import Path
DB = Path("scisearch_history.db")

def _connect():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS searches
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, result_count INTEGER,
                    searched_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    con.commit()
    return con

def save_search(query, count):
    with _connect() as con:
        con.execute("INSERT INTO searches(query, result_count) VALUES (?, ?)", (query, count))

def load_history():
    with _connect() as con:
        rows = con.execute("SELECT query, result_count, searched_at FROM searches ORDER BY id DESC LIMIT 30").fetchall()
    return [{"Pesquisa": r[0], "Resultados": r[1], "Data": r[2]} for r in rows]
