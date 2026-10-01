# Re-audit Request — Cogling Part 4

**Spec:** `specs/cogling/COGLING_V1.md`
**Patch:** `e165c35f3ec6b49873796447a7ae3e7eea00cbd4`
**Prior audit:** `audits/cogling-part-4.md`

Please re-audit Part 4 against the prior findings.

Changes:
- 4a: FD domains are now explicitly facial-analysis only and use the AGREED meanings. Whole-body surface now uses the AGREED Skin Appearance Layers: Natural, Environmental, Applied or Acquired.
- This also corrects the lingering Part 3 FD wording differences: FD-SURF includes scars where appropriate; FD-OBS is lighting, camera, expression and pose.
- 4b: added functional adult humanoid dentition baseline, no diet inferred, with explicit anti-child/rodent/oversized/tiny-pointed caricature rules; count/replacement/maturation/wear remain OPEN.
- 4c: body hair is no longer declared independent of sex-related anatomy; any sex-related/hormonal distributions remain OPEN and must use soft correlations rather than hard dependencies.
- 4d: interim preset/randomization/validation sampling weights are explicitly testing distributions, not approved Cogling population distributions.

If clean, state **PASS** and whether Part 4 may be FIRST-PASS ACCEPTED.

Write to `audits/cogling-part-4-reaudit.md`.
Do not edit the spec or begin Part 5.
