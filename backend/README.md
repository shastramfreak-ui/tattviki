# Tāttvikī Advanced Semantic Engine — v7 compatible

This is a **real self-hosted Python backend**, separate from the free static GitHub Pages site. It is for local learning, classrooms, and trusted environments. **Do not expose its development server directly to the public internet.** GitHub Pages cannot execute Python or keep a SQLite database.

## Start on Windows (two terminal windows)

Requirements: Python 3.11–3.13 and internet access **once** to install third-party packages.

1. Extract the Tāttvikī ZIP and open `Tattviki`.
2. Double-click **`START_WINDOWS.bat`** to serve the static website at `http://localhost:8000/#semantic`.
3. Double-click **`backend/START_ADVANCED_WINDOWS.bat`**. The first run downloads FastAPI, RDFLib, owlrl, pySHACL and dependencies. Keep the terminal open; it serves `http://127.0.0.1:8765`.
4. Open **Semantic Workbench → Full semantic engine**, enter `http://127.0.0.1:8765`, click **Connect / Check**, and choose the capability you want to use.
5. Your database is stored locally in `backend/.data/projects.sqlite3` by default. This is ignored by Git and **must never be committed or posted publicly**.

Manual equivalent from the `Tattviki` root:

```powershell
py -m pip install -r backend/requirements.txt
py -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
```

Run the website in a separate terminal:

```powershell
py -m http.server 8000
```

Open `http://localhost:8000/#semantic`.

## Advanced capabilities & accuracy

| Feature | Backend | Limits |
|---|---|---|
| SPARQL | RDFLib 7, SELECT/ASK/CONSTRUCT/DESCRIBE | Read-only, no SERVICE/FROM/remote federation, up to 150 result rows |
| RDFS inference | Built-in transitive closure | Subclass, subproperty, domain/range and type materialization; **subset** of complete RDFS semantics |
| OWL RL inference | OWL-RL (`owlrl`) | Materialization of the OWL 2 RL profile; depends on installed module |
| SHACL validation | pySHACL | SHACL Core (not JS plugins or advanced SHACL rules); depends on installed module |
| DL-style instance explorer | Named class intersection/union | Class names joined with `and`/`or`; **NOT** complete Manchester syntax |
| Optional HermiT classifying reasoner | Owlready2 + Java, separate worker | Experimental; timed 45 seconds; no external imports, under 1,000 asserted triples; Java/Owlready2 not installed in build environment |
| Version history | SQLite immutable snapshot revisions | Every save creates a new revision; 409 on concurrent edits |
| Collaboration | Accounts + owner/editor/viewer roles | No live cursor/realtime editing; owner can grant/revoke access; local server only by default |

To try optional experimental HermiT OWL DL classification:

```powershell
py -m pip install -r backend/requirements-dl.txt
java -version
```

Then choose **Try HermiT OWL DL (Java)**. Some ontologies cannot be classified by HermiT and may return an error. This optional integration is **not validated on this build machine** and should be treated as experimental; it is not promised to support every Protégé capability.

A built-in self-hosted API provides interactive docs at `http://127.0.0.1:8765/docs`.

### Example SPARQL against the sample enterprise model

```sparql
PREFIX ex: <https://example.org/tattviki/enterprise#>
SELECT ?dataset ?owner WHERE {
  ?dataset ex:ownedBy ?owner .
} ORDER BY ?dataset LIMIT 25
```

### Example SHACL

```turtle
@prefix ex: <https://example.org/tattviki/enterprise#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
ex:DatasetOwnerShape a sh:NodeShape ;
  sh:targetClass ex:Dataset ;
  sh:property [ sh:path ex:ownedBy ; sh:minCount 1 ; sh:class ex:Organization ] .
```

### Team workflow

1. Register a user with password **12 characters or longer**; the API stores PBKDF2-HMAC salted password hashes, not plaintext passwords.
2. **Create from editor** → selects your shared project. **Load into editor** → syncs a selected version.
3. Make changes in visual ontology editor → **Save new revision**. If another user saved first, a `409` version conflict tells you to reload before retrying.
4. Owner can grant `viewer` or `editor` to already-registered users or revoke access. Viewers cannot edit/restore. Anyone with project access can inspect revisions.
5. **Show history** → choose a revision → **Restore selected revision**. Restore creates a new immutable revision; existing history is preserved.

The shared JSON project is separate from browser-local undo/redo. Only explicit save actions publish modifications to the shared database.

## Deployment security before any shared online hosting

This is **development-grade authentication**, not a complete production deployment. For a public multi-user service, supply at least: HTTPS/reverse proxy, origin allowlist, secure session expiration/rotation, CSRF/CSP review, API authentication and rate limits for costly computations, audited dependency versions, isolation/sandboxing of reasoners, user and project quotas, input-size and execution-time constraints, persistent encrypted backups, a privacy and acceptable-use policy, and account-recovery flows. Run this backend in a separate secured service—not GitHub Pages.

To permit a specific trusted front-end origin, set `TATTVIKI_CORS_ORIGINS` to an explicit comma-separated list *before* starting uvicorn. E.g. local defaults include `http://localhost:8000`. Setting a public GitHub Pages origin may require secure HTTPS backend hosting and additional browser private-network permissions. **Never store private enterprise schemas or credentials in a public repository.**

### Tests

```powershell
py -m unittest -v backend.tests.test_api
py scripts/test_advanced_browser.py
```

`test_advanced_browser.py` uses an in-process HTTP adapter because the restricted test environment blocks local browser networking. It exercises the actual FastAPI routes with Playwright interactions, but does not prove deployment-specific CORS, SSL, public networking, or installed HermiT execution.
