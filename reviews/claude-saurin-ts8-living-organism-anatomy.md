# Saurin TS8 — Living-Organism Anatomy (DIAGNOSTIC / NOT FINAL)

**Author:** Claude
**Responds to:** `reviews/saurin-ts8-living-organism-anatomy-directive.md`
**Status:** DIAGNOSTIC / NOT FINAL. TS8 is **not** declared successful (directive §20). Several acceptance gates are only partly met; see §H.

## What TS8 is

TS8 is built on the TS7 clean-sheet signed-distance body (`RaceBodies/wf_saurin_body8.py`).
- No human or MPFB geometry is used.
- The head is the accepted TS6.1 head.
- It is one neutral adult.
- It is bare clay: no scales, horns, pigment, sex anatomy or dramatic pose/lighting.
- Head-top height is now **188.0 cm**, corrected from 186.7 in TS7.

TS8 adds **secondary anatomical architecture** to every system. Each piece is an explicit, named structure in the source.

A first TS8 attempt added these structures as separate volumes. It visibly failed the "assembled reptile parts" test (scapular domes, strut-like slings, knobs at the hips), so it was rebuilt. In the rebuild, secondary structures are mainly built as **planes, ridges and steps on the body surface**, or as masses seated inside the body shell. Only where the anatomy truly projects do they stand out.

| System | TS8 construction |
|---|---|
| **Cervical** | <ul><li>Dorsal cervical epaxial mass: a broad paired column from the occiput, spreading between the scapulae. In profile the back of the neck is a sloping wedge that supports the head.</li><li>Lateral cervical planes.</li><li>Ventral throat architecture: a hyoid/gular body, a low transverse gular fold, and a ventrolateral cervical band from the jaw angle to the sternal/shoulder root.</li><li>Cervicothoracic expansion: the neck widens from about 13.6 to 24 cm toward the inlet.</li></ul> |
| **Shoulder girdle** | <ul><li>No ball sockets.</li><li>The scapular plate is a flat blade raised on the dorsolateral rib field. It has a vertebral-border ridge and an oblique scapular-spine ridge running toward the acromion.</li><li>A deltoid-equivalent cap in two heads runs along the humerus to a deltoid insertion, so the mass follows the joint.</li><li>A low coracoid-pectoral plane sits at the front.</li><li>The shoulder joint moves inward (X 17.0 → 15.8) so it sits inside the thoracic outline.</li></ul> |
| **Thoracic shell** | <ul><li>Rounded-hexagonal rib volume (stronger chamfers than TS7), deepest at about U 138.</li><li>A narrow keeled sternal plate.</li><li>Oblique costal bands on the lateral and ventrolateral shell only.</li><li>A costal margin that is a structural step: the thorax slightly overhangs the lower trunk.</li></ul> |
| **Lower axial trunk** | <ul><li>Dorsal axial columns on either side of a vertebral groove.</li><li>An oblique flank line running from the costal margin to the iliac blade.</li><li>A ventral abdominal plate, with its edge where the flank meets it.</li><li>The torso narrows by redistributing depth and planes, not by a waist pinch.</li></ul> |
| **Pelvis / sacrum / femur** | <ul><li>A long front-to-back reptilian **iliac blade** ridge.</li><li>A lateral acetabular plane.</li><li>**Iliofemoral** and **puboischiofemoral** fans that the thigh grows out of.</li><li>A closed, non-sexual **ventral pelvic plate**.</li><li>A sacral platform.</li><li>**Caudofemoral strap + web** from the caudal base to the posterior femur.</li><li>No gluteal lobes and no cleft.</li></ul> |
| **Tail root / tail** | <ul><li>The **dorsal epaxial columns continue from the back onto the tail**, with a vertebral groove between them.</li><li>A **horizontal septum** line runs along each side: the epaxial/hypaxial boundary at the transverse processes.</li><li>A ventral haemal midline.</li><li>A low segmental rhythm, strengthening distally (articulated tail).</li><li>The path is unchanged: sacral origin → posterior projection → lateral/caudal sweep.</li></ul> |
| **Arms** | <ul><li>Lateral and medial epicondyles and an olecranon point.</li><li>An ulnar border.</li><li>Extensor and flexor fields that narrow into **wrist tendon paths** over the distal third.</li><li>Brachial flexor and extensor fields.</li></ul> |
| **Legs** | <ul><li>Iliotibial, femorotibial and puboischiotibial thigh fields.</li><li>Condylar flats and a patellar plate, with a **patellar tendon** to the tibial tuberosity.</li><li>A crural flexor mass that narrows into a **calcaneal tendon** running to the heel.</li><li>A tibial-crest plane and malleoli.</li></ul> |
| **Hands** | <ul><li>Dorsal knuckles and extensor tendons over the back of the hand.</li><li>Thenar and hypothenar palm planes.</li><li>**Claw beds** (ungual sheaths) before modest claws.</li><li>Five digits and an opposable thumb.</li></ul> |
| **Feet (redesign)** | <ul><li>A broad load-bearing heel pad.</li><li>A tarsal block with a distinct ankle transition.</li><li>**Five metatarsals fanning across a structural midfoot**, visible on the dorsum.</li><li>A flat plantar contact field.</li><li>Long articulated toes with stronger joints. Toe IV is the longest (a reptilian, not human, formula).</li><li>Modest claws on the toe axes.</li><li>Plantigrade: not digitigrade, raptor-like or pawed.</li></ul> |

