# Saurin Creator Biology Closure / Final First-Pass Audit

**Author:** Claude
**Responds to:** `reviews/chatgpt-saurin-creator-biology-closure-order.md` (e86b0bb)
**Phase:** design only. No anatomy was reopened, and the frozen reference (aff1b52) was not modified.

## 1. Tests performed

**Cross-race rostral-floor audit**
- Searched `MARCHFOLK_V1.md`, `GRASK_V1.md` and `GORRUND_V1.md` for numeric projection data.
- Marchfolk is a human midface with no projection numbers.
- Grask: "maxillary and mandibular projection distribution OPEN"; Grask are explicitly not muzzle- or snout-defined.
- Gorrund: "prognathism distribution OPEN"; moderate forward projection without a muzzle.
- **Result:** canon has no numeric projection range to compare against. No threshold was invented. The Saurin floor stays provisional (rostral index 0.255, reference 0.288), and the missing cross-race measurement is recorded as OPEN (§3 below).

**Head couplings**
- All re-checked against the variation diagnostics: rostral index, cranial length × rostrum floor, long rostrum → rostral and jaw depth, and orbit/eyeball.
- New measurement of the base-width / anterior-width taper on every width combination: anterior/base width ratio stays 0.60–0.73 (reference 0.685). The taper never inverts.

**Orbital placement** (`v18_02_orbital_placement.jpg`)
- Each orbit was moved with a smooth falloff: spacing ±3 %, vertical ±0.25 cm.
- The falloff drags the brow rim and postorbital planes along with the orbit instead of re-forming them, so this cannot validate placement cleanly.
- **Result:** placement stays LOCKED; its numeric tolerance is OPEN.

**Digit / claw proportion** (`v18_01_claw_length.jpg`)
- Each of the 20 claws was stretched along its own axis from its base ring, at reference curvature. Lengths tested: ×0.8, ×0.9, ×1.0, ×1.15, ×1.3, ×1.5.
- Foot-claw tips reach the ground plane at about +15 % length:
  - ×1.15: minimum tip height 0.008 cm
  - ×1.3: −0.11 cm (below the ground)
  - ×1.5: −0.29 cm
- Forefoot envelope grows by +0.35 cm at ×1.15 and +0.70 cm at ×1.3.
- Grasp, footwear and glove compatibility cannot be validated without a grip pose and equipment.
- **Result:** the reference anatomy is retained, no numeric creator range is canonized, and the ground-contact finding is recorded.

**Final contradiction audit** of the accepted creator envelope, using the variation package's measured cases:

| Check | Result |
|---|---|
| Frames are editable starting distributions, not castes; frame changes no stature or skull | Confirmed |
| Composition is independent of frame | Confirmed |
| Stature is isometric for every relationship; the Counterbalanced Pelvic-Axial Architecture survives 168 and 208 cm | Confirmed |
| No valid head falls out of Saurin identity | Confirmed: all single extremes PASS; failing combinations are CONSTRAINed |
| No valid tail recreates attached-appendage, threadlike, cylindrical or unsupported reads | Confirmed: those shapes are FAIL or CONSTRAINed |
| Displays stay valid on the cranial extremes | Confirmed |
| No creator rule reintroduces human assumptions | Confirmed |
| Randomization samples valid combinations; presets and NPCs use the same validity system | **Was missing from canon; written** (§264) |

## 2. Corrections made (documentation only; resolved from established canon)

- **§29 Dragon firewall** listed "horns" as unapproved. Reworded to: no mandatory/default dragon-style horn sets; controlled cranial display anatomy is valid under §100–102 / §260.
- **§59 Crest/frill firewall:** added a reconciliation note. The firewall rejects dragon/dinosaur-default structures. Restrained crests (~2.5 cm ceiling) and brow hornlets are valid; frills, hoods, fins and cheek spikes stay unapproved.
- **Part 1 creator-category note:** "ridge/surface controls" → Cranial Display controls.
- **§192 Headgear:** "optional low-profile ridges" → the full display family; "ridge-present/absent" → "display-present/absent".
- **§10:** 55–80 % is now marked as the racial envelope, with upper-end reachability set by frame/composition (§256).
- **§26:** carriage is now distinct from tail proportions, and the frozen stance is a reference stance (§257).
- **§146:** rostral floor marked provisional; cross-race check OPEN.
- **Header status, and the Part 6 status line after §254:** "PROPOSED FOR FINAL AUDIT" → ACCEPTED / COMPLETE.
- **`specs/STATUS.md`:** Saurin was listed both "in progress" and "not yet designed". Cleaned up.
- **`README.md`:** the race table still showed Pipkin "Part 6 next" and Cogling and Saurin "Not started". Updated to match `STATUS.md`.

