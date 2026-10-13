# RM-OT-05O replay (run from the repository root)

```bash
T=tools/rac/w1/rmot05o_drivers; N=reviews/rac-rmot05n-evidence; S=reviews/rac-rmot05o-evidence
```

## §2 Audit of the 05N delivery

```bash
python3 $T/o_sections.py --ref $N/RD2/GO-RD2-REF.obj --low $N/LOW/GO-RD2-LOW.obj --out $S/audit --tag RD2_REF_LOW
python3 $T/o_preserve.py --ref $N/RD2/GO-RD2-REF.obj --low $N/LOW/GO-RD2-LOW.obj --params $N/LOW/GO-RD2-LOW_params.json --out $S/audit/RD2_REF_LOW_preservation.json
python3 $T/o_legaxes.py $N/RD2/GO-RD2-REF.obj $S/stance/RD2_leg_axes        # hip 106 / knee 57 / ankle 11 declared
```

## §3 RD3a: stance only

```bash
python3 $T/o_stance.py --in $N/RD2/GO-RD2-REF.obj --axes $S/stance/RD2_leg_axes.json --out $S/stance/GO-RD3a-REF_stance.obj
```

## §4 RD3b: surface transitions

```bash
python3 $T/o_brush.py --in $S/stance/GO-RD3a-REF_stance.obj --strokes $S/surface/RD3b_strokes.json \
        --stance $S/stance/GO-RD3a-REF_stance_record.json --out $S/surface/GO-RD3b-REF_surface.obj
```

## §5 RD3c: proportion (proposal in `proportion/PROPOSAL_RD3c.md`)

```bash
python3 $T/o_crotch.py $S/surface/GO-RD3b-REF_surface.obj --crown 232.55
python3 $T/o_proportion.py --in $S/surface/GO-RD3b-REF_surface.obj --stance $S/stance/GO-RD3a-REF_stance_record.json \
        --d_femur 4.8 --d_shank 4.4 --crotch_z 99.97 --out $S/proportion/GO-RD3c-REF_proportion.obj
cp $S/proportion/GO-RD3c-REF_proportion.obj $S/final/GO-RD3-REF.obj
```

## §6 LOW: the same RD3 operation chain applied to the 05N GO-RD2-LOW

The 05N GO-RD2-LOW is the bounded local soft-tissue reduction. Applying the identical RD3 chain to it keeps REF and LOW paired.

```bash
python3 $T/o_stance.py --in $N/LOW/GO-RD2-LOW.obj --axes $S/stance/RD2_leg_axes.json --out $S/final/GO-RD3-LOW_step1_stance.obj
python3 $T/o_brush.py --in $S/final/GO-RD3-LOW_step1_stance.obj --strokes $S/surface/RD3b_strokes.json \
        --stance $S/stance/GO-RD3a-REF_stance_record.json --out $S/final/GO-RD3-LOW_step2_surface.obj
python3 $T/o_proportion.py --in $S/final/GO-RD3-LOW_step2_surface.obj --stance $S/stance/GO-RD3a-REF_stance_record.json \
        --d_femur 4.8 --d_shank 4.4 --crotch_z 99.97 --out $S/final/GO-RD3-LOW.obj
```

## REF/LOW audit in the RD3 frame

Station heights are carried by `final/station_z_RD3.json`, minus its `_note` key.

```bash
python3 $T/o_sections.py --ref $S/final/GO-RD3-REF.obj --low $S/final/GO-RD3-LOW.obj --out $S/final --tag RD3_REF_LOW --station_z ZMAP.json
python3 $T/o_preserve.py --ref $S/final/GO-RD3-REF.obj --low $S/final/GO-RD3-LOW.obj --params $S/final/LOW_regions_RD3frame.json --out $S/final/RD3_REF_LOW_preservation.json
python3 $T/o_legaxes.py $S/final/GO-RD3-REF.obj $S/final/RD3_leg_axes --hip_z 118.75 --knee_z 62.74 --ankle_z 10.84 --zmax 112 --thigh 71 101 --shank 22 51
```

## Blind gate

**Body wrapping.**

```bash
python3 tools/rac/w1/rmot05l_drivers/l_npz.py $S/final/GO-RD3-REF.obj OUT/GO-RD3-REF 203.75
python3 tools/rac/w1/rmot05l_drivers/l_npz.py $S/final/GO-RD3-LOW.obj OUT/GO-RD3-LOW 203.75
```

The neck cut is the 05N cut (191) plus the +12.75 cm frame shift.

**Sheets.**

```bash
python3 tools/rac/w1/rmot05k_drivers/k_blind.py GO-RD3 OUT run1
python3 tools/rac/w1/rmot05k_drivers/k_blind.py GO-RD3 OUT run2
```

The frozen control bodies are read from the RAC working store, unchanged since 05A–05N.

**Scoring and evaluation.**
- Prompt: `o_scorer_prompt_05O.md`; 3 fresh scorers per run.
- Revised rules (pre-registered in `blind/PREREGISTRATION.md`):

```bash
python3 $T/o_gate_eval.py $S/blind/key_K05a_GO-RD3.json $S/blind/scorer_K1.json $S/blind/scorer_K2.json $S/blind/scorer_K3.json \
                       -- $S/blind/key_K05b_GO-RD3.json $S/blind/scorer_L1.json $S/blind/scorer_L2.json $S/blind/scorer_L3.json
```

- Old criteria (provenance): `tools/rac/w1/rmot05f_drivers/f_tally.py`, same arguments.
