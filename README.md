# ccp-core

CCP is a standard way to describe a change, turn it into work, and record the result.

This repo contains the open core of CCP:
- the spec
- schemas
- examples
- a thin CLI
- scaffolding for CCP-governed projects

## The simple idea

Software teams have traditionally used pull requests as the main review object.

That made sense when humans were doing most of the implementation.

In agent-heavy projects, that starts to break down.

A PR is mostly about a patch:
- here is the code I changed
- please merge it

CCP is about the change itself:
- here is what we want to change
- here is what must not break
- here is what "done" looks like
- here is how we will check

So the shift is:

- **PR** = review the patch
- **CR** = review the change

## The main object: Change Request

The core CCP object is the **Change Request (CR)**.

A CR is the approved description of a change.

It answers five questions:

1. What are we changing?
2. Why are we changing it?
3. What must not break?
4. What does done look like?
5. How will we check?

That is the object humans should review before agents go implement.

## The four core objects

### Change Request
The approved change brief.

### Decision Record
The "why note" for important decisions.

### Execution Plan
The work plan derived from the approved change.

### Evidence Pack
The results pack showing the change actually met the agreed checks.

## The mental model

The easiest way to understand CCP is:

- **Git tracks source history**
- **CCP tracks change history**

Git tells you how the code changed.

CCP tells you what change was intended, what had to stay true, and how the result was checked.

## What this repo is for

This repo is for defining CCP itself as an open, portable, local-first standard.

CCP should work:
- as plain files in git
- on a local machine
- without a hosted control plane
- with different products or tools built on top of it

This repo is **not** the rich end-user product layer.

That comes later.

## Relationship to Foundry

Foundry is intended to be a richer implementation built on top of CCP.

A useful mental model is:

- **CCP** is like Git or OCI
- **Foundry** is like GitHub or Docker Desktop

CCP defines the portable format and workflow.

Foundry can implement that format and add UX, indexing, approvals, integrations, orchestration, and worker support.

## Repo contents

Typical contents in this repo include:
- spec drafts
- terminology and semantics
- object schemas
- examples and fixtures
- conformance material
- CLI scaffolding
- project templates

## Language used in this repo

We try to explain CCP in plain engineering language.

Instead of leaning too hard on abstract words, we prefer:

- what changes
- what stays true
- what done looks like
- how we check
- why this is the right change

Those five ideas are the practical core of CCP.

## Status

Early and for consultation.

The goal of this repo is to make the idea concrete enough to test, critique, and improve in the open.

## Getting started

At a high level, CCP use should feel like this:

```bash
ccp init
ccp new change-request
ccp validate
```

Exact CLI behavior will evolve, but the principle stays the same: describe the change first, then turn it into work, then record the result.

## One-sentence summary

**CCP is the standard way to write down a change before agents implement it, and to record the result afterward.**
