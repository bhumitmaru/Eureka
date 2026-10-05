import csv, io, logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, Response, flash
from config import Config, ROOT
from database.db import init_db, save_papers, query
from services.data_cleaner import clean_paper
from services.deduplicator import deduplicate
from services.ranking import rank
from services import cache
from api.openalex_api import OpenAlexAPI
from api.crossref_api import CrossrefAPI
from api.semantic_scholar_api import SemanticScholarAPI
from api.arxiv_api import ArxivAPI
from api.europe_pmc_api import EuropePMCAPI

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
app=Flask(__name__); app.config.from_object(Config)
init_db()

def demo_papers():
    with open(ROOT/'data'/'sample_data.csv',newline='',encoding='utf8') as f: return list(csv.DictReader(f))

DEMO_CONFERENCES = [
 {'name':'International Conference on Machine Learning','organizer':'ICML Foundation','date':'July 15–20, 2027','location':'Vienna, Austria','submission_deadline':'2027-02-01','topics':'Machine Learning, Deep Learning, AI','url':'https://icml.cc','source':'Demo dataset'},
 {'name':'IEEE International Conference on Data Engineering','organizer':'IEEE Computer Society','date':'May 3–7, 2027','location':'Bengaluru, India','submission_deadline':'2026-10-15','topics':'Data Engineering, AI, Databases','url':'https://ieeexplore.ieee.org','source':'Demo dataset'},
 {'name':'AAAI Conference on Artificial Intelligence','organizer':'Association for the Advancement of Artificial Intelligence','date':'February 20–27, 2027','location':'Vancouver, Canada','submission_deadline':'2026-08-15','topics':'Artificial Intelligence, NLP, Computer Vision','url':'https://aaai.org','source':'Demo dataset'},
 {'name':'ACM Conference on Health, Inference, and Learning','organizer':'Association for Computing Machinery','date':'June 10–12, 2027','location':'Boston, USA','submission_deadline':'2026-12-05','topics':'Healthcare AI, Machine Learning, Public Health','url':'https://acm-facct.org','source':'Demo dataset'},
 {'name':'International Joint Conference on Artificial Intelligence','organizer':'IJCAI Organization','date':'August 21–27, 2027','location':'Yokohama, Japan','submission_deadline':'2027-01-10','topics':'Knowledge Representation, AI, Robotics','url':'https://ijcai.org','source':'Demo dataset'},
 {'name':'European Conference on Computer Vision','organizer':'ECCV Association','date':'September 5–10, 2027','location':'Milan, Italy','submission_deadline':'2027-03-01','topics':'Computer Vision, Deep Learning, Imaging','url':'https://eccv.ecva.net','source':'Demo dataset'},
]
def search_papers(topic, page=1, source='all'):
    cache_key = f'{topic.lower().strip()}:{page}:{source}:{Config.DEMO_MODE}'
    cached = cache.get(cache_key)
    if cached is not None:
        logging.info('Cache hit for %s', topic); return cached
    if Config.DEMO_MODE: raw=demo_papers()
    else:
        clients={'openalex':OpenAlexAPI(),'crossref':CrossrefAPI(),'semantic':SemanticScholarAPI(),
                 'arxiv':ArxivAPI(),'europepmc':EuropePMCAPI()}
        if source not in clients and source != 'all':
            logging.warning('Unknown source selected: %s', source)
            source = 'all'
        chosen=clients if source=='all' else {source:clients[source]}
        raw=[]
        with ThreadPoolExecutor(max_workers=len(chosen)) as executor:
            futures={executor.submit(client.search, topic, page=page): key for key, client in chosen.items()}
            for future in as_completed(futures):
                key=futures[future]
                try: raw.extend(future.result())
                except Exception as e: logging.warning('%s unavailable: %s',key,e)
    cleaned=[p for p in (clean_paper(x) for x in raw) if p]
    papers, removed=deduplicate(cleaned); logging.info('%d duplicates removed',removed)
    results = rank(papers,topic); cache.set(cache_key, results); return results

@app.route('/')
def index(): return render_template('index.html', demo=Config.DEMO_MODE)
@app.route('/search',methods=['POST'])
def search():
    topic=request.form.get('topic','').strip(); source=request.form.get('source','all')
    if not topic: flash('Please enter a research topic.'); return redirect(url_for('index'))
    papers=search_papers(topic,source=source)
    if not papers and not Config.DEMO_MODE:
        flash('Live sources did not return results. Try another topic, source, or enable demo mode for offline testing.')
    save_papers(papers,topic)
    return render_template('papers.html',papers=papers,topic=topic,demo=Config.DEMO_MODE)
@app.route('/papers')
def papers():
    rows=query('SELECT * FROM papers ORDER BY relevance DESC, id DESC LIMIT 100')
    return render_template('papers.html',papers=rows,topic='Saved papers',demo=Config.DEMO_MODE)
@app.route('/paper/<int:paper_id>')
def paper_detail(paper_id):
    rows=query('SELECT * FROM papers WHERE id=?',(paper_id,))
    if not rows: return redirect(url_for('papers'))
    p=rows[0]; related=query('SELECT * FROM papers WHERE id != ? AND journal=? LIMIT 3',(paper_id,p['journal']))
    return render_template('paper_details.html',paper=p,related=related)
@app.route('/conferences')
def conferences():
    return render_template('conferences.html',conferences=DEMO_CONFERENCES,demo=Config.DEMO_MODE)
@app.route('/dashboard')
def dashboard():
    rows=query('SELECT * FROM papers ORDER BY id DESC')
    stats={'papers':len(rows),'conferences':len(DEMO_CONFERENCES),'authors':len({a for r in rows for a in (r.get('authors') or '').split(',') if a.strip()}),'open':sum(bool(r.get('open_access')) for r in rows)}
    years={}; sources={}
    for r in rows: years[str(r.get('publication_year') or 'Unknown')]=years.get(str(r.get('publication_year') or 'Unknown'),0)+1; sources[r.get('source','Unknown')]=sources.get(r.get('source','Unknown'),0)+1
    return render_template('dashboard.html',stats=stats,years=years,sources=sources)
@app.route('/export/papers.csv')
def export_papers():
    rows=query('SELECT title,authors,publication_year,journal,doi,url,citation_count,source,open_access FROM papers ORDER BY id DESC')
    out=io.StringIO(); pd.DataFrame(rows).to_csv(out, index=False)
    return Response(out.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=eureka_papers.csv'})
if __name__=='__main__': app.run(debug=True,port=5000)
