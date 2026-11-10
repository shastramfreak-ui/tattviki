/* v13 editorial pass: remove prominent boilerplate from older lessons while preserving IDs,
   stable completion records, domain-specific teaching material, and existing quiz keys. */
(()=>{'use strict';const C=window.OT,G=window.TATTVIKI_GUIDES;
 let audit={genericDescriptions:0,genericAnalogies:0,oldTemplateObjectives:0,genericExamples:0,genericGuideOpenings:0,genericChapterParagraphs:0,genericVerificationLists:0};
 const compact=(s,max=230)=>{s=String(s||'').replace(/\s+/g,' ').trim();return s.length>max?s.slice(0,max-1).replace(/\s+\S*$/,'')+'…':s;};
 for(const l of C.lessons){if(l.id.startsWith('shacl-'))continue;const g=G[l.id];if(!g)continue;
  if(/^Explore .+ in clinical studies|^Explore .+ in (?:a |the )/i.test(l.description||'')){
   audit.genericDescriptions++;
   l.description=compact((g.topicFacts||[])[0]||g.core?.[0]||g.recap||l.description,230);
  }
  if(/ is a specific modeling or engineering decision that affects/i.test(l.analogy||'')){
   audit.genericAnalogies++;
   l.analogy=compact(g.worked?.[1]?.replace(/^Now apply [^:]+:\s*/,'')||g.core?.[2]||l.analogy,330);
  }
  if(l.learn?.[0]?.startsWith('Define ')&&l.learn?.[1]?.startsWith('Apply this concept')){
   audit.oldTemplateObjectives++;
   l.learn=[compact(g.core?.[0]||l.learn[0],225),compact(g.decisions?.[2]||l.learn[1],230),compact(g.review?.a||l.learn[2],225)];
  }
  if(l.example?.includes('# Design focus:')&&g.exampleCode){audit.genericExamples++;l.example=g.exampleCode;}
  if(l.try?.startsWith('Practical investigation:')&&g.review?.a){l.try='Practice with a passing and failing graph: '+g.review.a+' Keep the changed source record and quality report as your evidence.';}
  if(g.subtitle?.startsWith('In this chapter,')){
   audit.genericGuideOpenings++;
   g.subtitle=compact(g.topicFacts?.[0]||g.recap||g.core?.[0],330);
  }
  if(/^The working context is /.test(g.core?.[1]||'')){
   audit.genericChapterParagraphs++;
   let focus=String(g.worked?.[1]||'').replace(/^Now apply [^:]+:\s*/,'').trim();
   g.core[1]=focus||g.core[1];
  }
  // Replace repeated cross-domain distractors with technically false, profile-aware near misses.
  // Keep the authoritative review answer and deterministic rotation unchanged for existing progress records.
  if(g.review?.wrong?.length===2 && (g.review.wrong[0].startsWith('Once a graph parses') || g.review.wrong[0].startsWith('Check that the graph looks') || g.review.wrong[0].startsWith('Treat the display label'))){
    const bank={
      SKOS:['Interpret every skos:broader link as an OWL subclass axiom without reviewing meaning.','Use the preferred display label as the permanent identifier of a scheme concept.','Assume synonyms prove two codes are exactly equivalent across versions.','Treat the absence of a label language tag as proof that multilingual rules are satisfied.'],
      OWL:['Assume an OWL subclass declaration rejects all records missing a required field.','Equate two individuals solely because their labels look similar.','Treat a model being serializable as evidence that its logical classes are satisfiable.','Assume OWL cardinality follows the closed-world rules of a relational database.'],
      SHACL:['Assume successful Turtle parsing proves the data conforms to its shapes.','Use an OWL domain declaration as a substitute for SHACL count constraints.','Skip deliberately invalid focus-node tests because all sample graph nodes are typed.','Treat a graph-wide validation report as equivalent to validating every enterprise application.'],
      SPARQL:['Assume a SELECT result has been validated for data quality without independent tests.','Treat the lexical order of IRIs as evidence of business priority.','Join on display labels alone when the query has stable entity IRIs.','Assume a successful LIMIT 10 query proves the full dataset is complete.'],
      Metadata:['Accept lineage claims without identifying a generating source or transformation.','Treat a catalog display name as a unique persistent dataset identifier.','Assume every field has a steward because a table has a schema.','Skip source-to-target metadata mapping validation when the file format is correct.'],
      MDM:['Merge entities solely because their normalized names have a high similarity score.','Assume every surviving source attribute is authoritative without provenance.','Assign a new master identifier whenever a preferred label changes.','Consider an unresolved match candidate equivalent to an approved golden record.'],
      RDM:['Treat a local status label as a global reference concept identifier.','Promote a candidate code to an approved vocabulary without steward review.','Assume source and target codes are equivalent because the English labels are similar.','Publish a new reference-data mapping without a version or consumer impact check.'],
      RDF:['Use the textual label of a resource in place of its stable IRI.','Assume a well-formed triple proves the intended real-world claim is true.','Replace a resource link with a quoted literal without reviewing the changed semantics.','Treat duplicate-looking statements as an ontology-level validation mechanism.'],
      Governance:['Approve a semantic change without recording its source or responsible steward.','Use a graph visualization as the sole evidence of regulatory readiness.','Assume policy acceptance follows automatically from syntactically valid RDF.','Skip impact review when a controlled vocabulary term is deprecated.'],
      'Enterprise Integration':['Assume source updates will always arrive in business order.','Use human-readable labels as the sole join key across source systems.','Ignore downstream consumers when the RDF export format remains unchanged.','Treat a successful one-record ingestion as proof of replay and idempotency.'],
      GraphRAG:['Treat an ungrounded model answer as evidence that graph retrieval succeeded.','Assume graph traversal replaces permission and provenance controls.','Accept one retrieval query as proof of robustness on multi-hop questions.','Equate an embedding similarity score with an asserted enterprise relationship.']
    };
    let options=bank[g.profile]||bank.Governance;
    let h=[...l.id].reduce((v,c)=>v+c.charCodeAt(0),0);let n=h%options.length;
    g.review.wrong=[options[n],options[(n+1+(h%2))%options.length]];
    const risk=g.review.q.startsWith('Which implementation risk matters');
    const versions=risk?[
      `During implementation of ${l.title}, which failure mode must the engineer address?`,
      `A reviewer challenges ${l.title}. Which engineering risk is relevant?`,
      `For a release involving ${l.title}, which concern deserves an explicit negative test?`,
      `Which risk could undermine ${l.title} even when the RDF syntax is valid?`,
      `What implementation assumption should be checked for ${l.title}?`
    ]:[
      `What is the decisive acceptance evidence for ${l.title}?`,
      `Before approving ${l.title}, which technical verification matters?`,
      `A team has implemented ${l.title}. What should its quality review demonstrate?`,
      `What would you check in a release test for ${l.title}?`,
      `Which acceptance test is defensible for ${l.title}?`
    ];
    if(risk||g.review.q.startsWith('Which acceptance check would meaningfully'))g.review.q=versions[h%versions.length];
  }
  if(g.verification?.[0]?.startsWith('Positive case:')){
   audit.genericVerificationLists++;
   let consequence=String(g.worked?.[2]||'').replace(/^Consider a counterexample\.\s*/,'').trim();
   g.verification=[
     'Acceptance fixture: '+(g.review?.a||'Validate the documented domain expectation.'),
     'Negative fixture: '+(consequence||'Modify a source value and identify the failed rule.'),
     'Consumer-change test: '+String(g.decisions?.[2]||'Compare the before and after semantic model.').replace(/^Operational boundary:\s*/,''),
     'Evidence: save the RDF or query, exact source references and report associated with '+l.title+'.'
   ];
  }
 }
 window.TATTVIKI_EDITORIAL_AUDIT=audit;
})();
