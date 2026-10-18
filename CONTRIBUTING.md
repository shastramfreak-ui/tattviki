# Contributing to Tāttvikī

Tāttvikī exists to teach semantic web and knowledge graph concepts without unnecessary jargon.

## What to contribute

- A clear explanation with one concrete everyday analogy.
- Working examples in RDF, Turtle, OWL, SKOS, SPARQL or SHACL, where appropriate.
- Link fixes, accessibility improvements or translations.
- New tools, approaches or methodology comparisons grounded in their primary documentation.
- New use cases with fictional, open-licensed or attribution-compatible sample data.

## Editorial checklist

1. **Accurate:** distinguish RDF and property graphs; OWL inference and SHACL validation; draft specifications and Recommendations.
2. **Runnable:** code examples must work with the documented tool. The starter Playground supports a small Turtle/SPARQL subset; advanced syntax requires a real library.
3. **Accessible:** explain each new acronym, write actionable alt text where needed, and avoid color-only meaning.
4. **Sourced:** link at least one authoritative reference (official specification, repository, documentation or credible paper); record dates for news.
5. **License-safe:** paraphrase source material; do not paste large sections of proprietary textbooks or vendor documentation.
6. **Reviewed:** keep a second pair of eyes on claims about reasoning, compliance, quality, tooling and licensing.
7. **Privacy-first:** do not add trackers or a user account requirement.

## How to add a lesson

Open `assets/content.js` and add an object under `lessons` with a unique `id`, valid `path`, `title`, `description`, `analogy`, learning points, example, activity, a three-option knowledge check and official reference URL. Use `node scripts/check_content.cjs` to catch missing fields before requesting a merge.

## How to add a tool

Add a unique entry in `assets/content.js` → `tools`. Provide a stable official HTTPS link, purpose, tag, and licensing category. Do not imply that a "free tier" is entirely open source or permanently free. Verify with the vendor/project website.

## Pull request summary template

Describe your learning goal, who benefits, what changed, how it was tested, and which sources verify new factual claims. Screenshots of the responsive layout are welcome when UI changed.


## Enterprise content & license policy (v3)

- Publish an original topic only if the title is unique and its example, acceptance criterion and implementation exercise are topic-specific. Do not add duplicate lessons to increase totals.
- Every lesson or external dataset must include a primary documentation URL and an explicit statement of redistribution rights when republishing material. Publicly viewable is not the same as openly licensed.
- Use original invented data for examples; do not copy employer or client schemas, medical records, screenshots, credentials or licensed terminology exports.
- Before adding real industry datasets, complete `LEGAL_AND_DATA_REVIEW.md` and request a separate technical/privacy review.
- Run `node scripts/check_content.cjs`, `node scripts/test_ui_render.cjs`, and the enterprise Python tests before submitting a change.
- Contributors should never imply endorsement by third-party organizations whose tools or standards are described.
