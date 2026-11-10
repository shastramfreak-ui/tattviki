# Content review — Tāttvikī v13

## What was audited

The v12 catalog included 707 topics. The user identified repetitive teaching and quizzes, so v13 adds 30 SHACL-specific chapters (737 total) **and performs a measurable template cleanup without changing existing lesson IDs**.

Structural checks find distinct lesson IDs/titles and require a guide for every lesson. The audit detects common stock phrases, placeholder examples and repeated verification lists. It also protects earlier completion records by retaining lesson identifiers.

## What was changed

- 240 weak copied analogies replaced with more context-relevant study scenarios.
- 240 template-like objective sets revised using domain-specific guide content.
- 190 placeholder examples using `# Design focus:` replaced by the corresponding guide code examples.
- 613 generic study-chapter openings replaced by more topic-oriented text.
- 613 reused 'working context' second paragraphs replaced with relevant scenario reasoning.
- 665 repeated verification lists replaced with technical checks derived from the corresponding lesson and risks.
- The most repeated generic quiz patterns receive varied, profile-aware distractors, while lesson IDs and existing correct-option rotation remain stable.
- 30 new SHACL chapters contain unique concept explanations, examples, pitfalls and targeted practice instructions.

To reproduce the template-level audit, run:

```bash
node scripts/audit_repetition.cjs
node scripts/check_content.cjs
python scripts/check_learning_guides.py
```

A machine-readable audit is in [`CONTENT_AUDIT_V13.json`](CONTENT_AUDIT_V13.json).

## What is *not* claimed

A template audit cannot prove all 737 lessons are free from **semantic overlap**, nor does it prove every technical definition is a comprehensive expert-authored chapter. Earlier content was largely generated from a common structure; some topics still deserve manual rewriting, additional worked code, diagrams and independent SME review. There are also deliberate prerequisite overlaps (for example, IRIs appear in RDF, SKOS and SHACL lessons).

Priority editorial queue for community review:

1. OWL 2 profile semantics and reasoner completeness.
2. SPARQL 1.1 advanced queries including UPDATE and federated scenarios.
3. SHACL Core versus SHACL 1.2 drafts and engine differences.
4. RDM mapping semantics and per-language SKOS integrity.
5. Metadata / MDM identity and lineage contract examples.
6. Retrieval evaluation and GraphRAG factual grounding.

The v13 Python/SHACL fixtures are original, synthetic educational materials. No restricted medical terminology tables or client datasets are shipped.
