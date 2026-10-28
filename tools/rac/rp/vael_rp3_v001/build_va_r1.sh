# build_va_r1.sh : Vael body / face source order §16 -- the selected provisional source VB2g + VC2 (final iteration, tag VB2gVC2h) rebuilt under its versioned ids VAL4-R1 (c1: VAL4 record
# + overrides) and VALF178-R1 (c2: MF-F-R base + the full Vael cfg + the identical VB2g / VC2 changes), stature re-solved to 178 cm; measured; then the
# rebuilt geometry is compared vertex-for-vertex with the candidate build (determinism) and copied into reviews/reference-assets (CANDIDATE, not frozen).
set -e
W=/home/claude/wayfarer-design/tools/rac/w1; RA=/home/claude/wayfarer-design/reviews/reference-assets; BP=/home/claude/stc/bin/python3; D=${VB_DIR:-/tmp/claude-0/rt/va2/vc2}
cd $D; mkdir -p r1
$BP $W/build_variant.py $RA/builds/VAL4_build.json c1_VB2gVC2h.json r1 VAL4-R1 > r1/VAL4-R1.log 2>&1 & $BP $W/build_variant.py $RA/builds/MF-F-R_build.json c2_VB2gVC2h.json r1 VALF178-R1 > r1/VALF178-R1.log 2>&1 & wait
python3 $W/run_candidate.py r1 VAL4-R1 ../MF-M-R_rest.npz >> r1/VAL4-R1.log 2>&1 & python3 $W/run_candidate.py r1 VALF178-R1 ../MF-M-R_rest.npz >> r1/VALF178-R1.log 2>&1 & wait
python3 - <<'E'
import numpy as np, json
out = {}
for r, c in (('VAL4-R1', 'VAL4-VB2gVC2h'), ('VALF178-R1', 'VALF178-VB2gVC2h')):
    a, b = np.load('r1/%s_r6.npz' % r), np.load('cand/%s_r6.npz' % c)
    out[r] = dict(candidate=c, max_abs_vertex_diff_cm=float(np.abs(a['V'] - b['V']).max()), stature=json.load(open('r1/%s_meas.json' % r))['stature_r6'])
json.dump(out, open('r1/determinism.json', 'w'), indent=1); print(out)
E
for i in VAL4-R1 VALF178-R1; do cp r1/${i}_r6.npz $RA/r6/; cp r1/${i}_build.json r1/${i}_meas.json $RA/builds/; done
echo R1_DONE
