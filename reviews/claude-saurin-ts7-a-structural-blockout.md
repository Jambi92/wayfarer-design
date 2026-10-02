# Saurin TS7-A — Clean-Sheet Structural Blockout (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-ts7-clean-sheet-body-reconstruction-directive.md`
**Status:** DIAGNOSTIC / NOT FINAL. This is the first TS7 bare-clay blockout, returned for Tyler / ChatGPT structural review. Nothing is declared final.

## Confirmation (directive §26)

The human-derived Saurin body foundation is **retired** for anatomical design purposes.
- The TS7 body contains **no MPFB / Marchfolk / human geometry**: no base mesh, no morph targets, no human topology, no human proportions as source.
- It is built directly from the Saurin requirements as a signed-distance construction. This is the same method that produced the accepted TS6/TS6.1 head.
- Source: `RaceBodies/wf_saurin_body7.py`. Every structural system there is an explicit, named anatomical part.

**Uses of Marchfolk.** It appears only as the 173 cm scale/height reference (TS7-A 1, TS7-D) and is never a geometry source.

**The one carried-over element** is the accepted TS6.1 cranium. Per §21 it is used unchanged and joined to the new cervical column.

**What TS7 does not use:**
- scales, horns or displays;
- pigmentation or clothing;
- genital or breast anatomy;
- dramatic lighting or pose.

It is one neutral adult Saurin (§17). No sex variants were made.

## Deliverables

All files are in `reviews/images/ts7-a/`.

| Directive item | File |
|---|---|
| TS7-A 1: Marchfolk 173 cm comparison (true scale) | `ts7a_marchfolk_comparison.jpg` |
| TS7-A 2–6: front, profile, rear, front 3/4, rear 3/4 (bare clay) | `ts7a_blockout.jpg` |
| TS7-B 1–4: skull/neck/thorax, shoulder girdle, thoracic shell, lower axial trunk | `ts7b_closeups_1.jpg` |
| TS7-B 5–8: pelvis/sacrum/tail root, pelvis/femur, hand, foot | `ts7b_closeups_2.jpg` |
| TS7-C: anatomy-chain sheet | `ts7c_anatomy_chain.jpg` |
| TS7-D: front, profile and rear silhouettes; normalized-height comparison with Marchfolk | `ts7d_silhouettes.jpg` |
| TS7-D: tail-front silhouette (SAU-SILHOUETTE) and tail-root rear silhouette | `ts7d_tail_silhouettes.jpg` |

**How the chain sheet is coloured.** Each vertex takes the colour of the structural system whose generating primitive is nearest to it. The colouring is therefore read from the construction, not painted.

**Files on Tyler's PC** (`RaceBodies/out/`):
- `SaurinTS7A_bare.blend` and `SaurinTS7A_bare.fbx`: a static mesh, about 2.9 M triangles at 1.5 mm resolution. It is not rigged.
- `saurin_ts7_body.npz`

## How the body is constructed (§3 chain)

1. **Cervical system.**
   - The neck is a planar column. It has dorsal (nuchal), lateral and ventral (throat) planes, not a round tube.
   - It rises from the thoracic inlet and runs straight up into the TS6.1 occipital, nuchal and gular masses, so skull → neck reads as one structure.
   - The paired dorsal epaxial columns continue from the neck down the whole back.
   - A ventrolateral cervical band runs from the jaw angle to the sternal/shoulder root.
2. **Thoracic shell.** It is deeper than wide, about 27 cm deep and 28 cm wide.
   - A narrower ventral sternal plate is bounded by ventrolateral transition planes, with a faint median line.
   - There is no pectoral organization: no pec masses and no nipple sites.
   - A low oblique rib field sits on the lateral planes.
   - An oblique costal-margin transition marks thorax → lower trunk.
3. **Elongated lower axial trunk** (about U 100–126 cm).
   - The cross-section changes, but there is no hourglass. The torso is a spindle that is widest at the costal margin and does not pinch at the waist.
   - It has its own dorsal, lateral and ventral planes. There is no navel and no human abdominal rectus.
4. **Pelvis / sacral complex.**
   - It is long front-to-back.
   - A dorsal sacral platform rises into the caudal base.
   - There is a lateral iliofemoral mass, and a ventral caudal-pelvic mass under the tail root.
5. **Posterior pelvic system (§11).** There are no gluteal lobes and no cleft. Hip extension is carried instead by **caudofemoral bands**, which run from the caudal base down and forward into the posterior femur (the reptilian tail-driven hip extensor). This is positive anatomy that ties tail, pelvis and thigh into one load path.
6. **Tail.**
   - The proximal caudal mass starts inside the sacral platform. Its base is about 19 × 21 cm, wider and taller than any previous version.
   - The resting path is: sacral origin → near-level posterior projection → controlled lateral/caudal sweep (about 30°).
   - The tail is about 134 cm long. Its sections are planar, with a low dorsal axial line.
7. **Shoulder girdle.**
   - The scapular field lies on the dorsolateral thoracic shell as a surface plane with a vertebral-border ridge.
   - A rounded shoulder root holds the humeral head.
   - A low coracoid-pectoral fan runs to the humerus, and a broad cervico-scapular fill sits in place of a clavicle-dominant shelf.
