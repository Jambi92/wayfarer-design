# RAC W2I5 — Saurin medial / posterior thigh finish / conditional canonicalization evidence

Order `reviews/chatgpt-rac-w2i5-saurin-final-thigh-canonicalization-order.md`; report `reviews/claude-rac-w2i5-saurin-canonicalization-closure-report.md`. CANDIDATE COPIES — canonicalization NOT performed (§12 conditions 1–3 failed); W1 references, the W2I4 candidate, the tool chain and canon are unchanged.

| File | Driver (`tools/rac/w1/w2i5_drivers/`) | Content |
|---|---|---|
| `bodies_F5.json` | `sa_w2i5_build.py full` | 62-body list on the W2I5 route (W2I4 route + W2I5 sculpt delta), W2I measure + J-2 limbs + ledger |
| `compare_F5.json`, `saeval_F5.json` | W2I `sa_compare.py`, `sa_eval.py` (unchanged) | cross-race and internal suites |
| `eval_F5.json` | W2I2 `sa_w2i2_eval.py` (unchanged) | limb / budget rows |
| `tailcap_F5.json` | `run_tailcap_fin5.py` (W1 `sa_tailcap2.py`, `TGT=rsi119`) | tail-cap regression |
| `quality5.json` | `sa_quality5.py` | strain / flips vs W2I4 and frozen, sculpted-edge statistics, 62-body flip / fold census, surfaced topology |
| `fieldcheck5.json` | `sa_fieldcheck5.py` | scale-field continuity; seed reuse identity |
| `thigh_relief5.json` | `sa_thighrelief5.py` | thigh fine-relief correlation length by sector (frozen / W2I3 / W2I4 / W2I5) |
| `relief_curve5.json` | `sa_reliefcurve5.py` | medial / posterior vertical autocorrelation curves (why the metric fails) |
| `surface_info5.json` | `sa_surface5.py` | surface regeneration with the saved W2I4 seeds |
| `sheets/*.jpg` | `sa_w2i5_render.py` | W2I3 / W2I4 / W2I5 thigh at matched camera (base and surfaced, M and F); evaluated-candidate SA-M188 / SA-F188; family |

Sculpt: `sa_sculpt.py` (surface-walk native band relief, defect fades, soft masks, repair-aware 62-body fold guard) + `sa_guardfix5.py` (residual-face closure). Prepared but NOT run (conditions failed): `sa_canon5.py` (W2 canonical file set), `sa_toolchain5.py` (W2 tool-chain counterparts and §263 re-verification).
