/* Tāttvikī v6 advanced studio. All advanced computation is performed by the optional local API.
   GitHub Pages serves this UI; it does NOT host FastAPI or persist shared data. */
(() => {
'use strict';
const API_KEY='tattviki-advanced-api', SESSION_KEY='tattviki-advanced-session';
let endpoint=localStorage.getItem(API_KEY)||'http://127.0.0.1:8765';
let token=sessionStorage.getItem(SESSION_KEY)||'';
let panel='reason',response='',connected=false,engines=null,projects=[],projectId='',projectVersion=null,username='',history=[];
const sampleShapes=`@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <https://example.org/tattviki/enterprise#> .
ex:DatasetOwnerShape a sh:NodeShape ;
  sh:targetClass ex:Dataset ;
  sh:property [ sh:path ex:ownedBy ; sh:minCount 1 ; sh:class ex:Organization ] .`;
const sampleQuery=`PREFIX ex: <https://example.org/tattviki/enterprise#>
SELECT ?dataset ?owner WHERE {
  ?dataset ex:ownedBy ?owner .
} ORDER BY ?dataset LIMIT 25`;
const htmlEscape=value=>String(value==null?'':value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function getRoot(){return document.getElementById('advanced-root');}
function render(){return `<section class="advanced-studio" id="advanced-root"><header class="advanced-top"><div><div class="eyebrow">ADVANCED WORKBENCH · OPTIONAL LOCAL ENGINE</div><h2>Reason. Validate. Collaborate.</h2><p>Execute SPARQL and ontology rules against your current model; share saved revisions with teammates using a self-hosted service.</p></div><span id="advanced-pill" class="advanced-status ${connected?'up':'down'}">${connected?'● Backend connected':'○ Backend offline'}</span></header>
<div class="advanced-connection"><label for="advanced-url">Semantic engine URL</label><input id="advanced-url" type="url" spellcheck="false" value="${htmlEscape(endpoint)}" placeholder="http://127.0.0.1:8765"><button data-advanced="connect" class="advanced-primary">Connect / Check</button><span class="advanced-hint">GitHub Pages stays static. Start <code>backend/START_ADVANCED_WINDOWS.bat</code> on your PC for these functions.</span></div>
<div class="advanced-nav" role="tablist" aria-label="Advanced studio modules">${[['reason','Infer & reason'],['sparql','Full SPARQL'],['shacl','SHACL validation'],['dl','DL-style explorer'],['team','Collaboration & history']].map(([id,name])=>`<button type="button" role="tab" aria-selected="${id===panel}" class="${id===panel?'active':''}" data-advanced="tab" data-tabid="${id}">${name}</button>`).join('')}</div>
<div id="advanced-content">${panelHtml()}</div><div class="advanced-output"><div class="advanced-output-title"><b>Execution output</b><button data-advanced="clear">Clear</button></div><pre id="advanced-result" tabindex="0" aria-live="polite">${htmlEscape(response||'Connect to a local semantic engine, choose a task, then run it. No result has been computed yet.')}</pre></div>
<div class="advanced-disclaimer">The RDFS engine implements a documented subset; OWL RL (owlrl) and standard SHACL (pySHACL) require optional Python packages. The DL-style explorer is not a complete Manchester syntax / OWL 2 DL reasoner. Collaboration requires a running API; nothing is shared by GitHub Pages alone.</div></section>`;}
function panelHtml(){switch(panel){
 case 'reason':return `<div class="advanced-info"><h3>Logical inference</h3><p>Apply RDFS subclass, subproperty, domain and range rules to the ontology you're editing. For OWL RL expansion, install the bundled Python dependencies.</p><div class="advanced-actions"><button data-advanced="rdfs" class="advanced-primary">Run RDFS closure</button><button data-advanced="owlrl">Run OWL RL inference</button><button data-advanced="hermit">Try HermiT OWL DL (Java)</button></div><p class="advanced-hint">Supports imported studio Turtle (not external network imports). Shows newly inferred triples.</p></div>`;
 case 'sparql':return `<div class="advanced-info"><h3>Query the entire ontology</h3><p>Execute RDFLib read-only SELECT, ASK, CONSTRUCT, and DESCRIBE against the studio's current Turtle graph. No SERVICE federation or remote fetching.</p><label for="advanced-query">SPARQL query</label><textarea id="advanced-query" rows="8" spellcheck="false">${htmlEscape(sampleQuery)}</textarea><div class="advanced-actions"><button data-advanced="sparql" class="advanced-primary">Execute query</button><button data-advanced="copyttl">Export current RDF</button></div></div>`;
 case 'shacl':return `<div class="advanced-info"><h3>Standards-based quality validation</h3><p>Use pySHACL to run actual SHACL Core constraints against your live ontology. Start with the sample constraint or paste your own shapes.</p><label for="advanced-shapes">SHACL shapes — Turtle</label><textarea id="advanced-shapes" rows="9" spellcheck="false">${htmlEscape(sampleShapes)}</textarea><div class="advanced-actions"><button data-advanced="shacl" class="advanced-primary">Validate data</button></div></div>`;
 case 'dl':return `<div class="advanced-info"><h3>DL-style named-class search</h3><p>Find individuals belonging to named classes (including limited RDFS subclass inference). Supported examples: <code>Dataset</code>, <code>Dataset and CuratedDataset</code>, <code>Dataset or Person</code>. Complex Manchester syntax requires a separate OWL DL reasoner.</p><label for="advanced-dl">Class expression</label><input id="advanced-dl" value="Dataset" spellcheck="false"><div class="advanced-actions"><button data-advanced="dl" class="advanced-primary">Find instances</button></div></div>`;
 case 'team':return `<div class="advanced-info"><h3>Collaborative projects and immutable revisions</h3><p>Create an account on your own local/server installation. Owners can assign editor/viewer roles. Every save creates a new revision; conflicting edits are rejected.</p><div class="advanced-auth"><label>Username<input id="advanced-username" autocomplete="username" placeholder="shubham"></label><label>Password (min 12 characters)<input id="advanced-password" type="password" autocomplete="current-password" placeholder="Your own password"></label><div class="advanced-actions"><button data-advanced="register">Register</button><button data-advanced="login" class="advanced-primary">Sign in</button><button data-advanced="logout">Sign out</button></div></div><div class="advanced-project-actions"><label>Shared project<select id="advanced-project"><option value="">Select a project</option>${projects.map(p=>`<option value="${htmlEscape(p.id)}" ${p.id===projectId?'selected':''}>${htmlEscape(p.name)} · v${p.version} · ${htmlEscape(p.role)}</option>`).join('')}</select></label><div class="advanced-actions"><button data-advanced="list">Refresh projects</button><button data-advanced="create">Create from editor</button><button data-advanced="load">Load into editor</button><button data-advanced="save" class="advanced-primary">Save new revision</button></div><label for="advanced-message">Revision note</label><input id="advanced-message" value="Updated classes and relationships" maxlength="300"><div class="advanced-actions"><button data-advanced="history">Show history</button><button data-advanced="restore">Restore selected revision</button></div><label>Revision history<select id="advanced-history"><option value="">Select revision</option>${history.map(r=>`<option value="${r.version}">v${r.version} · ${htmlEscape(r.editor)} · ${htmlEscape(r.message)}</option>`).join('')}</select></label><div class="advanced-share"><label>Invite registered username<input id="advanced-invite" placeholder="teammate"></label><label>Permission<select id="advanced-role"><option value="viewer">Viewer</option><option value="editor">Editor</option></select></label><button data-advanced="share">Set access</button><button data-advanced="revoke">Revoke access</button></div></div><p class="advanced-hint">Tokens are held in this tab's session storage. API uses salted PBKDF2 hashes, hashed session tokens, and SQLite role checks. For internet deployment, add HTTPS, account recovery, rate limits, backups, audited security configuration and private hosting.</p></div>`;
 default:return '';
}}
function result(value){response=typeof value==='string'?value:JSON.stringify(value,null,2);const n=document.getElementById('advanced-result');if(n)n.textContent=response;}
async function request(path,method='GET',payload){const base=endpoint.replace(/\/+$/,'');if(!/^https?:\/\//.test(base))throw Error('Enter a valid http:// or https:// backend address');const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),15000);try{const res=await fetch(base+path,{method,headers:{...(payload?{'content-type':'application/json'}:{}),...(token?{authorization:'Bearer '+token}:{})},body:payload?JSON.stringify(payload):undefined,signal:controller.signal});const data=await res.json().catch(()=>({detail:'Could not read server response'}));if(!res.ok)throw Error(`HTTP ${res.status}: ${typeof data.detail==='string'?data.detail:JSON.stringify(data.detail)}`);return data;}finally{clearTimeout(timeout);}}
function currentTurtle(){return window.TattvikiStudio.exportTurtle();}
async function perform(a){const input=id=>document.getElementById(id)?.value||'';
 if(a==='connect'){endpoint=input('advanced-url').trim();localStorage.setItem(API_KEY,endpoint);const h=await request('/api/health');connected=true;engines=h.engines;getRoot().querySelector('#advanced-pill').textContent='● Backend connected';getRoot().querySelector('#advanced-pill').className='advanced-status up';result(h);return;}
 if(a==='clear'){result('');return;}
 if(a==='copyttl'){const text=currentTurtle();const blob=new Blob([text],{type:'text/turtle'});const link=document.createElement('a');const uri=URL.createObjectURL(blob);link.href=uri;link.download='tattviki-live-ontology.ttl';link.click();setTimeout(()=>URL.revokeObjectURL(uri),1500);result('Exported the current ontology.');return;}
 if(a==='rdfs'||a==='owlrl'||a==='hermit')return result(await request('/api/reason','POST',{turtle:currentTurtle(),mode:a}));
 if(a==='sparql')return result(await request('/api/sparql','POST',{turtle:currentTurtle(),query:input('advanced-query')}));
 if(a==='shacl')return result(await request('/api/shacl','POST',{turtle:currentTurtle(),shapes:input('advanced-shapes')}));
 if(a==='dl')return result(await request('/api/dlquery','POST',{turtle:currentTurtle(),expression:input('advanced-dl')}));
 if(a==='login'||a==='register'){
  const ans=await request('/api/auth/'+(a==='register'?'register':'login'),'POST',{username:input('advanced-username'),password:input('advanced-password')});token=ans.token;username=ans.username;sessionStorage.setItem(SESSION_KEY,token);document.getElementById('advanced-password').value='';await refreshProjects();result(`Signed in as ${username}. You can now create and share ontology projects.`);return;
 }
 if(a==='logout'){if(token)await request('/api/auth/logout','POST');token='';username='';sessionStorage.removeItem(SESSION_KEY);projects=[];history=[];projectId='';projectVersion=null;drawPanel();result('Signed out.');return;}
 if(a==='list'){await refreshProjects();result({projects});return;}
 if(a==='create'){
  const doc=window.TattvikiStudio.model();const created=await request('/api/projects','POST',{name:doc.name||'New Ontology',document:doc});projectId=created.id;projectVersion=created.version;await refreshProjects();result('Created shared project v1. Owner permission granted.');return;
 }
 if(a==='load'){
  if(!projectId)throw Error('Select a project');const p=await request(`/api/projects/${encodeURIComponent(projectId)}`);if(!window.confirm('Replace your current local ontology with the shared revision? Download a JSON backup first if needed.'))return;
  window.TattvikiStudio.loadModel(p.document);projectVersion=p.version;window.dispatchEvent(new Event('hashchange'));result(`Loaded ${p.name} v${p.version}. Click Save new revision after editing.`);return;
 }
 if(a==='save'){
  if(!projectId)throw Error('Select a shared project');if(!Number.isInteger(projectVersion))throw Error('Load the shared project before saving; this prevents overwriting other revisions.');
  const p=await request(`/api/projects/${encodeURIComponent(projectId)}`,'PUT',{document:window.TattvikiStudio.model(),expected_version:projectVersion,message:input('advanced-message')||'Updated ontology'});
  projectVersion=p.version;await refreshProjects();result(`Saved revision ${p.version}.`);return;
 }
 if(a==='history'){
  if(!projectId)throw Error('Select a project');history=(await request(`/api/projects/${encodeURIComponent(projectId)}/history`)).revisions;drawPanel();result(history);return;
 }
 if(a==='restore'){
  if(!projectId)throw Error('Select a project');let version=Number(input('advanced-history'));if(!version)throw Error('Select a revision from history');if(!Number.isInteger(projectVersion))throw Error('Load the project first');
  if(!confirm(`Create a new revision restoring old revision ${version}?`))return;
  let r=await request(`/api/projects/${encodeURIComponent(projectId)}/restore/${version}`,'POST',{expected_version:projectVersion});projectVersion=r.version;await refreshProjects();result(`Restored v${version} as new revision ${r.version}. Load project to update the editor.`);return;
 }
 if(a==='revoke'){
  if(!projectId)throw Error('Select a project');const u=input('advanced-invite').trim();if(!u)throw Error('Enter the username to revoke');if(!confirm(`Revoke ${u}\'s access to this project?`))return;result(await request(`/api/projects/${encodeURIComponent(projectId)}/members/${encodeURIComponent(u)}`,'DELETE'));return;
 }
 if(a==='share'){
  if(!projectId)throw Error('Select a project');result(await request(`/api/projects/${encodeURIComponent(projectId)}/members`,'POST',{username:input('advanced-invite'),role:input('advanced-role')}));return;
 }
}
function drawPanel(){let c=document.getElementById('advanced-content');if(c)c.innerHTML=panelHtml();}
async function refreshProjects(){let reply=await request('/api/projects');projects=reply.projects;const target=projects.find(x=>x.id===projectId);if(!target){projectId='';projectVersion=null;}drawPanel();}
document.addEventListener('click',async ev=>{
 const b=ev.target.closest('[data-advanced]');if(!b||!getRoot()||!getRoot().contains(b))return;
 const a=b.dataset.advanced;
 if(a==='tab'){panel=b.dataset.tabid;getRoot().querySelectorAll('[data-advanced="tab"]').forEach(button=>{button.classList.toggle('active',button.dataset.tabid===panel);button.setAttribute('aria-selected',String(button.dataset.tabid===panel));});drawPanel();return;}
 b.disabled=true;try{result('Running '+a+'…');await perform(a);}catch(err){if(a==='connect'){connected=false;const p=document.getElementById('advanced-pill');if(p){p.className='advanced-status down';p.textContent='○ Backend offline';}}result('Error: '+err.message+'\nCheck that the optional backend is running and CORS origin is permitted.');}finally{b.disabled=false;}
});
document.addEventListener('change',ev=>{if(ev.target.id==='advanced-project'){projectId=ev.target.value;projectVersion=null;history=[];result('Project selected. Choose Load into editor before editing its next revision.');}});
window.TattvikiAdvanced={render,health:()=>({connected,engines,projectId,projectVersion})};
})();
