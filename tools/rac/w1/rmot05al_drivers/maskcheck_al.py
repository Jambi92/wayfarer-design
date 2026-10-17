# Read back .sculpt_mask from a staged blend; verify geometry identical to the 05AJ preflight baseline; report protection + joint/belly stats.
import sys, numpy as np, bpy, json
blend=sys.argv[1]; out=sys.argv[2]
bpy.ops.wm.open_mainfile(filepath=blend)
o=[x for x in bpy.data.objects if x.type=='MESH'][0]; me=o.data
V=np.zeros(len(me.vertices)*3); me.vertices.foreach_get('co',V); V=V.reshape(-1,3); W=np.array(o.matrix_world); V=V@W[:3,:3].T+W[:3,3]
B=np.load(sys.argv[3])['V']; geo=float(np.linalg.norm(V-B,axis=1).max()*1000)
M=np.zeros(len(V)); me.attributes['.sculpt_mask'].data.foreach_get('value',M); np.save(out.replace('.json','.npy'),M)
P=np.load('/home/claude/ag/protected_05AF.npz'); R=np.load('/home/claude/aj/regions_05AI.npz')
res=dict(geometry_max_dev_mm_vs_base=geo)
res['protected']={k:dict(min=round(float(M[P[k]].min()),3),n_lt1=int((M[P[k]]<1).sum())) for k in P.files}
res['regions_05AI']={k:dict(min=round(float(M[R[k]].min()),3),n_lt1=int((M[R[k]]<1).sum())) for k in ['torso','glute','pelvis_other']}
Wt=np.load('/home/claude/af/weights_05AE.npz'); names=[str(x) for x in Wt['names']]; o2n=np.load('/home/claude/af/old_to_new_05AE_to_05AF.npy'); lab=np.full(len(V),-1); lab[o2n]=Wt['W'].argmax(1)
z0=B[:,2].min(); Z=(B[:,2]-z0)*100
J={'elbow_L':(32.6,137.4,'upperarm_L','forearm_L'),'elbow_R':(-29.6,133.7,'upperarm_R','forearm_R'),'knee_L':(21.2,55.3,'thigh_L','shin_L'),'knee_R':(-18.2,55.2,'thigh_R','shin_R'),'ankle_L':(25.2,9.2,'shin_L','foot_L'),'ankle_R':(-22.1,9.1,'shin_R','foot_R'),'wrist_L':(36.9,117.2,'forearm_L','hand_L'),'wrist_R':(-34.7,113.0,'forearm_R','hand_R')}
res['joints']={}
for k,(x,z,a,b) in J.items():
    m=np.isin(lab,[names.index(a),names.index(b)])&(np.abs(Z-z)<2.5); res['joints'][k]=round(float(M[m].mean()),3)
res['bellies']={}
for k,(zlo,zhi,parts) in {'biceps_L':(140,150,['upperarm_L']),'biceps_R':(137,147,['upperarm_R']),'forearm_L':(122,132,['forearm_L']),'forearm_R':(118,128,['forearm_R']),'thigh_L':(62,90,['thigh_L']),'thigh_R':(62,90,['thigh_R']),'calf_L':(22,45,['shin_L']),'calf_R':(22,45,['shin_R'])}.items():
    m=np.isin(lab,[names.index(p) for p in parts])&(Z>zlo)&(Z<zhi); res['bellies'][k]=dict(mean=round(float(M[m].mean()),3),sculptable_share=round(float((M[m]<0.5).mean()),3))
for p in ['upperarm','forearm','thigh','shin']:
    m=np.isin(lab,[names.index(k) for k in names if k.startswith(p)]); res.setdefault('limb_sculptable_share',{})[p]=round(float((M[m]<0.5).mean()),3)
json.dump(res,open(out,'w'),indent=1); print(json.dumps(res,indent=0))
