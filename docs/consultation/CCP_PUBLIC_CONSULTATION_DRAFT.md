# Change Contract Protocol (CCP)
## Public Consultation Draft v0.1

**Status:** For consultation  
**One-sentence summary:** CCP is a standard way to describe a change, turn it into work, and record the result.

---

## 1. What CCP is

CCP is a standard way to describe a change **before** agents implement it, and to record the result **afterward**.

Git tells you **how the code changed**.

CCP tells you **what change was wanted, what had to stay true, and how the result was checked**.

That is the whole idea.

CCP is for projects where humans are no longer spending most of their time reviewing code diffs. Instead, humans review the **change itself** at the right level:

- what should change
- why it should change
- what must not break
- what "done" looks like
- how we will check the result

CCP gives that process a shared format and workflow so humans, agents, and tools can all work from the same description.

---

## 2. The main object: the Change Request

The main object in CCP is a **Change Request (CR)**.

A Change Request is the approved description of a change.

In plain English, a CR says:

1. What are we changing?
2. Why are we changing it?
3. What must not break?
4. What does done look like?
5. How will we check?

That is the review surface.

A pull request is mainly about a **patch**.

A Change Request is about the **change we actually want**.

---

## 3. A plain-language view of the CCP objects

CCP uses four core objects.

### 3.1 Change Request
The approved change brief.

This is where the team agrees on:
- what change is wanted
- what must stay true
- what success looks like
- what checks or proof will be required

### 3.2 Decision Record
The "why note".

Only needed when the reasoning matters enough to preserve. This records why a direction was chosen, what alternatives were considered, and what tradeoffs were accepted.

### 3.3 Execution Plan
The work plan.

Usually agent-generated. This turns an approved Change Request into executable work items, dependencies, validation steps, and likely affected areas.

### 3.4 Evidence Pack
The results pack.

Usually agent-generated after implementation. This contains the proof that the change met the agreed checks: tests, before/after examples, migration results, benchmarks, compatibility checks, and any remaining risks.

---

## 4. The simple mental model

Use this mental model when reading the rest of the spec:

- **Git** tracks source history
- **CCP** tracks change history

More precisely:

- Git answers: **what changed in the code?**
- CCP answers: **what change was intended, what had to stay true, and how was it checked?**

---

## 5. What CCP does and does not standardize

CCP **does** standardize:
- the shape of a Change Request
- the shape of related decision, planning, and results objects
- how those objects link together
- a shared status model
- basic project layout conventions
- validation rules and conformance expectations

CCP does **not** try to standardize:
- how your codebase is structured
- how your task system works internally
- which agent runtime you use
- which git host you use
- which UI or product you use to interact with CCP

CCP is meant to be portable and local-first. A project should be able to use CCP with plain files in git, with or without a larger product wrapped around it.

### A note on language

Some of the formal concepts underneath CCP can be described in heavier words such as "constraints", "invariants", "governance", or "contract".

Those concepts are real, but they are not the best day-to-day language.

This spec will prefer plain engineering language wherever possible:

- **what changes**
- **what must not break**
- **what done looks like**
- **how we check**
- **why this is the right change**

If you keep those five ideas in your head, the rest of CCP should feel straightforward.

---

## 6. Normative object set

CCP defines four core objects and two optional coordination objects.

### Required objects
1. **Change Request**
2. **Decision Record**
3. **Execution Plan**
4. **Evidence Pack**

### Optional coordination objects
5. **Task Claim / Lease**
6. **Review / Approval Event**

Implementations may enrich these objects but should not redefine their core semantics.

For the frozen v0.1 contract, these coordination objects are optional extension material. CCP does not require a portable event-log format or standalone review-event files for core-object interoperability.

Human review and approval become protocol-significant when they are reflected in the lifecycle state of the governed core object. Any standalone review or claim records remain supporting history.

---

## 7. v0.1 core field matrix

For v0.1, the field matrix below is normative for the four required CCP objects.

- **Required** means the field must be present in serialized form.
- **Nullable** means the literal `null` is allowed. If a field is not nullable and has no value, implementations should omit it rather than serialize `null`.
- **Primary author** describes who usually introduces or maintains the field: `human`, `machine`, or `either`.
- Change Requests and Decision Records are primarily human-authored objects. Execution Plans are primarily machine-authored planning objects. Evidence Packs are primarily machine-authored closeout objects that humans review.

### 7.1 Change Request

