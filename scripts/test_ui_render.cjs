#!/usr/bin/env node
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const src=['content.js','curriculum.js','deepdives.js','enterprise_curriculum.js','enterprise_cases.js','studio-templates.js','studio-graph.js','studio.js','advanced.js','semantic-workbench.js','app.js'];
async function testRoute(hash,words){
 const app={innerHTML:'',addEventListener(){}};
 const doc={title:'',getElementById(id){return id==='app'?app:null},addEventListener(){},activeElement:{tagName:'BODY'}};
 const location={hash};
 const w={addEventListener(){}};
 const ctx={window:w,document:doc,location,history:{replaceState(){}},localStorage:{getItem(){return null},setItem(){}},sessionStorage:{getItem(){return null},setItem(){}},fetch:async()=>({ok:false}),console};
 vm.createContext(ctx);
 for(let f of src)vm.runInContext(fs.readFileSync('assets/'+f,'utf8'),ctx,{filename:f});
 for(let word of words)assert(app.innerHTML.includes(word),`Missing ${word} on ${hash}`);
 console.log('render OK:',hash,app.innerHTML.length);
}
(async()=>{
 for(let [route,terms] of [['#semantic',['Semantic Workbench','INFERRED TYPES','Relationship inspector','Browser computation available']],['#studio',['Ontology Studio','OWL classes','Ontology graph explorer']],['#home',['613','Foundations','Make data meaningful']],['#learn',['613 focused topics','matching topics']],['#enterprise',['12 implementation blueprints','Customer 360','Regulatory controlled vocabulary']],['#workbench',['MDM × RDM × metadata workbench','Northstar Health','RDM crosswalk tester']],['#publishing',['Legal, licensing & privacy','OBO Foundry open license policy']],['#lesson/ent-07-00',['Versioned SKOS concept scheme releases','Implementation walkthrough']],['#project',['enterprise-mdm-rdm-metadata','clinical-study']]]) await testRoute(route,terms);
})().catch(e=>{console.error(e);process.exit(1)});
