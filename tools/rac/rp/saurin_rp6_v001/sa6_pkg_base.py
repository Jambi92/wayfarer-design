# sa6_pkg_base.py WORKDIR : base corrective package of rig v002 (order 07a3f24c §1-§2, §4): SA_RP6_correctives_v003.json + SA_RP6_correctives_{M,F}_v003.npz
#   in the rig's package folder (C.PKGDIR = EV6/rig_v002).  Same schema as SA_RP6_correctives_v002.json (sa6_pkg_v002.py: families with bone, parent-frame
#   axis, pivot, keys; pose keys with drivers), plus 'layer' / 'layer_params' on the elbow muscle families.  Arrays = the fit's CF_<c>.npz byte for byte.
import sys, os, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
assert C.RIGV == 'v002'
WD = sys.argv[1]; os.makedirs(C.PKGDIR, exist_ok=True); cj = {c: json.load(open(WD + '/CF_%s.json' % c)) for c in 'MF'}
for c in 'MF': shutil.copy(WD + '/CF_%s.npz' % c, C.PKGDIR + '/SA_RP6_correctives_%s_v003.npz' % c)
out = dict(status='RP6 RIG PILOT / NOT FROZEN', name='SA_RP6_correctives_v003', rig_version=C.RIGV,
           supersedes='SA_RP6_correctives_v002.json (rig v001; kept as the comparison record)', semantics=cj['M'].get('method', ''),
           arrays={c: 'SA_RP6_correctives_%s_v003.npz' % c for c in 'MF'}, array_sha256={c: C.sha(C.PKGDIR + '/SA_RP6_correctives_%s_v003.npz' % c) for c in 'MF'},
           source_sha256={c: C.sha(WD + '/CF_%s.json' % c) for c in 'MF'},
           configurations={c: dict(weights=os.path.basename(C.w_path(c)), weights_sha256=C.sha(C.w_path(c)), converged=cj[c].get('converged'),
                                   families=cj[c]['families'], pose_keys=cj[c]['pose_keys']) for c in 'MF'})
json.dump(out, open(C.PKGDIR + '/' + C.BASE_CORR, 'w'), indent=1)
print('base v003:', {c: (len(out['configurations'][c]['families']), len(out['configurations'][c]['pose_keys'])) for c in 'MF'})