## Deliverables

All files are in `reviews/images/ts8/`.

| Item | File |
|---|---|
| TS8-A complete neutral adult: front, profile, rear, front 3/4, rear 3/4 | `ts8a_complete.jpg` |
| TS8-A Marchfolk 173 cm reference, true scale | `ts8a_marchfolk_comparison.jpg` |
| TS8-B cervical (5 angles), shoulder girdle (6), thoracic shell (4) | `ts8b_thorax_shoulder_cervical.jpg` |
| TS8-C pelvis/sacrum/tail root (rear, rear 3/4, side, front 3/4, front) and pelvis → femur (3) | `ts8c_pelvis_femur_tailroot.jpg` |
| TS8-D elbow, knee, ankle, hand, foot (load-path construction) | `ts8d_limbs_hand_foot.jpg` |
| TS8-E **torso-only identity test**: shoulders → upper thighs; head, neck, hands, feet and tail beyond its base are removed from the mesh | `ts8e_torso_only.jpg` |
| TS8-F pure silhouettes: front, profile, rear, normalized Marchfolk M / Saurin / Marchfolk F, torso-only | `ts8f_silhouettes.jpg` |
| TS8-F tail-front (SAU-SILHOUETTE) and tail-root rear silhouettes | `ts8f_tail_silhouettes.jpg` |
| TS8-G anatomy chain: 11 constructed systems, colored from the construction, with load paths | `ts8g_anatomy_chain.jpg` |

**Note on TS8-E.** The torso crop cuts the mesh, so the cut tail base shows as an open cross-section in the rear views. That opening is an artifact of the test, not anatomy.

**Files on Tyler's PC** (`RaceBodies/out/`):
- `SaurinTS8_bare_3_5mm.blend` / `.fbx`: a static mesh, not rigged.
- `saurin_ts8_body.npz`: the full 1.5 mm surface, about 2.8 M triangles.

## H. Failure analysis (directive §20 TS8-H)

### What still reads human
- **Front torso-only view.** From the front, the paired thigh roots meet the ventral pelvic plate in a V that recalls a human groin line, though there is no human pelvis or genital form.
- **Arms.** The overall arm silhouette, an upper arm and forearm hanging in an A-pose, is still generic-humanoid. The parts read anatomical but not distinctly Saurin.
- **Shoulder corners from the front.** The deltoid-equivalent cap still makes a rounded shoulder corner. It is no longer a ball on a box, but its front-view rhythm is close to a lean human shoulder.

### What still reads mechanically implausible
- **Tail base from straight rear.** It still reads partly as a large round section emerging from the sacral platform. The epaxial columns and septum help in profile and rear 3/4, but the straight rear lacks a flattened sacral-to-caudal transition.
- **Foot.** It is long and very low. The metatarsal fan and heel pad are present, but the midfoot has little vertical structure, and the malleoli read as small knobs.
- **Neck/head junction from the front.** The neck is still a tall column under a narrower head. In profile it is now a supporting wedge, which meets the directive's profile requirement.

