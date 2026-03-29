# AGENTS.md

## What this repo is doing

This repo uses CCP.

That means we do **not** treat code diffs as the main review primitive. Instead, we treat a **Change Request (CR)** as the main review object.

In plain English:

- a PR says **here is the code I changed**
- a CR says **here is the change we want**

A CR is the approved change brief for the work.

It says:
- what should change
- why it should change
- what must not break
- what "done" looks like
- how we will check the result

If you are an agent working in this repo, that is the key thing to understand.

## When to open a Change Request

Open a CR before implementation when one or more of these is true:

- the team needs agreement on **what should change**
- the change could affect behavior, interfaces, schemas, workflows, or user expectations
- there are important rules that must stay true
- "done" is not obvious from the code alone
- the change is risky, broad, or likely to create debate
- the work needs a preserved written rationale

Do **not** skip a CR just because the code looks easy.

Easy implementation can still hide an important change.

## When a quick fix may not need a new CR

A tiny fix may not need a new CR when **all** of the following are true:

- it is clearly within the scope of an already approved CR, and
- it does not change the accepted outcome of that CR, and
- it does not add new risk or new "must not break" rules

If you are unsure, open the CR.

## What to put in a Change Request

Write the CR in plain engineering language.

Focus on five questions:

1. What are we changing?
2. Why are we changing it?
3. What must not break?
4. What does done look like?
5. How will we check?

A good CR should make the intended change obvious without requiring a reviewer to inspect implementation details.

### Good phrasing
Use language like:
- what changes
- what stays true
- done checks
- expected behavior
- before / after behavior
- affected parts of the system
- rollout or migration needs
- remaining risks

### Avoid
Avoid vague process-heavy wording when simple wording will do.

Prefer:
- "what must not break"

over:
- "invariants and constraints" unless you truly need that precision

Prefer:
- "how we will check"

over:
- "required evidence obligations"

## How to think about the other CCP objects

### Decision Record
This is the "why note".

Use it when the reasoning behind the change matters and should be preserved for later.

### Execution Plan
This is the work plan.

Usually this is generated from an approved CR. It breaks the change into executable work items.

### Evidence Pack
This is the results pack.

It should show that the approved checks were satisfied. Use before/after examples, tests, validations, migration outputs, benchmarks, or other concrete proof.

## Working style for agents

When you are preparing a CR or updating CCP objects:

- write plainly
- be concrete
- prefer examples over abstraction
- say what changes and what stays true
- make "done" testable
- avoid implementation detail unless it affects the shape of the change
- keep rationale short and high-signal
- link related objects cleanly

## Working style for implementation

Once a CR is approved:

- use the approved change brief as the source of truth
- generate or update the Execution Plan
- implement against the approved change
- produce an Evidence Pack that clearly maps back to the CR checks
- if implementation reveals that the approved change brief is wrong or incomplete, do **not** quietly improvise — update or amend the CR

## The simplest mental model

Remember:

- **Git tracks how the code changed**
- **CCP tracks what change we meant to make and how we checked it**

If you keep that in mind, you will usually make the right call.

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
