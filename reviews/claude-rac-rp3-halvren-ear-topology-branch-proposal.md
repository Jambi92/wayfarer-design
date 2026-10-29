# RAC RP3 — Halvren dedicated ear topology branch: PROPOSAL (not executed)

Order: `reviews/chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order.md` §9, §10, §21, §25.
Gate: `reviews/claude-rac-rp3-halvren-central-accept-ear-architecture-gate.md`.
Status: **proposal only. Nothing built.** It needs an author / ChatGPT order before work starts.

## Why a branch is needed

The shared elf engineering ear topology is the Fenn v002 sheet. Vael's RI3 six-ring cuff connectivity is its root variant. The audit (gate §2) found four things:

1. **The near-human end cannot be expressed at human size.**
   - The sheet's cleanly realizable floor is about L 6.2–6.3. Below that the front sheet compresses: the aspect limit is passed and slivers appear.
   - At that floor the free auricle measures about 0.30 HH, against 0.24 HH for the Marchfolk auricle (+25 %).
   - So HE1 cannot have "mostly human-like overall length and size" on this topology. Biology would be compromised to preserve reuse (§21).
2. **Root / concha.**
   - The Fenn rigid cuff rebuilds the raised cuff mound around the root, the failure where one ear reads as layered on another (anterior mound p90 0.45 cm).
   - The exact Vael RI3 root geometry removes the mound but collapses at human-forward lengths: branch self-intersections and degenerate or sliver faces at the lower postauricular corner.
   - The bounded Halvren root geometry HR1 fixes the central range HE1–HE3 only. It stays brittle at the bounds:
     - Marchfolk-proportion bound: one 3° sliver;
     - elf-forward bound (L 9.4, projection 42°): fails;
     - failures are non-monotone in length.
3. **Concha.** The sheet's concha is shallower than the Marchfolk cavum at every Halvren setting (see the measured `concha_depth_over_L`). The engineering layout has no human-size cavum bowl.
4. **Root footprint.** The engineering sheet attaches through a junction ring placed inside the v005 footprint. The concha sits about 0.4 cm further back than the Marchfolk concha.

## Proposed branch: `HALVREN_EAR_BRANCH_TOPOLOGY_v001` (working name HVT1)

**Principle:** one connectivity whose human-family structures exist at human size. The elven extension grows out of the upper helix; it is not a leaf attached to a cuff.

- **Root interface (kept).**
  - The unchanged 52-vertex v005 root loop, so face / scalp topology outside the root stays byte-identical, as for every elf branch.
  - No raised cuff perimeter. The skin inside the root loop is the attached concha / tragus skin, not a separate cuff, so there is one auricle by construction.
- **Human-family scaffold.** These come from the v005 family human auricle connectivity (the Marchfolk ear zone, 1,206 faces per side):
  - concha bowl (cavum + cymba);
  - crus of helix, tragus, antitragus and intertragic notch;
  - antihelix with stem and crura, and the triangular fossa;
  - helix roll and lobe.

  The scaffold is rebuilt as a clean all-quad layout with the same anatomical partition, so it is not a copy of MPFB vertices. That makes HE1 human-sized with a real human cavum.
- **Elven extension band.**
  - A fixed set of helix / scapha rows inserted between the superior crus and the helix apex (proposed 6–8 rows, graded).
  - Their spacing scales with the upper extension:
    - at the human-forward end the rows stay at a minimum spacing, producing a short shouldered apex rather than collapsing to zero;
    - at the elf-forward end they carry the taper.
  - Tip sharpness, sweep and vertical angle are geometry on that band.
  - Base width, projection and lobe stay in the scaffold.
- **Geometry layer.** The HVEAR1 domain architecture is reused unchanged: root, base, concha / tragus, lobe, projection, upper extension, tip, helix shoulder, tilt and sweep stay independent domains. No human↔elf scalar and no vertex interpolation of source ears.

## Acceptance criteria (before any Halvren ear is selected as central)

- **Range:**
  - one connectivity, both configurations;
  - from Marchfolk-size human-forward (free length 0.24–0.27 HH, projection 20–25°) to elf-forward (0.36–0.38 HH, projection up to about 42°);
  - Fenn-, Aelari- and Vael-influenced diagnostics included.
- **§21 gates at both bounds and at every probe:**
  - 100 % quads, 1 component, 0 boundary / non-manifold / degenerate, outward normals;
  - 0 branch self-intersections;
  - aspect < 10, minimum corner ≥ 10°;
  - density < 0.25 % of stature;
  - root valence 4 × 52;
  - 8-pose head / neck readiness clean.
- **One auricle:**
  - anterior attachment at skin level (p90 ≤ 0.20 cm);
  - concha depth at least the Marchfolk value at the human-forward end;
  - neutral clay root / concha closeups.
- **Firewalls:**
  - ear-domain arithmetic firewall (one-α R² < 0.8 for every HE);
  - HE1 not "Marchfolk + tip";
  - HE3 not a source duplicate.
- **Frozen Fenn / Aelari / Vael and v005:** untouched.

## Scope / stop rules

Halvren only. No rigging, UV, LOD or UE5 work, and no creator UI. The HE1 / HE2 / HE3 domain definitions (`ear_branch_lib.CAND`, HVEAR1) carry over as the geometry intent. Their realizations on the shared topology stay as reference evidence.
