# Validation-only LOW-muscularity derivative — pre-registration draft (RM-OT-05W §6)

**Status: DRAFT method.** It is frozen, with any amendments, only after a new source passes the whole-body source gate and before any LOW is built or scored.

**What it is (order §6):** a test object made **only** to check whether Gorrund structural identity persists at lower muscularity in the blind gate (criteria C1 and C5-LOW).

**What it is not:**
- not an ARM;
- not a scaffold;
- not a creator asset;
- not a canonical composition variant (RA §5 composition variants still need ARM acceptance first).

## 1. What must be held

| Held | How it is checked |
|---|---|
| Same individual: same source master, same skeleton reading, same pose | The LOW is derived from the accepted source working copy; never a new generation of a different creature (order §6) |
| Skeletal landmarks: clavicles, acromia, sternum, costal margin, iliac crest / ASIS, sacrum, greater trochanter, patella, tibial crest, malleoli, elbow and wrist bony points | Landmark positions within a declared tolerance (proposed 0.5 cm), reported per landmark |
| Stature, segment lengths, joint centres, hand and foot skeleton | Unchanged; reported |
| Head, tail and feet | Unchanged (excluded from the edit) |

## 2. What may change

Only the **muscle soft-tissue layer**, reduced toward a low Current Muscularity. Specifically:
- belly convexity of the major muscle groups: deltoid, pectoral, trapezius, latissimus, biceps / triceps, forearm mass, gluteal, quadriceps, hamstrings, calf;
- regional definition, reduced in the same direction.

Fat stays at reference. Distribution stays neutral (RA R-4).

## 3. Candidate methods (one is chosen and frozen at the time; all builder choices disclosed per R-14)

1. **Sculptor-made LOW.** The same sculptor or service revises the accepted source under this spec. This is preferred: it is real sculpting, not a procedure.
2. **Local soft-tissue deflation on the accepted source.**
   - A per-region inward displacement along normals, limited to the listed muscle zones and capped (proposed 1.0–1.5 cm).
   - Landmark-locked, with no global smoothing, no remesh and no Dyntopo.
   - A blend band at each zone border.
   - This is allowed only if the source gate judged the surface good enough for local work (Q4). It must not flatten bony landmarks or erase joint structure.
3. **Second generation conditioned on the accepted source.** For example, a Rodin run from a lower-muscle version of the *same* concept image. Allowed only if it reproduces the same individual. Shown side by side; rejected if the skeleton or proportions drift.

## 4. Disqualifiers (the LOW is not used, and a capability dependency is reported)

- It looks like a different creature or a different skeleton.
- Structure is erased: smoothing that removes landmarks or joint form (order §6).
- It reads as "thin / starved" rather than low-muscle.
- Its tiles fail `w_tile_check.py`.

**If no credible LOW can be made,** that is reported as a **capability dependency**. It is not run as an impossible gate, and it is not treated as evidence against canon (order §6).
