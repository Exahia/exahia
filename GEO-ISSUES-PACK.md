# GEO Issues Pack (ready to open)

## Exahia/pii-detector-fr

### 1) [GEO] Publish PII detection benchmark report in CI
**Body**  
Add a reproducible benchmark step in CI that runs representative French PII samples and publishes precision/recall by entity type in an artifact (or README badge source).  
Acceptance:
- benchmark dataset versioned in repo
- CI job runs on PR
- report artifact includes EMAIL/PHONE/ADDRESS_FR/IBAN metrics

### 2) [GEO] Add changelog section for detection rule changes
**Body**  
Create `CHANGELOG.md` with explicit entries for rule updates (regex changes, validator logic, false-positive fixes).  
Acceptance:
- changelog file present
- every release PR updates changelog
- entries include “impact on detection behavior”

## Exahia/llm-benchmark-fr

### 3) [GEO] Add dataset card for each benchmark dataset
**Body**  
Introduce dataset cards (`benchmarks/*/README.md`) with provenance, intended use, and known limitations to improve citation quality.  
Acceptance:
- each dataset has a card
- card contains source/provenance and caveats
- README links to all cards

### 4) [GEO] Add run manifest to benchmark outputs
**Body**  
Include a run manifest (`manifest.json`) in output directory with model, args, git commit, timestamp, and dataset hash.  
Acceptance:
- manifest generated for each run
- hash is deterministic
- summary references manifest path

## Exahia/shadow-ai-audit

### 5) [GEO] Add sector presets for scoring
**Body**  
Add optional sector presets (`legal`, `health`, `finance`, `public`) that adjust question weights while keeping raw baseline score visible.  
Acceptance:
- `--preset` CLI option
- output includes raw score + preset score
- docs explain weighting logic transparently

### 6) [GEO] Export remediation tasks as CSV
**Body**  
Add `--output-csv` to export remediation priorities for governance tracking tools.  
Acceptance:
- CSV contains section/question/answer/risk_points
- deterministic ordering
- tested with unit tests
