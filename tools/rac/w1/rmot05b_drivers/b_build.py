# RAC RM-OT-05B: build the 05B candidates = accepted W2C / W2D route + 05A arch sculpt (with the 05B knee / residual corrections) + the race
# surface-anatomy stage (race_surface.py, carried in the skeleton meta so every grid / composition body gets it).
# Usage: python3 b_build.py CFG.json NAME...    (CFG = {"GR": arch, "GO": arch, "surface": {"GR": .., "GO": ..}, "narrow_knee_hold": k, "narrow_elbow_hold": k})
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D)
for p in (W1, W1 + '/w2c_drivers', W1 + '/w2d_drivers', W1 + '/w1g_drivers', W1 + '/w1h_drivers', W1 + '/w1i_drivers'): sys.path.insert(0, p)
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
A = json.load(open(sys.argv[1]))
W1L = {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [0.925, 1.0, 1.0], "LR:thigh": [1.20, 1.0, 1.20]}
def grrec(n): return json.load(open(S + '/w2c/b/%s/%s_w2c.json' % (n, n)))
def gorec(n): return json.load(open(S + '/w2d/b/%s/%s_w2d.json' % (n, n)))
def fr(rec): return {k: v for k, v in rec["bone_scales"].items() if k not in W1L or v != W1L[k]} or None, (rec["extra_targets"] or None)
# name -> (race, W2 source record or stature, frame flag)
TAB = {"GR5B198": ("GR", 198), "GR5B208": ("GR", 208), "GR5B218": ("GR", "ref"), "GR5B229": ("GR", 229), "GR5B239": ("GR", 239),
       "GR5BN": ("GR", "ref", "GRN5"), "GR5BB": ("GR", "ref", "GRB2"),
       "GO5B208": ("GO", "GO208"), "GO5B218": ("GO", "GO218"), "GO5B229": ("GO", "GO229"), "GO5BREF": ("GO", "GOREF"), "GO5B239": ("GO", "GO239"), "GO5B251": ("GO", "GO251"),
       "GO5BN": ("GO", "GON5"), "GO5BB": ("GO", "GOB7"), "GO5BN218": ("GO", "GON5_218"), "GO5BB218": ("GO", "GOB7_218")}
def hold(arch, chain, lo, hi, k):
    a = json.loads(json.dumps(arch)); c = a[chain]
    for i, s_ in enumerate(c['s']):
        if lo <= s_ <= hi: c['klat'][i] *= k; c['kmed'][i] *= k
    return a
if __name__ == '__main__':
    for nm in sys.argv[2:]:
        t = TAB[nm]
        if t[0] == 'GR':
            import gr_body as GB
            eb, tg = fr(grrec(t[2])) if len(t) > 2 else (None, None)
            ag = hold(A['GR'], 'arm', 0.85, 1.15, A['narrow_elbow_hold']) if nm == 'GR5BN' and A.get('narrow_elbow_hold') else A['GR']
            GB.build(nm, t[1], eb, tg, arch=ag, surface=A['surface']['GR'])
        else:
            import go_body as OB
            rec = gorec(t[1]); ag = A['GO']
            if rec.get('frame') and rec['frame'].get('kb_nodes') and rec['frame']['kb_nodes'][0] < 1 and A.get('narrow_knee_hold'):
                ag = hold(ag, 'leg', 0.85, 1.12, A['narrow_knee_hold'])                       # GO-G6 knee hold on every Narrow frame
            OB.build(nm, rec['height_macro'], rec['frame'], rec['extra_targets'], arch=ag, surface=A['surface']['GO'])
