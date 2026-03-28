# CCP Core PRD
## Spec + reference toolkit

**Product/repo name:** CCP Core  
**Scope:** open specification, schemas, examples, conformance fixtures, and thin reference CLI

## 1. Purpose

This repo exists to define CCP independently from any one product implementation.

It should answer:

- what the CCP objects are
- what their required semantics are
- what lifecycle transitions are valid
- how CCP should work in a local-first git-based environment
- how an implementation proves it is CCP-compatible

This repo should **not** turn into Foundry. It is allowed to include a thin toolkit so the spec is executable and testable.

## 2. Outputs

The first public release of this repo should contain:

1. Consultation draft
2. Normative spec text
3. JSON schemas for:
   - Change Request
   - Decision Record
   - Execution Plan
   - Evidence Pack
4. Examples and golden fixtures
5. Conformance tests
6. Reference CLI (`ccp`)

## 3. Design constraints

- Keep the protocol implementation-neutral
- Do not require GitHub, Beads, Dolt, or any hosted service
- Preserve local-first operation
- Keep object history auditable
- Treat the CLI as **thin plumbing/porcelain**, not the product itself
- Avoid Foundry-specific product decisions leaking into the core spec

## 4. CLI scope

The CLI is intentionally modest. It should:

- scaffold valid objects
- validate objects and repos
- render human-friendly summaries
- index a control-plane repo
- apply status transitions with guardrails

It should not try to become:
- a team collaboration UI
- a hosted service
- a central scheduler
- a proprietary workflow engine

## 5. MVP milestones

### Milestone 1 — Spec skeleton
- publish consultation draft
- establish repo structure
- define object IDs and required fields
- define lifecycle state machine

### Milestone 2 — Schemas + examples
- write JSON schemas
- add example objects
- add golden fixtures

### Milestone 3 — CLI
- `ccp init`
- `ccp new`
- `ccp validate`
- `ccp render`
- `ccp index`
- `ccp transition`

### Milestone 4 — Conformance
- fixture-driven tests
- documented conformance profiles
- first tagged pre-release

## 6. Success criteria

- another team can understand CCP from this repo without reading Foundry docs
- an agent can create valid CCP objects with this repo alone
- a fully local demo can run without Foundry
- Foundry can depend on this repo as its source of truth for CCP semantics
