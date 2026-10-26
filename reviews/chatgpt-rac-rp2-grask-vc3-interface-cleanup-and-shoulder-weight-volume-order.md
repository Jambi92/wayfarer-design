# RAC RP2 — Grask VC3 interface cleanup + production-direction shoulder weighting order

**Date:** 2026-10-26  
**Authority:** Tyler / ChatGPT review of Claude return `bb029bb1421fd00729f5a7c011abfaf1411378c8`.  
**Parent gate:** `reviews/claude-rac-rp2-grask-elbow-vc-contact-and-shoulder-isolation-gate.md`.  
**Status entering this order:** Grask RP2 retopology remains AUTHOR ACCEPTED / FROZEN / CLOSED. Production deformation remains **not accepted**.

This order records the author rulings from the latest gate and authorizes two tightly bounded follow-ups:

- **Track E2:** one final contact-interface cleanup pass on VC3 at deep elbow flexion;
- **Track S2:** one production-direction shoulder weighting / volume-preservation pass based on the weighting-dominant classification.

No topology or source-anatomy reopening is authorized.

---

## 1. Immutable parents / hard firewall

Do not edit, resave over, reproject, smooth, retopologize, symmetrise, or otherwise change:

- `GR_U_REF_RP2_retopo_v003.blend`
- `GR_U_REF_RP2_SOURCE_3D_v005.blend`
- v003 sidecars / frozen landmark package / freeze record
- v001 / v002 retopo provenance
- prior diagnostic rigs and evidence packages

The accepted Basis/rest geometry remains exactly frozen v003.

No v004 retopology is authorized.

No production rig finalization, creator morphs, facial/oral work, UVs, materials, LODs, UE5 integration, animation, or another race is authorized.

Capture before/after hashes for all immutable parents. Stop on any mismatch.

---

# AUTHOR RULINGS

## 2. Elbow state

- H2 remains the preferred diagnostic elbow configuration through **60–120°**.
- VC3 is the best **numeric** 130° result so far but is **not visually accepted**.
- VC3 is therefore **not promoted**.
- 130° remains unresolved.
- The remaining defect is the high-frequency rumpled/contact-interface texture, not gross penetration, loop collapse, or closed-volume loss.

Do not reopen C1/C2/H1/H2/H3 search trees.

Do not add new helper bones.

---

## 3. Elbow volume metric correction

Retire the old "closed volume versus interpenetrating W0" as the primary 130° acceptance metric.

Going forward, primary elbow volume evaluation is:

1. **overlap-aware physical volume change relative to the straight-elbow base**; and
2. **local ring girth / mean ring radius** as the balloon/shrink check.

The old divergence-theorem closed-volume metric may remain in reports for continuity, but it is secondary because W0 double-counts overlap under interpenetration.

Report:
- double-covered overlap volume;
- overlap-aware physical volume;
- physical dV relative to straight elbow;
- ring radius/girth by station;
- comparison against C2/C2rx, H2 and VC3.

---

## 4. Shoulder state

- Primary classification is **WEIGHTING-DOMINANT**.
- Do not relocate GH.
- Retain the abduction girdle/scapular mechanics as a secondary component of the shoulder solution.
- The current S2 weighting direction is accepted as the correct direction, but not as production-ready because of local volume loss and strain spikes.

Do not reinterpret the shoulder result as a topology failure.

---

# TRACK E2 — VC3 CONTACT-INTERFACE CLEANUP

## 5. Purpose

Test whether VC3's high-frequency contact-interface rumpling at 130° can be removed without sacrificing its numeric gains.

This is the **last elbow corrective experiment authorized in RP2** unless a later explicit order reopens it.

The goal is not to redesign VC3.

The goal is only to smooth the localized contact-interface texture while preserving:

- 0 non-contact intersections;
- good crease depth;
- orientation improvement;
- loop spacing;
- volume restoration;
- girth;
- absence of ballooning.

---

## 6. Allowed method

Use one interface-aware smoothing / fairing method restricted to the actual 130° contact-interface support.

Examples allowed:
- contact-surface-aware Laplacian smoothing;
- tangent-plane smoothing;
- bilateral/geodesic field smoothing;
- curvature-limited fairing;
- constrained smoothing with volume/girth lock.

The operation must be restricted to the corrective field / derived posed deformation.

Do not alter frozen rest geometry.

Do not globally smooth the elbow.

Do not move the entire limb or create new volume outside the declared interface support.

---

## 7. Candidate limit

At most **two** cleanup candidates:

- **VC3F1:** one direct interface-fairing pass;
- **VC3F2:** one bounded refinement only if F1 is close but has one localized defect.

No third candidate.

No new helper chains.

No new elbow pivot.

No new global weight split.

---

## 8. Test angles

Primary:
- 130° left
- 130° right

Regression:
- 120° left/right

Sanity:
- 110° if the fairing field has nonzero activation there.

Below the activation range, prove the deformation is bit-identical to the accepted diagnostic configuration.

