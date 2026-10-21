#!/usr/bin/env node
/* Generate published sample outputs directly from the actual Studio authoring model. */
const fs=require('fs'),vm=require('vm'),path=require('path');
const base=path.resolve(__dirname,'..'),out=path.join(base,'projects/ontology-studio');
const sandbox={window:{},localStorage:{getItem(){return null;},setItem(){}},console};
for(const file of ['studio-templates.js','studio-graph.js','studio.js'])vm.runInNewContext(fs.readFileSync(path.join(base,'assets',file),'utf8'),sandbox,{filename:file});
const studio=sandbox.window.TattvikiStudio;
const check=studio.checks();
if(check.issues.length)throw Error('Cannot publish invalid sample ontology: '+check.issues.join('; '));
fs.mkdirSync(out,{recursive:true});
for(let [file,value] of [['enterprise-ontology.ttl',studio.exportTurtle()],['enterprise-ontology.rdf',studio.exportRdfXml()],['enterprise-ontology.jsonld',studio.exportJsonLD()],['editable-ontology-project.json',JSON.stringify(studio.model(),null,2)+'\n']])fs.writeFileSync(path.join(out,file),value,'utf8');
console.log('Studio sample exported:',studio.triples().length,'triples,',studio.model().classes.length,'classes');
