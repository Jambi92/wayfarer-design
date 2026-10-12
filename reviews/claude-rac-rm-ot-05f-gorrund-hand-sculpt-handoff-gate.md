# RAC RM-OT-05F — Gorrund hand-sculpt handoff gate

**Order:** `reviews/chatgpt-rac-rm-ot-05f-gorrund-hand-sculpt-handoff-stage-c-order.md`

**Result:** **HANDOFF READY — stopped at the author gate (order §8, second branch).**
- No genuine direct sculpt route exists in this environment, so no sculpt was produced or faked.
- Delivered: the production brief, the evidence and reference index, the re-entry validator and the blind-gate package. Each is self-tested.
- Stage C has not run.
- RM-OT-05 stays OPEN. Nothing is promoted. No canon change, no D4, no UE5.

## 1. Author rulings acknowledged

1. **Grask E3** is accepted as the developmental race-anatomy direction pending Stage C. Its organization is frozen, no Grask search was reopened, and it was not promoted.
2. **Gorrund 05E fails.**
   - P1, P2, P3, E1, E2 and every other 05C–05E candidate stay unpromoted.
   - No further tuning of the procedural generator.
   - No canon, posture, bulk or surface-detail workaround.
3. **The hand-sculpted Gorrund base mesh is authorized** within the existing canon and technical constraints.

## 2. Route determination (order §2, §8)

The repository has no direct sculpt or mesh-edit route that is independent of the exhausted procedural generator:
- no Blender, ZBrush or other interactive modelling tool is installed;
- the only mesh-shaping code is `arch_sculpt.py` and `race_base.py`, the 05A–05E procedural generator that the order forbids reusing to fake a sculpt.

Following the second branch of §8, this pass therefore produces the handoff package and stops. It records the exact external asset required (§4).

## 3. Deliverables

| Order § | Deliverable | Status |
|---|---|---|
| 5.1 | Production brief: `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md` | Done. Contains: the six families A–F with required forms, views, must-nots and per-family inward budget; locked constraints; protected measurements and stations (05D / 05E); must-not list from 05C–05E; front, ¾, profile, rear ¾ and silhouette targets (relational, against named evidence); low-composition and Narrow / Broad persistence; import / export expectations; sculptor checklist; validator checklist; blind-gate checklist. No new canon numbers: where canon has none, targets are marked relational / visual. |
| 5.2 | Evidence / reference index: `reviews/rac-rmot05f-handoff/README.md` | Done. Indexes the true floor and protected relations, failed human-reading examples, Grask E3 (contrast only), the matched camera / silhouette standard and low-composition persistence. Only what the handoff needs was copied. No failed candidate is labelled a reference. |
| 5.3 | Re-entry validator: `tools/rac/w1/rmot05f_drivers/` | Done and self-tested (§5 below). Ingest checks I1–I6; build at reference, low, Narrow and Broad; the 05D / 05E guards with unchanged thresholds; transport report. |
| 5.4 | Blind-gate package: `f_blind.py`, `f_scorer_prompt.md`, `f_tally.py` | Done and self-tested. Protocol and pass condition exactly as §5.4. |
| — | Start mesh, guide meshes, joints, stations, region masks, figures | `reviews/rac-rmot05f-handoff/template`, `data`, `figures` |

## 4. Exact external asset required

- **File:** `GO_sculpt_<ID>_r6.obj`. A two-character ID per version; each version is fully re-validated.
- **Base:** sculpted on `reviews/rac-rmot05f-handoff/template/GO_ref_route_r6.obj`.
- **Topology:** 13 380 vertices in the template's order, faces identical (MPFB base topology without helpers).
- **Frame:** cm; Z up; ground z = 0; +Y anterior; +X body left; R-6 neutral stance; 230.90 cm.
- **Untouched:** head / neck, hands / digits, toes / forefoot within 0.5 cm. No vertex inside the true floor.
- **Optional:** a high-resolution detail level (not validated here).
- **Content:** the six hard-form families of brief §4, within the canon guardrails of brief §3.

**Command on delivery:** `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_<ID>_r6.obj <ID>`. If that passes, run the blind gate (brief §10).

## 5. Validator and blind-package self-test

Details: `reviews/rac-rmot05f-handoff/validator_selftest/`.

