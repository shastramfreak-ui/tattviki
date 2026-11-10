"""Reproducible pure-Python training baseline for the Tāttvikī Retrieval Systems Lab.

Features: BM25, TF-IDF cosine, RRF, typed graph expansion, per-document ACLs and
Recall@k/Precision@k on visible gold documents. No external API or model.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json
import math
import re

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'corpus.json').read_text(encoding='utf-8'))
DOCS = DATA['documents']
EDGES = DATA['edges']
QUERIES = DATA['queries']
ALIASES = {
 'deactivated':'inactive','disabled':'inactive','closed':'inactive',
 'vendor':'supplier','source':'lineage','feeds':'consumes','depend':'dependency',
 'dependent':'dependency','equipment':'pump','machine':'pump','component':'valve',
 'owns':'owner','approval':'approved','graph':'relationship'
}

def terms(s: str, expand: bool = False) -> list[str]:
    tokens = [t for t in re.findall(r'[a-z0-9]+', s.lower()) if len(t)>1]
    return [ALIASES.get(t,t) for t in tokens] if expand else tokens

def readable(doc: dict, role: str) -> bool:
    if role not in {'viewer','engineer','steward'}:
        raise ValueError('Unknown role; fail closed')
    return role=='steward' or doc['access']=='public' or (role=='engineer' and doc['access']=='engineer')

def bm25(docs: list[dict], query: str) -> list[tuple[str,float]]:
    tokens=[terms(d['title']+' '+d['text']) for d in docs]
    average=sum(map(len,tokens))/max(1,len(tokens))
    ranked=[]
    for d,words in zip(docs,tokens):
        f=Counter(words);s=0.0
        for t in set(terms(query)):
            df=sum(t in x for x in tokens)
            idf=math.log(1+(len(docs)-df+0.5)/(df+0.5))
            if f[t]:s+=idf*f[t]*2.2/(f[t]+1.2*(0.25+0.75*len(words)/max(1,average)))
        ranked.append((d['id'],s))
    return sorted(ranked,key=lambda x:(-x[1],x[0]))

def tfidf(docs: list[dict], query: str) -> list[tuple[str,float]]:
    corpus=[terms(d['title']+' '+d['text'],True) for d in docs]
    freq=Counter(w for wordset in corpus for w in set(wordset))
    def embed(words):
        counted=Counter(words)
        return {w:n*(math.log((1+len(docs))/(1+freq[w]))+1) for w,n in counted.items()}
    q=embed(terms(query,True));nq=math.sqrt(sum(x*x for x in q.values()))
    scores=[]
    for d,words in zip(docs,corpus):
        v=embed(words); nv=math.sqrt(sum(x*x for x in v.values()))
        cos=sum(x*v.get(w,0) for w,x in q.items())/(nq*nv) if nq and nv else 0.0
        scores.append((d['id'],cos))
    return sorted(scores,key=lambda x:(-x[1],x[0]))

def rrf(*rankings: list[tuple[str,float]], k: int=60) -> list[tuple[str,float]]:
    results=Counter()
    for ranked in rankings:
        for rank,(doc,score) in enumerate((r for r in ranked if r[1]>0),1):
            results[doc]+=1/(k+rank)
    return sorted(results.items(),key=lambda x:(-x[1],x[0]))

def traverse(start: set[str], hops: int=2, role: str="viewer") -> tuple[set[str], list[dict]]:
    visited=set(start);frontier=set(start);links=[]
    for h in range(hops):
        following=set()
        for edge in EDGES:
            if not readable(edge,role):continue
            a,b=edge['a'],edge['b']
            if a in frontier or b in frontier:
                target=b if a in frontier else a
                if target not in visited:
                    visited.add(target);following.add(target);links.append({**edge,'hop':h+1})
        frontier=following
        if not frontier:break
    return visited,links

def search(query: str, mode: str='hybrid', role: str='viewer', top_k: int=5, hops: int=2) -> dict:
    if mode not in {'keyword','vector','hybrid','graph'}:raise ValueError('Unknown search method')
    visible=[d for d in DOCS if readable(d,role)]
    lex=bm25(visible,query);vec=tfidf(visible,query)
    ranks=lex if mode=='keyword' else vec if mode=='vector' else rrf(lex,vec)
    ranks=[(id,score) for id,score in ranks if score>0]
    paths=[]
    if mode=='graph':
        seed=set()
        for d in visible:
            if any(e.lower() in query.lower() or e.lower().replace('-',' ') in query.lower() or e.lower() in terms(query) for e in d['entities']):
                seed.update(d['entities'])
        for edge in EDGES:
            if not readable(edge,role):continue
            for e in (edge['a'],edge['b']):
                if e.lower() in query.lower() or e.lower().replace('-',' ') in query.lower():seed.add(e)
        lookup={d['id']:d for d in visible}
        for id,_ in ranks[:3]:seed.update(lookup[id]['entities'])
        visited,paths=traverse(seed,hops,role)
        base=dict(ranks)
        scored=[]
        for d in visible:
            overlap=len(set(d['entities'])&visited)
            score=0.2*overlap+base.get(d['id'],0)
            if score>0:scored.append((d['id'],score))
        ranks=sorted(scored,key=lambda x:(-x[1],x[0]))
    selected=ranks[:top_k]
    preset=next((p for p in QUERIES if p['q']==query),None)
    visible_ids={d['id'] for d in visible}
    gold={id for id in preset['gold'] if id in visible_ids} if preset else set()
    found=len(gold&{doc for doc,_ in selected})
    return {'results':selected,'visible':len(visible),'links':paths,
        'gold':sorted(gold),'recall_at_k':found/len(gold) if gold else None,
        'precision_at_k':found/len(selected) if preset and selected else None}

def main():
    import argparse
    parser=argparse.ArgumentParser(description='Compare BM25, TF-IDF, RRF and typed graph expansion (not a neural RAG system)')
    parser.add_argument('--query',default=QUERIES[0]['q'])
    parser.add_argument('--role',choices=['viewer','engineer','steward'],default='viewer')
    parser.add_argument('--mode',choices=['keyword','vector','hybrid','graph'],default='hybrid')
    parser.add_argument('--top-k',type=int,default=5)
    args=parser.parse_args();out=search(args.query,args.mode,args.role,args.top_k)
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
