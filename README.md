# CCP Core

Open specification and reference toolkit for the **Change Contract Protocol (CCP)**.

CCP is the open protocol/workflow/object-format for **human-governed, agent-executed software change**.

This repo intentionally contains two things together:

1. **`ccp-spec`** — the normative spec, schemas, examples, and consultation draft
2. **`ccp-cli`** — a thin reference toolkit for creating, validating, indexing, and rendering CCP objects locally

## Mental model

- **CCP** is to **Foundry** roughly as **Git** is to **GitHub**
- or as **OCI** is to **Docker**

Foundry is expected to be a strong product implementation of CCP, but CCP must still make sense:
- as plain files in git
- in a fully local workflow
- with no Foundry service running
- with some future implementation besides Foundry

## Repo layout

- `PRD.md` — build brief for this repo
- `AGENTS.md` — instructions for coding/design agents
- `docs/` — consultation draft, architecture, and repo notes
- `schemas/` — JSON schemas for CCP core objects
- `examples/` — example CCP objects
- `templates/` — local control-plane repo templates
- `src/ccp_cli/` — reference CLI
- `tests/` — conformance and CLI tests
- `control/` — this repo dogfooding CCP for its own evolution

## Immediate goal

Ship a public **v0.1 consultation draft** and a usable local CLI that can:
- initialize a CCP control-plane repo
- create new CCP objects
- validate them against schemas
- render concise summaries
- index a control-plane repo
- apply simple lifecycle transitions safely
