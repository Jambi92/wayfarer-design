# run_v003.sh : exact sequence that produced GR_U_REF_RP2_retopo_v003 (cloud workspace /tmp/claude-0/rt)
set -e; cd /tmp/claude-0/rt; BP=/home/claude/stc/bin/python3
# 1. cage29 = v002 cage27 + ankle fan 10 rings (ANKPHI), elbow 6 rings (ELBR), one more palm MCP-row ring (UPOST 14.18)
export FFW=0,0.2,0.4,0.55,0.7,0.8,0.9,1.0 TOEP1=0.3,0.45,0.6 FINP1=0.12,0.22,0.31,0.4,0.58,0.76 NFAN=18 FINMID=0
export UPOST=11.3,12.3,13.3,13.8,14.05,14.18,14.3 ANKPHI=8,17,26,35,44,53,62,71,80,90 ELBR=2.85,1.9,0.95,0,-0.95,-1.9
python3 build_cage.py cage29.npz
bash pipeL.sh cage29.npz L3B 2                      # x2 fit
bash runA.sh cage29 L3B                             # centfix / recipe / revsx / repairsafe / repairall / lrepair / optfix -> L3BO
# 2. last slivers and short-edge (longest/shortest edge) quads: direct local optimisation with fold + self-intersection guards
python3 optfix.py L3BO.npz _h1.npz; python3 optfix.py _h1.npz _h2.npz      # acceptance: edge ratio <= max(r0+0.05, 6.5)
OPT_RSEL=7.1 OPT_RMAX=5 OPT_RING=1 python3 optfix.py _h2.npz _h3.npz
OPT_RSEL=7.1 OPT_RMAX=5 OPT_RING=2 python3 optfix.py _h3.npz _h4.npz
OPT_OFF=0.05 OPT_RSEL=8 OPT_RMAX=9.0 OPT_RING=3 python3 optfix.py _h4.npz _h5_9.0.npz
# 3. thumb-web saddles: guarded surface relaxation (removes the v002 shading rumples; shape stays the source)
python3 relaxg.py _h5_9.0.npz v003.npz 2.8 40 -27.0,6.9,95.3 27.1,7.4,95.2
# 4. loops / seams / landmarks / origin / export, then the full audit on the EXPORTED blend
LEVEL=2 python3 tagloops.py cage29.npz v003.npz v003_loops.json; python3 seams.py v003.npz v003_loops.json v003_seams.json
python3 lm.py v003.npz v003_lm.json; python3 origin.py v003.npz v003_lm.json lm_src_v2.json v003_origin.json
ORIGIN_T=$(python3 -c "import json;print(','.join(repr(v) for v in json.load(open('v003_origin.json'))['translation_analysis_cm']))") \
RETOPO_NAME=GR_U_REF_RP2_retopo_v003 $BP export_retopo.py -- v003.npz v003_loops.json v003_seams.json out3/meta.json out3/GR_U_REF_RP2_retopo_v003.blend
bash finalaudit.sh out3/GR_U_REF_RP2_retopo_v003.blend v003_origin.json cage29 v003_rb
python3 make_landmarks2.py lm_src_v2.json v003_rb_lm.json v003_origin.json out3/GR_U_REF_RP2_retopo_v003_landmarks.json
python3 make_sidecar3.py out3/GR_U_REF_RP2_retopo_v003.json
