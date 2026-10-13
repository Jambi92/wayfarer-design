# RM-OT-05O blind scorer prompt (revision of tools/rac/w1/rmot05f_drivers/f_scorer_prompt.md; that file stays unchanged)

**Why it is revised (05N §15 / 05O §6).** The revised gate no longer requires scorers to discover a non-human species from a headless body. It asks *why* bodies group and look the way they do.

**What is kept.** Every field of the 05F prompt (class, confidence, drivers, basis, axial_cues, limb_cues, posture_read, groups, nonhuman_groups_distinguishable). That keeps `f_tally.py` usable and the old criteria reportable as provenance.

**What is added.** Per body, a structural description and a rating of the non-structural factors, plus one primary driver. Class C is no longer requested as a goal; the scorer is told that deciding species is not required.

Replace `{GREY}`, `{SIL}` and `{P}`, then give the scorer nothing else: no key, no race names, no previous results. Use one fresh, uninformed scorer per copy, 3 per run.

---

You are an independent visual scorer in a blind body-anatomy study. Use only the two images below (Read tool); do not open any other file or directory.

{GREY} (neutral grey)
{SIL} (same bodies, black silhouette)

Each code ({P}01–{P}12) shows one body, head and neck removed, height-normalized, front view + profile view. The set may contain ordinary humans and bodies of fictional humanoid races; you are not told which or how many. All bodies are upright, two arms, two legs, five digits. You are NOT asked to decide whether any body is non-human; the main task is to describe how each body is built and why bodies look alike or different.

For EVERY code give:
1. class: A = ordinary human-family body variation; B = unusual / extreme human-family body variation (e.g. very obese, very muscular, very thin, unusual proportions but still human); C = distinct humanoid race / species anatomy. (Give your honest best read; it is recorded but is not the goal.)
2. confidence: low / medium / high.
3. drivers: the specific features driving your read.
4. basis (for B or C): the MAIN reason, one of: bulk, fatness, muscularity, thinness, stature, single_feature, organization (how the body is structured: section shapes, joint transitions, load path, segment relations). Use n/a for A.
5. axial_cues: trunk / back / pelvis cues you used (list, may be empty).
6. limb_cues: limb / joint cues you used (list, may be empty).
7. posture_read: true if the body reads as hunched, crouched, bent-kneed or digitigrade, otherwise false.
8. structure: one short phrase each for
   - axial_section_shape (trunk cross-section / chest-to-pelvis organization as seen front and profile),
   - joint_integration (how shoulders, elbows, hips, knees, ankles join the segments),
   - segment_relations (relative lengths / sizes of trunk, legs, arms, hands, feet),
   - load_path (how the weight appears to travel from trunk through pelvis and legs to the feet).
9. non_structural_factors: rate each of posture_pose, limb_bulk, fat, muscularity, boxiness as none / minor / major (how much it drives your read of THIS body), with a few words.
10. primary_driver: the single biggest reason this body looks the way it does, one of: axial_section_shape, joint_integration, segment_relations, load_path, posture_pose, limb_bulk, fat, muscularity, boxiness, stature, other.

Then:
11. groups: groups of codes that look like the same kind of body, each with a short label and stable: true/false.
12. nonhuman_groups_distinguishable: if you see more than one non-human group, can they be told apart without labels? (true / false / null if fewer than two), and what distinguishes them.

Be honest and calibrated; do not assume any particular number of non-human bodies or that any must exist.

Return ONLY this JSON (no prose outside it):

```json
{"bodies": {"{P}01": {"class": "A", "confidence": "high", "drivers": "...", "basis": "n/a", "axial_cues": [], "limb_cues": [], "posture_read": false,
   "structure": {"axial_section_shape": "...", "joint_integration": "...", "segment_relations": "...", "load_path": "..."},
   "non_structural_factors": {"posture_pose": "none", "limb_bulk": "none", "fat": "none", "muscularity": "none", "boxiness": "none", "notes": "..."},
   "primary_driver": "segment_relations"}},
 "groups": [{"label": "...", "codes": ["{P}01"], "stable": true}],
 "nonhuman_groups_distinguishable": null, "distinguishing_features": "..."}
```
