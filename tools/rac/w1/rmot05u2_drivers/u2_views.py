# RM-OT-05U2 (READ-ONLY): annotated proposal views of the UNCHANGED 05U RETURN (no geometry is altered; these are not
# before/after views). Writes the RETURN in S3 vertex/face order plus three per-face label maps for q_render's palette:
#   CURRENT : 5 purple = current editable interface faces, 3 amber = protected faces touching the current frozen ring
#   PROPOSED: 5 purple = current interface, 1 red = proposed added source faces, 6 cyan = protected faces touching the
#             proposed new frozen ring (outside the extended region), 0 grey = remaining protected anatomy
#   DEFECTS : 7 pink = faces incident to the six reported upper-notch vertices, 9 orange = the two faces on each of the
#             05U V5 seam-outlier edges (theta -88.4 / s 8.0 and -85.7 / s 7.89), 5 purple = current interface
import sys, os, json, subprocess, numpy as np, trimesh
here = os.path.dirname(os.path.abspath(__file__)); RC = os.path.join(here, '..', 'rmot05r_drivers', 'r_compare.py')
s3p, retp, prop, out = sys.argv[1:5]; os.makedirs(out, exist_ok=True)
S = 'reviews/rac-rmot05s-evidence/repair/S3/'
s3 = trimesh.load(s3p, process=False); Vs = np.asarray(s3.vertices); Fs = np.asarray(s3.faces); lab = np.load(S + 'GO-05S-S3_face_labels.npy')
R = np.load(retp); ids = R['s3_vid1'] - 1; Vr = Vs.copy(); Vr[ids] = R['V']
inter = (lab == 4) | (lab == 5); P = np.load(os.path.join(prop, 'proposal_sets.npz')); J = json.load(open(os.path.join(prop, 'proposal_region.json')))
mesh = os.path.join(out, '_return_in_s3_order.obj')
with open(mesh, 'w') as f:
    f.write(''.join('v %.9g %.9g %.9g\n' % tuple(v) for v in Vr)); f.write(''.join('f %d %d %d\n' % tuple(x + 1) for x in Fs))
def touching(vs):
    m = np.zeros(len(Vs), bool); m[vs] = True; return m[Fs].any(1)
cur = np.zeros(len(Fs), int); cur[touching(P['current_frozen_ring']) & ~inter] = 3; cur[inter] = 5
region = inter.copy(); region[P['added_faces']] = True
pro = np.zeros(len(Fs), int); pro[touching(P['proposed_frozen_ring']) & ~region] = 6; pro[inter] = 5; pro[P['added_faces']] = 1
dfx = np.zeros(len(Fs), int); dfx[inter] = 5; dfx[touching(J['rule']['N0'])] = 7
e2f = {}
for i, fc in enumerate(Fs):
    for k in range(3): e2f.setdefault(tuple(sorted((int(fc[k]), int(fc[(k + 1) % 3])))), []).append(i)
for so in J['seam_outliers']: dfx[e2f[tuple(sorted(so['edge_s3_index0']))]] = 9
for n, L in (('current', cur), ('proposed', pro), ('defects', dfx)): np.save(os.path.join(out, '_labels_%s.npy' % n), L)
rows = lambda: ["CURRENT 05U RETURN: purple = editable interface, amber = protected faces on the current frozen ring|%s|%s" % (mesh, os.path.join(out, '_labels_current.npy')),
                "PROPOSED (not performed): red = added source faces (35), cyan = protected faces on the proposed new frozen ring, grey = stays protected|%s|%s" % (mesh, os.path.join(out, '_labels_proposed.npy')),
                "RESIDUAL DEFECTS on the 05U RETURN: pink = faces at the 6 upper-notch vertices, orange = faces on the 2 seam-outlier edges|%s|%s" % (mesh, os.path.join(out, '_labels_defects.npy'))]
POST = ['--box', '10', '45', '-28', '5', '148', '180', '--center', '27.5', '-10.5', '162', '--scale', '18', '--views', '0:0,20:0,330:0,0:-45', '--res', '560']
TOP = ['--box', '10', '45', '-28', '5', '148', '180', '--center', '28.9', '-13.3', '167.5', '--scale', '11', '--views', '0:0,20:0,330:0,0:-45', '--res', '560']
ARM = ['--box', '10', '60', '-30', '30', '140', '190', '--center', '31', '-1', '164', '--scale', '30', '--views', '180:0,90:0,0:0,135:10,45:10,180:-55', '--res', '480']
for name, cam, wire in (('P1_posterior_close_shaded', POST, 0), ('P2_posterior_close_wire', POST, 1), ('P3_upper_notch_zoom_wire', TOP, 1), ('P4_arm_context_incl_yaw45', ARM, 0)):
    subprocess.run([sys.executable, RC, '--out', os.path.join(out, name + '.png'), '--rows'] + rows() + ['--'] + cam + (['--wire', '1'] if wire else []), check=True)
os.remove(mesh)