| Field | Required | Nullable | Primary author | Semantics |
| --- | --- | --- | --- | --- |
| `id` | yes | no | either | Stable object identifier with `CR-` prefix. |
| `kind` | yes | no | either | Literal discriminator `change_request`. |
| `title` | yes | no | human | Short human-readable summary of the requested change. |
| `status` | yes | no | either | Current lifecycle state of the Change Request. |
| `type` | yes | no | human | High-level change category such as bug, feature, or migration. |
| `risk` | yes | no | human | Review and rollout risk posture for the change. |
| `sponsor` | no | no | human | Person or role sponsoring the change. Omit when no explicit sponsor is needed. |
| `owner` | no | no | either | Person, team, or system accountable for driving the Change Request forward. Omit when not assigned yet. |
| `problem_statement` | yes | no | human | Why the change is needed. |
| `desired_end_state` | yes | no | human | Outcome that must be true when the change is complete. |
| `acceptance_criteria` | yes | no | human | Non-empty list of conditions required to accept the change. |
| `non_goals` | no | no | human | Explicit out-of-scope items. Omit when no non-goals need to be stated. |
| `constraints` | yes | no | human | Non-empty list of implementation guardrails. |
| `required_evidence` | yes | no | human | Non-empty list of evidence categories required before closeout. |
| `linked_decision_records` | no | no | either | Decision Records that justify or constrain the change. Omit until such records exist. |
| `linked_execution_plans` | no | no | either | Execution Plans created to implement the change. Omit until planning begins. |
| `linked_evidence_packs` | no | no | either | Evidence Packs submitted against the change. Omit until evidence exists. |

### 7.2 Decision Record

| Field | Required | Nullable | Primary author | Semantics |
| --- | --- | --- | --- | --- |
| `id` | yes | no | either | Stable object identifier with `DR-` prefix. |
| `kind` | yes | no | either | Literal discriminator `decision_record`. |
| `title` | yes | no | human | Short human-readable summary of the decision. |
| `status` | yes | no | either | Current lifecycle state of the Decision Record. |
| `context` | yes | no | human | Background and forces that made the decision necessary. |
| `decision` | yes | no | human | Chosen direction or rule. |
| `alternatives_considered` | yes | no | human | Non-empty list of materially considered alternatives. |
| `consequences` | yes | no | human | Non-empty list of consequences introduced by the decision. |
| `supersedes` | no | no | human | Identifier of the earlier Decision Record replaced by this one. Omit when the record stands alone. |

### 7.3 Execution Plan

| Field | Required | Nullable | Primary author | Semantics |
| --- | --- | --- | --- | --- |
| `id` | yes | no | either | Stable object identifier with `EP-` prefix. |
| `kind` | yes | no | either | Literal discriminator `execution_plan`. |
| `change_request` | yes | no | either | Governing Change Request identifier for this plan. |
| `status` | yes | no | either | Current lifecycle state of the Execution Plan. |
| `tasks` | yes | no | machine | Non-empty ordered list of planned work items. |
| `tasks[].id` | yes | no | either | Stable task identifier within the plan or linked execution system. |
| `tasks[].title` | yes | no | machine | Human-readable description of the task's intended work. |
| `dependencies` | no | no | machine | Dependency edges between task identifiers listed in `tasks`. Omit when the plan has no explicit task dependencies. |
| `validation_plan` | yes | no | machine | Non-empty list of validations required before the change can move toward verification. |
| `rollout_plan` | no | no | machine | Ordered release, activation, or migration steps that go beyond basic merge and validation. Omit when no extra rollout steps are needed. |

### 7.4 Evidence Pack

| Field | Required | Nullable | Primary author | Semantics |
| --- | --- | --- | --- | --- |
| `id` | yes | no | either | Stable object identifier with `EV-` prefix. |
| `kind` | yes | no | either | Literal discriminator `evidence_pack`. |
| `change_request` | yes | no | either | Change Request identifier satisfied or evaluated by this evidence. |
| `status` | yes | no | either | Current lifecycle state of the Evidence Pack. |
| `acceptance_checklist` | yes | no | machine | Non-empty list evaluating the approved acceptance criteria. |
| `acceptance_checklist[].criterion` | yes | no | either | Acceptance criterion being evaluated, usually copied or derived from the Change Request. |
| `acceptance_checklist[].result` | yes | no | machine | Evaluation result for the criterion. |
| `artifacts` | yes | no | machine | Non-empty list of concrete evidence artifacts. |
| `artifacts[].path` | yes | no | machine | Stable path or locator for an evidence artifact. |
| `unresolved_risks` | yes | no | machine | Risks still open at verification time. Use an empty list when none remain. |

---

## 8. Workflow semantics

CCP uses separate state machines for each required object. The Change Request carries the end-to-end governance lifecycle, while Decision Records, Execution Plans, and Evidence Packs have narrower supporting lifecycles.

### 8.1 Change Request lifecycle

The recommended Change Request lifecycle is:

**draft → discussing → approved → planned → executing → verified → closed**

Allowed transitions:

- `draft -> discussing`
- `discussing -> approved`
- `approved -> planned`
- `planned -> executing`
- `executing -> verified`
- `verified -> closed`
- `verified -> executing`
- `verified -> discussing`

