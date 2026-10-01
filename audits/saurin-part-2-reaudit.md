# Re-audit: Saurin v1.0 Part 2

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` at commit `287a14b`
**Request:** `reviews/saurin-part-2-reaudit-request.md` (`ae53d8a`)
**Responds to:** `audits/saurin-part-2.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** All findings are resolved, and the patch adds no contradiction or hard dependency.

**Recommendation:** Saurin Part 2 may be accepted by Tyler.

## 2. Verification

| # | Point | Result | Basis |
| --- | --- | --- | --- |
| 1 | Rostral floor outside Marchfolk, Grask and Gorrund projection | **PASS** | New subsection in §40. At normalized head size, the minimum is "clearly outside the approved adult projection ranges," and it is described as an intentional non-overlap boundary. That matches the elven-ear and tail precedents for defining structures. |
| 2 | SAU-FACE-02 and 12 test the floor | **PASS** | Both now name the floor as their pass criterion. SAU-FACE-02 covers all three races. |
| 3 | Dentition infers no diet | **PASS** | §50 now specifies functional differentiated dentition with anterior and posterior roles and "no diet inferred." It no longer implies a population diet. This is consistent with the AGREED Grask, Gorrund, Pipkin and Cogling rows. |
| 4 | Stature accounting stated | **PASS** | New subsection in §55. Head height runs near to modestly below Marchfolk, and the neck stays near Marchfolk. The longer lower trunk is paid for mainly through reduced vertical head and thoracic contribution, not shorter legs. This is consistent with Part 1 §7, where the thorax is deep rather than tall, and it is still tested by SAU-FACE-22. |
| 5 | Speech and lip-sync OPEN, with a test | **PASS** | §76 adds the open item. SAU-FACE-23 checks readable speech shapes with no human lips, grin or snarl. |
| 6 | Grask tusks wording | **PASS** | §68 now says tusks aren't required and that limited tusk-like canine variation remains OPEN. |
| 7 | FD domains explicit | **PASS** | New subsection in §65, adapted sensibly to Saurin. FD-SURF covers scales and pattern. FD-HAIR stays empty unless biology later adds hair-like structures. FD-OBS covers lighting, pose, expression and camera, matching the AGREED meaning. It states that no surface domain can compensate for an FD-STRUCT failure. |
| 8 | No hearing, smell or vision bonus | **PASS** | §56 area, mirroring the bite firewall. |
| 9 | No unintended changes | **PASS** | Part 1, Tyler's tail decision and the carried tail questions, the culture firewall and the no-UE5 status are all unchanged. |

## 3. Completion recommendation

Saurin Part 2 may be accepted by Tyler. Part 3 (scales, surface and display structures, per §58–59 and §76) can begin when he says so.
