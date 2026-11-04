# sa6_pd2.py OUT.json [LAYERDIR] : RP6 re-check of the 19 accepted PD-2 creator states (order a407015 §18; closure order 58aa486c §2).
#   Each state = an accepted dense creator-composition body (canonical W2I6 face list, clean workspace cr_<STATE>.npy, hash-verified); the frozen cage is
#   realised on it through the frozen barycentric embedding (no topology / geometry change).
#   Step A (pre-rig, = RP5 PD-2 definition, sa_pd2.py): dense-source folds = canonical-base triangles whose normal flips (cos < 0) vs the canonical base,
#     or whose area collapses below 5 % of rest; neutral cage flips = quads whose normal flips vs the rest cage.  Reconciled with the RP5 ownership audit.
#   Step B (rig, RP6 creator-state assumptions): skeleton re-evaluated on the state (landmark joints via the same affine transfer as c2); the BASE
#     configuration's production weights (c1 for SA-M* states, c2 for SA-F* states; one weight set per base configuration, carried by topology); correctives
#     = base set + the per-state creator-state corrective layer (sa6_pd2_fit.py, LAYERDIR/CF_state_<STATE>.json) when present.  The full anatomical
#     34-pose suite at full angle; per pose three columns: LBS only / base correctives / base + state layer (production).
#   Ownership per pose (production column): a folded quad within 1 cm of a pre-rig source fold or a neutral cage flip of the state AND already folded under
#   plain LBS (closure v002 strict rule: a defect the correctives created or moved is never composition-owned) = COMPOSITION/PD-2
#     (screening signal; every such pose is also re-checked against the base column and LBS so a worsened defect is visible), else RIG-OWNED.  New
#     interpenetration and tears are always rig-owned unless they sit on a pre-rig fold.  Closed-body |dV| <= 100 cm3 (jaw poses exempt) as for c1 / c2.
#   REGRESSION = rig-owned defect on the state in a pose where the base configuration is clean.
import sys, os, json, glob, time, numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_skeleton as SK, sa6_fit as FT, sa6_pd2_fit as PF
OUT = sys.argv[1]; LD = sys.argv[2] if len(sys.argv) > 2 else None; WD = PF.WD
d = C.load(); z = PF.z; w = PF.w; F = PF.Fd
VR = np.load(C.W + '/src/saurin_w2_final_base.npz'); VR = VR[[k for k in VR.files if VR[k].shape == w['v_M'].shape][0]].astype(float)
def fn(P): return np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]])
nR = fn(VR); aR = np.linalg.norm(nR, axis=1); P0 = (z['bc'][:, :, None] * VR[F[z['tri']]]).sum(1)
def evalpose(R, S, Cr, spec, Ft, w0, vol):
    T = R.pose(spec); out = {}
    for tag, dl in (('lbs', None), ('base', Cr[0].delta(T)), ('prod', Cr[1].delta(T))):
        P = R.skin(T) if dl is None else R.skin(T, R.V + dl)
        f = np.nonzero(R.relcos(P, T) < 0)[0]; pen = np.nonzero(FT.penetration(R, P, Ft, w0))[0]; te = S.tear_edges(P)[0]
        out[tag] = dict(P=P, f=f, pen=pen, tears=S._E1[te], dV=(S.body_volume(P) - S.V0) if vol else 0.0)
    return out
ref = {}
for cfg in 'MF':                                           # base-configuration references (production weights + correctives, anatomical suite, full angle)
    R0 = SP.Rig(cfg, WD + '/W_%s.npz' % cfg); C0 = CC.Correctives.load(R0, WD + '/CF_%s.json' % cfg); ref[cfg] = {}
    for pn, spec in R0.suite('anat').items():
        T = R0.pose(spec); ref[cfg][pn] = int((R0.relcos(R0.skin(T, R0.V + C0.delta(T)), T) < 0).sum())
res = dict(status='RP6 RIG PILOT / NOT FROZEN', method=open(__file__).read().split('import')[0], dense_source_staged=C.have_workspace(), base_reference_flips=ref,
           rp5_ownership_audit='reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/validation/SA_PD2_ownership.json', states={})
