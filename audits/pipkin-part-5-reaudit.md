# Re-audit: Pipkin v1.0 Part 5 patch

**Auditor:** Claude
**Audited file:** `specs/pipkin/PIPKIN_V1.md` at commit `02e84ad`, with `specs/STATUS.md` at `0214355`
**Responds to:** `audits/pipkin-part-5.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS. Acceptance waits on one decision from Tyler.**

All author-side findings are resolved, and the patch introduces no contradiction or hard dependency. The one remaining item (4a, the brief's movement wording) is correctly left OPEN as Tyler's decision. Part 5 can be marked first-pass accepted once he chooses.

## 2. Verification

| Finding | Result | Basis |
| --- | --- | --- |
| 4a Brief movement conflict | **Correctly escalated, not resolved** | New §37 quotes both brief lines and states the brief is "OPEN and not silently superseded." It lists the three options and selects none. This matches the authority rule. |
| 4b Missing scope | **PASS** | New §38 plans a Part 6 (equipment fit, world compatibility, character-creation integration and the final first-pass review). It covers every item listed in the audit: <ul><li>clothing, armor, helmets and ears, footwear, gloves, belts and backpacks</li><li>collision</li><li>third-person, creator and targeting cameras</li><li>presets</li><li>randomization</li><li>lifecycle</li><li>consolidated OPEN list</li><li>permanent validation</li><li>combined identity</li><li>completion criteria</li></ul> §38 also says Part 6 planning doesn't accept Part 5 or complete Pipkin. `specs/STATUS.md` matches. |
| 4c Equal speed vs caricature | **PASS** | §4 now accepts a biomechanically necessary higher cadence and greater relative stride. It defines caricature as excess cadence, shortened excursion, added bounce or stylization. The equal-speed stress case now checks the walk-run transition. |
| 4d Narrow-base gait | **PASS** | §4 requires an "adult narrow-base gait" in which feet converge toward the line of progression relative to hip width. PIP-MOVE-03, 05 and 07 now check step width, and PIP-MOVE-07 also checks cadence variability. |
| 4e Swimming review reference | **PASS** | §24 now leaves swimming as OPEN gameplay and locomotion decisions and presumes no unlisted review. |
| 4e Sex like-for-like walk comparison | Not added (it was optional) | This can go into Part 6's permanent validation set if wanted. |

## 3. Notes

- The Part 5 status line ("TYLER DECISION PENDING") and STATUS.md are consistent.
- The brief (`rules/character-creation-brief.md`) is unchanged. That's correct until Tyler decides. If he supersedes the wording, the brief should carry a pointer, as with "large head," and the item goes into the terminology review.

## 4. Completion recommendation

1. Tyler chooses one §37 path:
   - supersede the wording,
   - keep it as visual tendency only, or
   - keep selected items as gameplay traits for later review.
2. ChatGPT records the choice in §37.
3. Part 5 is then first-pass accepted.
4. Part 6 begins on Tyler's approval.
