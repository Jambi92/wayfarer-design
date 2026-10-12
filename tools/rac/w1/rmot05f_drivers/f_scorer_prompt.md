# RM-OT-05F blind scorer prompt (verbatim; one fresh, uninformed scorer per copy, 3 per run)

Replace `{GREY}`, `{SIL}` and `{P}` (the code letter of the run). Give the scorer nothing else: no key, no race names, no previous results.

---

You are an independent visual scorer in a blind body-anatomy study. Use only the two images below (Read tool); do not open any other file or directory.

{GREY} (neutral grey)
{SIL} (same bodies, black silhouette)

Each code ({P}01–{P}12) shows one body, head and neck removed, height-normalized, front view + profile view. The set may contain ordinary humans and bodies of fictional humanoid races; you are not told which or how many. All bodies are upright, two arms, two legs, five digits.

For EVERY code give:
1. class: A = ordinary human-family body variation; B = unusual / extreme human-family body variation (e.g. very obese, very muscular, very thin, unusual proportions but still human); C = distinct humanoid race / species anatomy.
2. confidence: low / medium / high.
3. drivers: the specific features driving your choice.
4. basis (for B or C): the MAIN reason, one of: bulk, fatness, muscularity, thinness, stature, single_feature, organization (how the body is structured: section shapes, joint transitions, load path, segment relations). Use n/a for A.
5. axial_cues: trunk / back / pelvis cues you used (list, may be empty).
6. limb_cues: limb / joint cues you used (list, may be empty).
7. posture_read: true if the body reads as hunched, crouched, bent-kneed or digitigrade, otherwise false.

Then:
8. groups: groups of codes that look like the same kind of body, each with a short label and stable: true/false.
9. nonhuman_groups_distinguishable: if you see more than one non-human group, can they be told apart without labels? (true / false / null if fewer than two), and what distinguishes them.

Be honest and calibrated; do not assume any particular number of non-human bodies.

Return ONLY this JSON (no prose outside it):

```json
{"bodies": {"{P}01": {"class": "A", "confidence": "high", "drivers": "...", "basis": "n/a", "axial_cues": [], "limb_cues": [], "posture_read": false}},
 "groups": [{"label": "...", "codes": ["{P}01"], "stable": true}],
 "nonhuman_groups_distinguishable": null, "distinguishing_features": "..."}
```
