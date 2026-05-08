# Fab Ingest Smoke Fixture

This is a durable Alexandria fixture for testing Fab's remote ingest boundary.

It represents a completed external-agent run bundle. The content is deliberately
small: the point is to verify that Fab can read an Alexandria artifact bundle,
validate the manifest, register the artifact path, and append a state packet
without the agent cloning Fab or writing into Fab's store directly.

## Expected Fab Behavior

When ingested into a Fab store seeded with the pilot fixture:

- the manifest contract should match `contract_pilot_a3_false_positive` v1;
- the target workstream should be `ws_001`;
- Fab should append one packet to `ws_001`;
- Fab should preserve the artifact bundle root as an external path;
- the limitation should surface as an attention reason.

## Non-Goals

This fixture does not test commit monitoring, exactly-once ingestion, or
Alexandria write-back. Those belong to the watcher layer above `ingest-run`.
