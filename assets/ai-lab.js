/* Tāttvikī v11 — fully local, deterministic search methods training lab.
   TF-IDF is a lexical vector proxy; this lab DOES NOT generate neural embeddings or LLM answers. */
(() => {
'use strict';
const docRows=[
 ['D01','Northforge supplier record','Northforge Components is an approved industrial valve supplier. Supplier S-104 supplies Valve-742 for the East Plant.','supplier','public',['Northforge','Valve-742','Supplier-S104']],
 ['D02','Valve-742 installation','Valve-742 is installed in Pump-3 at East Plant. The replacement valve is compatible with the PX-4 pump assembly.','asset','engineer',['Valve-742','Pump-3','East-Plant']],
 ['D03','Pump-3 service plan','Maintenance Plan MP-9 covers Pump-3. A maintenance task was postponed pending arrival of the Valve-742 replacement.','maintenance','engineer',['Pump-3','Maintenance-MP9','Valve-742']],
 ['D04','Pump-3 maintenance approval','Approval APR-81 delayed Pump-3 service after the valve shipment missed the agreed delivery window. Engineer sign-off required.','approval','steward',['Pump-3','Approval-APR81']],
 ['D05','East Plant component register','East Plant operates Pump-3 and Sensor-17. Component replacement impact requires asset owner review.','asset','public',['East-Plant','Pump-3','Sensor-17']],
 ['D06','Customer 360 data product','Customer 360 is a governed data product. The Data Governance team is its owner and steward.','catalog','public',['Customer360','Data-Governance']],
 ['D07','Customer 360 source lineage','Customer 360 consumes CRM Accounts and ERP Parties datasets. The CRM is the system of record for contact preferences.','lineage','engineer',['Customer360','CRM-Accounts','ERP-Parties']],
 ['D08','CRM Accounts catalog entry','CRM Accounts dataset is produced by the Customer Platform application and feeds Customer 360. Its catalog owner is CRM Operations.','catalog','public',['CRM-Accounts','Customer-Platform','CRM-Operations']],
 ['D09','ERP Parties metadata','ERP Parties is an ERP source dataset containing supplier and customer party master identifiers. It contributes to Customer 360.','metadata','public',['ERP-Parties','Customer360']],
 ['D10','Data product access policy','Access to restricted data products requires an approved purpose, group-based permissions, and a current owner approval.','policy','public',['Access-Policy','Data-Governance']],
 ['D11','Audit control for data access','Every restricted data product access decision records requester, purpose, approver, policy version and expiry.','policy','steward',['Access-Policy','Approval-APR81']],
 ['D12','Reference-data status scheme','Party status is governed as a controlled vocabulary. Code ACT means Active and code INA means Inactive or deactivated.','rdm','public',['Party-Status','Code-ACT','Code-INA']],
 ['D13','Customer status mapping','The CRM value DISABLED maps to approved Party Status code INA. Mapping owner is Data Governance.','rdm','engineer',['Code-INA','Data-Governance']],
 ['D14','Supplier risk register','Northforge risk status was put under review after two late shipments. Vendor Risk Office owns the risk review.','supplier','steward',['Northforge','Vendor-Risk']],
 ['D15','Supplier contract metadata','The Northforge Components supply contract for Valve-742 contains replacement lead-time commitments and escalation policy.','supplier','public',['Northforge','Valve-742','Contract-44']],
 ['D16','Vendor risk oversight','Vendor Risk Office monitors repeated supplier delays. A risk flag does not automatically mean the supplier is deactivated.','policy','public',['Vendor-Risk','Northforge']],
 ['D17','Graph query design for dependencies','Dependency impact is traced by supplier supplies component, component installedIn asset, and asset governedBy maintenance plan.','architecture','public',['Northforge','Valve-742','Pump-3','Maintenance-MP9']],
 ['D18','Vector index engineering note','Enterprise search indexes document chunks with vector dimensions, model versions and document-level access controls.','architecture','public',['Search-Index']],
 ['D19','Hybrid retrieval architecture','Hybrid search combines BM25 keyword ranking and TF-IDF or neural vector ranking using reciprocal rank fusion. A reranker is optional.','architecture','public',['Search-Index']],
 ['D20','Context graph decision memory','A decision graph links an action to actor, evidence snapshot, applicable policy version, and recorded time.','architecture','public',['Decision-Graph','Approval-APR81']],
 ['D21','Graph provenance contract','Each extracted graph relation must link to the source document and its revision, so downstream explanations are auditable.','metadata','public',['Decision-Graph','Search-Index']],
 ['D22','Incident 917 critical alert','Incident INC-917 reported pressure anomalies for Sensor-17. The alert requires on-call engineer triage.','maintenance','engineer',['Sensor-17','East-Plant']],
 ['D23','Document access restrictions','Viewer access allows only public documents. Engineers may read engineering records; stewards may additionally inspect approval and risk records.','policy','public',['Access-Policy']],
 ['D24','Source freshness and stale index','The supplier-risk index checkpoint was recorded before the latest ERP update. Results must show source and ingestion timestamps.','metadata','steward',['Northforge','Search-Index']],
 ['D25','GraphRAG corpus-level summary','GraphRAG local search resolves entities and expands relevant text; global search can summarize detected communities across a corpus.','architecture','public',['Search-Index','Decision-Graph']],
 ['D26','Policy override temporal context','An emergency purchasing exception expires on the next review date. Approvals must be rechecked against valid time.','approval','steward',['Approval-APR81','Access-Policy']],
 ['D27','Customer 360 validation policy','Customer 360 publication requires a named steward, lineage evidence and documented quality checks before release.','policy','public',['Customer360','Data-Governance']],
 ['D28','Asset dependency semantic model','The maintenance ontology defines Supplier, Component, Machine, Site and MaintenancePlan classes with typed property paths.','ontology','public',['Northforge','Valve-742','Pump-3','East-Plant','Maintenance-MP9']]
];
const DOCS=docRows.map(([id,title,text,kind,access,entities])=>({id,title,text,kind,access,entities}));
const EDGES=[
 ['Northforge','supplies','Valve-742'],['Northforge','governedBy','Vendor-Risk'],['Northforge','coveredBy','Contract-44'],
 ['Valve-742','installedIn','Pump-3'],['Pump-3','locatedAt','East-Plant'],['Pump-3','governedBy','Maintenance-MP9'],
 ['Pump-3','affectedBy','Approval-APR81'],['East-Plant','hasSensor','Sensor-17'],['Customer360','ownedBy','Data-Governance'],
 ['Customer360','consumes','CRM-Accounts'],['Customer360','consumes','ERP-Parties'],['CRM-Accounts','producedBy','Customer-Platform'],
 ['CRM-Accounts','ownedBy','CRM-Operations'],['Party-Status','hasConcept','Code-ACT'],['Party-Status','hasConcept','Code-INA'],
 ['Access-Policy','approvedBy','Data-Governance'],['Code-INA','managedBy','Data-Governance'],
 ['Approval-APR81','appliesPolicy','Access-Policy'],['Approval-APR81','recordedIn','Decision-Graph'],
 ['Search-Index','provenanceTrackedBy','Decision-Graph']
].map(([a,relation,b])=>({a,relation,b,access:
 (b==='Approval-APR81'||a==='Approval-APR81')?'steward':
 (a==='Valve-742'&&b==='Pump-3'||a==='Pump-3'&&b==='Maintenance-MP9')?'engineer':'public'}));
const PRESETS=[
 {q:'Which assets depend on Northforge Valve-742?',gold:['D01','D02','D03','D17','D28'],explain:'Multi-hop dependency across supplier, component and maintenance plan.'},
 {q:'Who owns Customer 360 and which source datasets feed it?',gold:['D06','D07','D08','D09'],explain:'Catalog ownership and source lineage require compatible entity identifiers.'},
 {q:'How is data product access approved and audited?',gold:['D10','D11','D23'],explain:'Keyword precision and policy citations; steward-only decisions must remain restricted.'},
 {q:'Which reference code means deactivated customer?',gold:['D12','D13'],explain:'Exact approved code INA, including a synonym and a local-to-approved mapping.'},
 {q:'Why was Pump-3 service delayed?',gold:['D03','D04'],explain:'Answer requires engineering context plus approval evidence unavailable to viewers.'},
 {q:'What is the latest risk on Northforge supplier?',gold:['D14','D16','D24'],explain:'A current risk claim requires freshness and role-based access to risk records.'}
];
const ALIASES={'deactivated':'inactive','disabled':'inactive','closed':'inactive','vendor':'supplier','thirdparty':'supplier','source':'lineage','feeds':'consumes','dependent':'dependency','depend':'dependency','related':'relationship','engine':'machine','machine':'pump','equipment':'pump','owns':'owner','approval':'approved','audit':'audited','index':'retrieval','graph':'relationship','parts':'component','component':'valve'};
const tokenize=(s)=>String(s||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/).filter(w=>w.length>1);
const expand=(arr)=>arr.map(w=>ALIASES[w]||w);
const counts=(a)=>a.reduce((d,w)=>(d[w]=(d[w]||0)+1,d),{});
const canRead=(doc,role)=>role==='steward'||doc.access==='public'||role==='engineer'&&doc.access==='engineer';
function scoreBM25(docs,query){
  const terms=[...new Set(tokenize(query))]; const average=docs.reduce((s,d)=>s+tokenize(d.title+' '+d.text).length,0)/Math.max(1,docs.length);
  return docs.map(d=>{let tok=tokenize(d.title+' '+d.text),freq=counts(tok),sum=0;
    for(let t of terms){const df=docs.filter(x=>tokenize(x.title+' '+x.text).includes(t)).length;
      const idf=Math.log(1+(docs.length-df+0.5)/(df+0.5)); let f=freq[t]||0;
      if(f)sum+=idf*(f*2.2)/(f+1.2*(0.25+0.75*tok.length/average));}
    return {id:d.id,score:sum};}).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
}
function scoreVector(docs,query){
 const terms=docs.map(d=>expand(tokenize(d.title+' '+d.text)));
 const qterms=expand(tokenize(query)); const df={}; terms.forEach(t=>new Set(t).forEach(w=>df[w]=(df[w]||0)+1));
 const idf=(t)=>Math.log((1+docs.length)/(1+(df[t]||0)))+1;
 const vec=(tokens)=>{let m=counts(tokens);for(let k of Object.keys(m))m[k]=m[k]*idf(k);return m;};
 const qv=vec(qterms), qn=Math.hypot(...Object.values(qv));
 return docs.map((d,i)=>{let dv=vec(terms[i]),dn=Math.hypot(...Object.values(dv));const dot=Object.entries(qv).reduce((s,[w,v])=>s+v*(dv[w]||0),0);
  return {id:d.id,score:qn&&dn?dot/(qn*dn):0};}).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
}
const rrf=(rankings,k=60)=>{let score={};rankings.forEach(r=>r.filter(x=>x.score>0).forEach((x,i)=>score[x.id]=(score[x.id]||0)+1/(k+i+1)));
 return Object.entries(score).map(([id,v])=>({id,score:v})).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));};
