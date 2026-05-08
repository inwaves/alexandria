# Alexandria

Alexandria is the public research substrate used by Fab's MVP.

Agents can write completed artifact bundles under `artifacts/`. Humans and Fab can also use this repository for public research notes, transformed findings, and reviewed context.

## Seed Notes

This initial seed contains public-safe notes on scalable oversight and weak-to-strong generalization copied from the earlier research substrate. Frontmatter is intentionally minimal: `title`, `url`, and `created` when available.

## Fab Ingest Smoke Fixture

The bundle at `artifacts/safety-finetuning-pilot/ws_001/fab-ingest-smoke-001/`
is a durable smoke fixture for Fab's remote ingest boundary. It targets Fab's
pilot contract and can be ingested into a temporary Fab store seeded with
`fab pilot-fixture`.

## Expected Agent Artifact Shape

```text
artifacts/<program>/<workstream_id>/<run_id>/
  manifest.json
  artifact/
    report.md
    code/
    results/
    logs/
  READY
```
