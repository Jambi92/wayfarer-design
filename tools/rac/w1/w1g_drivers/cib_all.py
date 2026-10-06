# RAC W1g driver AS RUN (scratch paths = this session's working directories; kept for provenance).
# Builds the composition-infimum bony envelope (bony_envelope.py) for every body and re-runs the skeletal proxy with it.
# Usage: python3 cib_all.py [ids...]   (default: all)
import sys, os, json, glob, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import bony_envelope as B, skeletal_proxy as SP
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
F, G = S + '/w1f', S + '/w1g'
REF = os.environ.get('REF', F + '/final'); LEAN = os.environ.get('LEAN', F + '/final_lean')
COMP = os.environ.get('COMP', G + '/comp'); OUT = os.environ.get('OUT', G + '/skp'); CIB = os.environ.get('CIBD', G + '/cib')
NATIVE = ["MF-M-R", "MF-F-R", "FN", "AE", "VA", "HV", "DU-NAT", "PK-NAT", "CG-NAT", "SK", "SG"]
# AD-G14 bodies: id -> (ref prefix, skeleton lean_B prefix, donor grid id, donor ref prefix, donor lean prefix)
ADG14 = {"GO": (REF + '/GO', LEAN + '/GO-LEAN', 'GO0', F + '/go/GO0', F + '/go/GO0-LEAN'),
         "GR": (REF + '/GR', LEAN + '/GR-LEAN', 'GR0', F + '/gr/GR0', F + '/gr/GR0-LEAN'),
         "SKB229": (F + '/sk/SKB229', F + '/sk/SKB229-LEAN', 'SK229', F + '/sk/SK229', F + '/sk/SK229-LEAN'),
         "SKB208": (F + '/sk/SKB208', F + '/sk/SKB208-LEAN', 'SK', REF + '/SK', F + '/lean/SK-LEAN')}
for b in ("04", "12", "14"):
    ADG14["GOR-BODY-" + b] = (F + '/go/GOR-BODY-' + b, F + '/go/GOR-BODY-%s-LEAN' % b, 'GO0', F + '/go/GO0', F + '/go/GO0-LEAN')
ADG14["GOR-BODY-02"] = (F + '/go/GOR-BODY-02', F + '/go/GOR-BODY-02-LEAN', 'GO2080', F + '/go/GO2080', F + '/go/GO2080-LEAN')
EXTRA = json.loads(os.environ.get('EXTRA', '{}'))      # more AD-G14 entries (W1g bodies)
ADG14.update({k: tuple(v) for k, v in EXTRA.items()})

def donor_links(did, dref):
    """grid donor files: G/donor/<did>-Cmmmwww; (0.5,0.5) -> donor ref; (0.25,0.25) from G/donor or COMP if built there"""
    for st in ("rest", "r6"):
        p = G + '/donor/%s-C050050_%s.npz' % (did, st)
        if not os.path.lexists(p): os.symlink(dref + '_%s.npz' % st, p)
        q = G + '/donor/%s-C025025_%s.npz' % (did, st); c = COMP + '/%s-C025025_%s.npz' % (did, st)
        if not os.path.lexists(q) and os.path.exists(c): os.symlink(c, q)
        for m, w in B.GRID:
            t = B.tag(m, w); q = G + '/donor/%s-%s_%s.npz' % (did, t, st); c = COMP + '/%s-%s_%s.npz' % (did, t, st)
            if not os.path.lexists(q) and os.path.exists(c): os.symlink(c, q)

def one(cid):
    os.makedirs(CIB, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    if cid in NATIVE:
        comps = [LEAN + '/%s-LEAN_rest.npz' % cid, REF + '/%s_rest.npz' % cid] + sorted(glob.glob(COMP + '/%s-C*_rest.npz' % cid))
        if cid == "MF-M-R" and not os.path.exists(COMP + '/MF-M-R-C025025_rest.npz'): comps.append(F + '/low/MF-M-R-LOW_rest.npz')
        if cid == "SK" and not os.path.exists(COMP + '/SK-C025025_rest.npz'): comps.append(F + '/low/SK-LOW_rest.npz')
        refd, leand, rid = REF, LEAN, cid
    else:
        ref, lb, did, dref, dlean = ADG14[cid]
        donor_links(did, dref)
        gd = G + '/grid_' + cid; os.makedirs(gd, exist_ok=True)
        comps = B.assemble_grid(lb, G + '/donor', did, dlean, gd, cid) + [ref + '_rest.npz']
        # skeletal_proxy needs ref_dir/ID_rest|r6 and lean_dir/ID-LEAN_rest|r6
        refd = G + '/lnk_' + cid; os.makedirs(refd, exist_ok=True); leand = refd
        for st in ("rest", "r6"):
            for a, b in ((ref + '_%s.npz' % st, refd + '/%s_%s.npz' % (cid, st)), (lb + '_%s.npz' % st, refd + '/%s-LEAN_%s.npz' % (cid, st))):
                if os.path.lexists(b): os.remove(b)
                os.symlink(a, b)
        rid = cid
    R = B.cib(comps[1] if cid in NATIVE else ref + '_rest.npz', comps)
    if cid in NATIVE: R = B.cib(REF + '/%s_rest.npz' % cid, comps)
    cj = CIB + '/%s_cib.json' % cid; json.dump(R, open(cj, 'w'), indent=1, default=float)
    SP.main(refd, leand, rid, OUT, cj)
    return {S_: [round(R["bony"][S_][0], 2), R["argmin"][S_][0]] for S_ in ("S2", "S4", "S5", "S6")}

if __name__ == '__main__':
    ids = sys.argv[1:] or NATIVE + list(ADG14)
    for i in ids:
        print(i, json.dumps(one(i)), flush=True)
