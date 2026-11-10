const fs=require('fs'),assert=require('assert/strict');
global.window=global;global.localStorage={getItem:()=>null,setItem(){}};global.document={addEventListener(){}};
eval(fs.readFileSync('assets/shacl-scenarios.js','utf8'));
eval(fs.readFileSync('assets/shacl-lab.js','utf8'));
assert.equal(TATTVIKI_SHACL_SCENARIOS.length,6);let n=0;
for(const c of TATTVIKI_SHACL_SCENARIOS){let pass=TattvikiSHACL.validate(c.good,c.shapes),fail=TattvikiSHACL.validate(c.bad,c.shapes);assert(pass.conforms,`Should pass ${c.id}`);assert(!fail.conforms,`Should fail ${c.id}`);assert(fail.results.length>0,c.id);for(let r of fail.results){assert(r.focus&&r.path&&r.sourceConstraintComponent&&r.message)};n+=2;}
let people=TATTVIKI_SHACL_SCENARIOS.find(x=>x.id==='people');
assert(!TattvikiSHACL.validate(people.good.replace('ex:age 32','ex:age "32"'),people.shapes).conforms);
assert.throws(()=>TattvikiSHACL.validate(people.good,people.shapes.replace('sh:class ex:Person','sh:or ( ex:A ex:B )')),/Unsupported constraint sh:or/);
assert.throws(()=>TattvikiSHACL.validate(people.good,people.shapes.replace('sh:targetClass ex:Person','sh:targetClass ex:Person ; sh:closed true')),/Unsupported node-shape feature sh:closed/);
assert.throws(()=>TattvikiSHACL.validate('!!!',people.shapes),/Unsupported Turtle|Incomplete|Expected|Unknown/);
let reference=TATTVIKI_SHACL_SCENARIOS.find(x=>x.id==='reference');
assert(TattvikiSHACL.validate(reference.good,reference.shapes).conforms);
assert(TattvikiSHACL.validate(reference.bad,reference.shapes).results.some(r=>r.sourceConstraintComponent==='MaxCountConstraintComponent'));
let cat=TATTVIKI_SHACL_SCENARIOS.find(x=>x.id==='catalog');
assert(TattvikiSHACL.validate(cat.bad,cat.shapes).results.some(r=>r.sourceConstraintComponent==='InConstraintComponent'));
console.log(`PASS ${n+7} SHACL fixture and negative-cases checks; browser subset does not silently accept sh:or`);