---

## 9. E2 acceptance criteria

A candidate may be selected only if:

### Geometry integrity
- 0 non-contact intersections at 130° both sides;
- no new local inversions;
- no folds outside intended contact/crease zones;
- rest return effectively zero.

### Crease
- left <= 3.5 mm;
- right <= 3.5 mm;
- no visible upper-crease spike.

### Orientation
- no material regression versus VC3;
- preferred <= 100 left / <= 90 right.

### Loop
- >= 0.50 both sides.

### Physical volume
Using the corrected overlap-aware metric:
- physical volume must remain materially better than C2/C2rx;
- no more than 10% loss of VC3's physical-volume improvement.

### Ring girth
- no ring radius > straight-base + 0.35 cm;
- no station should shrink materially below C2 unless necessary for contact.

### Strain
- p95 no worse than VC3 + 3 percentage points;
- no new max-strain spike > 125% unless visually demonstrated harmless and isolated.

### Visual
This is the decisive criterion:
- contact must read as compressed flesh;
- remove the irregular crumpled/rippled texture that caused VC3 rejection;
- no shelf, ridge, isolated lump, balloon, faceted band, or artificial crease wall.

If the visual still reads as rumpled even when numeric criteria pass, **reject the candidate**.

---

## 10. Ripple / texture measurement

Retain the existing ripple metric, but expand the evidence:

- p95 high-frequency displacement;
- local curvature variation along the contact seam;
- displacement gradient along and across the interface;
- same-camera shaded closeups.

Use metrics as support only.

Visual author readability remains authoritative.

---

## 11. Required E2 evidence

Provide:

- VC3 vs VC3F1 vs VC3F2 if used;
- 130° left/right clay closeups;
- 3/4 contact-line views;
- wire closeups;
- contact cross-sections;
- ripple/curvature plots;
- physical volume plots;
- ring girth/radius plots;
- strain maps;
- displacement-field maps;
- support mask;
- intersection/orientation/inversion overlays;
- rest-return check.

Explicitly state:

1. Was the VC3 rumpling visibly removed?
2. Were all numeric VC3 gains preserved?
3. Did the corrected physical-volume metric remain improved versus C2/C2rx?
4. Was any new artifact introduced?
5. Is 130° accepted as a usable diagnostic deformation, or still unresolved?

If no candidate passes, **close RP2 elbow experimentation** and carry 130° forward as an unresolved production-rig/contact-corrective item.

Do not continue experimenting.

---

# TRACK S2 — SHOULDER PRODUCTION-DIRECTION WEIGHTING + VOLUME PRESERVATION

## 12. Purpose

Turn the weighting-dominant shoulder finding into a more production-representative deformation direction without claiming final production weights.

Preserve:
- existing GH placement;
- accepted diagnostic landmark architecture;
- abduction girdle/scapular mechanics where they help.

Improve:
- anterior axillary fold behavior;
- shoulder-fan loop spacing;
- crease/orientation quality;
- local volume preservation;
- local strain distribution.

---

## 13. Baseline architecture

Use:

- v002 diagnostic landmarks;
- W0 rest and frozen v003 Basis;
- S1 girdle mechanics as the secondary mechanics layer where applicable;
- S2 weighting direction as the starting weighting concept.

Do not relocate GH.

Do not change topology.

Do not alter global arm proportions.

---

## 14. Shoulder weighting scope

Bound the weighting work to:

- anterior axillary fold;
- shoulder fan;
- proximal upper arm;
- deltoid transition;
- immediately adjacent pectoral / lat transition only where required for continuity.

Do not diffuse changes broadly through torso, spine, forearm or hand.

The goal is to improve shoulder behavior, not globally reweight the character.

---

## 15. Candidate limit

At most **three** shoulder candidates:

- **SW1:** refined bounded weighting with current S1 mechanics;
- **SW2:** SW1 + one local volume-preserving corrective/helper field;
- **SW3:** one final bounded refinement only if SW2 is close and one localized issue remains.

No broader search.

No production freeze.

---

## 16. Volume-preservation mechanism

Because S2 clears crease/orientation but loses too much local volume, authorize one local production-direction volume-preservation mechanism.

Allowed:
- bounded pose-space corrective;
- local helper influence;
- local volume-conserving field;
- mild corrective bulge distributed over deltoid / axillary mass.

Not allowed:
- GH relocation;
- topology edit;
- global torso bulge;
- shoulder silhouette balloon;
- large deltoid lump;
- volume restoration that recreates the original crease failure.

---

## 17. Shoulder test set

Both sides:

- abd45;
- abd90;
- flex90;
- ext30;
- abd90_girdle;
- flex90_girdle.

Regression:
- all D1 poses;
- every additional pose whose changed weights/mechanics have non-zero influence.

---

## 18. Shoulder acceptance targets

### Intersections / crease
- 0 non-contact intersections where not declared contact anatomy;
- flex90 crease target 0–2 mm;
- abd90 crease target <= 2 mm.

