# Fenn ear branch — preparation note (order 2de0e28 §15; preparation only, nothing built)

This note was unlocked by the craniofacial hidden-ear PASS. No ear geometry or topology was built. The next order shapes the prototypes.

## 1. Branch region definition (active family v005)

Source: `ear_branch_region_v005.json`. Ear zone = family faces whose four vertices have hm08 `w_ears` > 0.5 (carried through the family map).

Per side:

| Item | Value |
|---|---|
| Ear-zone faces / vertices | 1,206 / 1,233 |
| Root boundary | **one closed loop of 52 vertices** |
| Bounding box (lateral × anteroposterior × vertical) | 1.89 × 3.88 × 5.65 cm |
| Valence of interior vertices | 4 everywhere (the 8 valence-3 and 48 valence-1/2 counts are boundary artefacts of the face subset) |

**Proposed branch** = the ear zone plus one transition ring outside the 52-vertex root loop. Nothing else on the head or body changes: face, orbit, mouth, scalp and neck topology are untouched.

## 2. Mapping plan (active v005 → Fenn ear branch)

**Outside the branch:**
- vertices keep their v005 index and their hm08 map row unchanged;
- production V = M @ (Fenn hm08), exactly as in the body-family realization.

**The 52 root vertices** keep their map rows. They are the attachment.

**The 2 × 1,181 interior ear vertices are replaced by the Fenn ear patch:**
- an all-quad disc in the W1e ear parameterization: front sheet + back sheet + rim, bridged to the 52-vertex root;
- each new vertex is stored as a fixed offset in a head-local root frame (root centroid, root normal, skull up), authored per candidate (E1 / E2 / E3);
- so every candidate shares one vertex count, one face list and one map structure.

**Branch record:**
- a `branch_map` listing v005 indices removed and added;
- the new face list;
- per-vertex root-frame offsets.

Configuration 1 and configuration 2 share it. The geometry is fitted to each head by the same root-frame construction.

**Budget:** face / ears density must stay ≤ 0.25 % of stature (the current ear zone is 0.100 %). The upper extension needs added rows along the helix, so the target is about 1.5–2× the current ear-zone face count.

## 3. Canon-derived reference evidence (W1e)

`tools/rac/w1/ear_families_v2.py`, family `FN-elven` (author decisions E-D1…E-D6; W1p: 22 / 22 directional rows). Parameters are in `W1e_FN-elven_params.json`:

| Parameter | Value |
|---|---|
| Length | 8.6 cm at Marchfolk head scale |
| Maximum half-width | 1.80 cm |
| Taper | continuous taper from 0.30 |
| Projection | 50° (the greatest of the elves, E-D3) |
| Tilt / sweep | 32° / 1.6 cm |
| Lobe fraction | 0.15 |
| Relief | helix roll; Y-shaped antihelix (stem, superior and inferior crura) bounding the triangular fossa; concha split into cymba and cavum by the crus of the helix; tragus, antitragus, intertragic notch |

This is EVIDENCE geometry: a double-sided procedural slab, attached as a separate mesh in W1, never topologically joined. It is the shape guide, not production topology.

## 4. Technical proposal for E1 / E2 / E3 (one shared topology)

| Candidate | Length (× head-height ratio) | Projection | Tilt / sweep | Base width | Intent |
|---|---|---|---|---|---|
| E1 restrained | 7.6 cm | 42° | 28° / 1.2 cm | 1.75 | shortest that still reads Fenn; full non-human construction |
| **E2 balanced (proposed central)** | **8.6 cm (W1e FN-elven)** | **50°** | **32° / 1.6 cm** | **1.80** | W1e reference realized on production topology |
| E3 stronger | 9.4 cm | 55° | 35° / 1.9 cm | 1.85 | stronger, still central-population |

Shared by all three: helix, antihelix with crura, cymba / cavum, tragus / antitragus, lobe, and an upper extension with the tip emerging from the helix (not a stretched human tip).

**Checks to run then:**
- T-4 quality, density, root continuity, local self-intersection;
- root-only source deviation;
- static head / neck rotation root check.

**Stop:** nothing is built until ChatGPT orders the prototypes.
