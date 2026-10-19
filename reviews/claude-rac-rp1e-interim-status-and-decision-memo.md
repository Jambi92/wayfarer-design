# RAC RP1E Gorrund — interim status and decision memo (Claude, 2026-10-19)

This is not the RP1E gate. RP1E is still in progress. It records where the recovery stands so ChatGPT/Tyler can decide early whether the remaining scope is acceptable as framed.

Order: `reviews/chatgpt-rac-rp1e-gorrund-contact-zone-recovery-order.md`.
Progress log with all numbers and methods: `reviews/rac-rp1e-evidence/RP1E_progress.md`.

## 1. Done (authored in the Blender UI on Tyler's PC, verified in the cloud)
- **Hands:** both rebuilt as isolated manual sub-cages: palm rings, 5 digit tubes, webs at the measured cleft tops.
- **Axillae:** coarse cage re-laid out (136 vertices moved). Coarse-cage axilla intersections 32 → 0.
- **Feet:** both rebuilt as sub-cages (shin ring → 5 sections → toe cap → 4 toe tubes; the source has 4 free toes, the fifth is fused). Current file `GO_U_REF_RP1E_retopo_v006.blend`:
  - 2096 V / 2094 quads, closed, 0 non-manifold, genus 0;
  - **0 coarse self-intersections**;
  - identical to the frozen foot design (max 0.08 mm).

## 2. Measured state of the whole body (cloud simulation of the v006 cage)
Stack: per-colour ownership targets, Subdivision → Nearest → 2 × [Smooth → Nearest]; final level Project ± 2 cm + Nearest (feet Nearest + Smooth).

Self-intersecting face pairs:

| Zone | L1 | L2 | L3 | L4 (earlier full run) |
|---|---|---|---|---|
| axillae | 42 | 262 | 2278 | 9596 |
| head (ears, jaw) | 28 | 130 | 1393 | 3373 |
| perineum | 0 | 0 | 27 | 306 |
| feet | 0 | 7 | 61 | 358 (design sim) |
| hands | – | – | ≈ 270 * | 270–550 |

\* Provisional hand colours (the digit segmentation must be regenerated).

Deviation at L3, source → result (median / p95 / max mm, share over the max):
- general: 0.07 / 0.89 / 33.8, 2.0 % over 3 mm;
- head/muzzle/ears: 0.10 / 13.9 / 37.9, **12.2 % over 1.5 mm**;
- hands: 0.6–1.6 % over;
- feet: 1.9 % over;
- tail root: 0 %.

## 3. What is still missing — source features the cage does not represent at all
| Feature | Source geometry | Current deviation | Needed |
|---|---|---|---|
| **Ears** (identity zone) | Detailed pinna: thin helix blade (≈ 1 cm thick, rising to z 204.5 and folding forward), antihelix ridges, concha pocket ≈ 2.4–4 cm deep hidden under the helix | median 15–19 mm; 61 % of the head's over-limit points | full ear sub-cage per side: base ring → back of pinna → helix rim → dish → concha floor (≈ 100–150 cage verts per ear) |
| **Jaw underside / chin–chest** (identity zone) | Skin-fold pocket under the jaw on both sides, ≈ 1.5 cm deep | median 7–8 mm; 31 % of the head's over-limit points | jaw-line pocket loops |
| **Pouch** | Thin belly flap at z ≈ 99–100 over a pocket | median 12.6 mm, p95 30 mm | pocket invagination under the flap |
| **Axilla front slits** | 1–2 mm pocket, top crease z 141 (back) → 154 (front) | median 10–12 mm; also most of the remaining self-intersections | arm/trunk junction loop on the crease plus explicit slit walls on both sheets |
| Muzzle front, nostrils | Small concavities | 2–4 mm | local loops |

Prototype evidence:
- One cloud-designed concha pocket (an inset plus 3 rings) lowers the L-ear over-limit share from 19.1 % to 9.6 % with 0 coarse self-intersections. The rest of that ear's miss is the uncovered helix blade.
- Generic automatic pocket and patch generators failed: they add 8–148 coarse self-intersections because the coarse head cage has no clean loop around the ear. The ears need hand-designed sub-cages, like the hands and feet.

## 4. Risk to the final gate
- **Self-intersections must be 0 at the final level, in every zone.** Even the zones that already have dedicated sub-cages still fold at L4: feet 358, in plantar web clefts with 0.8–3.6 mm source gaps; hands 270–550.
  - Contact gaps of 0.8–2 mm (toe webs, finger webs, the axilla slit) are at or below the L4 face size, about 1.5–3 mm.
  - The R middle/ring distal phalanges are fused in the source; separated, they leave about 1.2–1.8 mm at the bridge.
  - Reaching exactly 0 in every cleft, slit and pocket has **not been demonstrated anywhere** in RP1/RP1E.
- **Ears to T-2 max 1.5 mm** needs artist-level pinna topology, entered by numeric vertex typing in the UI (about 25 key presses per vertex). This is feasible but slow, and its success is not yet demonstrated.
- **Rough remaining effort under the current rules:**
  - design: ears 2 × (4–8 h), jaw 2–3 h, pouch 2–4 h, axilla slits 4–6 h;
  - UI authoring: about 400–600 more vertices;
  - then hand-colour regeneration, the progressive L1–L4 gates, nails, landmarks, silhouettes and the gate sheets;
  - several more long sessions, with real risk of ending at the stop rule anyway.

## 5. Decisions the author may want to take now (Claude takes none of them; the work continues as ordered meanwhile)
1. **Continue as ordered.** Claude proceeds feature by feature: ears → jaw → pouch → axilla slits → hands/feet L4 residuals → gates. Expect several more sessions; the outcome may still be the stop-rule verdict.
2. **Contact/cavity scope ruling.** State whether non-visible interior surfaces count for T-1/T-2 and self-intersection:
   - the axilla slit walls;
   - the concha floor under the helix;
   - the pouch interior;
   - sub-mm toe/finger web floors.

   For example, exempt them as listed micro-detail, or measure self-intersection only above a stated gap. This is a contract decision; Claude will not assume it.
3. **Transcription ruling.** Every RP1E sub-cage so far (hands, feet) was designed vertex-by-vertex in the cloud, then transcribed by hand in the Blender UI by typing each coordinate in the N panel. The topology and positions are authored by Claude, not by a remesher.
   - Could cloud-designed sub-cage patches instead be brought into the PC file through the Blender UI: File → Import, join, then merge the boundary vertices? The result would be identical, and the UI still does the stitching and checks.
   - This would cut UI time by about 10× for the ears, jaw and pouch.
   - The current rule ("final shape authoring in the Blender UI only; cloud scripts only for prep, diagnostics, masks, repair and evidence") reads as forbidding it, so Claude keeps typing unless told otherwise.
4. **Stop now** with "RP1E MANUAL CONTACT-ZONE RECOVERY FAILED / AUTHOR DECISION REQUIRED", using this memo as the evidence base.

Current default: option 1, continuing.
