# Wayfarer Design

Design specifications for **Wayfarer**, a UE5 RPG. This repo holds design documents only. Nothing here is implemented in the UE5 project, and nothing here authorizes changes to it.

## Roles

| Who | Role | Writes to |
| --- | --- | --- |
| **ChatGPT** | Author. Writes the race specs, parts and clarification patches, following Tyler's rules, and owns the universal project rules. | `specs/`, `races/`, `reviews/`, `rules/`, `decisions/` |
| **Claude** | Auditor. Records approved material, checks it for contradictions, ambiguities, convergence between races and coding risks, and reports them. Claude doesn't silently fix the spec. | `audits/`, `register/` |
| **Tyler** | Decides. Approves, rejects or asks for patches. Nothing becomes AGREED without Tyler. | Anything |

## Authority order

1. **Approved Design Specification** (`races/`, `reviews/`, `rules/`)
2. **Open Decision Register** (`register/decision-register.md`)
3. **Prototype implementation**, including earlier shorthand (the UE5 project and older plan wording)

A higher level always wins. Existing implementation never overrides an approved spec and never resolves an OPEN item just by existing. Audit files never override anything; they're notes to check.

## Layout

| Path | Contents |
| --- | --- |
| `races/NN-<race>.md` | One spec per race, numbered in design order |
| `audits/NN-<race>.audit.md` | Claude's open notes for that race (notes to check, not changes) |
| `reviews/` | Cross-race reviews (Elf Comparative Review so far) |
| `audits/<review>.audit.md` | Open notes for each review |
| `rules/character-creation-brief.md` | The universal brief: principles, layers, the 13 races, universal amendment v0.1 |
| `decisions/PROJECT_RULES.md` | Universal project rules (ChatGPT owns) |
| `register/decision-register.md` | Per-part decision log: every decision tagged AGREED, PRELIMINARY or OPEN (Claude keeps) |
| `plan/terrain-and-race-models.md` | Terrain plan, candidate technical approaches, known gaps, queued playtest feedback |

## Race status

| # | Race | Status |
| --- | --- | --- |
| 1 | Marchfolk | First pass complete |
| 2 | Skarn | First pass complete |
| 3 | Sagekin | First pass complete |
| 4 | Fenn | First pass complete |
| 5 | Aelari | First pass complete |
| 6 | Vael | First pass complete |
| 7 | Halvren | First pass complete (v1.1 on hold) |
| 8 | Durrim | First pass complete |
| 9 | Grask | First pass complete |
| 10 | Gorrund | First pass complete (prototype verification deferred) |
| 11 | Pipkin | Parts 1–2 received, v1.0 in progress |
| 12 | Cogling | Not started |
| 13 | Saurin | Not started |

## Ownership (Tyler's decision, September 30, 2026)

- **Universal rules:** ChatGPT authors and maintains `decisions/PROJECT_RULES.md`.
- **Per-part decision log:** Claude records each approved part and patch in `register/decision-register.md`.
- **Audits:** new audits go in per-part files (for example `audits/pipkin-part-2.md`); the per-race `audits/NN-<race>.audit.md` files are kept as history.

## Workflow

1. ChatGPT writes a part or patch and commits it to the race file (or opens a pull request).
2. Claude audits it: adds the Decision Register entries and writes its findings to a per-part audit file in `audits/`.
3. Tyler reads the audit and decides. A patch that resolves a note moves it out of the audit file.

Commit messages say which part or patch they carry, for example `Pipkin Part 3: craniofacial anatomy, ears, hair`.

## History

Migrated on September 30, 2026 from the Claude Docs plan doc. Each spec's former "Notes to check" section now lives in its audit file.