## 3. Final accepted creator relationships

All are in `specs/saurin/SAURIN_V1.md`, new **Part 7** (§255–§266). It separates six value types:
- racial hard bounds;
- first-pass creator hard bounds (validated at their extremes);
- soft distributions (provisional);
- coupled rules;
- locked biology;
- OPEN items.

**Tail (§256)**
- Length drives base and fullness; base ≈ length^1.18.
- Root-sufficiency band 0.75–1.20.
- Peak loss rate ≤ 1.25 × reference.
- Mid area 0.27–0.48 of root; distal area ≥ 0.065 of root.
- Balance guard: +3° extra lean, relative to the reference.
- Frame/composition set the reachable upper length: ~78 % Balanced, 80 % Broad, ~72 % Narrow + high fat. **80 % is an envelope, not an entitlement.**
- Muscularity follows composition.
- Caudal fat is graded over the proximal tail.
- Carriage is distinct from proportions.
- Stature is isometric.
- Pelvis/sacrum is never altered.

**Reference stance (§257):** about 8.8° lean needed under the uniform-density model. Recorded, not fixed; carried to posture/locomotion/animation.

**Body (§258):**
- Proportion hard bounds as validated.
- Thoracic depth/width 0.80–1.00.
- Frame/composition separation, with the Gate 6 human-anatomy prohibitions kept.

**Head (§259):**
- Validated single-control bounds.
- Couplings: rostral index 0.255–0.335 (provisional floor), cranial length × floor, long rostrum → depth, base/anterior taper, orbit/eyeball.
- Orbital placement locked.

**Displays (§260):**
- The six-family range is canon.
- Footprint ratio ≥ 0.060; neutral neck clearance ≥ ~7 cm; crest ceiling ~2.5 cm; natural asymmetry ≥ 0.70.
- Not hair, not a sex or culture marker, no stats.
- Breakage belongs to the acquired layer.

**Other:**
- Claws (§261): reference retained, range OPEN.
- Scales (§262): field-aware rules only, no global slider, no numeric canon.
- Sex (§263): no established requirement, nothing assumed, OPEN.
- Randomization, presets and NPCs (§264): driver variables sampled first, dependents inside their coupled bands, FAIL shapes rejected, the same system for all.

**Candidate numbers not canonized:** soft-distribution widths are provisional only. Per-field scale ranges, claw ranges, orbital-spacing tolerance and the display moment limit were not made canon.

## 4. OPEN items carried forward (§265)

1. Balanced neutral standing posture and living balance; the final density model.
2. Absolute balance limits once posture is fixed.
3. The exact caudal-base landmark for measuring tail length.
4. Cross-race numeric rostral floor: normalized midface/rostral projection ranges for Marchfolk, Grask and Gorrund, for the universal comparative review.
5. Numeric lower-trunk minimum against Marchfolk.
6. A numeric Broad-vs-Gorrund boundary.
7. Population adipose tendencies.
8. Display mass-moment limit and clearance through the head/neck range of motion.
9. Prominent horns, spikes and plates beyond the validated families, and crests above ~2.5 cm.
10. Orbital placement/spacing tolerance.
11. Hand/foot claw and digit numeric ranges (grasp, footwear, gloves).
12. Numeric per-field scale ranges.
13. Sex-related anatomy.
14. World-space validation of the longest tails (up to ~170 cm of reach behind the heel).
15. The universal facial-control architecture and statistical calibration of soft distributions.

None of these blocks first-pass completion.

## 5. Files reconciled

| File | Change |
|---|---|
| `specs/saurin/SAURIN_V1.md` | Header; §10, §26, §29, Part 1 creator note, §59, §146, §192, §249 pointer, Part 6 status line; new Part 7 (§255–§266) |
| `specs/STATUS.md` | Saurin entry cleaned up |
| `README.md` | Race table |
| `reviews/images/saurin-creator-biology-closure/` | `v18_01_claw_length.jpg`, `v18_02_orbital_placement.jpg`, `v18_claws.json` |
| `tools/rodin/creator-biology/closure/` | `claws.py`, `clawr.py`, `orbit.py`, `compose18.py` |
| Audit history in `reviews/` (unchanged) | `claude-saurin-creator-biology-variation.md`, `saurin-creator-parameter-register.md` |

## 6. Status

No blocking contradiction remains.

**SAURIN — FIRST-PASS COMPLETE.**

Stopped. No UE5, production morphs, rigging, animation, final idle/locomotion design, clothing/armor, external sex anatomy, universal facial-control architecture or 13-race comparative revisions.

## 7. Commits

Closure commit: SHA_PLACEHOLDER

— Claude
