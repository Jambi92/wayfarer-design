# va_freeze_promote.py EVIDIR REVERIFY.json : Vael final author acceptance / freeze-by-record closure order (2026-10-29) §6-§8 -- promotes
# VAEL_RP3_FREEZE_CANDIDATE.json to the authoritative VAEL_RP3_FREEZE.json with record / status edits only (no geometry, no blend resave).
# Requires the verification-only re-read-back (va_freeze_verify.py on the E: copies) to equal the recorded read-back.
import sys, json, hashlib
EV, RV = sys.argv[1:3]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
C = EV + '/VAEL_RP3_FREEZE_CANDIDATE.json'; rec = json.load(open(C)); RB = json.load(open(EV + '/VAEL_RP3_freeze_readback.json')); RR = json.load(open(RV))
ACC = {'VA_M_REF_RP3_v001.blend': ('42f0cebbf9588bb9acc7fd7746ff804f84fa104cf2d672285372375af2de855b', '887c93176058ddc007de28f3cfab47a50cc409c969ab9cfb2be4f5d68e410719'),
       'VA_F_REF_RP3_v001.blend': ('516b18e8933a2d33f62cf51472408d9588af2c23179ff7b2f5119775dd75bc3a', None)}
FACE = 'f8367ab09385d218559b6d3cac52ed159a9249cf12d91807e93e3b095d9ac297'
chk = dict(reverify_equals_recorded_readback=RR == RB, reverify_all_pass=RR['all_pass'])
for f, (s, g) in ACC.items():
    v = rec['files'][f]; chk[f] = dict(sha256_equals_accepted=v['sha256'] == s, geometry_hash_equals_accepted=(g is None or v['geometry_hash'] == g), face_topology_equals_accepted=v['face_topology_hash'] == FACE,
                                       verts=v['verts'] == 59076, quads=v['quads'] == 59074)
ok = all(x if isinstance(x, bool) else all(x.values()) for x in chk.values())
if not ok: print('PROMOTION BLOCKED', json.dumps(chk, indent=1)); sys.exit(1)
only_open = all((not v['deformation']['poses_worse_than_family']) or v['deformation']['poses_worse_than_family'] == ['neck_rot45'] for v in rec['files'].values())
assert only_open and set(rec.get('open_items', {})) == {'VA_M_REF_RP3_v001.blend'}, 'candidate carries an open item other than the accepted c1 neck_rot45 fold'
rec['record'] = 'VAEL RP3 FINAL PASS — AUTHOR ACCEPTED / FROZEN'
rec['date'] = '2026-10-29'
rec['authority'] = 'reviews/chatgpt-rac-rp3-vael-final-author-acceptance-freeze-closure-order.md (author review of Claude return 4df3e0c); parent reviews/chatgpt-rac-rp3-vael-final-consolidation-freeze-order.md'
rec['freeze_method'] = ('freeze-by-record through RECORD PROMOTION after author acceptance of VAEL-CF-EARROOT-1: VAEL_RP3_FREEZE_CANDIDATE.json (4df3e0c) promoted with status / carry-forward edits only; '
                        'no geometry / topology rebuild; both production .blend files byte-identical to the read-back of 4df3e0c (not re-saved); this record is authoritative over the sidecar / embedded RAC_status strings')
rec['promotion'] = dict(candidate_record='reviews/rac-rp3-evidence/vael_rp3_final/VAEL_RP3_FREEZE_CANDIDATE.json', candidate_sha256=sha(C),
                        verification_only=dict(file='VAEL_RP3_freeze_reverify.json', sha256=sha(RV), **chk), edits=['record', 'date', 'authority', 'freeze_method', 'promotion', 'carry_forward', 'accepted_residuals',
                        'accepted_diagnostic_notes', 'author_decision', 'open_items (resolved)', 'gate_pass_by_file / all_gates_pass (with the accepted carry-forward)', 'not_done'])
