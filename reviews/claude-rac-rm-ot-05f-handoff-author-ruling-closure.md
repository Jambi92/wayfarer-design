# RAC RM-OT-05F — handoff author ruling: closure and freeze

**Order:** `reviews/chatgpt-rac-rm-ot-05f-handoff-author-ruling-freeze-order.md`
**Result:** rulings applied, handoff package frozen, **STOP** (order §10). The next action is external / direct production of the Gorrund sculpt.

## Status (authoritative, per order §1)

| Item | Status |
|---|---|
| RM-OT-05 | **OPEN** |
| Grask E3 | Accepted developmental race-anatomy direction, pending Stage C. Frozen; not promoted; search not reopened |
| Gorrund | **Unaccepted.** **EXTERNAL SCULPT REQUIRED — AWAITING ASSET.** P1, P2, P3, E1, E2 and every other 05C–05E body stay unpromoted |
| Stage C | **Blocked** until a genuine Gorrund sculpt passes re-entry and the replicated blind gate |
| D4 / UE5 / canon promotion | None |

## Confirmations

1. **Q1 applied.** Brief §3 (family A row) now states the approved controlling interpretation:
   > Planar anatomical zones and plane breaks are allowed and desired, but they must exist on an anatomically shaped, radiused thoracic cross-section. "Planar" describes surface organization, not a rectangular body section.

   The allowed and not-allowed lists are written out. "Mechanically slab-sided" and "circular / cylindrical" were added to the family A must-nots (§4A), to the silhouette target (§5) and to the sculptor checklist (§8). This is recorded as an interpretation of existing canon, not new canon.
2. **Waist wording corrected without changing canon.** Every 05F place that could read as a race-wide "no waist hollow" rule now says that the **reference sculpt** must not rely on a human-style pinched waist or waist hollow as the readability cue. Canon-valid waist variation stays available through Frame / composition. Changed places:
   - brief §3 (family A waist row);
   - §4A (required forms and front view);
   - §5 (silhouette target);
   - §8 (sculptor checklist).

   No canon file, no Frame / composition system and no validator was changed.
3. **Handoff package frozen.**
   - The brief and `reviews/rac-rmot05f-handoff/README.md` carry the FROZEN status and the EXTERNAL SCULPT REQUIRED status.
   - The six family intents are unchanged.
   - No validator threshold was changed.
   - The region map is labelled an editing-jurisdiction guide only; the brief text governs anatomy.
4. **No new procedural Gorrund body was generated.** `arch_sculpt.py`, `race_base.py` and the 05C–05E drivers were not run or changed in this pass.
5. **Grask freeze.** Grask E3's status and organization are unchanged. The brief already forbids borrowing its scapular / hump and high-calf / long-cord cues for Gorrund (brief §4D, §4F, §7).
6. **Stage C remains blocked** (order §8).

## Expected external asset on re-entry

- File: **`GO_sculpt_<ID>_r6.obj`** (two-character ID)
- Base: **`reviews/rac-rmot05f-handoff/template/GO_ref_route_r6.obj`**
- Same 13 380 vertices in the same order, identical faces; R-6 neutral stance; cm, Z up, +Y anterior, +X body left
- No-touch zones within 0.5 cm; no true-floor violation; the six hard-form families expressed structurally
- No rewrite of topology, skeleton, stature route, joint centres, long bones, plantigrade feet, digit count, Frame / composition or rig compatibility
- Re-entry command, unchanged: `python3 tools/rac/w1/rmot05f_drivers/f_reentry.py GO_sculpt_<ID>_r6.obj <ID>`, then the replicated blind gate (`f_blind.py`, `f_scorer_prompt.md`, `f_tally.py`) with every existing condition

## Files changed

- `reviews/gorrund-rm-ot-05f-hand-sculpt-production-brief.md`: frozen status line; Q1 approval; waist correction; region-map jurisdiction wording.
- `reviews/rac-rmot05f-handoff/README.md`: frozen / awaiting-asset status line.
- `reviews/claude-rac-rm-ot-05f-handoff-author-ruling-closure.md`: this report.
- `specs/STATUS.md`, `reviews/claude-pass2-r5-reference-mesh-queue.md`: status / tracking only.

No race canon file was edited. No contradiction requiring a canon edit was found.
