const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const sandbox={window:{},document:{addEventListener(){}}};vm.createContext(sandbox);
vm.runInContext(fs.readFileSync('assets/ai-lab.js','utf8'),sandbox);
const lab=sandbox.window.TattvikiAILab;
assert.equal(lab.DOCS.length,28);assert.equal(lab.PRESETS.length,6);
assert.equal(lab.EDGES.length,20);
assert.equal(lab.rrf([[{id:'a',score:1},{id:'b',score:0.2}],[{id:'b',score:1},{id:'c',score:0.4}]])[0].id,'b');
for(const role of ['viewer','engineer','steward'])for(const mode of ['keyword','vector','hybrid','graph']){
 const found=lab.retrieve({query:'Pump-3 Northforge access policy',role,mode,topK:12});
 for(const hit of found.selected){
   assert(role==='steward'||hit.document.access==='public'||(role==='engineer'&&hit.document.access==='engineer'));
 }
 if(mode==='graph')for(const edge of found.neighborhood.traced){
   assert(role==='steward'||edge.access==='public'||(role==='engineer'&&edge.access==='engineer'));
 }
}
const anon=lab.retrieve({role:'viewer',mode:'graph',query:'Pump-3 approval'});
assert(!anon.neighborhood.traced.some(e=>e.access==='steward'));
assert(lab.retrieve({role:'steward',mode:'graph',query:'Pump-3 approval'}).neighborhood.traced.some(e=>e.access==='steward'));
for(const p of lab.PRESETS){const r=lab.retrieve({role:'steward',mode:'hybrid',query:p.q,topK:8});assert(r.recall!==null);}
console.log('PASS: 28 synthetic documents, 20 graph edges, 6 questions, 4 retrieval modes, 3 role simulations, RRF, metrics and edge filtering');
