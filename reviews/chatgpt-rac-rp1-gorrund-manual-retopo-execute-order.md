# RAC RP1 — execute Gorrund manual production-retopo pilot

Date: 2026-10-18
Authority: reviews/tyler-chatgpt-rac-rp1-gorrund-release-decisions.md
Prepared pilot: reviews/chatgpt-rac-rp1-gorrund-production-retopo-pilot-HOLD.md
Master plan: reviews/chatgpt-rac-retopology-rigprep-master-plan.md

## 1. Release
The HOLD on the prepared RP1 Gorrund pilot is released.

Execute the prepared pilot exactly as written, subject to the author ruling above.

## 2. Contract writeback first
Before any geometry work, update:
specs/RAC_PRODUCTION_MESH_CONTRACT.md

Replace the flagged proposed RP1 tolerance values with the accepted author values:
- T-1: median <= 0.5 mm; p95 <= 1.5 mm; maximum <= 3.0 mm.
- T-2 identity zones: median <= 0.3 mm; p95 <= 0.8 mm; maximum <= 1.5 mm.
- T-3: stature +/-1.0 mm; bbox +/-2.0 mm per axis.
- T-6: target <= 1.0 mm; none above 1.5 mm; individually report values above 1.0 mm.
- T-7: silhouette IoU >= 0.995.
- Gorrund nail projection tolerance: +/-0.15 mm.
- T-4 / T-5 accepted as RP1 quality targets.

Record that these remain production standards, not biology canon.

## 3. Method
Use only:
M-B — fully manual retopology in Blender.

Do not use:
- QuadriFlow;
- automatic quad remesh;
- automatic remesh as the production topology generator.

Manual polygon construction with snapping/projection onto the derived welded working copy is required.

Diagnostic scripts may be used for:
- source verification;
- welded working-copy preparation;
- masks/groups;
- landmarks;
- deviation analysis;
- topology analysis;
- evidence rendering.

They must not substitute for the manual retopology authoring step.

## 4. Source
Start only from the immutable frozen Gorrund source identified in the pilot:
E:/UnrealProjects/Wayfarer 5.8/RaceBodies/source/Gorrund-Neutral-C/05AW4/GO-05AW4_nails_final.blend

SHA-256:
5a4e45d40158e7dc92f6f8ba13d67ada2403e3e3dcda9048382323ee43a22d5e

Verify at entry and again at exit.

Never write to the source.

## 5. Required RP1 repairs
Resolve in the new production topology:
- left-hand contact handle;
- right-hand contact handle;
- left-axilla micro-tunnel;
- raw split-position/perineal seam handling;
- tail-root slivers;
- nail-support density discontinuity.

Target production topology:
- 1 component;
- 0 boundary;
- 0 non-manifold;
- genus 0;
- outward normals;
- quad-dominant per contract;
- deformation-loop and creator-density targets satisfied.

## 6. Anatomy protection
Do not redesign:
- leonine head/muzzle;
- ears;
- body composition;
- tail root/axis/taper;
- hands/digits;
- plantigrade feet;
- toes;
- nails;
- accepted proportions;
- native stature.

The visual veto in the ruling is absolute: numeric compliance cannot rescue a visible identity regression.

## 7. Checkpoints
Because this is the first manual production pilot, checkpoint before large irreversible expansion of the manual topology:

- RP1-A: welded source + landmarks + manual topology layout plan, no finished body required.
- RP1-B: trunk/girdle/pelvis/major limb loop network.
- RP1-C: head, hands, feet, tail and identity-zone topology.
- RP1-D: full closed production mesh + cleanup + evidence.

If a checkpoint reveals that the manual topology plan cannot satisfy the accepted deviation gates without changing anatomy, STOP rather than forcing it.

## 8. Evidence
Return:
reviews/claude-rac-rp1-gorrund-production-retopo-pilot-gate.md

Evidence:
reviews/rac-rp1-evidence/

Include:
- source hash in/out;
- production file hash;
- vertex/edge/quad/triangle counts;
- topology integrity;
- genus;
- loop/density audit;
- two-way deviation by zone;
- landmark drift;
- silhouette IoU;
- stature/bbox;
- foot/nail metrics;
- source-vs-production front/profile/rear/3-4 sheets;
- closeups of head, both hands, both feet/nails, tail root, axilla and perineum;
- overlay and deviation heat maps;
- any micro-detail exemptions.

## 9. Output
Use the prepared RP1 output path:
E:/UnrealProjects/Wayfarer 5.8/RaceBodies/production/Gorrund/RP1/

Do not overwrite accepted checkpoints.

## 10. Stop
At completion return:

RP1 Gorrund production-mesh pilot — PASS / CONSTRAIN / FAIL

Then STOP for Tyler/ChatGPT family-pilot acceptance.

Do not start RP2 Grask.
Do not start other races.
Do not start final rigging, skin weighting, creator implementation or UE5.