**Identity (T0)** — the start mesh fed back in:
- ingest PASS;
- all guards PASS at reference, low, Narrow and Broad;
- volume 1.0000;
- reproduction p90 0.000 cm (max 0.165 cm where the route already touched the floor);
- protected relations unchanged: bitroch ÷ crest 1.1846; pelvis ÷ thorax breadth 1.0234; pelvic d ÷ thorax d 0.8570; S4 ÷ S2 b 0.8391; S3 ÷ S2 d 0.9187.

**Transport (T1).** The failed 05D E1 surface was used only as a known non-zero signal. It is not a candidate.
- Ingest PASS; all guards PASS in all four states.
- The reference rebuild reproduces the delivered surface exactly (error 0.000 cm).
- Retention medians: 0.94–1.01 at low composition; 0.99–1.01 at Narrow and Broad.

**Negative tests** fail as required:
- uniform scale × 1.02 fails I2 / I3;
- 4 cm inside the floor fails I5;
- a moved hand fails I4 / I6.

**Tally:**
- a synthetic full pass passes;
- seven failing variants fail: bulk basis, low composition B, control in the group, merged with Grask, no cues, control C, single run only.

**Blind runner:** a dry run renders a 12-body sheet labelled DRY RUN. It was not scored.

## 6. Findings for the author

**Q1 — trunk section wording vs canon (family A).**
- 05E §10, carried into order 05F §4A, asks for a "planar / faceted slab … defined lateral edges".
- `GORRUND_V1` Part 2 says the thoracic cross-section is "**Anatomically shaped, never circular, rectangular or boxy**".
- The brief reconciles them as planar *zones* and plane breaks on an anatomically shaped, radiused section, not a rectangle (brief §3).
- **Please confirm this reading**, or rule otherwise. It changes the brief's family A only.

**Correction to the 05E record.** Checking every 05F family against canon showed that the failed 05E candidates also conflicted with canon clauses that 05E did not check:
- P1–P3 used a **box trunk section** ("never … rectangular or boxy");
- P2 / P3 had **uniform-diameter limbs** ("substantial never means uniform limb diameter") and near-columnar wrists ("never tiny or uniformly columnar").

None was promoted, so nothing changes in status. The brief now names these clauses as must-nots. Other clauses written into the brief as guardrails:
- knees never "bulbous, spiked or armor-like";
- elbows "never isolated knobs";
- no hunch or exaggerated lumbar arch;
- GO-P2b / P3 no lateral outrigging;
- GO-P6 no thorax → pelvis step;
- GO-G4 neck base never produced by trapezius.

**Transport constraint the sculptor must respect.** The limb families D and E have little inward room above the true floor (p10 0.4 cm, median about 1.5 cm). Their forms have to be built mainly by re-shaping and outward planes, or they will be clamped at low composition. This is in brief §4 / §6, with the budget map in `figures/floor_margin.png`.

**Action needed from the author.** Commission the external sculpt (or name a sculptor or workflow) and return the OBJ. This session can then run re-entry and the replicated blind gate. Stage C follows only if both pass.

## 7. Stage C

**Not started** (order §6): there is no accepted Gorrund sculpt yet.

## 8. Files

### Added

- `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`
- `reviews/claude-rac-rm-ot-05f-gorrund-hand-sculpt-handoff-gate.md` (this file)
- `reviews/rac-rmot05f-handoff/`: README, `template/` (4 OBJ), `data/` (joints, stations, regions), `figures/` (region map, floor margin), `evidence/05d`, `evidence/05e`, `validator_selftest/`
- `tools/rac/w1/rmot05f_drivers/`: `f_common.py`, `f_export.py`, `f_regionmap.py`, `f_ingest.py`, `f_reentry.py`, `f_guard.py`, `f_blind.py`, `f_scorer_prompt.md`, `f_tally.py`, `f_selftest_inputs.py`, `f_tally_selftest.py`

### Changed

- `tools/rac/w1/race_base.py`: `skin_frames`, `sculpt_layer`, and the `sculpt` spec key in `organize`. These are inert without the key; every earlier spec reproduces unchanged.
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`: phase state only.

No canon file changed. The self-test bodies (`GO5FT0*`, `GO5FT1*`) are scratch-only and not registered as reference assets.