### Orientation
- materially better than W0;
- target <= 100 faces in flex90 if achievable without volume/strain regression;
- no new local inversions.

### Loop spacing
- target >= 0.50 at the shoulder fan;
- minimum acceptable diagnostic direction >= 0.45 if accompanied by clear visual improvement and no other failures.

### Volume
Use a local shoulder-zone physical/sectional volume proxy.

The current S2 ~−45 to −49% flex90 zone loss is not acceptable as production direction.

Target:
- recover at least **50% of S2's excess zone loss relative to W0**;
- preferred flex90 zone proxy no worse than −30%.

### Strain
- remove or reduce S2's localized max-strain spikes;
- preferred max < 150%;
- any remaining >150% spike must be isolated, explained, and visually benign.

### Visual
- smooth axillary fold;
- believable deltoid continuity;
- no arm-torso tearing;
- no shoulder cap collapse;
- no inflated deltoid;
- preserve Grask's accepted girdle slope and long-limbed anatomy.

---

## 19. Shoulder mechanics rule

Retain S1-style girdle/scapular motion for abduction where it clearly helps.

Do not force large scapular/clavicular motion into flex90 if the current architecture does not support it cleanly.

If flex90 remains primarily weight/corrective-driven, report that honestly.

Do not redesign the entire shoulder hierarchy in this order.

---

## 20. Shoulder evidence

Provide:

- W0 / S1 / S2 / SW candidates;
- left and right;
- front / rear / 3/4 front / 3/4 rear;
- axillary closeup;
- shoulder-fan wire closeup;
- volume/section plots;
- loop-spacing plots;
- strain maps;
- contact/intersection overlays;
- orientation/inversion overlays;
- weight maps;
- corrective/helper field maps if used;
- clavicle/scapular motion readout.

---

# CROSS-TRACK CONTROLS

## 21. Nail / knee / other regions

- Nail Plate Rigidity v2 remains gating.
- Nail Cap Historical v1 remains report-only.
- v002 knees remain diagnostic baseline.
- No knee work.
- No hand/thumb production work in this order.
- No facial work.

---

## 22. Diagnostic files

Derived files are allowed.

Suggested:
- `GR_U_REF_RP2_rigdiag_v007_elbow.blend`
- `GR_U_REF_RP2_rigdiag_v007_shoulder.blend`

or one clearly partitioned v007 diagnostic file if there is zero cross-interference.

Every derived file must:
- preserve frozen v003 rest geometry exactly;
- be tagged DIAGNOSTIC / NON-PRODUCTION;
- log all active weights/helpers/correctives;
- record exact file/hash/geometry hashes.

Do not overwrite prior diagnostics.

---

## 23. Regression

For any selected elbow or shoulder candidate:

- run all directly affected poses;
- prove unrelated poses are bit-identical or numerically negligible;
- run the 43-pose suite if influence reaches outside the targeted region;
- report all fixed, unchanged and regressed criteria.

Any unexpected cross-region regression is a stop condition.

---

## 24. Required return

Commit:

1. `reviews/claude-rac-rp2-grask-vc3-interface-cleanup-shoulder-weight-volume-gate.md`;
2. Track E2 configs/tools/evidence;
3. Track S2 configs/tools/evidence;
4. derived file manifests/hashes;
5. before/after immutable-parent hashes;
6. narrow `specs/STATUS.md` update;
7. session handoff.

The gate must explicitly state:

### Elbow
- selected cleanup candidate or none;
- whether VC3 rumpling was removed;
- corrected physical-volume result;
- ring-girth result;
- crease/orientation/loop/strain;
- whether 130° is now accepted diagnostically or carried forward unresolved.

### Shoulder
- selected SW candidate or none;
- flex90/abd90 crease;
- orientation;
- loop spacing;
- volume recovery;
- max strain;
- whether weighting-dominant classification remains;
- whether any topology issue is demonstrated.

### Global
- parent integrity;
- regressions;
- whether production deformation is accepted (**not automatically**);
- exact next ChatGPT decision.

---

## 25. Stop rules

STOP FOR CHATGPT REVIEW after both tracks.

Do not proceed to:

- production rig finalization;
- production skinning freeze;
- more elbow experimentation if E2 fails;
- retopology edits;
- facial/oral/eye work;
- creator morphs;
- UV/materials;
- LODs;
- UE5;
- another race.

---

## FINAL AUTHOR RULING

- Grask RP2 retopology remains **ACCEPTED / FROZEN / CLOSED**.
- VC3 is rejected visually despite numeric success.
- One final VC3 contact-interface cleanup pass is authorized.
- The primary elbow volume metric is now overlap-aware physical volume relative to the straight-elbow base plus ring girth.
- Shoulder is **WEIGHTING-DOMINANT**.
- GH stays fixed.
- A bounded production-direction shoulder weighting + volume-preservation pass is authorized.
- No topology or source-anatomy reopening is authorized.
