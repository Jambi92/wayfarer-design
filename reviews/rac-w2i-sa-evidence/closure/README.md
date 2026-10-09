# RAC W2I1 — Saurin closure evidence

Order `reviews/chatgpt-rac-w2i1-saurin-closure-order.md`; report `reviews/claude-rac-w2i-saurin-final-closure-report.md`. NON-CANON diagnostics; no Saurin anatomy written back.

| File | Driver (`tools/rac/w1/w2i_drivers/`) | Content |
|---|---|---|
| `tailcap2.json` | `sa_tailcap2.py` | D2 same-state reachable caps (RSI 1.19 primary, 1.00 report), named cases |
| `tailcap2_lift8.json` | `sa_tailcap2.py` (CURV=-8) | cap regression at +8 deg carriage (information) |
| `joints.json` | `sa_joints.py` | J-2 joints (Gate 4 / 5 construction axes), defensibility checks, invariance audit, per-body limb / joint / S7 readings |
| `base_identity.json` | (inline check) | working base == frozen `saurin_final_base.npz` (a925e067…) |
| `limbcmp.json` | `sa_limbcmp.py` | comparator readings (MF, GR, GO, CG, DU137C), section control, vertical budget, validator rows |
| `crotch.json` | `sa_crotch.py` | surface crotch heights (MEASUREMENT LIMIT; not used in scoring) |
| `carriage.json` | `sa_carriage.py` | D4 carriage 0 / +4 / +8 / +12 deg: silhouette, width profile, tail geometry, invariance, lean |
| `sheets/sa_carriage_*.jpg` | `sa_carriage_render.py` | carriage renders (full + close front) |
| `sheets/sa_j2_joints.jpg` | `sa_joint_sheet.py` | J-2 joints on the frozen SA-M188 |
| `tables.md` | `../../../tools/rac/w1/gen_w2i1_docs.py` | generated tables |

Order of runs: `sa_tailcap2.py`, `sa_joints.py`, `sa_crotch.py`, `sa_limbcmp.py joints.json crotch.json limbcmp.json`, `sa_carriage.py carriage.json save`, `sa_carriage_render.py`, `sa_joint_sheet.py joints.json`, `CURV=-8 TGT=rsi119 STATES=Balanced-188,Broad-188,Narrow+fat-hi-188,Broad-208 sa_tailcap2.py`.
