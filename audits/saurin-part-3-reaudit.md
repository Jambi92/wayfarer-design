# Re-audit: Saurin v1.0 Part 3

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` at commit `a9c7121`
**Request:** `reviews/saurin-part-3-reaudit-request.md` (`fd92eba`)
**Responds to:** `audits/saurin-part-3.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** All findings are resolved. One wording note is non-blocking.

**Recommendation:** Saurin Part 3 may be accepted by Tyler.

## 2. Verification

| # | Point | Result | Basis |
| --- | --- | --- | --- |
| 1 | Whole-body surface uses the Skin Appearance Layers | **PASS** | New "Whole-body Skin Appearance Layers" subsection after §122. Scales, pigment, patterns, claws, ridges and aging are Natural. Dirt, wetness and weathering are Environmental. Paint and cosmetics are Applied. Scars, damage and wear are Acquired. The layers can't be collapsed into one slider. See note 3.1. |
| 2 | FD domains face-only; facial FD-SURF is a subset of Natural | **PASS** | Both stated explicitly. Environmental wetness is kept distinct from FD-OBS. |
| 3 | Palms and soles; SAU-SURF-27 | **PASS** | §106A gives fine, flexible, low-relief contact scales with localized pad-like thickening at pressure points, a gradual transition into the joint fields, and neither paw pads nor human palms. SAU-SURF-27 tests the fist, the weapon or tool grip and the planted foot. This delivers Part 1's "pad/sole organization." |
| 4 | Pupils and membrane as identity choices | **PASS** | §95 now calls the pupil an Iksar-inspired identity phenotype with no claim of superior sensory performance. §98 says the same of the membrane. Part 2 §45's "cannot be assumed from 'reptilian'" is now answered properly. |
| 5 | Ridges are integumentary, FD-SURF | **PASS** | §100: keratin over the approved skull, not bony horns, with slight rugosity allowed. The Part 2 FD-STRUCT and surface-neutral tests stay closed. |
| 6 | SAU-SURF-28 gaze readability | **PASS** | It covers conversation distance across pupil dilation and ocular-tissue visibility, "without humanizing the eye." |
| 7 | Thermoregulation OPEN | **PASS** | §124 adds it, with no cold, heat or temperature gameplay modifier implied. |
| 8 | Hair categories | **PASS** | A creator note in the Part 1 notes area: no human hair assets. Ridge and surface controls may sit in a race-aware category "without pretending those structures are hair." |
| 9 | Occupational wear in Acquired | **PASS** | Thickened, polished or abraded grip, knee and contact scales. |
| 10 | No belly-scute plating | **PASS** | §84. |
| 11 | No regressions | **PASS** | The diff only adds text or reworded clarifications. The mandatory tail, the §115 garment OPEN item, Parts 1–2, all firewalls and the no-UE5 status are unchanged. |

## 3. Non-blocking note

3.1 **Layer naming.** The AGREED rule has three layers: Natural, Environmental, and **Applied or Acquired**. Pipkin and Cogling list them that way. Saurin shows Applied and Acquired as separate bullets. The content is correct, and separating them is useful for Saurin.

For consistency, label them as the two halves of the third layer, for example "Applied or Acquired — Applied: … / Acquired: …". Also add the Cogling §132 line saying the Skin Appearance Layers are separate from the Character Architecture Layers. This can go in the next patch.

## 4. Completion recommendation

Saurin Part 3 may be accepted by Tyler. Part 4 begins when he says so.
