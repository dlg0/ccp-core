# CCP golden fixtures

These fixtures are stable CCP inputs used to exercise schema validation, linked object flows, and failure handling.

Treat them as golden cases:
- change them only when the intended CCP behavior changes
- add a new fixture instead of silently changing the meaning of an existing one

## Layout

- `positive/minimal/` holds the smallest schema-valid object for each CCP kind
- `positive/linked/` holds schema-valid objects that reference each other as one coherent scenario
- `negative/schema/` holds objects that should fail JSON Schema validation
- `negative/semantic/` holds objects that should pass JSON Schema validation but fail higher-level semantic checks

## Naming conventions

Fixture filenames match object ids: `{id}.json`.

The prefix still indicates the CCP object kind:
- `CR-####` for Change Requests
- `DR-####` for Decision Records
- `EP-####` for Execution Plans
- `EV-####` for Evidence Packs

The numeric bands describe the fixture family:
- `1000` series for positive minimal fixtures
- `2000` series for positive linked fixtures
- `3000` series for negative schema fixtures
- `4000` series for negative semantic fixtures

When a scenario spans multiple objects, reuse the same numeric suffix across the set. For example, `CR-2001`, `DR-2001`, `EP-2001`, and `EV-2001` are one linked positive scenario.

## Expected outcomes

- `positive/minimal` fixtures should validate against the frozen CCP v0.1 JSON Schemas one file at a time
- `positive/linked` fixtures should validate against the schemas and should resolve correctly when a consumer checks cross-object references
- `negative/schema` fixtures should fail schema validation, and each fixture should keep the failure focused on one specific shape problem
- `negative/semantic` fixtures should remain schema-valid while failing semantic checks such as unresolved links or missing governing objects

The current automated coverage validates every file under `fixtures/positive/` in `tests/test_examples_validate.py`. Negative fixtures are intended for must-fail validator and CLI coverage.

## Reuse guidance

- use `positive/minimal` when a test only needs one valid object shape
- use `positive/linked` when the behavior depends on relationships between CCP objects
- use `negative/schema` when the failure should happen at JSON Schema validation time
- use `negative/semantic` when the input should survive schema validation and fail later semantic checks
- keep each negative fixture narrow so the expected failure is obvious
- keep filenames, ids, and directory placement aligned
- prefer adding a new numbered scenario over repurposing an existing golden fixture