cf = rec['carry_forward']; cf['carried'] = ['VAEL-CF-SHOULDER-1', 'VAEL-CF-EARROOT-1']; cf['new_ids'] = ['VAEL-CF-EARROOT-1']
cf['VAEL_CF_EARROOT_1'] = dict(configuration='c1 / VA_M_REF_RP3_v001', pose='neck_rot45', item='one new fold pair on two left ear-cuff quads at the lobe / root junction under carried MPFB weights',
                               measured=rec['open_items']['VA_M_REF_RP3_v001.blend']['neck_rot45'], rest_dihedral_deg=112, posed_dihedral_deg=155, flips=0, contacts=0, root_inversions=0, c2='clean',
                               ear_readiness='0 / 0 / 0 on all 8 dedicated poses (both configurations)', cause='affected vertices carry ~1.0-1.6 % neck_01 weight instead of moving rigidly with the skull',
                               diagnostic_proof='ear branch bound 100 % to head: all 18 Standard v1 poses equal the family realization (diagnostics/deform_VAL4-R1-VD2-VF2_rigid_head_ear_weights.json)',
                               classification='RIG / WEIGHT / EAR-ROOT CORRECTIVE CARRY-FORWARD (production rig / skin-weighting stage); not a source or topology blocker',
                               required_production_action=['bind the Vael external-ear branch effectively rigidly to the head / skull', 'remove the inherited neck-weight tail from the external ear / root cuff', 'revalidate neck rotation', 'preserve the accepted RI3 root / concha geometry'])
rec['accepted_residuals']['c1_neck_rot45_ear_cuff_fold'] = dict(id='VAEL-CF-EARROOT-1', note='classified rig / weight stage, non-topology-blocking (author ruling 2026-10-29)')
rec['accepted_residuals']['unmasked_source_vs_new_ear_anatomy'] = 'expected source-vs-new-ear divergence localised to the ear (VAEL_unmasked_anatomy_localisation.json)'
rec['accepted_residuals']['branch_face_placeholder_UV'] = 'ear branch faces carry a zero placeholder UV (UV / materials out of scope)'
rec['author_decision'] = dict(resolved='VAEL FINAL CONSOLIDATION NEEDS AUTHOR DECISION (4df3e0c) resolved by author acceptance of VAEL-CF-EARROOT-1',
                              rulings=['RI3 geometry, VAEL_EAR_BRANCH_TOPOLOGY_v002 and the source body are not implicated', 'register VAEL-CF-EARROOT-1; preserve VAEL-CF-SHOULDER-1', 'do not reopen RI3; do not modify the production blends'])
rec['resolved_open_items'] = rec.pop('open_items')
def ok_file(v):
    d = v['deformation']; exc = set(d['excess_over_marchfolk_gt5']) - ({'shoulder_flex90_l'} if v['configuration'] == 'c1' else set())
    rest = [x for x in d['poses_worse_than_family'] if not (v['configuration'] == 'c1' and x == 'neck_rot45')]
    return not exc and not rest
rec['gate_pass_by_file'] = {k: (rec['gate_pass_by_file'][k] or ok_file(v)) and ok_file(v) for k, v in rec['files'].items()}
rec['gate_pass_note'] = 'all gates pass with the registered carry-forwards VAEL-CF-SHOULDER-1 (c1 shoulder_flex90 +6) and VAEL-CF-EARROOT-1 (c1 neck_rot45 cuff fold); every other check unchanged from the candidate record'
rec['all_gates_pass'] = all(rec['gate_pass_by_file'].values()) and rec['readback']['all_pass'] and rec['gates']['ear_firewall_all_hold'] and rec['gates']['probes_all_clean'] and rec['ear_branch']['face_topology_identical_c1_c2']
rec['not_done'] = ['production ear rigging (VAEL-CF-EARROOT-1 and VAEL-CF-SHOULDER-1 owned by production rigging)', 'creator morphs', 'final UV / materials', 'LODs', 'UE5 integration', 'low-light physiology (not decided)',
                   'Halvren (next; not started)', 'no universal elf anatomy / topology declared']
assert rec['all_gates_pass'], 'promotion inconsistent'
json.dump(rec, open(EV + '/VAEL_RP3_FREEZE.json', 'w'), indent=1); print('VAEL_RP3_FREEZE.json', sha(EV + '/VAEL_RP3_FREEZE.json'), rec['gate_pass_by_file'])
