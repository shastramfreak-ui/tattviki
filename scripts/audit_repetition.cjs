// Reproducible content audit. This is not an LLM-generated quality score.
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const s={window:{}};
for(const f of ['content','curriculum','enterprise_curriculum','learning-guides','ai-curriculum','graph-learning','shacl-learning','editorial-patches'])vm.runInNewContext(fs.readFileSync('assets/'+f+'.js','utf8'),s,{filename:f+'.js'});
const L=s.window.OT.lessons,G=s.window.TATTVIKI_GUIDES;
const count=(fn)=>L.filter(fn).length;
const patterns={remaining_generic_descriptions:count(l=>/^Explore .+ in clinical studies/i.test(l.description)),remaining_generic_analogy:count(l=>/is a specific modeling or engineering decision that affects/i.test(l.analogy)),remaining_generic_objectives:count(l=>l.learn?.[0]?.startsWith('Define ')&&l.learn?.[1]?.startsWith('Apply this concept')),remaining_template_examples:count(l=>l.example?.includes('# Design focus:')),remaining_generic_guide_openings:count(l=>G[l.id]?.subtitle?.startsWith('In this chapter')),remaining_generic_core_2:count(l=>G[l.id]?.core?.[1]?.startsWith('The working context is ')),remaining_generic_verification:count(l=>G[l.id]?.verification?.[0]?.startsWith('Positive case:'))};
const keys=L.map(l=>l.id),titles=L.map(l=>l.title.toLowerCase());assert.equal(new Set(keys).size,keys.length);assert.equal(new Set(titles).size,titles.length);
assert.equal(keys.length,737);for(let l of L)assert(G[l.id],`No guide ${l.id}`);
const payload={current_lessons:L.length,paths:s.window.OT.paths.length,shacl_lessons:L.filter(x=>x.path==='shacl-mastery').length,editorial_changes:s.window.TATTVIKI_EDITORIAL_AUDIT,remaining:patterns,note:'This audit identifies repeated phrase templates, not all possible semantic redundancy. Further subject-matter editorial review remains necessary.'};
fs.writeFileSync('CONTENT_AUDIT_V13.json',JSON.stringify(payload,null,2)+'\n');
console.log(JSON.stringify(payload,null,2));
for(let [k,v] of Object.entries(patterns))assert.equal(v,0,k+' remains');