rp5 = json.load(open(C.R + '/reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation/validation/SA_PD2_ownership.json'))
ONLY = [x for x in os.environ.get('PD2_STATES', '').split(',') if x]   # optional subset; results merge into an existing OUT
if ONLY and os.path.exists(OUT): res['states'] = json.load(open(OUT))['states']
for path in sorted(glob.glob(C.W + '/cr_*.npy')):
    nm = os.path.basename(path)[3:-4]
    if ONLY and nm not in ONLY: continue
    t0 = time.time(); VB = np.load(path).astype(float); nB = fn(VB); aB = np.linalg.norm(nB, axis=1)
    sflip = (nR * nB).sum(1) / (aR * aB + 1e-20) < 0; scol = aB < 0.05 * aR; bad = sflip | scol; Vs = (z['bc'][:, :, None] * VB[F[z['tri']]]).sum(1)
    q0 = np.cross(P0[d['Q'][:, 2]] - P0[d['Q'][:, 0]], P0[d['Q'][:, 3]] - P0[d['Q'][:, 1]]); q1 = np.cross(Vs[d['Q'][:, 2]] - Vs[d['Q'][:, 0]], Vs[d['Q'][:, 3]] - Vs[d['Q'][:, 1]])
    nflip = np.nonzero((q0 * q1).sum(1) < 0)[0]
    pts = np.r_[VB[F[bad]].mean(1) if bad.any() else np.zeros((0, 3)), Vs[d['Q'][nflip]].mean(1) if len(nflip) else np.zeros((0, 3))]; kd = cKDTree(pts) if len(pts) else None
    R, cfg = PF.state_rig(nm); S = CC.Solver(R); S.V0 = S.body_volume(R.V); Ft = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, Ft)
    Cb = CC.Correctives.load(R, WD + '/CF_%s.json' % cfg); lf = (LD + '/CF_state_%s.json' % nm) if LD else None
    Cp = CC.Correctives.load(R, lf) if lf and os.path.exists(lf) else Cb
    r5 = rp5[nm]
    st = dict(base_config=cfg, state_layer=os.path.basename(lf) if Cp is not Cb else None,
              prerig=dict(source_triangles=int(len(F)), source_flipped=int(sflip.sum()), source_collapsed=int(scol.sum()), source_folds_union=int(bad.sum()),
                          neutral_cage_flips=int(len(nflip)), neutral_cage_flip_regions=sorted({str(d['qlab'][q]) for q in nflip}),
                          rp5_audit=dict(source_flipped=r5['source_flipped'], source_collapsed=r5['source_collapsed'], cage_flipped_quads=r5['cage_flipped_quads'], owner=r5['owner']),
                          reconciled=bool(r5['source_flipped'] == int(sflip.sum()) and r5['source_collapsed'] == int(scol.sum()) and r5['cage_flipped_quads'] == len(nflip))),
              poses={})
    tot = dict(rig_flips=0, comp_flips=0, rig_pen=0, rig_tears=0, vol_fail=0, base_rig_flips=0, lbs_flips=0); regress = []
    for pn, spec in R.suite('anat').items():
        vol = not any('jaw' in e[0] for e in spec); o = evalpose(R, S, (Cb, Cp), spec, Ft, w0, vol); pr = o['prod']
        def near(idx_pts):
            if kd is None or not len(idx_pts): return np.zeros(len(idx_pts), bool)
            return kd.query(idx_pts)[0] <= 1.0
        cf = near(Vs[R.Q[pr['f']]].mean(1)) if len(pr['f']) else np.zeros(0, bool); cp_ = near(Vs[pr['pen']]); ct = near(Vs[pr['tears']].mean(1)) if len(pr['tears']) else np.zeros(0, bool)
        # closure v002 (strict): a defect is composition-owned only if it sits at a pre-rig fold AND plain LBS already shows it there (else the
        # correctives created / worsened it -> rig-owned)
        lb = o['lbs']; cf = (cf & np.isin(pr['f'], lb['f'])) | R.rest_inverted[pr['f']];   # creator-inverted neutral quads: always composition (closure v003)
        cp_ &= np.isin(pr['pen'], lb['pen'])
        if len(pr['tears']): lt = {tuple(e) for e in np.sort(lb['tears'], 1)}; ct &= np.array([tuple(e) in lt for e in np.sort(pr['tears'], 1)])
        bf = o['base']['f']; bcomp = ((near(Vs[R.Q[bf]].mean(1)) & np.isin(bf, lb['f'])) | R.rest_inverted[bf]) if len(bf) else np.zeros(0, bool)
        row = dict(lbs_flips=int(len(o['lbs']['f'])), base_flips=int(len(bf)), base_rig_flips=int((~bcomp).sum()),
                   flips=int(len(pr['f'])), composition_pd2=int(cf.sum()), rig_owned=int((~cf).sum()), new_penetration=int(len(pr['pen'])), rig_penetration=int((~cp_).sum()),
                   tears=int(len(pr['tears'])), rig_tears=int((~ct).sum()), dV_cm3=round(float(pr['dV']), 2), volume_ok=bool(abs(pr['dV']) <= 100),
                   regions=sorted({str(R.ql[q]) for q in pr['f']})[:8], composition_regions=sorted({str(R.ql[q]) for q in pr['f'][cf]})[:8])
        st['poses'][pn] = row
        tot['rig_flips'] += row['rig_owned']; tot['comp_flips'] += row['composition_pd2']; tot['rig_pen'] += row['rig_penetration']; tot['rig_tears'] += row['rig_tears']
        tot['vol_fail'] += int(not row['volume_ok']); tot['base_rig_flips'] += row['base_rig_flips']; tot['lbs_flips'] += row['lbs_flips']
        if (row['rig_owned'] or row['rig_penetration'] or row['rig_tears'] or not row['volume_ok']) and ref[cfg][pn] == 0: regress.append(pn)
    st.update(totals=tot, regressions_vs_base=regress, owner='CLEAN (no rig-owned defect)' if not (tot['rig_flips'] or tot['rig_pen'] or tot['rig_tears'] or tot['vol_fail'])
              else 'RIG-OWNED DEFECTS ON THIS STATE')
    res['states'][nm] = st
    print('%-8s base %s prerig src %d cage %d reconciled %s | prod rig flips %d pen %d tears %d volfail %d comp %d | base-only rig %d | regress %s  %.0fs' % (
        nm, cfg, bad.sum(), len(nflip), st['prerig']['reconciled'], tot['rig_flips'], tot['rig_pen'], tot['rig_tears'], tot['vol_fail'], tot['comp_flips'], tot['base_rig_flips'], regress[:5], time.time() - t0), flush=True)
res['summary'] = dict(states=len(res['states']), clean_states=sum(s['owner'].startswith('CLEAN') for s in res['states'].values()),
                      cage_or_topology_owned=0 if all(s['prerig']['neutral_cage_flips'] == 0 or 'SOURCE' in s['prerig']['rp5_audit']['owner'] for s in res['states'].values()) else 'CHECK')
json.dump(res, open(OUT, 'w'), indent=1); print(res['summary'])
