# Saurin TS9 — Pass Toward Tyler's Anatomical Target Reference (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:**
- Tyler's anatomical target reference sheet, 2026-10-02. It is saved as `reviews/images/ts9/tyler_anatomical_target_reference_2026-10-02.png`.
- Tyler's instruction: "use this for reference on the sculpting".

**Status:** DIAGNOSTIC / NOT FINAL.

## Owner direction (recorded for ChatGPT)

The reference contains forms that TS7/TS8 had excluded:
- human-style pectorals with small nipples;
- a segmented rectus abdominis (six-pack) and a narrow waist / V-taper;
- rounded hip masses on either side of the tail root;
- a modest smooth crotch form;
- pads on the sole.

Claude asked how to treat these. **Tyler chose "Follow it literally."** TS9 therefore applies the reference as drawn. **This is an owner decision that overrides the TS7/TS8 directive bans** (TS7 §11/§17, TS8 §8/§18/§21 gates 10–11) for this pass.

No spec text has been changed. If this direction is to become canon, ChatGPT should update the Saurin spec and directives so they agree with it. Until then, this is a conflict between the reference and the TS7/TS8 directives, flagged here for resolution.

## What TS9 is

**Construction.**
- A new module, `RaceBodies/wf_saurin_body9.py`, built on the TS8 signed-distance (code-built) construction.
- It has a slimmer axial core, and **explicit muscle bellies** define the surface over that core. About 45 bellies, each with an origin, a belly and an insertion, separated by creases.
- Head-top height is 188 cm. It is still bare clay: no scales, horns or pigment.

**Systems built from the reference:**

| Region | Construction |
|---|---|
| Neck | Long, slim neck with paired ventral cords and an upper-trapezius slope from the nuchal column to the shoulder |
| Back | Middle/lower trapezius, infraspinatus/teres, latissimus wings (V-taper), erector columns, spinal groove |
| Front torso | Pectorals in three fascicles, small nipples, serratus fingers, external obliques, segmented rectus abdominis with linea alba |
| Shoulder and arm | Three-headed deltoids. Upper arm: biceps, triceps long + lateral heads, brachialis. Forearm: brachioradialis, extensor and flexor groups, wrist tendons |
| Hip | Hip masses flanking the tail root, a tensor, and a modest crotch form |
| Thigh | Rectus femoris, vastus lateralis, vastus medialis teardrop, sartorius, adductors, two hamstrings |
| Lower leg | Two gastrocnemius heads, soleus, tibialis anterior, calcaneal tendon |
| Feet | Long splayed clawed toes, a narrow heel, and toe pads plus a metatarsal pad (sole pads as in the reference) |
| Tail | Thick root between the hip masses; the tail descends to rest along the ground and sweeps to the side, as in the reference |
| Hands | The TS8 hands: knuckles, tendons, claw beds, claws |

## Deliverables

All files are in `reviews/images/ts9/`.

| File | Content |
|---|---|
| `ts9_reference_vs_ts9.jpg` | **The reference's five views against TS9's same five views** |
| `ts9a_complete.jpg` | Front, profile, rear, front 3/4, rear 3/4 |
| `ts9a_marchfolk_comparison.jpg` | Marchfolk 173 cm, true scale |
| `ts9b_neck_shoulder_thorax.jpg` | Head–neck–shoulder transition, girdle, thoracic shell / axial trunk |
| `ts9c_pelvis_hip_tailroot.jpg` | Pelvis–sacrum–tail root integration, upper leg and hip joint |
| `ts9d_limbs_hand_foot.jpg` | Elbow, knee, ankle, hand, foot |

**On Tyler's PC (`RaceBodies/out/`):**
- `SaurinTS9_bare_3_5mm.blend` / `.fbx`: a static, unrigged mesh. **Usable as a sculpt base.**
- `saurin_ts9_body.npz`: the full 1.5 mm surface.

## Honest comparison with the reference

**Matched:**
- overall lean, long-limbed, upright build;
- muscle-group layout front and back;
- V-taper with a narrow waist;
- pectoral, abdominal and oblique organization;
- tail root between the hip masses;
- descending, laterally sweeping tail;
- long clawed toes with pads.

**Not matched.** This is the ceiling of the code-built method.
1. **Surface fidelity.**
   - The reference is hand-sculpted. Its muscles flow into each other with fascia, tendon sheets and striation.
   - TS9 bellies are smooth and still read as distinct pieces. Their starts and ends are rounded, which is most visible on the back (scapular group) and the upper-thigh rods.
2. **Proportions.**
   - The reference has heavier thighs and calves (a strong calf diamond).
   - Its neck is slimmer with more pronounced cords, and its joints are more articulated.
   - TS9's legs are leaner and more column-like. Knee and ankle transitions are simpler.
3. **Feet.** The reference foot is a more developed reptilian foot: raised arch, heavier toe segments, larger claws. TS9's foot is lower and flatter.
4. **Hands and forearms.** The reference has more tendon definition and longer, heavier fingers.
5. **Small artifacts.**
   - The tensor/rectus-femoris origins form a small vertical knob at the front of each hip.
   - Serratus fingers read slightly blocky in close-up.

## Recommendation

The structural direction now has a clear visual target. Further code-built iteration has diminishing returns for this level of anatomical definition. The efficient next step is:
1. Use **`SaurinTS9_bare_3_5mm`** (or TS8, if the TS7/TS8 rules are kept) as the **base mesh for a hand-sculpt pass** in Blender sculpt mode or ZBrush, with the reference sheet as the target. Tyler chose this route earlier.
2. ChatGPT to reconcile the TS7/TS8 directives and the Saurin spec with Tyler's "follow the reference literally" decision before any surface work (Regional Scale Architecture) is restored.

No spec text was changed. No UE5 implementation.

— Claude
