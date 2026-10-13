# RAC RM-OT-05T1 — execute the 05T handoff-validation block and return closure

**Authority:** Tyler directive, October 13, 2026.  
**Repository:** `Jambi92/wayfarer-design`, `main`.  
**Parent order:** `reviews/chatgpt-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-stop-order.md` at commit `4aa9232390e668ec436973dc1dbbfd9add11a446`.

## Direction

Proceed now with the existing **RM-OT-05T** order in full. This is an execution/resume order, not a scope expansion and not a replacement specification.

The author has reviewed the current repository state. No later Claude closure for 05T is present on `main`. Treat 05T as the controlling order and complete its handoff-validation/release work exactly as written.

### Required work

1. Validate the existing `GO-05S_interface_handoff.blend` and its S3/F1/B2 references under the checks in 05T.
2. Verify editable versus frozen sets, boundary protection, transforms/units, labels, masks/isolation, and reference-object safety.
3. Exercise the actual recommended OBJ export path with an unchanged round-trip fixture. Do not weaken exact protected-region checking to make the fixture pass.
4. Run the required disposable protection tests:
   - authorized small interface displacement is recognized;
   - protected-vertex displacement is rejected;
   - frozen-boundary displacement is rejected;
   - authorized local topology change still preserves correspondence outside the editable interface.
5. Create and verify the sculptor entry point `START_HERE.md`, including the first-session desktop fixture check and the exact return contract.
6. Produce the compact self-contained 05T sculptor release with package-specific manifest, hashes, clean-extraction/link checks, dependency/version instructions, and supported replay/test evidence.
7. Commit the required closure:
   - `reviews/claude-rac-rm-ot-05t-gorrund-direct-sculpt-handoff-validation-closure.md`
   - evidence under `reviews/rac-rmot05t-release/`
8. Update `specs/STATUS.md` only to reflect the verified 05T outcome and the resulting wait state. Do not imply Gorrund acceptance or Stage C completion.

### Non-negotiable guardrails

- **No S4, RD5, replacement full body, automatic candidate generation, scripted morphology sweep, interpolation/relaxation retry, global smoothing/remesh, new LOW, blind study, scaffold, Rodin generation, or unrelated RAC work.**
- Do not alter the master `base.glb`; its preserved SHA-256 remains `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b`.
- Preserve Gorrund beastfolk identity, leonine head/tail canon, plantigrade/body guardrails, and the later 13,380-vertex rig-contract validation requirement.
- No canon promotion, D4, UE5 implementation, production rigging, or creator implementation.
- Do not hire/contact anyone, install software, spend credits, or fabricate an interactive test that was not actually performed.
- Any requirement that cannot be verified must remain explicitly **PENDING** or **FAILED** with the exact limitation.

## Completion state

After the 05T closure and release are committed, **STOP AWAITING DIRECT-SCULPT RETURN**.

The expected state is:

- **Gorrund: UNACCEPTED / DIRECT SCULPT REQUIRED**
- **Grask E3: FROZEN**
- **RM-OT-05: OPEN**
- **Stage C: BLOCKED**
- **D4 / UE5 / production rigging / creator implementation: NOT STARTED**
- **Canon promotion: NOT PERFORMED**

Do not invent a “next morphology pass” after closure. The next substantive Gorrund action begins only when an actual edited direct-sculpt asset is returned for verification and author visual review.
