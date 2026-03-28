# Change Contract Protocol (CCP)
## Public Consultation Draft v0.1

**Status:** For consultation  
**Intended role:** Open protocol, workflow, and object-format for human-governed, agent-executed software change  
**Reference implementation:** Foundry  
**Working principle:** Humans review intent, constraints, and evidence. Agents execute implementation.

---

## 1. Why CCP exists

Traditional pull requests collapse several distinct jobs into one artifact:

- deciding whether a change should happen
- deciding what the intended outcome is
- reviewing implementation mechanics
- deciding whether it is safe to ship

That worked tolerably when humans both authored and reviewed code. It degrades when implementation is largely agent-produced and agent-reviewed. In that world, PR diffs become a poor human collaboration primitive because they are downstream, noisy, and implementation-biased.

CCP exists to move human review to the level where humans add the most value:

- **admission:** should this change enter the stack at all?
- **change contract:** what must be true when it is done?
- **design intent:** what shape of solution is acceptable?
- **risk posture:** what needs extra scrutiny or rollout control?
- **evidence review:** did the delivered outcome satisfy the approved contract?

CCP is therefore a protocol for **human-governed, agent-executed change management**.

---

## 2. What CCP is and is not

### CCP is
- an **open object model** for change requests, decision records, execution plans, and evidence packs
- a **workflow semantic model** describing state transitions and review responsibilities
- a **storage- and transport-neutral protocol** that can be implemented locally, self-hosted, or in a hosted product
- a **local-first collaboration pattern** that works with git-like source histories and distributed execution workers

### CCP is not
- a replacement for Git
- a source-code hosting platform
- a specific queueing engine, scheduler, or cloud service
- a mandatory UI
- a mandatory central database

Foundry is expected to implement CCP, but CCP must remain usable without Foundry.

---

## 3. Design goals

1. **Human review should happen above implementation diffs.**
2. **Local-first operation should be possible with no mandatory SaaS dependency.**
3. **The protocol should compose with Git repositories, Dolt/Beads task systems, and heterogeneous worker runtimes.**
4. **The durable record should preserve the “why”, not just the “what changed”.**
5. **Execution should be distributable across local agents, hosted agents, and mixed environments.**
6. **The protocol should support both small bug fixes and major architectural changes.**
7. **Implementations should be able to add features without fragmenting the core object model.**

---

## 4. Non-goals

- Standardizing source control operations
- Standardizing model/provider APIs for coding agents
- Standardizing every possible evidence artifact format
- Standardizing a UI or permissions model beyond minimum interoperability needs
- Requiring branches or prohibiting merge-to-main workflows

---

## 5. Core concepts

### 5.1 Change Request
The primary human-reviewed object. A Change Request describes the problem, the intended end state, constraints, risks, and the evidence needed to accept the work.

### 5.2 Decision Record
A durable record of an architecturally or operationally significant decision, including context, alternatives, decision, and consequences.

### 5.3 Execution Plan
A machine-oriented decomposition of an approved Change Request into epics, tasks, dependencies, validation steps, and rollout steps. Usually agent-generated.

### 5.4 Evidence Pack
A structured artifact containing the proof that a completed change satisfied the approved contract: tests, before/after outputs, validation summaries, migration results, benchmark deltas, and unresolved risks.

### 5.5 Worker
A process, agent, or human-operated runtime that discovers eligible work, claims it, executes it, validates it, and publishes progress and evidence.

### 5.6 Pull-based worker model
Workers discover work from shared state and claim it themselves. A central scheduler is optional, not required. Claiming should use leases or equivalent claim semantics so work can be resumed if a worker dies.

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

---

## 7. Suggested minimum fields

