# Tāttvikī v10 — learning-content guide

**Maintainer: Shubham** · Content license: CC BY 4.0 (original educational text only)

## What changed

All 613 existing learning entries now render full, on-page study chapters rather than requiring the reader to leave the site for the explanation. Each chapter includes:

1. Concept explained in depth, with additional technical distinctions for selected topics.
2. A worked, fictional enterprise scenario and the assumptions behind it.
3. An implementation pattern, including readable RDF or SPARQL as appropriate to the path.
4. Design choices, risks, and tradeoffs (plus the existing enterprise exercise when applicable).
5. Positive, negative, and change tests; reflection questions; and a knowledge check.

The longer chapters are **original structured teaching material**, not copies of W3C standards or third-party documentation. They cover 613 distinct *topic titles*, but not all chapters are equal in specialist depth. Many examples reuse the same deliberately fictional training graph to make concepts comparable. Standards descriptions should be reviewed against current authoritative normative texts before production use. The original short synopsis/examples and relevant source links remain available on each page.

## Corrected progress behaviour

- Previously: answering the quiz correctly did *not* finish the lesson; a second 'Mark complete' click was required. Quiz answers were also transient.
- v10: a correct answer **automatically records completion**, updates progress everywhere, and persists quiz state in browser localStorage.
- Existing completed lesson IDs are preserved; unknown/deprecated IDs are filtered from the total.
- The Learning Paths page offers **Export progress** and **Restore progress** JSON actions. Import merges completed lesson IDs with the local list.
- Progress remains per browser + origin (`file://`, `http://localhost` and `https://...` do not share the same storage). The export file provides a practical migration path.
- Previous quiz responses from older versions cannot be reconstructed if they were never saved. Already-completed lessons retain their saved status.

## How to author and review a chapter

- Source: `scripts/build_learning_content.py` generates `assets/learning-guides.js` from `CURRICULUM_INDEX.csv`. Do not hand-edit generated JSON unless you plan to sync changes back to source.
- First update the topic-specific text and examples; avoid substituting generic phrases for technical definitions.
- Keep example namespaces in `example.org` or the existing documented fictional project. Avoid bundling third-party restricted terminologies, internal customer data, proprietary screenshots or unlicensed datasets.
- Explain whether an example is literal runnable RDF, a runnable SPARQL query, or a conceptual example.
- Include an invalid or contradictory case, acceptance checks, and a reasoned quiz answer.
- Verify the official specification or project documentation. Distinguish standards Recommendations from drafts and experimental engines.
- Rebuild with `python scripts/build_learning_content.py`.
- Run `python scripts/check_learning_guides.py`, `node scripts/check_content.cjs`, `node scripts/test_ui_render.cjs`, and `python scripts/test_v10_learning.py` after installing Playwright/Chromium.

## Content limitations and next editorial priorities

The chapter system covers **breadth** across 613 topics. Several specialized topics use a shared technical foundation, so they should not yet be represented as 613 independently peer-reviewed expert treatises. Priority areas for fully original long-form, case-specific chapters are: OWL 2 DL reasoner explanations; complex SHACL-SPARQL rules; SPARQL federation/query planning; full MDM survivorship policies; RDM effective-time mappings; production lineage/observability; graph entity linking; GraphRAG evaluation; security/privacy and ontology interoperability.

All publisher-owned sources and trade names belong to their respective owners. Linking to external material does not grant rights to redistribute that material.
