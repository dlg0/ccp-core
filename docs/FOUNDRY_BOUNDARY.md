# CCP / Foundry Separation Note

## Recommendation

Yes — keep them separate.

Not just because the writing is cleaner, but because they are genuinely different things with different jobs.

## The clean split

### CCP
CCP is the **protocol/specification layer**.

It defines:
- the object model
- the workflow semantics
- the minimum required fields
- the state transitions
- portability and local-first expectations
- conformance expectations

Question CCP answers:
> “What is the interoperable way to represent and run this style of human-reviewed, agent-executed change workflow?”

### Foundry
Foundry is the **product/reference implementation layer**.

It defines:
- UX
- CLI
- worker runtime behavior
- indexing/search
- integrations
- hosting and commercial packaging
- analytics and admin features
- implementation defaults

Question Foundry answers:
> “What is the best concrete tool for using CCP in practice?”

## Why one document is the wrong shape

If you put them in one PRD, one of two bad things happens:

1. **The protocol gets contaminated by product choices.**  
   You accidentally standardize “whatever Foundry happened to do first”.

2. **The product gets blurred into theory.**  
   The Foundry doc stops being a real buildable product spec and turns into a philosophy paper.

That is why the right structure is:

- **CCP Consultation Draft / Spec**
- **Foundry Product PRD**
- optional **Boundary Note** like this one

## The dependency direction

The direction should be:

**CCP first in principle, Foundry first in implementation speed.**

Meaning:
- Foundry may move quickly and influence CCP through dogfooding
- but Foundry should not secretly become the only way CCP makes sense

## Litmus tests

If the answer to any of these is “no”, the split is being violated.

1. Can a team use CCP objects without Foundry?
2. Can a team read a Change Request outside Foundry and still understand it?
3. Can Foundry export its control-plane data in a CCP-compatible form?
4. Could someone else build another CCP implementation?
5. Does the Foundry PRD contain features that are clearly product-only, not protocol-required?

## Practical implication

For this project:

- publish **CCP** as the public consultation spec
- publish **Foundry** as the implementation/product PRD
- use the project itself as the first open CCP-governed Foundry dogfood project
