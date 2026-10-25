# run_v002.sh : exact sequence that produced GR_U_REF_RP2_retopo_v002 (cloud workspace /tmp/claude-0/rt)
set -e; cd /tmp/claude-0/rt; BP=/home/claude/stc/bin/python3
# 1. revised authored cage (v001 architecture + support loops); CLPUSH=0.4 (web-cap pull) is the feet/hands default
export FFW=0,0.2,0.4,0.55,0.7,0.8,0.9,1.0          # forefoot planes (6 -> 8, denser at the toe-MTP row)
export TOEP1=0.3,0.45,0.6                          # toe proximal-phalanx stations (2 -> 3)
export FINP1=0.12,0.22,0.31,0.4,0.58,0.76          # finger proximal-phalanx stations (those proximal of the port are dropped)
export UPOST=11.3,12.3,13.3,13.8,14.05,14.3        # palm rings distal of the thumb split (4 -> 6, MCP row support)
export NFAN=18                                     # shoulder fan rings (14 -> 18)
export FINMID=0
python3 build_cage.py cage27.npz
# 2. x2 Catmull-Clark + guarded projection / polish / crease capture / fold + intersection cleanup
bash pipeL.sh cage27.npz L2J 2
# 3. quality: centroid capture, quad optimisation recipe, undo near self-intersections, guarded patch repair
python3 centfix.py L2J.npz L2Jf.npz 1.0
bash recipe.sh L2Jf.npz L2Jfv
python3 revsx.py L2Jf.npz L2Jfv.npz L2Jfw.npz
python3 centfix.py L2Jfw.npz L2Jfx.npz 1.0
bash repairsafe.sh L2Jfx.npz L2K
CGUARD=1 CREASE_BOX=31.5,34.5,-2.5,0.5,87.5,90.5 python3 crease.py L2K.npz _m1.npz 4 0.03
python3 centfix.py _m1.npz _m2.npz 1.0
python3 revsx.py L2K.npz _m2.npz L2L.npz
LDEV=0.06 bash repairall.sh L2L.npz _n1 3
python3 revsx.py L2L.npz _n1.npz _n2.npz
python3 centfix.py _n2.npz L2M.npz 1.0
LDEV=0.1 LOFF=0.15 LIT=80 python3 lrepair.py L2M.npz _o_5_0.15.npz 5
python3 foldfix.py _o_5_0.15.npz _o_5_0.15f.npz
python3 revsx.py L2M.npz _o_5_0.15f.npz L2N.npz
python3 optfix.py L2N.npz v002.npz                 # last 4 web-root clusters: direct local optimisation (<=0.3 mm off-surface)
# 4. gates (all in the v005 source frame)
python3 gate.py v002.npz v002_gate.json; python3 dev.py v002.npz v002_dev.json
$BP sxq.py v002.npz v002_sx.npy; python3 folds.py v002.npz; python3 flipchk.py v002.npz; python3 hardlist.py v002.npz v002_hard.json
LEVEL=2 python3 tagloops.py cage27.npz v002.npz v002_loops.json; python3 loopaudit.py v002.npz v002_loops_audit.json
python3 lm.py /tmp/claude-0/src3d/v5/v005.npz lm_src_v2.json; python3 lm.py v002.npz v002_lm.json; python3 lmdrift.py lm_src_v2.json v002_lm.json v002_lmdrift.json
python3 identity.py v002.npz v002_identity.json; python3 iou.py v002.npz v002_iou.json; python3 symm.py v002.npz v002_symmetry.json
python3 seams.py v002.npz v002_loops.json v002_seams.json; python3 poleaudit.py v002.npz v002_loops_audit.json v002_pole_audit.json ev2/cmp v002
# 5. production origin + export
python3 origin.py v002.npz v002_lm.json lm_src_v2.json v002_origin.json
ORIGIN_T=$(python3 -c "import json;print(','.join(repr(v) for v in json.load(open('v002_origin.json'))['translation_analysis_cm']))") \
RETOPO_NAME=GR_U_REF_RP2_retopo_v002 $BP export_retopo.py -- v002.npz v002_loops.json v002_seams.json out2/meta.json out2/GR_U_REF_RP2_retopo_v002.blend
$BP readback_rt.py -- out2/GR_U_REF_RP2_retopo_v002.blend v002_prod.npz
python3 make_landmarks2.py lm_src_v2.json v002_lm.json v002_origin.json out2/GR_U_REF_RP2_retopo_v002_landmarks.json
python3 make_sidecar2.py out2/GR_U_REF_RP2_retopo_v002.json