Status intent:

- `draft`: problem framing is still incomplete or informal.
- `discussing`: the Change Request is explicit and open for human review.
- `approved`: reviewers have approved the admission, contract, and risk posture.
- `planned`: at least one Execution Plan exists and work can be decomposed into executable tasks.
- `executing`: workers are implementing and validating the approved change.
- `verified`: evidence has been submitted and machine validation has passed.
- `closed`: the change is complete under policy.

### 8.2 Decision Record lifecycle

Decision Records use a smaller lifecycle because they record design choices rather than end-to-end delivery.

States: `draft`, `accepted`, `superseded`

Allowed transitions:

- `draft -> accepted`
- `accepted -> superseded`

### 8.3 Execution Plan lifecycle

Execution Plans track planning and delivery progress for an approved Change Request.

States: `draft`, `planned`, `executing`, `blocked`, `done`

Allowed transitions:

- `draft -> planned`
- `planned -> executing`
- `executing -> blocked`
- `blocked -> executing`
- `executing -> done`
- `done -> executing`

`done -> executing` is allowed when the approved contract has not changed but more implementation work is required after validation or evidence review.

### 8.4 Evidence Pack lifecycle

Evidence Packs model evidence assembly and review, not the full change lifecycle.

States: `draft`, `submitted`, `accepted`, `rejected`

Allowed transitions:

- `draft -> submitted`
- `submitted -> accepted`
- `submitted -> rejected`
- `rejected -> draft`

---

## 9. Failure and loop-back semantics

If an Evidence Pack is reviewed and found deficient, the Change Request loop-back depends on which kind of problem was found. The Evidence Pack itself may move from `submitted` to `rejected`, but the governing Change Request distinguishes two cases:

### Case A: implementation or evidence problem
Examples:
- tests missing
- regression evidence incomplete
- output does not satisfy an accepted criterion
- migration evidence missing

**Loop-back:** `verified -> executing`

This means the approved contract stands, but execution or evidence is incomplete.

### Case B: contract or intent problem
Examples:
- approved acceptance criteria were ambiguous
- reviewers discover that the requested end state was wrong
- decision rationale is incomplete for the actual blast radius

**Loop-back:** `verified -> discussing`  
or  
**follow-on amendment:** a new Change Request linked to the original

This means the contract itself must be amended, not just the implementation.

---

## 10. Merge timing semantics

CCP does **not** require “evidence accepted before merge”. The recommended default is:

- workers merge to main during **executing**
- merge happens after machine validation and policy checks pass
- final human evidence review governs **closeout**, not basic integration

Reasoning:
- it avoids recreating PR review as a blocking gate
- it keeps main as the integration surface
- it reduces branch drift and stale-context execution

For high-risk changes, implementations should separate:
- **merge**
- **activation**
- **release**
- **migration execution**

This can be done using flags, staged rollout, migration guards, and release controls.

---

## 11. Storage model

CCP is intentionally storage-neutral, but the recommended model is:

### 11.1 Source plane
Git repositories for code and source artifacts

### 11.2 Control plane
A dedicated git-backed repository for:
- Change Requests
- Decision Records
- Evidence manifests
- review policy
- protocol metadata
- optional coordination history when an implementation chooses to persist it

For the frozen v0.1 compatibility baseline, the portable default requires only the four core object directories. Event logs and standalone review histories remain optional extensions.

### 11.3 Execution plane
A live task store such as Dolt/Beads holding:
- executable task decomposition
- claim/lease state
- worker progress
- operational execution metadata

This yields three distinct histories:
1. **source truth**
2. **decision/contract truth**
3. **execution truth**

That separation is intentional.

---

## 12. Transport model

CCP objects may be exchanged through:
- git sync
- filesystem sync
- webhooks
- HTTP APIs
- event buses
- CLI commands

An implementation is conformant if it preserves the object semantics and lifecycle, regardless of transport.

---

## 13. Local-first stance

CCP must work fully locally.

A project should be able to:
- keep source repos locally
- keep the control-plane repo locally
- keep Beads/Dolt locally
- run workers locally
- review Change Requests locally
- sync later to shared remotes if desired

Hosted products are allowed, but not required for protocol participation.

---

## 14. How workers discover work

Workers should not require a master scheduler.

The recommended discovery flow is:

1. sync control-plane repo
2. read approved Change Requests and active Execution Plans
3. read execution-plane task state
4. find eligible unclaimed or expired-lease tasks
5. atomically claim via lease
6. materialize repo/worktree
7. execute and validate
8. publish status/events/evidence
9. renew or release claim

This is the **pull-based worker** pattern.

---

## 15. How agents learn how to author CCP objects

CCP does not mandate one mechanism, but recommends three layers:

