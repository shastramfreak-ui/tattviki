/* Tāttvikī SHACL learning workbench. Browser: explicit SHACL Core teaching subset.
   Server-grade validation: pySHACL or Apache Jena; never equate this implementation with full SHACL. */
(()=>{'use strict';
const presets=window.TATTVIKI_SHACL_SCENARIOS||[];
const NS={rdf:'http://www.w3.org/1999/02/22-rdf-syntax-ns#',sh:'http://www.w3.org/ns/shacl#',xsd:'http://www.w3.org/2001/XMLSchema#'};
const sk=(p,k)=>p+k;
const TERM=/\s+|#[^\n]*|"(?:\\.|[^"\\])*"(?:@[a-zA-Z]+(?:-[a-zA-Z0-9]+)*|\^\^(?:[\w-]*:[\w.-]+|<[^<>]+>))?|<[^<>]*>|[\[\];,.()]|[+-]?\d+(?:\.\d+)?|[\w-]*:[\w.-]+|[A-Za-z_][\w-]*/gy;
function parse(text){
 let prefixes={...NS};let clean=text.replace(/(?:^|\n)\s*(?:@prefix|PREFIX)\s+([\w-]*):\s*<([^<>\s]+)>\s*\.?\s*(?=\n|$)/gim,(_,p,u)=>{prefixes[p]=u;return '\n';});
 let tokens=[],p=0;
 while(p<clean.length){TERM.lastIndex=p;let match=TERM.exec(clean);if(!match)throw Error('Unsupported Turtle character near '+JSON.stringify(clean.slice(p,p+25)));
 let tok=match[0];if(!/^\s+$/.test(tok)&&!tok.startsWith('#'))tokens.push(tok);p=TERM.lastIndex;}
 let at=0,b=0,triples=[];const next=()=>tokens[at],pop=()=>tokens[at++];
 function expect(v){let t=pop();if(t!==v)throw Error('Expected '+v+' but found '+(t||'end of graph'));}
 function term(){let t=pop();if(!t)throw Error('Incomplete Turtle term');
  if(t==='['){let node={k:'blank',v:'_:b'+(++b)};if(next()!==']')predicates(node,']');expect(']');return node;}
  if(t==='('){let values=[];while(next()!==')'&&next()!==undefined)values.push(term());expect(')');return {k:'list',v:values};}
  if(t==='a')return {k:'iri',v:sk(prefixes.rdf,'type')};
  if(t.startsWith('<'))return {k:'iri',v:t.slice(1,-1)};
  if(t.startsWith('"')){let m=t.match(/^("(?:\\.|[^"\\])*")(?:@([\w-]+)|\^\^(.+))?$/);if(!m)throw Error('Invalid literal '+t);let lexical;try{lexical=JSON.parse(m[1]);}catch(_){lexical=m[1].slice(1,-1);}
    let datatype=m[3]?termFromString(m[3]).v:(m[2]?sk(prefixes.rdf,'langString'):sk(prefixes.xsd,'string'));
    return {k:'literal',v:String(lexical),dt:datatype,lang:m[2]||''};}
  if(/^[+-]?\d/.test(t)){let decimal=t.includes('.');return {k:'literal',v:t,dt:sk(prefixes.xsd,decimal?'decimal':'integer'),lang:''};}
  if(t==='true'||t==='false')return {k:'literal',v:t,dt:sk(prefixes.xsd,'boolean'),lang:''};
  return termFromString(t);
 }
 function termFromString(t){let m=t.match(/^([\w-]*):([\w.-]+)$/);if(!m||!(m[1] in prefixes))throw Error('Unknown or unsupported term '+t);return{k:'iri',v:prefixes[m[1]]+m[2]};}
 function predicates(subject,closing){while(true){let pred=term();if(pred.k!=='iri')throw Error('Predicates must be IRIs');while(true){let object=term();triples.push({s:subject,p:pred.v,o:object});if(next()===','){pop();continue;}break;}
  if(next()===';'){while(next()===';')pop();if(next()===closing||next()==='.'||next()===undefined)break;continue;}break;}}
 while(at<tokens.length){let subject=term();if(!['iri','blank'].includes(subject.k))throw Error('Subject must be an IRI or blank node');predicates(subject,'.');expect('.');}
 return {triples,prefixes};
}
const eq=(a,b)=>a&&b&&a.k===b.k&&a.v===b.v&&a.dt===b.dt&&a.lang===b.lang;
const uri=(p,s)=>NS[p]+s;
function validate(dataInput,shapeInput){
 let data=parse(dataInput),shapes=parse(shapeInput);let d=data.triples,ss=shapes.triples;
 const obj=(triples,s,p)=>triples.filter(x=>x.s.v===s.v&&x.p===p).map(x=>x.o);
 let nodeShapes=ss.filter(x=>x.p===uri('rdf','type')&&x.o.v===uri('sh','NodeShape')).map(x=>x.s);
 if(!nodeShapes.length)throw Error('No sh:NodeShape was found. Declare a shape with a sh:targetClass.');
 let supported=new Set(['path','minCount','maxCount','datatype','class','nodeKind','pattern','in','minInclusive','maxInclusive','hasValue','message','severity']);
 let report=[],checked=0;
 for(let shape of nodeShapes){
  for(let declaration of ss.filter(x=>x.s.v===shape.v&&x.p.startsWith(NS.sh))){
    const component=declaration.p.slice(NS.sh.length);
    if(!['targetClass','targetNode','property'].includes(component))throw Error('Unsupported node-shape feature sh:'+component+'. Use pySHACL/Jena for full validation.');
  }
  let types=obj(ss,shape,uri('sh','targetClass')),targets=obj(ss,shape,uri('sh','targetNode'));
  if(!types.length&&!targets.length)throw Error('Each shape needs sh:targetClass or sh:targetNode');
  let focus=[...targets];for(let type of types){for(let st of d.filter(x=>x.p===uri('rdf','type')&&x.o.v===type.v))if(!focus.some(x=>x.v===st.s.v))focus.push(st.s);}
  let propNodes=obj(ss,shape,uri('sh','property'));
  for(let pn of propNodes){const constraints=ss.filter(x=>x.s.v===pn.v);for(let c of constraints){if(!c.p.startsWith(NS.sh))continue;let field=c.p.slice(NS.sh.length);if(!supported.has(field))throw Error('Unsupported constraint sh:'+field+'. Use pySHACL/Jena for full validation.');}
   if(!obj(ss,pn,uri('sh','path')).length)throw Error('Every sh:property needs sh:path.');}
  for(let f of focus){checked++;
   for(let pn of propNodes){let path=obj(ss,pn,uri('sh','path'))[0];if(path.k!=='iri')throw Error('Only direct IRI sh:path supported in the offline workbench.');
    let vals=obj(d,f,path.v);const all=(name)=>obj(ss,pn,uri('sh',name));const first=(name)=>all(name)[0];
    let severity=obj(ss,pn,uri('sh','severity'))[0]?.v?.split('#').pop()||'Violation';
    function issue(rule,val,message){let custom=first('message')?.v;report.push({focus:f.v,path:path.v,sourceShape:shape.v,sourceConstraintComponent:rule,severity,value:val?.v??null,message:custom?custom+' — '+message:message});}
    if(first('minCount')&&vals.length<Number(first('minCount').v))issue('MinCountConstraintComponent',null,'Expected at least '+first('minCount').v+' value(s); found '+vals.length);
    if(first('maxCount')&&vals.length>Number(first('maxCount').v))issue('MaxCountConstraintComponent',null,'Expected at most '+first('maxCount').v+' value(s); found '+vals.length);
    if(first('hasValue')&&!vals.some(x=>eq(x,first('hasValue'))))issue('HasValueConstraintComponent',first('hasValue'),'Required value is missing');
    for(let v of vals){
     if(first('datatype')&&(v.k!=='literal'||v.dt!==first('datatype').v))issue('DatatypeConstraintComponent',v,'Expected datatype '+first('datatype').v);
     if(first('nodeKind')){let k=first('nodeKind').v;let kinds={'Literal':['literal'],'IRI':['iri'],'BlankNode':['blank'],'IRIOrLiteral':['iri','literal'],'BlankNodeOrIRI':['blank','iri'],'BlankNodeOrLiteral':['blank','literal']};let permitted=kinds[k.split('#').pop()];if(!permitted)throw Error('Unsupported sh:nodeKind '+k);if(!permitted.includes(v.k))issue('NodeKindConstraintComponent',v,'Expected '+k.split('#').pop());}
     if(first('class')&&!d.some(x=>x.s.v===v.v&&x.p===uri('rdf','type')&&x.o.v===first('class').v))issue('ClassConstraintComponent',v,'Object is not explicitly typed as '+first('class').v);
     if(first('in')){let allowed=first('in');if(allowed.k!=='list')throw Error('Only direct sh:in ( ... ) lists are supported');if(!allowed.v.some(t=>eq(t,v)))issue('InConstraintComponent',v,'Value is not in the permitted list');}
     if(first('pattern')){let re;try{re=new RegExp(first('pattern').v);}catch(_){throw Error('Invalid sh:pattern regex');}if(!re.test(v.v))issue('PatternConstraintComponent',v,'Value does not match '+first('pattern').v);}
     for(let bound of ['minInclusive','maxInclusive'])if(first(bound)){let n=Number(v.v),lim=Number(first(bound).v);if(!Number.isFinite(n)||!(bound==='minInclusive'?n>=lim:n<=lim))issue((bound==='minInclusive'?'MinInclusive':'MaxInclusive')+'ConstraintComponent',v,'Value must be '+(bound==='minInclusive'?'>= ':'<= ')+lim);}
    }
   }
  }
 }
 return {conforms:report.length===0,results:report,checked,shapes:nodeShapes.length,dataTriples:d.length,shapeTriples:ss.length};
}
function short(s){if(s==null)return '—';return String(s).replace('https://tattviki.example/education/','ex:').replace(NS.sh,'sh:').replace(NS.xsd,'xsd:').replace('http://purl.org/dc/terms/','dct:');}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function load(key,def){try{const v=JSON.parse(localStorage.getItem(key));return typeof v==='string'?v:def;}catch(_){return def;}}
const base=presets[0];let index=0;
let data=load('tattviki-shacl-data',base.bad),shapes=load('tattviki-shacl-shapes',base.shapes),mode='bad',result=null,error='',expanded=false;
function save(){try{localStorage.setItem('tattviki-shacl-data',JSON.stringify(data));localStorage.setItem('tattviki-shacl-shapes',JSON.stringify(shapes));}catch(_){}}
function choose(i,which='bad'){index=Math.max(0,Math.min(presets.length-1,Number(i)));mode=which;data=presets[index][which];shapes=presets[index].shapes;result=null;error='';save();}
function run(){try{result=validate(data,shapes);error='';}catch(e){result=null;error=e.message;}return result;}
function download(filename,value){const u=URL.createObjectURL(new Blob([value],{type:'text/turtle;charset=utf-8'}));let a=document.createElement('a');a.href=u;a.download=filename;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),2000);}
function render(){let s=presets[index],done=result;
 return `<div class="eyebrow">DESIGN • EXECUTE • INTERPRET • REPAIR</div><h1 class="page-title">SHACL Validation Lab</h1><p class="subhead">Create constraint shapes, test a real RDF data graph, diagnose violations, then repeat with a passing fixture. This browser checks an explicit <strong>SHACL Core subset</strong>; the full Python and Apache Jena workflows are provided below.</p>
 <section class="shacl-metrics"><div><b>${presets.length}</b><span>Domain cases</span></div><div><b>${done?done.checked:'—'}</b><span>Focus nodes tested</span></div><div><b>${done?done.results.length:'—'}</b><span>Validation findings</span></div><div><b>${done?(done.conforms?'PASS':'FAIL'):'Ready'}</b><span>Latest result</span></div></section>
 <div class="shacl-header panel"><label for="shacl-scenario">Choose an industry scenario</label><select id="shacl-scenario" aria-label="SHACL scenario">${presets.map((p,i)=>`<option value="${i}" ${index===i?'selected':''}>${esc(p.title)}</option>`).join('')}</select><p class="tiny">${esc(s.goal)}</p><div class="row wrap"><button class="ghost-btn" data-shacl="bad">Load broken graph</button><button class="ghost-btn" data-shacl="good">Load valid graph</button><button class="ghost-btn" data-shacl="reset">Reset shapes</button><button class="primary-btn" data-shacl="run">▶ Validate graph</button></div></div>
 <div class="shacl-editor-grid"><section class="panel shacl-editor"><div class="row between"><h3>01 · RDF data graph</h3><button class="ghost-btn" data-shacl="download-data">Export Turtle</button></div><p class="tiny">Instances and assertions to test. Change a value, remove a property or change rdf:type.</p><textarea id="shacl-data" spellcheck="false" aria-label="Editable RDF data graph">${esc(data)}</textarea></section>
 <section class="panel shacl-editor"><div class="row between"><h3>02 · SHACL shapes graph</h3><button class="ghost-btn" data-shacl="download-shapes">Export shapes</button></div><p class="tiny">Change targetClass, path, count, datatype, class, nodeKind, pattern, allowed values or numeric bounds.</p><textarea id="shacl-shapes" spellcheck="false" aria-label="Editable SHACL shapes graph">${esc(shapes)}</textarea></section></div>
 <section class="panel shacl-results" aria-live="polite"><div class="row between wrap"><h3>03 · Validation report</h3><span class="shacl-status ${error?'is-error':done?.conforms?'is-success':done?'is-warning':''}">${error?'Syntax / unsupported feature':done?done.conforms?'Conforms':'Non-conformant':'Not yet validated'}</span></div>${error?`<p class="shacl-error">${esc(error)}</p>`:!done?'<p class="tiny">Load a scenario and select Validate graph. The result includes the focus node, property, constraint component and message.</p>':done.conforms?`<p class="shacl-ok">✓ ${done.checked} focus node(s) conform to the supported shapes. ${done.dataTriples} data triples checked.</p>`:`<p>${done.results.length} violation(s) found across ${done.checked} targeted node(s). Repair the data or shapes and validate again.</p><div class="shacl-issues">${done.results.map((v,i)=>`<article><strong>${i+1}. ${esc(short(v.sourceConstraintComponent))}</strong><span>Focus: <code>${esc(short(v.focus))}</code> · Path: <code>${esc(short(v.path))}</code></span><span>${esc(v.message)}${v.value!==null?' · Value: '+esc(short(v.value)):''}</span></article>`).join('')}</div>`}</section>
 <section class="shacl-help-grid"><article class="panel"><h3>04 · Run full SHACL with Python</h3><p>Install <code>rdflib</code> and <code>pyshacl</code>, then run the included project.</p><pre class="code-box"><code>python -m pip install -r requirements.txt\npython validate.py --scenario ${esc(s.id)} --data bad\npython validate.py --scenario ${esc(s.id)} --data good</code></pre><p class="tiny">Full pySHACL runs locally; it is <strong>not</strong> automatically hosted by GitHub Pages.</p></article><article class="panel"><h3>05 · Validate in another tool</h3><p><strong>Apache Jena CLI:</strong> export both Turtle files then run:</p><pre class="code-box"><code>shacl validate --shapes shapes.ttl --data data.ttl</code></pre><p class="tiny">For GraphDB, configure a SHACL-enabled repository first, then load shapes according to its specific repository workflow.</p></article></section>
 <details class="panel shacl-details"><summary>What the offline validator supports—and what requires pySHACL / Jena</summary><p>Supported: targetClass, targetNode, minCount/maxCount, datatype, class, nodeKind, regular-expression pattern, value list (sh:in), hasValue, numeric minInclusive/maxInclusive, direct IRI paths, basic Turtle property lists. Missing from the offline subset: sh:or/and/not, inverse or sequence paths, sh:qualifiedValueShape, sh:node, SPARQL-based constraints, SHACL-AF, inference regimes, recursion, full RDF dataset semantics. Unsupported SHACL constraints produce an explicit error instead of a false pass.</p><p>SHACL evaluates a data graph against a shapes graph. This differs from OWL open-world inference, and a passing validation report does not imply your data represents every business requirement.</p></details>
 </div>`;}
 document.addEventListener('click',e=>{const b=e.target.closest('[data-shacl]');if(!b)return;let op=b.dataset.shacl;
 if(op==='run'){run();}
 else if(op==='bad'||op==='good'){choose(index,op);}
 else if(op==='reset'){shapes=presets[index].shapes;result=null;error='';save();}
 else if(op==='download-data'){download(presets[index].id+'-data.ttl',data);return;}
 else if(op==='download-shapes'){download(presets[index].id+'-shapes.ttl',shapes);return;}
 else return;
 if(location.hash.startsWith('#shacl')){document.getElementById('app')?.dispatchEvent(new CustomEvent('tattviki-render-request',{bubbles:true}));}
 });
 document.addEventListener('change',e=>{if(e.target.id==='shacl-scenario'){choose(e.target.value);if(location.hash.startsWith('#shacl'))document.getElementById('app')?.dispatchEvent(new CustomEvent('tattviki-render-request',{bubbles:true}));}});
 document.addEventListener('input',e=>{if(e.target.id==='shacl-data'){data=e.target.value;result=null;save();}if(e.target.id==='shacl-shapes'){shapes=e.target.value;result=null;save();}});
 window.TattvikiSHACL={parse,validate,render,choose,run,getCurrent:()=>({index,data,shapes,result,error}),presets};
})();
