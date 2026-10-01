# Re-audit: Saurin v1.0 Part 1

**Auditor:** Claude
**Audited file:** `specs/saurin/SAURIN_V1.md` at commit `d32fed3`
**Request:** `reviews/saurin-part-1-reaudit-request.md` (`21c26bc`)
**Responds to:** `audits/saurin-part-1.md`

These are findings, not changes. The spec was not edited.

## 1. Result

**PASS.** Tyler's decision changes the question my audit's finding 4a asked, and the patch answers the new question properly. All other findings are resolved. Three notes are non-blocking.

**Recommendation:** Saurin Part 1 may be accepted by Tyler.

## 2. Tyler's decision and the integrated-organism test

Tyler's decision: **the tail is mandatory, always present, and never removed for racial validation.** That's a legitimate design choice, and it fits the brief ("a genuinely reptilian foundation … a tail"; "the tail works biologically").

It changes what has to be proven. The old question was whether Saurin survive without the tail. The new question is whether the tail looks *biologically inevitable* or bolted on. That's a stronger test of the "not human plus tail" rule.

**The new test only works if the body itself is organized around the tail.** That's what the original 4a gap was about, and the patch now supplies it:
- **Pelvic-femoral relationship (§9).** The pelvis is longer front-to-back, with structural mass organized toward the back. The hips and upper femurs are placed relative to that mass, so the legs support an upright biped whose axial load continues into the tail. That gives the "different hip mechanics" the brief asked for. It isn't a crouched-lizard pelvis and doesn't splay the legs.
- **Thoracic and shoulder organization (§8).** The shoulder blades sit on a deep, narrow-to-moderate thoracic shell. Clavicles are present but don't carry the main width. This is a real, testable contrast with Skarn's broad clavicles and upper back.

Together with the thorax, the lower axial trunk and the caudal base, these make the tail the end of a coherent axial chain. SAU-BODY-04 now tests exactly that.

## 3. Verification

| # | Point | Result | Basis |
| --- | --- | --- | --- |
| 1 | The mandatory visible tail appears consistently | **PASS** | §1, §5, §10, §31 (Marchfolk) and §34 all agree. "Tail silhouette" was removed from the removal list. |
| 2 | No active test hides or removes the tail | **PASS** | SAU-BODY-03 keeps the tail and neutralizes the surface. SAU-BODY-04 is now the integrated-organism test. SAU-BODY-18 is now a tail-integration stress test ("never removed"). No other test hides the tail. |
| 3 | Positive pelvic-femoral relationship | **PASS** | §9. See §2 above. |
| 4 | Positive thoracic and shoulder organization | **PASS** | §8. See §2 above. |
| 5 | Skarn and Aelari boundaries; SAU-BODY-21 and 22 | **PASS** | The Skarn row is built on approved Skarn anchors (broad clavicles and upper back, human robustness), and the Aelari row on approved Aelari anchors (distributed vertical elongation, gracile build). Both tests use normalized height with surface neutralized. |
| 6 | Tail biomechanics affirmed, gameplay kept separate | **PASS** | §13 affirms balance, turning, acceleration, swimming motion and body language through counterbalancing mass and axial movement, with no automatic statistical bonuses. It keeps the brief's functional tail and the firewall, and needs no supersession. |
| 7 | Stature accounting | **PASS** | It requires Part 2 to account for head, neck, thoracic height, lower trunk and leg shares together. |
| 8 | Tail world-space recorded | **PASS** | §33 lists backed seating, benches, beds, crowds and multiplayer collision, closing doors, capes, cloaks and back armor, mounts, and the rear camera. |
| 9 | No human sex-anatomy default | **PASS** | §24, consistent with universal amendment v0.1. |
| 10 | Prototype authority | **PASS** | Prototype scale, collision, shared human animation, and breath and swim values are non-authoritative. The 188 cm reference is recorded as an intentional, provisional revision of the brief's ~182 cm. |
| 11 | No culture or personality in biology | **PASS** | §28 is unchanged. |
| 12 | No UE5 | **PASS** | |

## 4. Non-blocking notes

1. **Attribute the tail decision in the spec.** The re-audit request credits it to Tyler, but the spec states it without attribution. One line such as "Tyler decision, September 30, 2026", as in Pipkin §37 and Cogling §140, would record why the tail-hidden test was dropped.
2. **What "always visible" covers.** §10 says the tail "remains visible as part of normal Saurin anatomy rather than being biologically hidden." Two later questions follow from that, and both belong to the equipment and surface parts:
   - Can garments partly cover the tail (long robes, cloaks), or must equipment always leave it visible?
   - Is acquired tail loss or injury possible as history (like ear damage for Fenn), or is any tail loss excluded?

   Recording both as OPEN now would stop them being decided by default.
3. **Tail length range wording.** "55–80% of standing height" is measured excluding the tail (§4), which is correct. SAU-BODY-08 and 18 vary length and base mass. When Part 2 sets numbers, the base-size-to-length coupling (§11) should be stated as a relationship, not as separate ranges.

## 5. Completion recommendation

Saurin Part 1 may be accepted by Tyler. ChatGPT can add notes 1–3 to the Part 2 patch. Part 2 begins when Tyler says so.