## 7.1 Change Request
```yaml
id: CR-0001
title: Emit required VEDA demand tables for declared demand nodes
status: approved
type: bug
risk: medium
sponsor: emily
owner: david
problem_statement: >
  Demand declarations currently do not lower into the required VEDA tables.
desired_end_state: >
  Valid demand declarations lower consistently and produce documented mappings.
acceptance_criteria:
  - Representative demand declarations lower correctly
  - Required tables are emitted
  - Invalid declarations fail clearly
non_goals:
  - Full demand model redesign
constraints:
  - No silent coercion
  - Preserve current schema where possible
required_evidence:
  - before_after_snapshots
  - regression_tests
  - invalid_example_error
linked_decision_records:
  - DR-0007
linked_execution_plans:
  - EP-0012
```

## 7.2 Decision Record
```yaml
id: DR-0007
title: Demand lowering should fail explicitly on ambiguous mappings
status: accepted
context: >
  The team considered silent default mappings but rejected them.
decision: >
  Ambiguous mappings must raise an explicit diagnostic.
alternatives_considered:
  - silent default mapping
  - warning-only fallback
consequences:
  - clearer user experience
  - slightly more up-front authoring friction
supersedes: null
```

## 7.3 Execution Plan
```yaml
id: EP-0012
change_request: CR-0001
status: executing
tasks:
  - id: BEAD-481
    title: Add lowering rule for demand declarations
  - id: BEAD-482
    title: Add regression fixtures
  - id: BEAD-483
    title: Add invalid-mapping diagnostics
dependencies:
  - BEAD-482 depends_on BEAD-481
validation_plan:
  - snapshot tests
  - compiler diagnostics checks
rollout_plan:
  - merge directly to main after machine validation
```

## 7.4 Evidence Pack
```yaml
id: EV-0009
change_request: CR-0001
status: submitted
acceptance_checklist:
  - criterion: Representative demand declarations lower correctly
    result: pass
  - criterion: Invalid declarations fail clearly
    result: pass
artifacts:
  - path: evidence/snapshots/before-after.md
  - path: evidence/tests/regression-summary.json
  - path: evidence/examples/invalid-case.txt
unresolved_risks: []
```

---

## 8. Workflow semantics

The recommended CCP lifecycle is:

**draft → discussing → approved → planned → executing → verified → closed**

### 8.1 Draft
Problem is being framed. Discussion may still be informal.

### 8.2 Discussing
The Change Request is now explicit and open for human review. Decision Records may be drafted here.

### 8.3 Approved
Human reviewers have approved the admission, contract, and risk posture. The change is authorized to enter planning.

### 8.4 Planned
Execution Plan exists. Work can be decomposed into task-system items such as Beads epics/issues.

### 8.5 Executing
Workers are implementing and validating. Merge-to-main may occur here, depending on policy.

### 8.6 Verified
Evidence Pack has been submitted and machine validation has passed.

### 8.7 Closed
The change is considered complete under policy.

---

## 9. Failure and loop-back semantics

If an Evidence Pack is reviewed and found deficient, CCP distinguishes two cases:

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
- append-oriented status/event records

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
- custom evidence artifact types
- analytics
- dashboards
- hosted orchestration

Implementations should not:
- redefine Change Request semantics
- make hosted infrastructure mandatory for basic interoperability
- make exported CCP objects unusable outside their product

---

## 18. Proposed repo layout for the control plane

```text
ccp-control-plane/
  README.md
  protocol/
    version.json
    profiles.md
  policies/
    review-policy.yaml
    risk-policy.yaml
  change-requests/
    CR-0001/
      change-request.md
      events.log.yaml
      linked-discussion.md
  decision-records/
    DR-0007.md
  execution-plans/
    EP-0012.yaml
  evidence/
    EV-0009/
      evidence-pack.yaml
      artifacts/
  templates/
    change-request.md
    decision-record.md
    evidence-pack.yaml
  schemas/
    change-request.schema.json
    decision-record.schema.json
    execution-plan.schema.json
    evidence-pack.schema.json
```

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
2. Which review events are mandatory for protocol interoperability?
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
