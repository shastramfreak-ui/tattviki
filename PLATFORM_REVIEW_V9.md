# Tāttvikī v9 — Visual Explorer and Theme Review

## Problem resolved

The previous layout stacked dozens of nodes in long, fixed type columns. They became too small to read after fitting to the viewport, and the page had no light theme option. The v9 Studio opens with a graph-of-groups overview. It allows people to choose a more suitable layout before expanding to all individual entities.

## Features delivered

- Five layout modes: Overview, Radial, Organic, Hierarchy, Swimlanes.
- Group/category drill-down and five semantic scope filters.
- Four visual density levels: 45, 80, 150 and 240 entities.
- Wheel zoom, plus/minus, fit, pointer dragging and two-pointer pinch, node repositioning.
- Interactive entity selection with existing editor inspector.
- Neighbor focus, relationship labels, graph search, full-width focus and SVG export.
- Theme switch applies across site, persisted in browser localStorage.
- Dark and light graph palettes preserve type distinctions and entity label contrast.
- No external JavaScript package, font, CDN, or graph API requirement.

## Tested

- **26 v9 browser interaction checks passed** in a headless Chromium browser including graph layout changes, zoom/pan, pointer node movement, labels, category drilldown, light/dark switching, graph controls on mobile, navigation, and Turtle export.
- 613 lessons, 27 tools and 7 methods pass the static curriculum validator.
- All 9 representative site routes pass the static DOM renderer.
- Turtle, RDF/XML and JSON-LD exports parse as isomorphic RDFLib graphs (512 enterprise example triples).
- Six enterprise MDM/RDM Python unit tests pass.

## Limits and deployment

Graph render limit is a visualization performance control. It does not remove data from the authored ontology. This client-side graph is not a 3D engine or a full SPARQL/OWL inference engine; those features still use the separately hosted backend. Node drag positions are not persisted into the RDF model. The static GitHub Pages app works without a paid service. Deploy the entire `Tattviki` directory contents (not the containing folder) at the Git repository root.

## Content and branding

The learning examples are fictional, no restricted medical terminologies are bundled, and the visible creator credit remains **Shubham**.
