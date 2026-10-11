# RAC W3D part 1: C1R central Skarn face validation (invariants vs the accepted body; face metrics vs matched Marchfolk) -> w3d/c1r.json
import os, sys, json, hashlib, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.dirname(D))
import w3c_face as WF, arm_measure as AM
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
SET = [('SK208-C1R', S + '/w1f/final/SK', S + '/w2a/st/MFM203', 'SK208 central (MF203 endpoint, not matched)'),
       ('SKM190-C1R', S + '/w2b/st/SKM190', S + '/w2b/st/MFM190', '190 config 1'), ('SKF190-C1R', S + '/w2b/st/SKF190', S + '/w2b/st/MFF190K3', '190 config 2'),
       ('SKM183-C1R', S + '/w2b/st/SKM183', S + '/w3c/b/MFM183', '183 config 1'), ('SKM203-C1R', S + '/w2b/st/SKM203', S + '/w2a/st/MFM203', '203 config 1'),
       ('SKM190-NLOW-C1R', S + '/w3c/b/SKM190-NLOW', S + '/w3c/b/MFM190-NLOW', '190 Narrow + low muscle'), ('SKM190-B-C1R', S + '/w3c/b/SKM190-B', S + '/w3c/b/MFM190-B', '190 Broad, ref. composition')]
KEYS = WF.KEYS
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
BODYK = ['torso_share', 'leg_share', 'arm_share', 'shoulder_breadth_share', 'thorax_breadth_share', 'crest_share', 'knee_over_femur', 'wrist_over_forearm', 'ankle_over_shin', 'hand_share', 'foot_share']
out = {}
for nid, old, mf, nm in SET:
    new = S + '/w3d/b/' + nid
    a = np.load(old + '_r6.npz'); b = np.load(new + '_r6.npz'); hw = a['w_head'] + a['w_neck_01']; body = a['keep'].astype(bool) & (hw < 0.02)
    disp = np.linalg.norm(b['V'] - a['V'], axis=1); Ha = a['V'][a['keep'].astype(bool), 2].ptp(); Hb = b['V'][b['keep'].astype(bool), 2].ptp()
    mo = AM.measure(old + '_r6.npz'); mn = AM.measure(new + '_r6.npz')
    bodyd = {k: mn['ratio'][k] - mo['ratio'][k] for k in BODYK}
    fo = WF.metrics(old + '_r6.npz'); fn = WF.metrics(new + '_r6.npz'); fm = WF.metrics(mf + '_r6.npz')
    r = dict(name=nm, old=dict(path=old.replace(S, '$S') + '_r6.npz', sha256=sha(old + '_r6.npz')), new=dict(path=new.replace(S, '$S') + '_r6.npz', sha256=sha(new + '_r6.npz')),
             mf=mf.replace(S, '$S'), stature_old=float(Ha), stature_new=float(Hb), body_max_disp_cm=float(disp[body].max()), changed_verts=int((disp > 1e-4).sum()),
             body_ratio_max_abs_delta=float(max(abs(v) for v in bodyd.values())), face_new={k: fn[k] for k in KEYS}, face_old={k: fo[k] for k in KEYS}, face_mf={k: fm[k] for k in KEYS},
             pct_vs_mf={k: 100 * (fn[k] - fm[k]) / abs(fm[k]) for k in KEYS}, HH=fn['HH'], FPI=fn['FPI'])
    out[nid] = r
    print(nid.ljust(16), 'dH %.3f body_disp %.4f body_ratio %.5f | vs MF: HH_H %+.1f Eu %+.1f BGP %+.0f BGB %+.1f NJT %+.1f MAL %+.1f NP %+.1f FPI %.4f' % (
        Hb - Ha, r['body_max_disp_cm'], r['body_ratio_max_abs_delta'], r['pct_vs_mf']['HH_H'], r['pct_vs_mf']['Eu_HH'], r['pct_vs_mf']['BGP'], r['pct_vs_mf']['BGB_HH'], r['pct_vs_mf']['NJT'], r['pct_vs_mf']['MAL'], r['pct_vs_mf']['NP'], fn['FPI']), flush=True)
json.dump(out, open(S + '/w3d/c1r.json', 'w'), indent=1)
