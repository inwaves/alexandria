# Alexandria

Alexandria is the public research substrate used by Fab's MVP.

Agents can write completed artifact bundles under `artifacts/`. Humans and Fab can also use this repository for public research notes, transformed findings, and reviewed context.

## Seed Notes

This initial seed contains public-safe notes on scalable oversight and weak-to-strong generalization copied from the earlier research substrate. Frontmatter is intentionally minimal: `title`, `url`, and `created` when available.

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
