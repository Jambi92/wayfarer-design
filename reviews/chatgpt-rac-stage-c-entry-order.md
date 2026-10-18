# RAC Stage C — entry order (Grask E3 + Gorrund combined validation) — HOLD FOR D1–D3

**Status:** PREPARED BY CLAUDE under `reviews/chatgpt-rac-stage-c-release-after-05ax4-HOLD.md` §5 ("if incomplete: prepare precise Stage C entry order"). It is **HOLD** until Tyler / ChatGPT record decisions D1–D3 (§3). After that it can be executed as written.
**Date:** 2026-10-18.
**Basis:** 05D Stage C; 05E §9; 05F §6; 05H / 05J Stage C purpose and status lines. Resolution: `reviews/claude-rac-stage-c-entry-resolution.md`.

## 1. Frozen sources (verify hashes at entry; stop on mismatch)

**Gorrund:** `GO-05AW4_nails_final.blend`, PC `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Neutral-C\05AW4\`.
- blend sha `5a4e45d40158e7dc92f6f8ba13d67ada2403e3e3dcda9048382323ee43a22d5e`
- glb sha `e6b325039993b48de1daf1b82da7054c9f466131daf41c2dcc14a0709adb6fc8`
- Stature 204.5225 cm; author-approved reference sculpt (05AX4).

**Grask E3:** the frozen `GR.E3` spec in `reviews/rac-rmot05d-evidence/candidates.json` (05D), unchanged since aaa3433.
- Per D3, the body is built or supplied and its mesh hash is recorded in C0.
- **Grask W2 is not rerun.**

**Roster comparators:** the frozen W2-era bodies already used for roster lineups. They are listed and hashed in C0, not rebuilt.

## 2. Scope (blocks)

**C0 — Entry (read-only).**
- Verify hashes.
- Build the source manifest.
- Write the Stage C protocol file `specs/RAC_STAGE_C_PROTOCOL.md`. It freezes the validator list and thresholds exactly as they exist (W2C / W2D, UFCA / MPFB / ALPC) and maps each validator to the sculpted Gorrund per D1 / D2.
- **No new thresholds.** Where a validator cannot apply to a sculpted mesh, mark it **N/A with reason**; do not invent a replacement.

**C1 — Variant states** (branch on D1):
- **D1(a):** Reference state only. Narrow / Broad / low / high are recorded as **DEFERRED TO CREATOR**. C1 is empty.
- **D1(b):** A separate derivation block, executed and author-reviewed **before** C2. It derives bounded deformations of the sculpt, each with technical and visual gates. It is a new order; it is not authorised here.
- **D1(c):** Re-fit the W1i procedural Gorrund to the sculpt (fit report: per-station deviation), then generate variants procedurally. The sculpt remains the visual reference.

**C2 — Validator suite (05E §9.2).**
- Run on Grask E3 and Gorrund (states per D1, statures per D2):
  - stature endpoints and representative internal heights;
  - matched heights;
  - Frame extremes, where states exist;
  - composition states, where they exist;
  - protected skeletal relations at stations;
  - clearance / intersection guards;
  - the UFCA / MPFB / ALPC guards that remain authoritative.
- Fix **implementation** regressions only. Do not reintroduce donor-human soft tissue.

**C3 — Full-roster read (05E §9.3, 05F §6).**
- Matched-scale lineup in front / 3-4 / profile / rear and body-only silhouettes.
- Distinctness checks:
  - Grask vs Gorrund;
  - each vs Skarn / Marchfolk at matched height;
  - Saurin coherence.
- No pair may separate only by thin / broad or by scale (05H / 05J).

**C4 — Author package (05E §9.4).**
- Sheets per available state.
- Matched-height comparisons.
- Roster lineup.
- Pass / fail tables.
- Exact specs and parameters.
- Unresolved risks.
- ACCEPT / CONSTRAIN / FAIL per race.

## 3. Decisions required before execution

| # | Decision | Recorded answer |
|---|---|---|
| D1 | Gorrund variant method: (a) reference-only, variants deferred to creator / (b) derive from the sculpt in a separate block / (c) procedural re-fit | ___ |
| D2 | Stature mapping of the 204.5 cm sculpt: (a) shape-only, scaled to GOREF 230.9 (×1.1290) / (b) adopt 204.5 as a new lower bound (canon-scale revision) / (c) native height, scaled only for matched pairs | ___ |
| D3 | Grask E3 body: (a) procedural build from frozen `GR.E3`, hash recorded / (b) sculpted E3 first | ___ |

## 4. Allowed and forbidden edits

**Allowed:**
- read-only measurement and rendering;
- uniform scaling for comparison only (per D2), never saved over a frozen source;
- procedural builds from frozen specs (D1(c) / D3(a));
- writing the protocol file, evidence and reports.

**Forbidden:**
- any sculpt or geometry edit of `GO-05AW4_nails_final` or any frozen roster body;
- Grask W2 rerun;
- new thresholds;
- repairing Gorrund's carried hand / axilla debt;
- D4, UE5, production rigging, creator implementation, class / gameplay and language / story work;
- self-promotion to canon.

## 5. Evidence

`reviews/rac-stagec-evidence/`, containing:
- source manifest with hashes;
- the protocol file;
- per-race validator tables (PASS / FAIL / N/A with reason);
- matched-height sheets;
- roster lineup;
- distinctness table;
- the author package.

Gate report: `reviews/claude-rac-stage-c-gate.md`.

## 6. Technical gates

- Source hashes match.
- Every frozen source is unchanged after the run (re-hash).
- Each validator either runs with existing thresholds or is N/A with a reason.
- No mesh integrity regressions (Gorrund: genus 3, 1 / 0 / 0, 0 SI, as in 05AX4).

## 7. Visual / canon gates

- Grask and Gorrund are individually readable at matched heights.
- Neither collapses into Skarn / Marchfolk.
- Separation is not by scale or thin-vs-broad alone.
- Saurin is coherent.
- Canon identities are preserved: Gorrund leonine plantigrade beastfolk; Grask E3 per its accepted direction.

## 8. Stop conditions

- Hash mismatch.
- A protocol defect (a validator undefined for the source): stop and report; do not invent a replacement.
- A decision D1–D3 is still blank.
- Any result needing a Tyler visual / canon ruling.
- The C4 package is complete: **stop for author review; never promote at Stage C.**

## 9. Return and state transitions

Return three status lines (05H):
- `Grask E3 Stage C — ACCEPT / CONSTRAIN / REJECT / NOT RUN`
- `Gorrund Stage C — ACCEPT / CONSTRAIN / REJECT / NOT RUN`
- `Combined Stage C — ACCEPT / CONSTRAIN / REJECT / NOT RUN`

State: Stage C **AUTHOR REVIEW REQUIRED**. Grask E3 stays FROZEN until the author accepts. Nothing is promoted to canon by this order.
