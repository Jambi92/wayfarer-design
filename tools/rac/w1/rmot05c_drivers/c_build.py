# RAC RM-OT-05C: build the base-surface candidates = accepted 05B skeleton route (05A architecture + 05B knee / residual corrections and
# Narrow holds, cfg_final of RM-OT-05B, WITHOUT the 05B surface stage) + the 05C race base-surface organization (race_base.organize, spec in
# the skeleton meta so every grid / CIB / composition body gets it).
# Usage: python3 c_build.py CFG05B.json SPECS.json NAME...
#   NAME = GR5C<cand>[N|B|229] or GO5C<cand>[N|B]  (cand = A|B|C);  low composition: GR5C<cand>-LOW / GO5C<cand>-LOW (muscle 0, weight 0.5)
import os, sys, json, subprocess
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D)
for p in (W1, W1 + '/w2c_drivers', W1 + '/w2d_drivers', W1 + '/w1g_drivers', W1 + '/w1h_drivers', W1 + '/w1i_drivers', W1 + '/rmot05b_drivers'): sys.path.insert(0, p)
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
A = json.load(open(sys.argv[1])); SP = json.load(open(sys.argv[2]))
import b_build as BB                                   # 05B tables (W2 source records, frame flags) and the Narrow hold
GRT = {'': 'ref', '229': 229, 'N': 'GRN5', 'B': 'GRB2'}
GOT = {'': 'GOREF', 'N': 'GON5', 'B': 'GOB7'}
def run(args): r = subprocess.run(['python3'] + args, capture_output=True, text=True, cwd=W1); print(r.stdout[-300:], r.stderr[-800:], flush=True)
if __name__ == '__main__':
    for nm in sys.argv[3:]:
        race, rest = nm[:2], nm[4:]; cand, var = rest[0], rest[1:]
        spec = SP[race][cand]
        if var == '-LOW':
            src = nm.replace('-LOW', '')
            run([W1 + ('/w2c_drivers/gr_comp.py' if race == 'GR' else '/w2d_drivers/go_comp.py'), nm, src, '0.0', '0.5']); continue
        if race == 'GR':
            import gr_body as GB
            t = GRT[var]
            if t in ('GRN5', 'GRB2'): eb, tg = BB.fr(BB.grrec(t)); H = 'ref'
            else: eb, tg, H = None, None, t
            ag = BB.hold(A['GR'], 'arm', 0.85, 1.15, A['narrow_elbow_hold']) if var == 'N' and A.get('narrow_elbow_hold') else A['GR']
            GB.build(nm, H, eb, tg, arch=ag, racebase=spec)
        else:
            import go_body as OB
            rec = BB.gorec(GOT[var]); ag = A['GO']
            if rec.get('frame') and rec['frame'].get('kb_nodes') and rec['frame']['kb_nodes'][0] < 1 and A.get('narrow_knee_hold'):
                ag = BB.hold(ag, 'leg', 0.85, 1.12, A['narrow_knee_hold'])
            OB.build(nm, rec['height_macro'], rec['frame'], rec['extra_targets'], arch=ag, racebase=spec)
