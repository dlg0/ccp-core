# AGENTS.md — CCP Core

You are working in the **CCP Core** repo.

Your mission is to make CCP real as an **open spec + thin reference toolkit**, without accidentally turning this repo into Foundry.

## North star

Humans review **intent, constraints, and evidence**.  
Agents execute implementation.

CCP defines the interoperable objects and workflow semantics that make that possible.

## What this repo owns

This repo owns:
- the public consultation draft
- the normative CCP core spec
- schemas
- examples and golden fixtures
- conformance rules
- a small local CLI

This repo does **not** own:
- rich product UX
- hosted control planes
- proprietary permissions/admin models
- full worker orchestration productization
- GitHub/Beads/Dolt-specific product behavior beyond examples and optional profiles

Those belong in **Foundry** or other implementations.

## Read these first

1. `PRD.md`
2. `docs/consultation/CCP_PUBLIC_CONSULTATION_DRAFT.md`
3. `docs/ARCHITECTURE.md`
4. `docs/FOUNDRY_BOUNDARY.md`
5. `TASKS.md`

## Immediate priorities

1. Stabilize the core object model
2. Keep lifecycle semantics crisp and minimal
3. Make the CLI genuinely usable in a local repo
4. Add examples and fixtures before adding complexity
5. Keep implementation-specific details out of the spec

## Rules

- Prefer **portable, boring, explicit** design
- Prefer JSON schemas and examples over prose-only rules
- If a decision is Foundry-specific, move it out of CCP
- Do not make hosted services mandatory
- Keep the CLI thin and scriptable
- Use the `control/` directory to dogfood CCP changes for this repo itself

## Agent workflow in this repo

When making a nontrivial protocol change:

1. Open or update a Change Request under `control/change-requests/`
2. Add or update a Decision Record if the protocol choice is materially architectural
3. Update schemas/examples/tests together
4. Run CLI validation across the repo
5. Update the consultation draft or normative spec if semantics changed

## Definition of done

A CCP core change is done when:
- the object semantics are clearly documented
- schemas/examples/tests agree
- the CLI can operate on the changed object model
- the change can be understood without Foundry-specific context

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->