### What remains too geometric
- **Costal margin and ventral plate edges.** They read as crisp, designed lines (the TS8-E front view) rather than soft anatomical transitions.
- **Dorsal vertebral groove.** It is very straight and uniform from neck to sacrum.
- **Limb segments.** They are still fairly uniform planar extrusions between joints. The muscle fields are present but weak at full-body distance.

### What is deliberately unresolved
- **Sex-related Saurin anatomy.** It is neutral and non-sexual. There is a closed ventral pelvic plate and no dimorphism (directive §18).
- **Body-composition variation.** Lean neutral only.
- **Tail phenotype variants.** The neutral tail only.
- **Rigging and joint deformation.** The mesh is static.
- **Display structures.** Not shown.
- **Exact skeletal anatomy.** Vertebral counts and rib counts are not modelled; only their surface consequences are.

### What must be fixed before Regional Scale Architecture returns
1. Straight-rear tail base: a broader, flatter sacral-to-caudal fairing.
2. Front shoulder rhythm: a scapular/girdle silhouette that is less human at the shoulder corner.
3. Softer, more biological costal and ventral-plate transitions, so that they are anatomy and not drawn lines.
4. Foot midfoot and ankle volume: a structural arch and less knobby malleoli.
5. Limb plane hierarchy strong enough to read at full-body distance.
6. Neck width-to-head relationship from the front.

## Acceptance gates (§21), honest

| # | Gate | Result |
|---|---|---|
| 1 | Neck not a cylinder/tower | **Partial.** Profile passes (sloping epaxial wedge supports the head). The front still reads as a tall column. |
| 2 | Shoulders not balls on a box | **Mostly.** No ball sockets; the scapular plate and deltoid cap follow the joint. The front corner rhythm is still close to human. |
| 3 | Thorax is a biological shell | **Partial.** Profile and 3/4 show rib-field volume and the costal step. The front is still too flat. |
| 4 | Lower trunk has anatomy, no human waist | **Pass.** Flank and ventral plates, dorsal columns, no pinch. |
| 5 | Pelvis, sacrum, femora and tail form one mechanical system | **Partial.** Side and rear 3/4 read coherent (fans, caudofemoral strap, epaxial continuity). The straight rear is weaker. |
| 6 | Tail root not an attached wedge | **Partial.** Better articulated. The straight rear still has a round-section read. |
| 7 | Limbs have segment/joint/tendon architecture | **Partial.** Tendons, condyles and epicondyles are present but subtle at full-body distance. |
| 8 | Hands non-human yet functional | **Pass (provisional).** |
| 9 | Feet non-human, plantigrade, mechanically credible | **Partial.** The redesign is in place; the midfoot volume is thin. |
| 10 | No human buttocks/cleft | **Pass.** |
| 11 | No human sexual dimorphism | **Pass.** |
| 12 | Torso-only test reads Saurin | **Partial.** It does not read human: no pectorals, waist, navel or gluteal forms; it has dorsal columns and a scapular plate. It does not yet read convincingly as a *living* Saurin. It reads as a constructed anatomical study. |
| 13 | Silhouette differs for anatomical reasons | **Pass.** At normalized height the trunk, pelvis and limb silhouette differ from both Marchfolk sexes because of the axial and pelvic construction. Nothing decorative causes it. |
| 14 | Bare clay convincing without scales | **Partial.** |
| 15 | One evolved/developed body, not assembled parts | **Partial.** Much better than the first TS8 attempt (no attached parts). The procedural construction still shows in edge crispness and uniform segments. |

**Recommendation.** Do not proceed to surface treatment. The next pass should target the six items listed above under "What must be fixed before Regional Scale Architecture returns".

**Remaining limit of this method.** Procedural construction is now limiting the "living" quality, mainly the crisp lines and uniform segments. A hand-sculpt refinement pass on the TS8 mesh would be the efficient way to soften transitions while keeping the anatomy. That pass would be in Blender or ZBrush, which Tyler chose earlier for the Saurin.

No spec text was changed. No UE5 implementation.

— Claude
