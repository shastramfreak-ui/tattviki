# Enterprise metadata × MDM × RDM × semantics — executable lab

**Fictional organization:** Novella Research Group. Every source row and organization name is invented. No proprietary, clinical, personal, or customer system content is supplied.

## The actual problem
CRM and ERP both maintain party identities and statuses; analysts require a governed customer dimension, stewards own the canonical identity, and the catalog must show the downstream blast radius of changes. RDM aligns incompatible codes (`CRM ACT` / `ERP A` => approved concept `ACTIVE`); MDM creates a master party using a deterministic **synthetic registration key**; DCAT and Dublin Core publish catalog metadata; PROV-O records sources and column-level lineage. SHACL checks that the resulting semantic graph meets data contract requirements.

## Workflow

```bash
cd projects/enterprise-mdm-rdm-metadata
python -m pip install -r requirements.txt
python generate.py
python run_queries.py
python -m unittest -v test_lab.py
python generate.py --break-shape  # deliberate negative SHACL test: exits nonzero
```

## Input / output

- `data/crm_parties.csv` and `data/erp_parties.csv`: duplicate synthetic source records and legal names.
- `data/status_reference.csv`: approved RDM crosswalk including source, local codes, canonical meaning and release version.
- `data/catalog.csv`: metadata for four technical data assets, owning teams and classifications.
- `data/lineage.csv`: table and column lineage and pipeline transformation labels.
- `generate.py`: deterministic `registration_key` merging, ERP-preferred survivorship, unresolved-record quarantine, semantic output, validation.
- `output/enterprise.ttl`: generated and fully queryable RDF graph.
- `output/quality_report.json`: explicit master count, quarantine and graph size.
- `output/shacl-report.txt`: validator report.
- `queries/`: four real SPARQL examples (golden records, reference mappings, downstream impact, metadata catalog discovery).
- `test_lab.py`: real unit tests, not screenshots or fake console responses.

## Training scenarios

1. Change CRM party C100 to `HOLD` without changing ERP E800. Inspect the modeled conflict and determine stewardship priority; discuss why status survivorship is distinct from identity matching.
2. Delete one `registration_key` and inspect the quarantine result. Add a steward approval queue rather than auto-merging by display name.
3. Add another RDM code without a canonical mapping. The pipeline must record the unmapped value and avoid silently converting it to `ACTIVE`.
4. Add one upstream `source_column` to the lineage file, regenerate, and inspect how column-level provenance changes.
5. Deliberately break SHACL with `--break-shape`; use the report to pinpoint the missing approved status.
6. Replace the toy matching rule with tested blocking + score thresholds + manual review. Never silently union uncertain identity clusters.

## Important boundaries

The matching policy is deterministic and deliberately simplistic: **do not treat it as a production MDM engine**. Master identity and source provenance require human governance, business rules, privacy review and robust audit. SHACL confirms stated graph constraints but cannot prove records refer to the same legal person. The example catalog license links apply only to these invented teaching records, not to real source exports. No external service calls are made.

## Standards links

- W3C DCAT 3: https://www.w3.org/TR/vocab-dcat-3/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- W3C SKOS: https://www.w3.org/TR/skos-reference/
- W3C SHACL: https://www.w3.org/TR/shacl/
- DCMI Terms: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
