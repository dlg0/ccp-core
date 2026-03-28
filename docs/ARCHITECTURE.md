# CCP Core Architecture

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
Change Requests, Decision Records, Execution Plans, Evidence Packs, and related events.

### 3. Execution plane
Live task coordination. This may be Beads + Dolt, a simpler local queue, or another compatible system.

CCP core defines the control-plane semantics. It does not mandate the execution plane.

## Control-plane storage

The recommended default is a dedicated git repo containing structured CCP objects and append-oriented history.

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
