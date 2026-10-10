# RAC W3B section 23 sheets for the scale fields: per named field a close camera on its core (auto-aimed along the core's mean normal),
# rows = reference / size min valid / size max valid / relief min valid / relief max valid (+ the first invalid size / relief point), surfaced
# copies (canonical surface elsewhere). Extreme-body comparison: canonical relief carried by SA-M188 / SA-M188-N-FAHI / SA-M208 / SA-M188-B.
# Usage: python3 w3b_scale_sheets.py face | body | extreme
import os, sys, json, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG, w3b_sheet as SS
ENV = json.load(open(C.W + '/scale/envelope.json'))
def cam(k, name='v'):
    Z = SC.ref(); core = SC.weight(RG.masks()[k]) >= 0.9
    if (Z['Vu'][core, 0] > 1.0).mean() > 0.3 and (Z['Vu'][core, 0] < -1.0).mean() > 0.3: core = core & (Z['Vu'][:, 0] > 1.0)      # bilateral field: aim at the right side
    P = Z['Vu'][core]; n = Z['N'][core].mean(0); n /= np.linalg.norm(n)
    c = np.median(P, 0); ext = np.percentile(np.linalg.norm(P - c, axis=1), 80)
    sc = float(np.clip(2.0 * ext, 2.5, 16.0)); a = np.degrees(np.arctan2(n[0], n[1])); e = np.degrees(np.arcsin(np.clip(n[2], -0.95, 0.95)))
    return '%s:%.1f:%.1f:%.2f:%.2f:%.2f:%.2f' % (name, a, e, c[0], c[1], c[2], sc), c, sc
def variants(k):
    e = ENV[k]; out = [('ref', 1.0, 1.0, False, 'reference (canonical W2)')]
    if e.get('size') and e['size'].get('min_valid') is not None:
        out += [('smin', e['size']['min_valid'], 1.0, True, 'size min valid x%.2f' % e['size']['min_valid']), ('smax', e['size']['max_valid'], 1.0, True, 'size max valid x%.2f' % e['size']['max_valid'])]
        fh = e['size']['first_invalid_high']
        if isinstance(fh, (list, tuple)): out.append(('sfail', fh[0], 1.0, True, 'size FIRST FAIL x%.2f (%s)' % (fh[0], ','.join(f.split('_')[0] for f in fh[1]))))
    if e.get('relief') and e['relief'].get('min_valid') is not None:
        out += [('rmin', 1.0, e['relief']['min_valid'], False, 'relief min valid x%.2f' % e['relief']['min_valid']), ('rmax', 1.0, e['relief']['max_valid'], False, 'relief max valid x%.2f' % e['relief']['max_valid'])]
        fh = e['relief']['first_invalid_high']
        if isinstance(fh, (list, tuple)): out.append(('rfail', 1.0, fh[0], False, 'relief FIRST FAIL x%.2f (%s)' % (fh[0], ','.join(f.split('_')[0] for f in fh[1]))))
    return out
def field_sheet(keys, out, title):
    Z = SC.ref(); views = []; rows = []
    for k in keys:
        v, c, sc = cam(k, k[:12]); w = SC.weight(RG.masks()[k])
        for tag, s, r, rs, lab in variants(k):
            t = 'sf_%s_%s' % (k, tag)
            rel = Z['disp'] if tag == 'ref' else SC.variant(w, s, r, reseed=rs)[0]
            Sv = Z['Vu'] + rel[:, None] * Z['N']
            SS.ensure(t, Sv, Z['Fu'], v.replace(k[:12], 'c'), res=700, box=lambda X, c=c, sc=sc: np.linalg.norm(X - c, axis=1) < 0.9 * sc)
            rows.append((t, '%s\n%s' % (k, lab)))
    return SS.sheet(out, title, ['Surfaced copies (canonical W2 relief elsewhere). Close camera aimed along the field core normal. Diagnostic only.'], rows, 'c:0:0:0:0:0:1', ['close view'], cell=420)
if __name__ == '__main__':
    if sys.argv[1] == 'face':
        for k in RG.CLASS['face']: print(field_sheet([k], 'w3b_face_%s.jpg' % k, 'W3B RM-UF-04 facial scale field - %s' % k))
    if sys.argv[1] == 'body':
        # order section 23 body list: dorsal trunk, ventral trunk, neck / shoulder, elbow / wrist, hip / knee / ankle, forearm / shin, dorsal hand / foot, tail
        for k in ('S_dorsal_trunk', 'V_chest_abdomen', 'S_upper_posterior_neck', 'A_neck_flexion', 'A_elbow', 'A_knee', 'S_forearm', 'S_shin', 'S_dorsal_foot', 'S_dorsal_tail', 'V_tail_underside', 'A_tail_articulation'):
            print(field_sheet([k], 'w3b_body_%s.jpg' % k, 'W3B RM-UB-08 body scale field - %s' % k))
    if sys.argv[1] == 'interact':
        I = json.load(open(C.W + '/interact/results.json'))
        rows = [('ix_' + k, '%s\nridge m %s, relief %s, size %s\nmin legibility %.2f\nface aspect %.2f, eye vis %.2f' % (k, v['m'], v['r'], v['s'], v['min_legibility_required'], v['face_aspect'], v['eye_vis_0'])) for k, v in I.items()]
        print(SS.sheet('w3b_ridge_scale_interaction.jpg', 'W3B section 19 - ridge x facial scale interaction (surfaced head)', ['Per-field relief / size at each field\'s own valid-interval end (rmin / rmax / smin / smax); ridge m = hidden normalized strength. Legibility = ridge strength / scale relief near the ridge (>= 1.0 required).'],
                       rows, 'hF:0:4:0:12:182:22;hF34:35:12:0:9:182:24;hP:90:0:0:6:181.5:26', ['front', 'front 3/4', 'profile'], cell=360))
    if sys.argv[1] == 'extreme':
        import w3b_bodies as BD
        Z = SC.ref(); rows = []
        for k in ('S_dorsal_trunk', 'V_chest_abdomen', 'A_elbow', 'A_knee', 'S_dorsal_tail'):
            v, c, sc = cam(k, 'c')
            for bid in ('SA-M188', 'SA-M188-N-FAHI', 'SA-M188-B', 'SA-M208', 'SA-F188'):
                P = BD.build(bid); Vu, Fu = igl.upsample(P, C.F0); Nu = igl.per_vertex_normals(Vu, Fu); Sv = Vu + Z['disp'][:, None] * Nu
                # same field core, located on this body
                core = SC.weight(RG.masks()[k]) >= 0.9; cb = np.median(Vu[core], 0); t = 'ex_%s_%s' % (k, bid)
                vv = v.split(':'); vv[3:6] = ['%.2f' % x for x in cb]; SS.ensure(t, Sv, Fu, ':'.join(vv), res=700, box=lambda X, cb=cb, sc=sc: np.linalg.norm(X - cb, axis=1) < 0.9 * sc)
                rows.append((t, '%s\n%s' % (k, bid)))
        print(SS.sheet('w3b_body_extremes.jpg', 'W3B RM-UB-08 - canonical scale fields carried by accepted body extremes', ['Same field core and camera direction on each body; relief carried along each body\'s normals (W2 convention).'], rows, 'c:0:0:0:0:0:1', ['close view'], cell=420))
