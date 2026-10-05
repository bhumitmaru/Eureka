import sqlite3
from config import Config

SCHEMA='''CREATE TABLE IF NOT EXISTS papers (id INTEGER PRIMARY KEY, title TEXT, authors TEXT, abstract TEXT, publication_year INTEGER, journal TEXT, doi TEXT, url TEXT, citation_count INTEGER, source TEXT, open_access INTEGER, relevance INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS conferences (id INTEGER PRIMARY KEY, name TEXT, organizer TEXT, date TEXT, location TEXT, country TEXT, submission_deadline TEXT, registration_deadline TEXT, topics TEXT, url TEXT, source TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS searches (id INTEGER PRIMARY KEY, query TEXT, timestamp TEXT DEFAULT CURRENT_TIMESTAMP, result_count INTEGER);'''
def conn():
    c=sqlite3.connect(Config.DATABASE); c.row_factory=sqlite3.Row; return c
def init_db():
    c=conn(); c.executescript(SCHEMA); c.commit(); c.close()
def save_papers(papers, query):
    c=conn(); c.execute('INSERT INTO searches(query,result_count) VALUES (?,?)',(query,len(papers)))
    c.executemany('INSERT INTO papers(title,authors,abstract,publication_year,journal,doi,url,citation_count,source,open_access,relevance) VALUES (:title,:authors,:abstract,:publication_year,:journal,:doi,:url,:citation_count,:source,:open_access,:relevance)',papers); c.commit(); c.close()
def query(sql,args=()):
    c=conn(); rows=[dict(x) for x in c.execute(sql,args).fetchall()]; c.close(); return rows
