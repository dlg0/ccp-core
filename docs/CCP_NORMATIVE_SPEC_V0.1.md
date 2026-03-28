# Change Contract Protocol (CCP)
## Normative Specification v0.1

**Status:** Normative  
**Protocol version:** v0.1  
**Scope:** Binding object, lifecycle, repository, and interoperability rules for CCP v0.1  
**Working principle:** Humans review intent, constraints, and evidence. Agents execute implementation.

---

## 1. Scope

This document defines the normative CCP v0.1 compatibility baseline.

It specifies:

- the required CCP core objects
- the required fields and semantics for those objects
- the allowed lifecycle transitions for those objects
- the portable on-disk repository contract for v0.1
- the interoperability rules that implementations must preserve

This document does not define product UX, hosted orchestration, proprietary permissions models, or implementation-specific worker behavior beyond the minimum semantics needed for interoperability.

If this document conflicts with the consultation draft, this document governs v0.1 compatibility.

---

## 2. Conformance Language

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT", and "MAY" in this document are to be interpreted as normative requirements.

An implementation is CCP v0.1 compatible only if it preserves the object semantics, lifecycle semantics, and repository contract defined here.

---

## 3. Required Object Set

CCP v0.1 defines four required core objects and two optional coordination objects.

### Required core objects

1. Change Request
2. Decision Record
3. Execution Plan
4. Evidence Pack

### Optional coordination objects

1. Task Claim / Lease
2. Review / Approval Event

CCP v0.1 names these coordination concepts, but it does not define a required field matrix, canonical repository location, or portable serialized form for them.

Implementations MAY add additional objects, but they MUST NOT redefine the core semantics of the four required objects.

Human review and approval become normative for v0.1 only when reflected in the lifecycle state of the relevant core object. Optional coordination artifacts MAY record supporting history, but they do not replace core object status.

---

## 4. Core Object Rules

### 4.1 General rules

- Each serialized core object MUST have a stable identifier in its object-specific namespace.
- Each serialized core object MUST include a `kind` discriminator with the literal value defined for that object type.
- Required fields MUST be present in serialized form.
- Optional fields MUST be omitted when unknown or not applicable unless a field's own semantics require an empty list.
- Implementations MUST preserve the field semantics defined below when transforming, transporting, or exporting objects.

### 4.2 Change Request

| Field | Required | Primary author | Semantics |
| --- | --- | --- | --- |
| `id` | yes | either | Stable object identifier with `CR-` prefix. |
| `kind` | yes | either | Literal discriminator `change_request`. |
| `title` | yes | human | Short human-readable summary of the requested change. |
| `status` | yes | either | Current lifecycle state of the Change Request. |
| `type` | yes | human | High-level change category such as bug, feature, or migration. |
| `risk` | yes | human | Review and rollout risk posture for the change. |
| `sponsor` | no | human | Person or role sponsoring the change. Omit when no explicit sponsor is needed. |
| `owner` | no | either | Person, team, or system accountable for driving the Change Request forward. Omit when not assigned yet. |
| `problem_statement` | yes | human | Why the change is needed. |
| `desired_end_state` | yes | human | Outcome that must be true when the change is complete. |
| `acceptance_criteria` | yes | human | Non-empty list of conditions required to accept the change. |
| `non_goals` | no | human | Explicit out-of-scope items. Omit when no non-goals need to be stated. |
| `constraints` | yes | human | Non-empty list of implementation guardrails. |
| `required_evidence` | yes | human | Non-empty list of evidence categories required before closeout. |
| `linked_decision_records` | no | either | Decision Records that justify or constrain the change. Omit until such records exist. |
| `linked_execution_plans` | no | either | Execution Plans created to implement the change. Omit until planning begins. |
| `linked_evidence_packs` | no | either | Evidence Packs submitted against the change. Omit until evidence exists. |

### 4.3 Decision Record

| Field | Required | Primary author | Semantics |
| --- | --- | --- | --- |
| `id` | yes | either | Stable object identifier with `DR-` prefix. |
| `kind` | yes | either | Literal discriminator `decision_record`. |
| `title` | yes | human | Short human-readable summary of the decision. |
| `status` | yes | either | Current lifecycle state of the Decision Record. |
| `context` | yes | human | Background and forces that made the decision necessary. |
| `decision` | yes | human | Chosen direction or rule. |
| `alternatives_considered` | yes | human | Non-empty list of materially considered alternatives. |
| `consequences` | yes | human | Non-empty list of consequences introduced by the decision. |
| `supersedes` | no | human | Identifier of the earlier Decision Record replaced by this one. Omit when the record stands alone. |

### 4.4 Execution Plan

| Field | Required | Primary author | Semantics |
| --- | --- | --- | --- |
| `id` | yes | either | Stable object identifier with `EP-` prefix. |
| `kind` | yes | either | Literal discriminator `execution_plan`. |
| `change_request` | yes | either | Governing Change Request identifier for this plan. |
| `status` | yes | either | Current lifecycle state of the Execution Plan. |
| `tasks` | yes | machine | Non-empty ordered list of planned work items. |
| `tasks[].id` | yes | either | Stable task identifier within the plan or linked execution system. |
| `tasks[].title` | yes | machine | Human-readable description of the task's intended work. |
| `dependencies` | no | machine | Dependency edges between task identifiers listed in `tasks`. Omit when the plan has no explicit task dependencies. |
| `validation_plan` | yes | machine | Non-empty list of validations required before the change can move toward verification. |
| `rollout_plan` | no | machine | Ordered release, activation, or migration steps that go beyond basic merge and validation. Omit when no extra rollout steps are needed. |

### 4.5 Evidence Pack

