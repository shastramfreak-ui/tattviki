# Tāttvikī v3 — preliminary publication and legal-risk review

**Review date:** 18 October 2026  
**Status:** Preliminary engineering and content hygiene review; not legal advice and not clearance to publish under any country's law.

## Executive assessment

The repository was designed to reduce copyright, privacy, confidentiality and licensing risks, **not to guarantee immunity from claims**. It should not be made public until the owner checks trademarks for the project name and gets a qualified legal review if substantial business/regulated data, copyrighted terminology files, other people's source code, or externally provided screenshots will be added.

| Risk | Current approach | Required review before publishing new content |
|---|---|---|
| Real enterprise confidential data | Synthetic CRM/ERP, metadata and study examples; not taken from client systems | Search for client/project identifiers, internal schemas, secrets, system URLs and protected material |
| Licensed vocabularies | Prefer OBO Foundry or other verified openly licensed vocabularies; link to proprietary sources but do not bundle their content | Check per-resource license, whether derivative mappings are redistributable and territorial rules |
| W3C documentation | Our own explanations with source links, not pasted standard excerpts | If copying standards text, comply with appropriate W3C document license/notice and status requirements |
| Third-party code | No bundled proprietary applications; link to tools and documentation | Inspect dependencies and include notices if code is vendored |
| Third-party images/logos | Original icon/illustrative diagrams; no vendor logos packaged | Permission, license and trademark review if adding other imagery |
| Personal/medical data | No real patient/customer/employee records in training assets | Avoid reidentification and consult data protection counsel before any real input |
| Project branding | Name Tāttvikī requested by owner; no clearance statement | Search India and relevant countries' trademark databases for confusingly similar marks, classes and usage |
| Content CC BY 4.0 | Original educational content marked CC BY 4.0 | Include author credit, license and change notices; license is irrevocable once granted |
| MIT code | Existing original code under MIT | Maintain copyright and source notices; does not license trademarks or third-party data |

## Trademark status

No definitive trademark availability determination was performed. A general web search for "Tāttvikī" and "Tattviki" is **not** a trademark clearance search. The [Indian Trademark Registry public search](https://tmrsearch.ipindia.gov.in/tmrpublicsearch) requires an interactive login/OTP/captcha in the observed flow. Owner should perform an official search, including phonetic and transliterated variants, and get professional advice before registering a domain or filing a mark.

## Reference checks — primary documents

- [W3C 2023 Document License](https://www.w3.org/copyright/document-license-2023/)
- [W3C DCAT 3 Recommendation](https://www.w3.org/TR/vocab-dcat-3/)
- [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [OBO Foundry open licensing principles](https://obofoundry.org/principles/fp-001-open.html)
- [Wikidata reuse license](https://www.wikidata.org/wiki/Wikidata:Licensing)
- [Creative Commons Attribution 4.0 legalcode](https://creativecommons.org/licenses/by/4.0/legalcode.en)
- [Indian IP Public Trademark Search](https://tmrsearch.ipindia.gov.in/tmrpublicsearch)

## Recommended publication controls

1. Require every contributed dataset and third-party asset to have a declared author, source URL, license, rights-holder and permission evidence.
2. Apply pre-commit/CI checks for high-risk strings, email-like identifiers, internal addresses and common secret patterns; this is defense in depth, not a guarantee.
3. Avoid publishing a screenshot or terminology export from an employer's systems.
4. Use short independent summaries and references instead of copying proprietary documentation.
5. Label simulated case studies and model-generated examples clearly as fictional and non-certified.
6. Run an expert technical review of ontology semantics, identity resolution and SHACL before describing examples as production-ready.
7. Have a contribution process for removal requests, licensing corrections, errata and privacy reports.

## Existing content depth and caveats

- 13 starter lessons: extended original explanations.
- 240 legacy micro-lessons: distinct titles, brief contextual primers with common pedagogical structure.
- 360 enterprise focused lessons: distinct topics, module-specific scenarios, example triples, deliverable prompts, negative-path tests and authoritative external sources; they still use a common educational structure and are **not** 360 individually peer-reviewed training chapters.
- 12 industry blueprints: manually specified source systems, MDM, RDM, semantic patterns, risks and acceptance criteria.
- 2 runnable local Python lab projects; browser workbench is a **teaching simulator**.

Do not use lesson counts as proof of editorial depth or standards conformance. All user-contributed material requires review.

## Public demonstration datasets
- All bundled CRM, ERP, clinical-study and metadata records are **fabricated educational fixtures**. Do not add production extracts, client exports or identifiable records.
- Use the Gene Ontology and other OBO resources as *external references only* until the individual ontology license and attribution requirements have been checked. No external vocabulary bulk download is bundled.
- The site does not imply endorsement by referenced tools or standards organizations. Credit their trademarks to their respective owners.
- A project brand and domain trademark search is recommended before launch.


## v5 Ontology Studio review

- All default individuals, organizations, systems, controlled vocabulary examples and ontologies in the Studio are invented for teaching. No employer, client, actual participant, patient or proprietary internal asset data is included in the Studio default project.
- The studio's generated example uses W3C namespace identifiers (RDF, RDFS, OWL, XSD, SKOS, SHACL, DCTERMS), which are published technical vocabularies. It does not bundle proprietary clinical controlled-vocabulary terms or definitions.
- The studio is an **independent reimplementation of generic ontology modeling workflows**, not a copy of Protégé or WebProtégé. No Protégé trademarks, logos, UI artwork, code, or API libraries are packaged. Protégé is only referenced factually for comparison and interoperability.
- Avoid labeling Tāttvikī as "Official Protégé" or claiming third-party affiliation. Trademark clearance for the new site's name remains outstanding. This is a technical content review, **not a legal opinion**.
- All current studio authoring data is stored in browser localStorage, not on a user-account server. JSON backups and ontology exports may contain users' own data: the users control disclosure; warn against sharing confidential ontologies or uploading them to public GitHub repositories.
- Do not treat classroom structural checks as certification under full OWL 2 DL / SHACL. Use standalone validators/reasoners and human review for regulated use.
