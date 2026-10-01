# Wayfarer Design Workflow

## Roles
- **ChatGPT: Author.** Creates and revises design specifications and resolves audit findings.
- **Claude: Auditor.** Reviews authored specifications for contradictions, ambiguity, missing positive anatomical identity, cross-race conflicts, and violations of project rules.
- **Tyler: Project owner.** Final human authority over project direction.

## Canonical authority
1. Approved Design Specification
2. Open Decision Register
3. Prototype Implementation

Prototype code or earlier shorthand never silently overrides an approved specification.

## Workflow
1. ChatGPT authors or revises a spec in `specs/`.
2. Claude audits the current spec and records findings in `audits/`.
3. Claude does not silently rewrite approved design to resolve a finding.
4. ChatGPT reads the audit, resolves accepted findings in the specification, and records important decisions in `decisions/`.
5. A race is marked FIRST-PASS COMPLETE only after its final audit has no blocking contradiction.

## Ownership (Tyler's decision, September 30, 2026)
- ChatGPT maintains the universal rules in `decisions/PROJECT_RULES.md`.
- Claude keeps the per-part decision log in `register/decision-register.md`, recording AGREED / PRELIMINARY / OPEN entries for each approved part and patch.
- New audits use per-part files in `audits/`; per-race `audits/NN-<race>.audit.md` files are history.

## Current phase
DESIGN ONLY. Do not modify Unreal Engine 5 or begin technical implementation unless Tyler explicitly changes the project phase.

## Shared-workspace rule
Repository files are the persistent shared record. Chat transcripts may contain working discussion, but approved repository specifications take precedence over temporary chat context once reconciled.