### 15.1 Open object format
The schemas and templates are public and git-backed.

### 15.2 Repo-local instructions
Projects may provide `AGENTS.md`, `SKILL.md`, or equivalent instructions describing:
- when a Change Request is required
- how to fill it out
- what local constraints apply
- where evidence should be published

### 15.3 CLI ergonomics
Implementations such as Foundry may provide a CLI:
- `foundry cr new`
- `foundry cr validate`
- `foundry dr new`
- `foundry evidence publish`
- `foundry plan generate`

The protocol must remain usable without that CLI.

---

## 16. Conformance profiles

### Profile L1: Local
- file-backed or git-backed control plane
- local workers
- no hosted dependencies required

### Profile T1: Team
- shared remote repos
- shared task store
- distributed workers
- webhook or polling sync allowed

### Profile H1: Hosted
- managed UI/API allowed
- may add convenience services
- must preserve CCP semantics and exportability

---

## 17. Extension model

Implementations may add:
- richer permissions
- richer review workflows
- coordination histories such as task-claim logs or review events
- custom evidence artifact types
- analytics
- dashboards
- hosted orchestration

Implementations should not:
- redefine Change Request semantics
- treat extension events as a replacement for core object status
- make optional coordination objects mandatory for basic interoperability
- make hosted infrastructure mandatory for basic interoperability
- make exported CCP objects unusable outside their product

---

## 18. v0.1 repo layout and serialization policy

For v0.1, the canonical portable representation is one JSON file per core object under a control-plane root.

- A project may keep the control plane in a standalone repository or in a subdirectory such as `control/` inside a source repository. Both are conformant.
- Unset optional fields are omitted rather than serialized as `null`.
- Markdown, YAML, directory-per-object layouts, and event-log files are possible future extensions, but they are not the v0.1 portable default.

Canonical layout relative to the control-plane root:

```text
<control-plane-root>/
  change-requests/
    CR-0001.json
  decision-records/
    DR-0007.json
  execution-plans/
    EP-0012.json
  evidence-packs/
    EV-0009.json
```

When a control plane is embedded inside a source repository, the same layout appears under the `control/` directory.

---

## 19. Relationship to Foundry

CCP and Foundry should be treated as distinct things.

### CCP
- the open protocol / object model / workflow semantics
- portable
- implementation-neutral
- suitable for public consultation and external adoption

### Foundry
- the product
- the reference implementation
- may provide UI, CLI, hosted services, indexes, worker runtime helpers, and analytics
- should implement CCP faithfully and may add optional extensions

The test is simple:

> A team should be able to use CCP without Foundry.  
> A team should not need to use Foundry in order to understand or exchange CCP objects.

---

## 20. Recommendation on project structure

Yes: maintain **two distinct primary documents**.

### Document A: CCP public consultation spec
Audience:
- external collaborators
- open-source users
- prospective implementers
- protocol reviewers

Purpose:
- define the open protocol
- gather feedback
- establish interoperability expectations

### Document B: Foundry product PRD
Audience:
- product and engineering team
- implementation planners
- commercial stakeholders

Purpose:
- define the Foundry product
- prioritize features
- define MVP/MMP roadmap
- specify UX, integrations, worker services, and product-specific extensions

A third supporting artifact is useful:

### Document C: CCP/Foundry boundary note
Purpose:
- keep the line clean between protocol and product
- prevent product decisions from leaking into the protocol unnecessarily
- document what is normative vs implementation-specific

---

## 21. Dogfooding proposal

This CCP/Foundry design effort should become the first open dogfood project.

Recommended setup:
- publish the CCP consultation draft publicly
- run the project itself using CCP objects
- keep a public control-plane repo
- let contributors open Change Requests against the protocol and repo skeleton
- use Foundry as one implementation path, but keep all core objects portable and visible

This gives the protocol immediate credibility because it is used to govern its own evolution.

---

## 22. Consultation questions

1. Should Change Requests be markdown with front matter, pure YAML/JSON, or dual-format?
2. Which optional review events would be most useful to standardize in a future version?
3. Should Evidence Packs support partial acceptance or only pass/fail closeout?
4. Should task claim/lease semantics be standardized at the protocol layer or left implementation-specific?
5. How strict should conformance be around local-first export/import?
6. What minimum fields are required for a portable Change Request?

---

## 23. Next recommended artifacts

1. publish this consultation draft
2. publish JSON Schemas and templates
3. publish a reference control-plane repo skeleton
4. publish the Foundry product PRD separately
5. run the CCP consultation process as the first open CCP-governed project

---

## 24. Working title note

**Change Contract Protocol (CCP)** is a good working title because it describes the center of gravity: the approved contract around a change.

If later refinement is desired, naming alternatives can be explored, but the protocol should be named independently of Foundry.
