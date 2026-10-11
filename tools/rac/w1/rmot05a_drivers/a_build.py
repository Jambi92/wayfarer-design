# RAC RM-OT-05A: build the architecture-rebuild candidates on the accepted W2C / W2D routes + arch_sculpt (written back into the skeleton).
# Usage: python3 a_build.py ARCH.json NAME...   (names from the table below)
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D)
for p in (W1, W1 + '/w2c_drivers', W1 + '/w2d_drivers', W1 + '/w1g_drivers', W1 + '/w1h_drivers', W1 + '/w1i_drivers'): sys.path.insert(0, p)
A = json.load(open(sys.argv[1]))
GRN5 = json.load(open('/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w2c/b/GRN5/GRN5_w2c.json'))
GRB2 = json.load(open('/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w2c/b/GRB2/GRB2_w2c.json'))
W1L = {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [0.925, 1.0, 1.0], "LR:thigh": [1.20, 1.0, 1.20]}
def fr(rec): return {k: v for k, v in rec["bone_scales"].items() if k not in W1L or rec["bone_scales"][k] != W1L[k]}, (rec["extra_targets"] or None)
GON5 = {"bone_scales": {"LR:clavicle": [1, 0.95, 1], "spine_02": [0.95, 1, 1], "spine_03": [0.95, 1, 1], "pelvis": [0.98, 1, 1], "LR:thigh": [0.98, 1, 0.98]}, "kb_nodes": [0.98, 0.98, 0.965, 0.95, 0.95, 0.95]}
GOB7 = {"bone_scales": {"LR:clavicle": [1, 1.015, 1], "pelvis": [1.05, 1, 1], "LR:thigh": [1.05, 1, 1.05]}, "kb_nodes": [1.05, 1.05, 1, 1, 1, 1]}
TAB = {"GRA198": ("GR", 198), "GRA208": ("GR", 208), "GRA218": ("GR", "ref"), "GRA229": ("GR", 229), "GRA239": ("GR", 239),
       "GRAN": ("GR", "ref", "N"), "GRAB": ("GR", "ref", "B"),
       "GOA208": ("GO", 0.685), "GOA218": ("GO", "GO218"), "GOA239": ("GO", "GO239"), "GOA229": ("GO", 0.8241), "GOAREF": ("GO", 0.8369140625), "GOA251": ("GO", None),
       "GOAN": ("GO", 0.8369140625, GON5), "GOAB": ("GO", 0.8369140625, GOB7)}
if __name__ == '__main__':
    for nm in sys.argv[2:]:
        t = TAB[nm]
        if t[0] == 'GR':
            import gr_body as GB
            eb, tg = (None, None)
            if len(t) > 2: eb, tg = fr(GRN5 if t[2] == 'N' else GRB2)
            GB.build(nm, t[1], eb, tg, arch=A['GR'])
        else:
            import go_body as OB
            mac = t[1]
            if mac is None: mac = 'GO251'
            if isinstance(mac, str): mac = json.load(open(OB.W + '/b/%s/%s_w2d.json' % (mac, mac)))['height_macro']
            ag = json.loads(json.dumps(A['GO']))
            if nm == 'GOAN' and A.get('narrow_knee_hold'):      # GO-G6: the joint-structure field holds knee scale on the Narrow frame
                lg = ag['leg']
                for i, s_ in enumerate(lg['s']):
                    if 0.85 <= s_ <= 1.12: lg['klat'][i] *= A['narrow_knee_hold']; lg['kmed'][i] *= A['narrow_knee_hold']
            OB.build(nm, mac, t[2] if len(t) > 2 else None, None, arch=ag)
