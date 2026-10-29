# hv_bf_manifest.py EVIDIR : Halvren body / face source order §18 / §23 -- family candidate manifest for every propagated body x face candidate (v005
# realization hash, validator, technical pass, source record hashes) and the source sidecars of the candidate records (definition, construction,
# determinism, regeneration identity). The recommended central pair HB2 + HF2 is also written as diagnostic production blends
# HV_{M,F}_REF_RP3_bodyfam_v002 (run_hv_bf_prod.sh), whose hashes are added here when present.
import sys, os, json, glob, hashlib, numpy as np
E = sys.argv[1]; W = '/tmp/claude-0/rt/hv'; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest(); jl = lambda p: json.load(open(p)); RA = '/home/claude/wayfarer-design/reviews/reference-assets'
TS = jl(W + '/hbe/HV_bf_technical.json'); DEF = jl(W + '/hb/HV_source_definitions.json')
man = dict(record='HALVREN RP3 body x face source-candidate family manifest (DIAGNOSTIC; family human auricle = non-final ear; NOT frozen)', order='reviews/chatgpt-rac-rp3-halvren-body-face-source-order.md (2026-10-29)',
           definition=dict(file='HV_source_definitions.json', sha256=sha(W + '/hb/HV_source_definitions.json'), version=DEF['version']), candidates={}, production={})
for i, t in TS.items():
    man['candidates'][i] = dict(source_r6='reviews/reference-assets/r6/%s_r6.npz' % i, source_r6_sha256=sha('%s/r6/%s_r6.npz' % (RA, i)), build_sha256=sha('%s/builds/%s_build.json' % (RA, i)),
                                family_npz_sha256=sha('%s/hbe/fam/%s_fam.npz' % (W, i)), validator='%d / %d' % (t['validator'], t['stations']), technical_pass=t['technical_pass'], regen=t['regen'],
                                worst_flip_excess_vs_MF_v005=t['worst_flip_excess'], new_contact_class=t['new_contact_class'], density_max_over_limit=t['density_max_over_limit'])
ph = W + '/hbprod/prod_hashes.jsonl'
if os.path.exists(ph):
    for l in open(ph):
        x = json.loads(l); n = os.path.basename(x['file']); rb = jl('%s/hbprod/readback/%s_readback.json' % (W, n.replace('.blend', '')))
        man['production'][n] = dict(sha256=x['sha256'], geometry_hash=x['geometry_hash'], face_topology_hash=x['face_topology_hash'], verts=x['verts'], quads=x['quads'], readback_max_abs_diff_m=rb['max_abs_diff_vs_candidate_m'], readback_faces_equal=rb['faces_equal_candidate'],
                                    status='DIAGNOSTIC central-pair candidate HB2 + HF2 (pelvis held; family human auricle); NOT frozen')
det = {}
for c in ('HVC1', 'HVF178'):
    a = np.load('%s/hb/cand/%s-HB2HF2_r6.npz' % (W, c)); b = np.load('%s/hb_det/cand/%s-HB2HF2_r6.npz' % (W, c)); det[c + '-HB2HF2'] = dict(independent_rebuild_max_abs_dV_cm=float(np.abs(a['V'].astype(float) - b['V'].astype(float)).max()), faces_identical=bool(np.array_equal(a['F'], b['F'])))
man['determinism'] = det
json.dump(man, open(E + '/HALVREN_RP3_bf_candidate_manifest.json', 'w'), indent=1)
for b in sorted(glob.glob(W + '/hb/cand/*_build.json')):
    r = jl(b); i = r['id']; tag = i.split('-', 1)[1]; c = 'c1' if i.startswith('HVC1') else 'c2'
    side = dict(id=i, race='Halvren', configuration=c, tag=tag, status='SOURCE CANDIDATE - NOT accepted, NOT frozen (Halvren body / face source order)', definition='HV_source_definitions.json %s (body %s, face %s)' % (DEF['version'], tag[:3], tag[3:] or 'current'),
                construction=('tools/rac/w1/build_variant.py: HVC1_build.json + c1_%s.json' % tag) if c == 'c1' else ('tools/rac/w1/build_variant.py: MF-F-R_build.json + c2_%s.json (the HVF178 route)' % tag),
                overrides=r['overrides'], height_macro=r['height_macro'], height_solve=r.get('height_solve'), stature_r6=r['stature_r6'],
                r6_sha256=sha('%s/r6/%s_r6.npz' % (RA, i)), build_sha256=sha('%s/builds/%s_build.json' % (RA, i)), pelvis='held: no pelvic target or bone scale (order §16); ratio deltas are the stature / leg coupling only',
                ear='family human auricle, non-final (ears locked)')
    if i in TS: side['family'] = man['candidates'][i]
    json.dump(side, open('%s/sources/%s_source_sidecar.json' % (E, i), 'w'), indent=1)
print('manifest', len(man['candidates']), 'production', list(man['production']), det)