function buildNeighborhood(seed,hops,role='viewer'){
 let visited=new Set(seed),frontier=new Set(seed),traced=[];
 for(let h=0;h<hops;h++){let next=new Set();
  for(let e of EDGES){if(canRead({access:e.access},role)&&(frontier.has(e.a)||frontier.has(e.b))){
   const v=frontier.has(e.a)?e.b:e.a;
   if(!visited.has(v)){visited.add(v);next.add(v);traced.push({...e,hop:h+1});}
  }}frontier=next;if(!frontier.size)break;}
 return {entities:visited,traced};
}
const state={query:PRESETS[0].q,role:'viewer',mode:'hybrid',hops:2,topK:5,preset:0,runs:0,last:null};
function retrieve(opts={}){
 const {query=state.query,role=state.role,mode=state.mode,hops=state.hops,topK=state.topK}=opts;
 const visible=DOCS.filter(d=>canRead(d,role));let lex=scoreBM25(visible,query),vec=scoreVector(visible,query);
 const core=mode==='keyword'?lex:mode==='vector'?vec:rrf([lex,vec]);
 const scored=core.filter(x=>x.score>0),rankIds=scored.map(x=>x.id);
 let neighborhood={entities:new Set(),traced:[]}, hits=scored.map(x=>({...x,source:'retrieval'}));
 if(mode==='graph'){
  let seed=new Set(visible.filter(d=>d.entities.some(e=>tokenize(query).includes(e.toLowerCase())||query.toLowerCase().includes(e.toLowerCase().replace(/-/g,' ')))).flatMap(d=>d.entities));
  for(let term of EDGES.filter(e=>canRead({access:e.access},role)).flatMap(e=>[e.a,e.b])){
   if(query.toLowerCase().includes(term.toLowerCase())||query.toLowerCase().includes(term.toLowerCase().replace(/-/g,' ')))seed.add(term);
  }
  for(let d of scored.slice(0,3).map(x=>visible.find(y=>y.id===x.id)))if(d) d.entities.forEach(e=>seed.add(e));
  neighborhood=buildNeighborhood(seed,hops,role);
  const base=new Map(scored.map((x,i)=>[x.id,{...x,baseRank:i+1}]));
  hits=visible.map(d=>{let overlap=d.entities.filter(e=>neighborhood.entities.has(e)).length; let original=base.get(d.id);return {id:d.id,score:overlap*0.20+(original?.score||0),source:overlap?'graph-expanded':'retrieval',overlap};})
    .filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
 }
 const selected=hits.slice(0,topK).map((x,i)=>({...x,rank:i+1,document:visible.find(d=>d.id===x.id),lexical:lex.find(y=>y.id===x.id)?.score||0,vector:vec.find(y=>y.id===x.id)?.score||0}));
 const preset=PRESETS.find(p=>p.q===query);const accessibleGold=preset?preset.gold.filter(id=>visible.some(d=>d.id===id)):[];
 const matched=preset?selected.filter(h=>accessibleGold.includes(h.id)).length:null;
 return {selected,visible:visible.length,hidden:DOCS.length-visible.length,mode,lex,vec,neighborhood,
    recall:preset&&accessibleGold.length?matched/accessibleGold.length:null,
    precision:preset&&selected.length?matched/selected.length:null,
    gold:accessibleGold,unavailableGold:preset?preset.gold.length-accessibleGold.length:0,preset};
}
const esc=(s)=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=(n)=>Number(n).toFixed(3);
function graphHTML(result){
 const entityList=[...result.neighborhood.entities].slice(0,28),edges=result.neighborhood.traced.slice(0,24);
 if(state.mode!=='graph')return `<div class="ai-hint">Switch to <strong>Graph expansion</strong> to follow typed edges and inspect the supporting evidence.</div>`;
 return `<div class="ai-graph-data"><div><b>${entityList.length}</b><span>matching graph entities</span></div><div><b>${edges.length}</b><span>traversed links</span></div><div><b>${state.hops}</b><span>maximum hops</span></div></div>
 <div class="ai-relations" aria-label="Graph path trace">${edges.map(e=>`<div class="ai-edge"><span>${esc(e.a)}</span><code>${esc(e.relation)} →</code><span>${esc(e.b)}</span></div>`).join('')||'<p>No typed graph links for this query. Try a supplier or product query.</p>'}</div>`;
}
function resultsHTML(){let r=state.last||retrieve();state.last=r;
 return `<section class="ai-results"><div class="ai-metrics">
 <div><strong>${r.selected.length}</strong><small>evidence results</small></div><div><strong>${r.visible}</strong><small>authorized sources</small></div><div><strong>${r.recall===null?'—':Math.round(r.recall*100)+'%'}</strong><small>Recall@${state.topK} (visible gold)</small></div><div><strong>${r.precision===null?'—':Math.round(r.precision*100)+'%'}</strong><small>Precision@${state.topK}</small></div></div>
 ${r.preset?`<div class="ai-explainer"><strong>Question intent:</strong> ${esc(r.preset.explain)} <span class="ai-small">Gold evidence judged for this synthetic case: ${esc(r.gold.join(', ')||'none visible')} ${r.unavailableGold?`(${r.unavailableGold} restricted)` : ''}</span></div>`:'<div class="ai-explainer">Custom query: results are ranked, but metrics require a labelled relevance set.</div>'}
 <div class="ai-result-grid"><div class="ai-doc-list"><div class="ai-subhead"><h3>Ranked source evidence</h3><span>Original fictional source snippets · no generated answers</span></div>
 ${r.selected.map(x=>`<article class="ai-doc"><div class="ai-doc-top"><span class="ai-rank">#${x.rank}</span><h4>${esc(x.document.title)}</h4><span class="ai-kind">${esc(x.document.access)}</span></div><p>${esc(x.document.text)}</p><div class="ai-scores"><span>${esc(x.id)}</span><span>BM25 ${fmt(x.lexical)}</span><span>TF-IDF ${fmt(x.vector)}</span><span>${x.source==='graph-expanded'?'Graph-expanded':'Ranked'}${x.overlap?' · '+x.overlap+' entities':''}</span></div></article>`).join('')||'<div class="ai-hint">No evidence matched. Try a sample question or different retrieval mode.</div>'}</div>
 <div class="ai-side"><div class="ai-subhead"><h3>Explain the retrieval</h3></div><p class="ai-small"><b>Keyword:</b> BM25 term-frequency ranking. <b>Vector proxy:</b> TF-IDF cosine with transparent synonym mappings—not neural embeddings. <b>Hybrid:</b> RRF of ranked results. <b>Graph:</b> allowed relationship traversal over linked entity IDs.</p>
 <p class="ai-small">The role selector illustrates <strong>pre-retrieval filtering</strong> for documents and graph links. All synthetic fixtures are bundled in JavaScript; this is a <strong>teaching simulation, not production access control</strong>.</p>${graphHTML(r)}</div></div></section>`;
}
function render(){
 const r=state.last||retrieve();state.last=r;
 return `<div class="ai-lab-page"><div class="eyebrow">HANDS-ON ADVANCED LEARNING · OFFLINE</div><div class="ai-hero"><div><h1>Retrieval Systems Lab</h1><p>Compare keyword search, vector-space ranking, hybrid fusion and knowledge-graph expansion on <b>${DOCS.length} synthetic enterprise documents</b>. See exactly which evidence each method retrieves—and when it fails.</p><div class="ai-hero-actions"><button class="primary-btn" data-route="lesson/ai-vector-01">Start vector lessons →</button><button class="ghost-btn" data-route="lesson/ai-graphrag-04">Explore GraphRAG lesson ↗</button></div></div><div class="ai-hero-symbol" aria-hidden="true"><span>BM25</span><span>TF‑IDF</span><span>RRF</span><span>KG</span></div></div>
 <div class="ai-warning"><strong>Transparent teaching simulation:</strong> this lab runs real BM25, TF-IDF/cosine, RRF and a curated graph walk in your browser. TF-IDF is <b>not</b> a neural embedding model. There is no LLM, external network request or generated answer. Role profiles demonstrate filtering only, not real authorization.</div>
 <section class="ai-config" aria-label="Retrieval configuration"><div class="ai-field ai-wide"><label for="aiQuery">Ask a question</label><input id="aiQuery" value="${esc(state.query)}" placeholder="e.g. Which assets depend on Northforge?" maxlength="240"/></div>
 <div class="ai-field ai-wide"><label for="aiPreset">Try a guided question</label><select id="aiPreset"><option value="custom" ${state.preset===-1?'selected':''}>Custom question</option>${PRESETS.map((p,i)=>`<option value="${i}" ${state.preset===i?'selected':''}>${esc(p.q)}</option>`).join('')}</select></div>
 <div class="ai-field"><label for="aiRole">Permission profile</label><select id="aiRole">${['viewer','engineer','steward'].map(x=>`<option value="${x}" ${state.role===x?'selected':''}>${x[0].toUpperCase()+x.slice(1)}</option>`).join('')}</select></div>
 <div class="ai-field"><label for="aiTopK">Evidence results (top-k)</label><select id="aiTopK">${[3,5,8,12].map(x=>`<option value="${x}" ${state.topK===x?'selected':''}>${x} results</option>`).join('')}</select></div>
 <div class="ai-field"><label for="aiHops">Maximum graph hops</label><select id="aiHops">${[1,2,3].map(x=>`<option value="${x}" ${state.hops===x?'selected':''}>${x} hop${x>1?'s':''}</option>`).join('')}</select></div>
 <div class="ai-field ai-submit"><button class="primary-btn" data-ai-action="run">Run retrieval ↗</button></div></section>
 <div class="ai-mode-group" role="group" aria-label="Retrieval method">${[['keyword','BM25 keyword'],['vector','TF-IDF vector proxy'],['hybrid','Hybrid RRF'],['graph','Graph expansion']].map(([key,label])=>`<button class="${state.mode===key?'active':''}" data-ai-mode="${key}" aria-pressed="${state.mode===key}">${label}</button>`).join('')}</div>
 ${resultsHTML()}
 <section class="ai-patterns" aria-label="Choosing the right retrieval strategy"><div class="ai-subhead"><h3>When to use each approach</h3><span>Four techniques, different tradeoffs</span></div><div class="ai-pattern-grid">
 <article><strong>BM25 · exact facts</strong><p>Part numbers, error codes, clause references and names. Weak on paraphrases with no shared terms.</p></article>
 <article><strong>Vector search · semantic similarity</strong><p>Paraphrased questions and related descriptions. A similarity score is not a verified claim.</p></article>
 <article><strong>Hybrid RRF · mixed corpora</strong><p>Fuse lexical and semantic rankings. Evaluation is still necessary; fusion cannot repair poor source quality.</p></article>
 <article><strong>Graph expansion · connected facts</strong><p>Multi-hop dependencies and provenance. Requires accurate entity links and strict traversal limits.</p></article>
 </div></section>
 <section class="ai-next"><h2>Turn this experiment into a production design</h2><p>Start with a fixed relevance set, enforce permission filters before retrieval, compare methods on the same corpus, and inspect each supporting source. The downloadable Python capstone reproduces the core algorithms without model APIs.</p><div class="ai-next-links"><button data-route="lesson/ai-rag-04" class="ghost-btn">Learn RRF →</button><button data-route="lesson/ai-context-01" class="ghost-btn">Context graphs →</button><button data-route="lesson/ai-production-07" class="ghost-btn">Architecture decisions →</button></div></section>
 </div>`;
}
function refresh(){state.last=retrieve(); if((location.hash||'').startsWith('#retrieval'))window.dispatchEvent(new Event('hashchange'));}
// State follows the page during re-renders; event handlers are delegated and do not duplicate.
document.addEventListener('change', e=>{
 const t=e.target;if(t.id==='aiPreset'){let i=Number(t.value);state.preset=t.value==='custom'?-1:i;if(i>=0)state.query=PRESETS[i].q;refresh();}
 else if(t.id==='aiRole'){state.role=t.value;refresh();}
 else if(t.id==='aiTopK'){state.topK=Math.max(1,Number(t.value)||5);refresh();}
 else if(t.id==='aiHops'){state.hops=Math.max(1,Number(t.value)||2);refresh();}
});
document.addEventListener('click',e=>{
 const t=e.target.closest('[data-ai-action],[data-ai-mode]');if(!t)return;
 if(t.dataset.aiMode){state.mode=t.dataset.aiMode;refresh();return;}
 if(t.dataset.aiAction==='run'){state.query=document.getElementById('aiQuery')?.value.trim()||state.query;state.preset=PRESETS.findIndex(p=>p.q===state.query);state.runs++;refresh();}
});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.id==='aiQuery'){e.preventDefault();document.querySelector('[data-ai-action="run"]')?.click();}});
window.TattvikiAILab={render,retrieve,scoreBM25,scoreVector,rrf,buildNeighborhood,DOCS,EDGES,PRESETS,state};
})();