8. **Limbs.**
   - Each limb is a planar segment, not a round tube.
   - Muscle fields follow reptilian groupings:
     - Thigh: iliotibial, femorotibial and puboischiotibial.
     - Shank: a crural flexor mass and an anterior tibial plane.
     - Forearm: extensor and flexor fields either side of the ulnar border.
     - Upper arm: brachial flexor and extensor fields.
9. **Hands.** Five digits with an opposable thumb. Fingers are moderately elongated with tapered distal phalanges, and restrained claws continue the digit axis.
10. **Feet.** Plantigrade, with a flat plantar contact and a long forefoot. There are five toes, and digit IV is the longest (a reptilian toe formula, not the human one). Toes taper, with restrained claws.

**Reference measurements:**
- Head-top height 186.7 cm. That is 1.3 cm under the 188 cm target, a placement detail fixed by raising the atlas next pass.
- Crotch about 84 cm.
- Shoulder joints at about 152 cm.

## Negative tests (§23), honest

| Fails if… | Result | Notes |
|---|---|---|
| head and tail removed, torso looks like an ordinary human | **Pass** | There are no pectorals, waist, navel, human ribcage silhouette or human shoulder slope. The torso is a deep planar column (normalized-height silhouette vs Marchfolk in TS7-D). |
| pelvis recognizably human with a tail attached | **Pass / watch** | The pelvis is long and posterior-weighted, with an iliofemoral mass. From straight front, the groin boundary at the top of the thighs still forms a V. |
| human gluteal cleft remains | **Pass** | There is no cleft and there are no gluteal hemispheres. |
| breasts / human sex traits define the neutral body | **Pass** | None are present. |
| neck remains a human cylinder | **Partial** | The neck is planar and continuous with the occiput, so it is not a human neck. From the front, though, it reads as a long, nearly uniform column ("periscope"). It needs more differentiation of the throat, cervical mass and inlet, and possibly a shorter visible length. |
| shoulder girdle visibly copied from human | **Partial** | It is not copied. However, the shoulder roots read as rounded caps, and the coracoid-pectoral fan seen from the front can suggest a clavicle V. |
| chest = human pectorals/ribcage with grooves | **Pass** | It is a sternal plate with transition planes and no pectoral masses. |
| waist = human hourglass by default | **Pass** | It is a spindle with no pinch. |
| tail root looks glued on | **Partial** | In profile the dorsal line flows from the back into the tail. From the rear and rear 3/4, the base still reads partly as a large tube issuing from the sacral platform. Next step: a flatter, broader sacral-caudal fairing. In rear 3/4 the caudofemoral bands show as rounded forms beside the tail base; they should read as diagonal bands, not lobes. |
| front tail silhouette resembles genitals | **Pass** | Straight front shows the tail only as a lateral sweep beside the leg (`ts7d_tail_silhouettes.jpg`). |
| limbs = human limbs with claws | **Partial / weak** | The limbs are no longer human surface anatomy, but they are still fairly generic, smooth, long segments. The thigh and shank fields are subtle at full-body distance. |
| reptilian identity depends on scales/horns | **Pass** | None are used. |
| structural difference only from muscularity | **Pass** | The build is lean and neutral. The difference comes from proportions, sections and the chain. |
| angularity becomes fantasy armour | **Pass** | Planes and transitions are soft. There are no plates, blades or spikes. |
| upright bipedal function sacrificed | **Pass** | It stands as an upright plantigrade biped with knees and elbows aligned. |

## Positive test (§24), honest answer

**Featureless clay test:** does it read as one upright reptilian organism whose head, neck, thorax, trunk, pelvis, legs and tail developed together?
- **Mostly yes for the axial chain.** Head → cervical column → deep thorax → long trunk → sacral platform → tail now reads as one continuous system (see the chain sheet).
- **Not yet for the limbs and girdle.** They are coherent but generic, and they don't carry the same design language as strongly.

**Could it be mistaken for Marchfolk with phenotype removed?** No. The silhouette, sections and proportions are clearly different at normalized height.

**Known limits of this blockout:**
- It is a procedural construction, and some transitions look synthetic and mannequin-smooth.
- The neck reads long from the front.
- The feet read thin and flat.
- It is a static mesh with no rig yet.

These are structural notes for the next TS7 iteration, not surface work.

## Proposed next TS7 iteration (after review)

1. Cervical differentiation: a throat/gular field, a broader lateral cervical mass toward the inlet, and possibly about 3–4 cm less visible neck.
2. Sacral-caudal fairing, so the tail base grows out of a broad, flatter sacral plate in rear view.
3. Caudofemoral bands that read as diagonal straps, not rounded forms.
4. Girdle: a less ball-like shoulder root, and a scapular field with more presence in profile.
5. Limb plane hierarchy strong enough to read at full-body distance.
6. Fuller tarsal/forefoot mass.
7. Raise the atlas 1.3 cm to reach 188.0 cm.

No spec text was changed. No surface, scales, displays or sex variation were added. There is no UE5 implementation.

— Claude
