# build_hp.sh : Halvren body / face source order §17 PELVIS AUTHOR-DECISION PACKAGE (diagnostic only; nothing here becomes source canon) -- three
# conceptual central pelvis directions on the HB2HF2 candidate (both configurations):
#   HP-A  human-family-dominant: HB2HF2 as built (no pelvic term; only the leg / stature coupling)
#   HP-B  mild mixed relational: pelvis bone Y x 1.02 (pelvic vertical) + hip-scale-horiz-decr 0.05 (crest / hip breadth) -- a relation none of the frozen
#         elves uses (Fenn widens X / Z, Aelari raises Y and Z, Vael raises X / Y / Z)
#   HP-C  stronger mixed: pelvis bone Y x 1.035 + hip-scale-horiz-decr 0.10
# Full + lean (skeletal-envelope) builds, skeletal proxy, measured with run_candidate.py; HP-A reuses the HB2HF2 candidate builds.
W=/home/claude/wayfarer-design/tools/rac/w1; RB=/home/claude/wayfarer-design/reviews/reference-assets/builds; BP=/home/claude/stc/bin/python3; D=${HP_DIR:-/tmp/claude-0/rt/hv/hp}
mkdir -p $D/cand $D/lean $D/skp; cd $D; echo '{"muscle": 0.0, "weight": 0.0}' > lean.json
python3 - <<'E'
import json, sys
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/halvren_rp3_v001'); import hv_defs as H
P = {'HPB': dict(pelvis=[1.0, 1.02, 1.0], horiz=0.05), 'HPC': dict(pelvis=[1.0, 1.035, 1.0], horiz=0.10)}
for k, p in P.items():
    o = H.overrides('HB2HF2'); o['bone_scales']['pelvis'] = p['pelvis']; o['targets']['hip-scale-horiz-decr'] = p['horiz']
    json.dump(o, open('c1_HB2HF2-%s.json' % k, 'w'), indent=1); json.dump(H.c2(o), open('c2_HB2HF2-%s.json' % k, 'w'), indent=1)
json.dump(dict(P=P, note='diagnostic pelvis directions on HB2HF2; not source canon'), open('HP_definitions.json', 'w'), indent=1)
E
b(){ $BP $W/build_variant.py $1 $2 cand $3 > cand/$3.log 2>&1; python3 $W/run_candidate.py cand $3 /tmp/claude-0/rt/hv/partA/ref/MF-M-R_rest.npz >> cand/$3.log 2>&1; echo "BUILT $3 $?"; }
for t in HB2HF2-HPB HB2HF2-HPC; do b $RB/HVC1_build.json c1_$t.json HVC1-$t & b $RB/MF-F-R_build.json c2_$t.json HVF178-$t & wait; done
for n in HVC1-HB2HF2 HVF178-HB2HF2; do for f in _build.json _r6.npz _meas.json _rest.npz; do cp /tmp/claude-0/rt/hv/hb/cand/$n$f cand/; done; done
L(){ $BP $W/build_variant.py cand/$1_build.json lean.json lean $1-LEAN > skp/$1-LEAN.log 2>&1; python3 $W/skeletal_proxy.py cand lean $1 skp > skp/$1_skp.log 2>&1; echo "SKP $1 $?"; }
for n in HVC1-HB2HF2 HVF178-HB2HF2 HVC1-HB2HF2-HPB HVF178-HB2HF2-HPB HVC1-HB2HF2-HPC HVF178-HB2HF2-HPC; do L $n; done
echo HP_DONE
