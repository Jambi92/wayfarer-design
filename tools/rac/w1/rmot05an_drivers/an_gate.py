# 05AN checkpoint gate. Usage: an_gate.py CHECKPOINT.blend PREV_VF.npz OUT_PREFIX
# geometry gates vs the immediately preceding saved state (same topology): seams, SI, flips, degenerates, 1/0/0, protected;
# cumulative vs the frozen 05AL baseline: displacement, segment mean radius, joint drift, orientation (flip vs 05AL reference for
# triangles that exist there, own pre-step reference for rotated triangles) with crimp-resolution classification.
import sys, json, subprocess, numpy as np, scipy.sparse as sp
sys.path.insert(0,'/home/claude/an'); sys.path.insert(0,'/home/claude/al')
import anmetrics as AM, predict_an as PA
from predict2 import nrm
blend, prev, pre = sys.argv[1:4]
subprocess.run(['bash','/home/claude/ag/gates.sh',prev,blend,pre],stdout=open(pre+'_gates.log','w'),stderr=subprocess.STDOUT)
G=json.load(open(pre+'_gates.json'))
V=np.load(pre+'_VF.npz')['V']; F=np.load(prev)['F']; VP=np.load(prev)['V']
R=dict(vs_previous={k:G.get(k) for k in ['topology_identical','pairs_opened_gt_0_01mm','self_intersecting_faces','flipped_faces','degenerate_faces','position_welded_ac1','protected_max_disp_mm','height_cm','bbox_extent_cm','flip_sites_cm']})
VB=AM.V0; Rg=np.load('/home/claude/aj/regions_05AI.npz'); d=np.linalg.norm(V-VB,axis=1)*1000
R['cumulative_vs_05AL']=AM.cum(V); R['regions_max_mm']={k:round(float(d[Rg[k]].max()),4) for k in Rg.files if Rg[k].size}
R['segment_mean_radius_change_pct']=AM.radius(V); R['joint_centre_drift_mm']=AM.joints(V)
di=np.linalg.norm(V-VP,axis=1)*1000; m=AM.limb&(di>0.01); R['incremental']=dict(median=round(float(np.median(di[m])),3),p95=round(float(np.percentile(di[m],95)),3),max=round(float(di[AM.limb].max()),3)) if m.any() else {}
ref,isnew=PA.reference(F,np.load('/home/claude/an/start_VF.npz')['V'] if F.shape==np.load('/home/claude/an/start_VF.npz')['F'].shape else VP)
vf=sp.csr_matrix((np.ones(F.size),(F.ravel(),np.repeat(np.arange(len(F)),3))),shape=(len(V),len(F)))
dot=(nrm(V,F)*ref).sum(1); fl=np.flatnonzero(dot<0); rb=PA.ringang(VB,F,vf); rn=PA.ringang(V,F,vf)
R['orientation_vs_05AL']=dict(reference_flips=[dict(face=int(f),base_ring_angle=round(float(rb[f]),1),now_ring_angle=round(float(rn[f]),1),cls=('CRIMP_RESOLVED' if rb[f]>60 and rn[f]<30 else 'INVERSION')) for f in fl],
    local_inversions_now=int((rn>90).sum()), local_inversions_base=int((rb>90).sum()))
json.dump(R,open(pre+'_an_gate.json','w'),indent=1); print(json.dumps(R))
