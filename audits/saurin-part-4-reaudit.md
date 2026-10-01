# Re-audit: Saurin v1.0 Part 4

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` at commit `0e60197`
**Request:** `reviews/saurin-part-4-reaudit-request.md` (`d01764f`)
**Responds to:** `audits/saurin-part-4.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** All three required fixes and all recommendations are resolved. One note is non-blocking.

**Recommendation:** Saurin Part 4 may be accepted by Tyler.

## 2. Verification

| # | Point | Result | Basis |
| --- | --- | --- | --- |
| 1 | Inherited phenotype is in Biological Anatomy and expressed through Natural | **PASS** | §137 and §161 now match the AGREED consistency-resolution rule: Natural is an appearance layer, not an inheritance category. |
| 2 | Saved data follows the architecture layers | **PASS** | §156 lists the four architecture layers. Separately:<br>• Environmental is transient<br>• Applied is stored with Presentation<br>• Acquired is individual history |
| 3 | Manual choice keeps the full range | **PASS** | §134 now matches the AGREED Sagekin rule. SAU-CC-25 tests it. |
| 4 | Acquired-History Randomization | **PASS** | §142A adds a third domain. It's lockable on its own (§143–144), can't alter anatomy or presentation, and excludes major loss states. Tattoo-equivalents stay in Presentation. |
| 5 | SAU-CC-26 | **PASS** | |
| 6 | Creator gameplay firewall, SAU-CC-27 | **PASS** | §161A covers every creator dimension. "Visual extrema cannot be used as hidden min-max controls." |
| 7 | Pupil dilation is a state | **PASS** | §149 stores the pupil's shape and dilation range, previewed under lighting. SAU-CC-28 tests it. |
| 8 | Tail layer assignment | **PASS** | §145: length, base and taper are Anatomy and Frame; muscularity and adiposity are Composition. |
| 9 | Tail base scales with length and mass, SAU-CC-29 | **PASS** | §145 now states the relationship. This closes my Part 1 re-audit note 3. |
| 10 | NPC narrative exceptions | **PASS** | §157: marked non-baseline and kept out of presets, randomization, distributions and NPC baseline generation. Consistent with the AGREED Vael rule. |
| 11 | Tail extremes vs world-space proxies | **PASS** | §166 ties the final tail ranges to SAU-BODY-20 and its list. |
| 12 | No regressions | **PASS** | The diff adds text only and replaces two lines. The mandatory tail, rostrum floor, manual agency, Parts 1–3 and the no-UE5 status are unchanged. |

## 3. Non-blocking note

The brief's single "Scars and Tattoos" randomize button now spans two domains:
- Acquired History for scars
- Presentation for tattoo-equivalents

That's correct biologically. The future UI can keep one button that calls both domains while still respecting their separate locks. No spec change is needed; this is for the implementation phase.

## 4. Completion recommendation

Saurin Part 4 may be accepted by Tyler. Part 5 begins when he says so.
