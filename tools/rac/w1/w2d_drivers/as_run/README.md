# RAC W2D AS RUN (scratch paths = this session's working directories; kept for provenance)
Order of runs: `st.sh` (GOREF + 208 / 218 / 239 / 251 cm), `skb.sh` (Broad Skarn 229 = accepted Skarn 229 + W2B Broad write), `fr.sh` (first frame probes GON / GONF / GOB / GOBF and the composition states),
`run_search.py` with `ad3args*.txt` (AD-3 limb-present proportion probes, `search_ad3.json`), `lp.sh` (GOLP218 full build = probe GOLA),
`fr2.py` / `fr3.py` / `fr4.py` (Narrow upper-only GON3; Broad GOB3-7), `n4.py` / `n5.py` (Narrow with pelvis: GON4, final GON5 + 218 cm),
`ext.py` (named-extreme searches: GOX12 axial breadth; GOX14 = spine_03 Y probe, which is upper-thorax LENGTH, not depth — kept as a mis-axis probe; GOD14 = depth sculpt ka / kp from r 0.3),
`m218.py` (GO229, 218 cm frame / extreme bodies), `comp2.py` (composition states at 208 / 218 cm), `chk.py` (skeletal rows), `probes.py` (probes.json, construction.json).
Joint sections: `cd $S/w1r/jbw; python3 ../../../w2c1_drivers/joint_section.py $S/w1r/jbw OUT.json BODIES...` (bodies in reviews/rac-w2d-go-evidence/joint_sections.json).
Evaluation: `w2d_reg.py REG.json; w2d_spec.py SPEC.json; w2d_eval.py REG.json SPEC.json w2d.json <W2C1 joints.json joints2.json joints3.json> <W2D joints.json joints2.json>`; tables: `gen_w2d_docs.py`; sheets: `render_AS_RUN.sh`.
