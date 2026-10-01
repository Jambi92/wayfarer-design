# Targeted Sculpt 1 — Gorrund Load Path and Saurin Dedicated Sculpt

**Author:** Claude
**Responds to:** `reviews/claude-detailed-targeted-sculpt-instruction.md`
**Status:** RETURNED FOR TYLER / CHATGPT REVIEW. Not declared final.
**Scope:** Gorrund and Saurin only. No other race was touched. No spec edits, no Pass 2 work, no UE5 work.

All images are in `reviews/images/targeted-sculpt-1/`. Every image uses the Iteration 3 fixed orthographic camera, neutral composition and neutral expression, with no costume.

## Method and tooling

- Both sculpts are scripted as shape keys on top of the solved Iteration 3 bodies. They live in `RaceBodies/wf_sculpt_lib.py` and `wf_sculpt_run.py`.
- They change shape only. Muscle and fat stay at the neutral setting.
- They are reproducible and stay rigged. The `.blend` and `.fbx` files are on Tyler's PC:
  - `RaceBodies/out/GorrundSculpt_{Masc,Fem}`
  - `RaceBodies/out/SaurinSculpt_{Masc,Fem}`
- The pre-sculpt bodies are kept unchanged for comparison.
- This is procedural sculpting, not hand sculpting. The limits are listed at the end.

---

## 1. Gorrund — axial load-path sculpt

**Sheets:**
- `gorrund_{Masc,Fem}_true_scale.jpg`: Marchfolk, Grask, pre-sculpt Gorrund and sculpted Gorrund.
- `gorrund_{Masc,Fem}_normalized.jpg`: Grask, pre-sculpt Gorrund and sculpted Gorrund.
- `gorrund_{Masc,Fem}_overlay.jpg`: silhouette overlay (grey = shared, orange = added by the sculpt).

**What changed.** One continuous field runs along the chain shoulder girdle → thorax → lower axial trunk → pelvis → proximal lower limbs:

- **Shoulder girdle:** the clavicle line was widened by 2 cm per side, and the arm bones were moved to match so the rig stays valid. The neck-to-shoulder ramp (trapezius line) was raised and filled, so the shoulders sit on the thorax rather than being added deltoid mass.
- **Thorax:** this is the largest change. Ribcage depth went up about 13% and breadth about 9%, peaking at the mid-thorax, so it reads as a large skeletal cage and not uniform inflation.
- **Lower axial trunk:** width and depth were carried down from the thorax to the pelvis, so there is no abrupt narrow waist. The anterior abdominal wall was held back, so there is no belly. The waist remains as anatomy.
- **Pelvis:** broader and deeper pelvic base.
- **Proximal lower limbs:** the upper thigh was expanded radially at the femoral base and hip-joint transition, fading out by mid-thigh. This is bone-scale volume, not muscle definition.
- **Not changed:** stature, arm length, the head and neck, and joint and extremity size.

**Measured change at 229 cm** (pre-sculpt → sculpt; share of stature after the sculpt):

| Measurement | Masculine | Feminine |
|---|---|---|
| Shoulder joint width | 56.0 → 61.4 cm (+10%), 26.8% | 50.3 → 55.7 cm (+11%), 24.3% |
| Chest depth | 32.0 → 36.1 cm (+13%), 15.8% | 29.3 → 33.0 cm (+13%), 14.4% |
| Chest width | +9% | +9% |
| Waist girth | +8% | +8% |
| Hip width | +4% | +14% |
| Hip depth | +4% | +6% |

**Against Grask at equal height:** Grask is rangy and limb-led. Gorrund now reads clearly as axial and torso-led. The anti-targets I checked were taller Skarn, bodybuilder, obese giant, hunch and long arms. On the sheets I judge none of them triggered, but this is for the Author to confirm.

**Remaining limit:** the masculine base mesh shows a slight pectoral lower edge from MPFB's chest topology. A hand-sculpt pass could soften it.

---

## 2. Saurin — dedicated sculpt

