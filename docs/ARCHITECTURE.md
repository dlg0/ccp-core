# CCP Core Architecture

This note explains the shape of the system around the frozen CCP v0.1 contract.

- The binding v0.1 rules live in `docs/CCP_NORMATIVE_SPEC_V0.1.md`.
- The consultation draft in `docs/consultation/CCP_PUBLIC_CONSULTATION_DRAFT.md` remains useful background, but it is not the compatibility source of truth.
- Machine-readable version metadata lives in `protocol/version.json`.

## Canonical idea

CCP is a **protocol and object model**, not a centralized system.

A valid CCP workflow can exist with:
- source repos in git
- a separate git-tracked control-plane repo
- optional task/execution backends
- local or hosted workers

## Planes

### 1. Source plane
The code and other implementation artifacts.

### 2. Control plane
Change Requests, Decision Records, Execution Plans, Evidence Packs, and any optional coordination history an implementation chooses to keep.

### 3. Execution plane
Live task coordination. This may be Beads + Dolt, a simpler local queue, or another compatible system.

CCP core defines the control-plane semantics. It does not mandate the execution plane.

## Control-plane storage

The recommended default is a dedicated git repo containing structured CCP objects and any optional extension history a project wants to keep.

For the frozen v0.1 portable contract, the control plane uses one JSON file per core object under a control-plane root. That root may be a standalone repository or a repo-local `control/` directory.

Review-event files, task-claim logs, and other coordination history may exist as extensions, but they are not required by the portable v0.1 baseline.

Reasoning:
- auditable
- local-first
- branchable/forkable
- works offline
- can be mirrored or hosted anywhere

## Workers

Workers are usually **pull-based**:
- sync shared state
- discover ready work
- claim work with a lease
- execute
- validate
- publish evidence
- release or renew the claim

The worker model is an implementation pattern, not a protocol requirement, but CCP should describe enough semantics that Foundry and other tools can behave coherently.

## CLI role

The `ccp` CLI should be:
- easy to script
- easy for agents to use
- boring
- deterministic

It should never become the only way to understand CCP.

It should follow the normative spec and protocol metadata, not replace them.