| Field | Required | Primary author | Semantics |
| --- | --- | --- | --- |
| `id` | yes | either | Stable object identifier with `EV-` prefix. |
| `kind` | yes | either | Literal discriminator `evidence_pack`. |
| `change_request` | yes | either | Change Request identifier satisfied or evaluated by this evidence. |
| `status` | yes | either | Current lifecycle state of the Evidence Pack. |
| `acceptance_checklist` | yes | machine | Non-empty list evaluating the approved acceptance criteria. |
| `acceptance_checklist[].criterion` | yes | either | Acceptance criterion being evaluated, usually copied or derived from the Change Request. |
| `acceptance_checklist[].result` | yes | machine | Evaluation result for the criterion. |
| `artifacts` | yes | machine | Non-empty list of concrete evidence artifacts. |
| `artifacts[].path` | yes | machine | Stable path or locator for an evidence artifact. |
| `unresolved_risks` | yes | machine | Risks still open at verification time. Use an empty list when none remain. |

---

## 5. Lifecycle Semantics

CCP v0.1 uses separate state machines for each required core object. Implementations MUST enforce only the transitions allowed for the relevant object type.

### 5.1 Change Request lifecycle

States:

`draft -> discussing -> approved -> planned -> executing -> verified -> closed`

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

### 5.2 Decision Record lifecycle

States: `draft`, `accepted`, `superseded`

Allowed transitions:

- `draft -> accepted`
- `accepted -> superseded`

### 5.3 Execution Plan lifecycle

States: `draft`, `planned`, `executing`, `blocked`, `done`

Allowed transitions:

- `draft -> planned`
- `planned -> executing`
- `executing -> blocked`
- `blocked -> executing`
- `executing -> done`
- `done -> executing`

`done -> executing` is allowed when the approved contract has not changed but more implementation work is required after validation or evidence review.

### 5.4 Evidence Pack lifecycle

States: `draft`, `submitted`, `accepted`, `rejected`

Allowed transitions:

- `draft -> submitted`
- `submitted -> accepted`
- `submitted -> rejected`
- `rejected -> draft`

---

## 6. Failure and Loop-Back Semantics

If an Evidence Pack is reviewed and found deficient, the governing Change Request MUST loop back based on the type of problem found.

### 6.1 Implementation or evidence problem

Examples include missing tests, incomplete regression evidence, unmet accepted criteria, or missing migration evidence.

Required loop-back:

- `verified -> executing`

This means the approved contract still stands, but execution or evidence is incomplete.

### 6.2 Contract or intent problem

Examples include ambiguous acceptance criteria, a wrong approved end state, or incomplete decision rationale for the actual blast radius.

Required loop-back or amendment path:

- `verified -> discussing`
- or a follow-on Change Request linked to the original

This means the contract itself must be amended, not just the implementation.

---

## 7. Merge Timing Semantics

CCP v0.1 does not require evidence acceptance before merge.

The recommended default is:

- workers merge to main during `executing`
- merge happens after machine validation and policy checks pass
- final human evidence review governs closeout, not basic integration

Implementations MAY impose stricter policy, but they MUST NOT redefine the object lifecycle semantics in order to do so.

---

## 8. Repository Contract

CCP v0.1 is storage-neutral, but it defines one portable repository contract for interoperable serialized core objects.

### 8.1 Portable serialized form

- The canonical portable representation for v0.1 is one JSON file per core object.
- The control plane MAY live in a standalone repository or in a repo-local `control/` subdirectory.
- Unset optional fields MUST be omitted rather than serialized as `null`.
- Markdown, YAML, directory-per-object layouts, and event-log files are not part of the v0.1 portable default.

### 8.2 Canonical layout

Relative to the control-plane root, the canonical layout is:

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

When a control plane is embedded inside a source repository, the same layout appears under `control/`.

---

## 9. Interoperability Rules

### 9.1 Storage and transport neutrality

Core object semantics are independent of storage and transport.

Implementations MAY exchange CCP objects through git sync, filesystem sync, webhooks, HTTP APIs, event buses, or CLI commands, but they MUST preserve:

- object identity
- required field semantics
- lifecycle semantics
- repository exportability in the portable v0.1 form

### 9.2 Local-first baseline

Hosted products are allowed, but they are optional.

An implementation claiming CCP v0.1 compatibility MUST allow teams to read, validate, and exchange CCP core objects without requiring a hosted control plane operated by a specific vendor.

### 9.3 Extension rules

Implementations MAY add richer permissions, review workflows, coordination histories such as task-claim logs or review events, evidence artifact types, analytics, dashboards, or hosted orchestration.

Implementations MUST NOT:

- redefine the core semantics of Change Requests, Decision Records, Execution Plans, or Evidence Packs
- treat optional coordination artifacts as a substitute for required core object lifecycle state
- make optional coordination objects mandatory for basic read, validate, or exchange of CCP core objects
- require hosted infrastructure for basic CCP object interoperability
- export CCP objects in a form that prevents use outside the implementation

### 9.4 Product boundary

Product behavior such as UX, reviewer assignment models, approval policy, event-log schema and storage, indexing strategy, worker runtime defaults, integrations, analytics, and commercial packaging is outside the CCP v0.1 normative surface unless explicitly serialized into CCP objects without changing their defined meaning.

---

## 10. Non-Normative Consultation Material

The consultation draft remains useful background and rationale, but the following consultation-draft sections are non-normative for CCP v0.1 compatibility:

- sections 1 through 5, covering motivation, framing, design goals, and conceptual explanation
- sections 20 through 24, covering project-structure recommendations, dogfooding, consultation questions, next artifacts, and naming notes

For v0.1 compatibility, the normative baseline is the material captured in this document: the object set, core field rules, lifecycle semantics, repository contract, and interoperability rules.