**Sheets:**
- `saurin_{Masc,Fem}_true_scale.jpg`: Marchfolk, pre-sculpt Saurin and sculpted Saurin, with the complete tail in every view.
- `saurin_{Masc,Fem}_normalized.jpg`: diagnostic sheet; the tail is excluded from stature.
- `saurin_{Masc,Fem}_closeups.jpg`:
  - head: front, profile, 3/4
  - tail base: profile and both rear 3/4 views
  - hand: front and back, plus an eye closeup
  - foot: front, side, 3/4
- `saurin_{Masc,Fem}_scale_regions.jpg`: region diagram with legend.

### Head — Layered Rostral-Cranial Integration (replaces the human-derived placeholder)

- **Cranial vault:** about 20% lower above the orbits and longer front-to-back. The forehead slopes back into the vault, so there is no vertical forehead or human nasal root.
- **Orbital/temporal platform:** broader at eye level, which also spaces the eyes wider. The eyes are forward-facing, with no brow scowl.
- **Rostrum:**
  - The whole midface and jaw block projects about 7 cm (masculine) as one skeletal unit.
  - The base is broad and joins the orbit and cheek regions, with a moderate taper toward the tip.
  - It is compact, with no long muzzle, dragon wedge or crocodilian snout.
- **Nasal region:** the external nose is removed. A nasal dorsum line runs from the orbital root to the rostral tip.
- **Jaw:** the chin is removed and the lower jaw rises into a tapered line toward the tip. The posterior jaw angle is widened (deep jaw base). The mouth line follows the rostrum, with no grin.
- **Auricular region:** the pinna is collapsed into a shallow rim around a recessed opening. There is no lobule and no point.
- **Eyes:** amber iris with a vertically elliptical pupil at neutral dilation. The nictitating membrane is **not represented**; see the limits below.
- **Cranial ridges:** none were added, since they are optional and not baseline.

### Tail-base integration and complete tail

- **Sacral sculpt:** a shape key carries the lower spine, sacrum and posterior pelvis back into the caudal base and fills the gluteal cleft, so the body's centerline continues into the tail.
- **Tail root:** it starts inside the sacral mass and is widest where it leaves the body, with a taller cross-section at the root. It then tapers gradually in a relaxed gravity curve.
- **Tail dimensions (both sexes):**
  - length 128 cm (68% of 188 cm);
  - base about 23 cm, with a root flare of about 27 cm;
  - the tip rests about 63–66 cm above the ground.
- **Not changed:** the tail is not toggleable and not prehensile. No collision or gameplay meaning is derived from it.

### Hands and feet

- Fingers are moderately elongated (finger share 1.07). There are five digits with an opposable thumb.
- Every finger and toe has a modest, non-retractable claw-like nail.
- The feet are broad and plantigrade with a longer forefoot.
- Palms, finger pads and soles are in the fine contact-scale field. They are not mammalian paw pads and not smooth human skin.

### Regional Scale Architecture (no uniform texture)

- **Field assignment:** every skin vertex is assigned to one field (structural, articulation, fine, ventral, contact or general), following the spec's distribution. The region diagram shows the mapping.
- **Relief:** each field is rendered as cell-edge relief at its own scale:
  - large, low structural cells;
  - small articulation cells;
  - very fine facial, auricular and throat cells;
  - broad, transversely stretched ventral cells with no continuous scutes;
  - fine contact cells on palms and soles.
- **Material:** matte grey (Workbench). No wet, metallic or emissive look is implied.

---

## Tooling limits and items for review

1. **Nictitating membrane.** It is not shown, because the renderer doesn't display translucent geometry. It belongs with eye shading and animation. The identity decision is unchanged.
2. **Mouth.** The lips are reduced but are still derived from the human base mesh. A hand sculpt should cut the mouth line further back along the jaw.
3. **Tail geometry.** The tail is a separate bone-parented mesh, sculpted to look continuous. For a game asset it should be merged and skinned to new tail bones. That is technical work for later, not Pass 1.
4. **Scales.** The scales are procedural displacement for reference only. Final scale layout is a texture and normal-map task.
5. **Gorrund.** The scripted sculpt achieves the intended load-path chain within the base mesh topology. A hand-sculpt finish would mostly address surface quality.

## Spec/model conflicts

None found. No spec was edited.

Neither Gorrund nor Saurin is declared final. Both are returned for Tyler/ChatGPT review.
