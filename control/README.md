# Control plane for this repo

This repo dogfoods CCP for its own evolution.

Current v0.1 chain:
- `CR-0001` governs the CCP Core v0.1 portable baseline
- `DR-0001` through `DR-0005` record the supporting v0.1 decisions
- `EP-0001` tracks the implementation work for that baseline
- `EV-0001` records the verification evidence for the same change

Use these directories:
- `change-requests/`
- `decision-records/`
- `execution-plans/`
- `evidence-packs/`

Repo-local control-plane notes live alongside the dogfood chain:
- `protocol/version.json` pins the CCP version metadata and points to repo-local notes
- `profiles.md` records the active conformance profile notes for this repo
- `policy/` holds the minimal review and evidence policy placeholders for local use

The goal is not process theater. Keep records concise, structured, and linked.
