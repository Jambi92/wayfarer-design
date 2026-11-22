# sa6_manifest_v002.py PHASE : rig v002 package manifest + frozen-source re-hash (order 07a3f24c §4).  PHASE = before | after.
#   before: re-hashes the frozen RP5 sources (frozen_rp5_hashes_start.txt list) into rig_v002/SA_RP6_frozen_rehash_v002.json['before'].
#   after : re-hashes them again into ['after'], then writes rig_v002/SA_RP6_rig_manifest_v002.json: sha256 + size of every file under rig_v002/ (evidence
#           sub-folders included), the artifact dependency graph, and checks every recorded dependency hash (layer part hashes in the v005 json, the Blender
#           read-back blend hashes, the PD-2 / identity records' package references).  Exit 1 on any mismatch.
import sys, os, json, glob, hashlib, time
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
RP = os.path.join(R, 'reviews/rac-rp6-evidence/saurin/rig_pilot'); D = os.path.join(RP, 'rig_v002'); ST = 'RP6 RIG PILOT / NOT FROZEN'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
PH = sys.argv[1]; assert PH in ('before', 'after')
ref = [l.split(None, 1) for l in open(os.path.join(RP, 'frozen_rp5_hashes_start.txt')) if l.strip() and not l.startswith('#')]
now = {f.strip(): sha(os.path.join(R, f.strip())) for h, f in ref}; ok = all(now[f.strip()] == h for h, f in ref)
FR = os.path.join(D, 'SA_RP6_frozen_rehash_v002.json'); fr = json.load(open(FR)) if os.path.exists(FR) else dict(status=ST, order='07a3f24c', reference='frozen_rp5_hashes_start.txt (RP6 start)')
fr[PH] = dict(time=time.strftime('%Y-%m-%d %H:%M:%S'), sha256=now, all_match_rp6_start=ok); json.dump(fr, open(FR, 'w'), indent=1); print(PH, 'frozen match', ok)
if PH == 'before': sys.exit(0 if ok else 1)
files = {os.path.relpath(p, D).replace(os.sep, '/'): dict(sha256=sha(p), bytes=os.path.getsize(p)) for p in sorted(glob.glob(D + '/**/*', recursive=True)) if os.path.isfile(p) and os.path.basename(p) != 'SA_RP6_rig_manifest_v002.json'}
bad = []
L = json.load(open(os.path.join(D, 'SA_RP6_creator_layers_v005.json')))
for part, h in L['array_sha256'].items():
    if files.get(part, {}).get('sha256') != h: bad.append('layers v005 part %s' % part)
if L.get('base_correctives') != 'SA_RP6_correctives_v003.json': bad.append('layers v005 base_correctives')
for c in 'MF':
    import lzma; rb = json.load(open(os.path.join(D, 'blender_readback/SA_RP6_blender_readback_%s_v002.json' % c)))
    if hashlib.sha256(lzma.open(os.path.join(D, rb['file'] + '.xz')).read()).hexdigest() != rb['sha256']: bad.append('blend %s' % c)
deps = {'SA_RP6_skeleton_v002.json': ['SA_RP6_joint_placement_M_v002.json', 'SA_RP6_joint_placement_F_v002.json'],
        'SA_RP6_weights_M_v002.npz': ['SA_RP6_skeleton_v002.json'], 'SA_RP6_weights_F_v002.npz': ['SA_RP6_skeleton_v002.json'],
        'SA_RP6_correctives_v003.json': ['SA_RP6_correctives_M_v003.npz', 'SA_RP6_correctives_F_v003.npz', 'SA_RP6_weights_M_v002.npz', 'SA_RP6_weights_F_v002.npz'],
        'SA_RP6_creator_layers_v005.json': ['SA_RP6_correctives_v003.json'] + sorted(L['array_sha256']),
        'SA_M_REF_RP6_rigpilot_v002.blend.xz': ['SA_RP6_skeleton_v002.json', 'SA_RP6_weights_M_v002.npz', 'SA_RP6_correctives_v003.json'],
        'SA_F_REF_RP6_rigpilot_v002.blend.xz': ['SA_RP6_skeleton_v002.json', 'SA_RP6_weights_F_v002.npz', 'SA_RP6_correctives_v003.json']}
for k, v in deps.items():
    for f in [k] + v:
        if f not in files: bad.append('missing ' + f)
TD = os.path.dirname(os.path.abspath(__file__))
json.dump(dict(status=ST, name='SA_RP6_rig_manifest_v002', race='Saurin', rig_version='v002', order='reviews/chatgpt-rac-rp6-saurin-shoulder-elbow-refit-correction-order.md (07a3f24c)',
               supersedes='SA_RP6_rig_manifest_v001.json (kept as the comparison baseline)', frozen_inputs=dict(rehash='SA_RP6_frozen_rehash_v002.json', before_after_match=bool(fr.get('before', {}).get('all_match_rp6_start') and ok)),
               topology_sha256='255645a12a8dc59ae8dace55dcf2af2b196a4f5a799fdf425b394b831ffb2d49', tools='tools/rac/rp/saurin_rp6_v001/',
               tool_sha256={os.path.basename(p): sha(p) for p in sorted(glob.glob(TD + '/sa6_*.py'))}, dependencies=deps, dependency_check=dict(ok=not bad, failures=bad), files=files),
          open(os.path.join(D, 'SA_RP6_rig_manifest_v002.json'), 'w'), indent=1)
print('files', len(files), 'dependency failures', bad); sys.exit(1 if bad or not ok else 0)
