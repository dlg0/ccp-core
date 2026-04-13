# CCP Profile Notes

This repo publishes the CCP v0.1 portable baseline and dogfoods it with a
repo-local `control/` directory.

## Active baseline

This repo currently operates at the `L1: Local` profile:

- the control plane is file-backed and git-backed
- validation runs locally from the repo
- no hosted control-plane service is required

## Compatibility notes

`T1: Team` and `H1: Hosted` remain valid downstream deployment profiles, but
they are not required to read, validate, or exchange the CCP core objects in
this repo.
