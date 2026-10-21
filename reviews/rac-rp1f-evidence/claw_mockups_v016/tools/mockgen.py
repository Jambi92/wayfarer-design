# mockups: build claw targets for one hand per variant and splice them into v014 for rendering only (not production)
import json, numpy as np, subprocess, sys
d=json.load(open('hand_sdf.json')); h=json.load(open('hand_frames.json'))
var={
 'A_scaled_sheath': dict(root=0.9,depth=0.35,ext=0.9,hook=0.45,arch=0.15,r0=0.5,lat=0.6,taper=0.7,rtip=0.02,k=0.15,blur=0.12),
 'B_thick_claw':    dict(root=0.8,depth=0.1,ext=1.4,hook=0.8,arch=0.3,r0=0.75,lat=0.6,taper=0.8,rtip=0.025,k=0.05,blur=0.15),
 'C_clawlike_nail': dict(root=1.0,depth=0.55,ext=0.5,hook=0.25,arch=0.05,r0=0.75,lat=0.75,taper=0.9,rtip=0.03,k=0.08,blur=0.0),
}
nails=['A_L17','A_L18','A_L19','A_L20','A_Lthumb']
out={}
for vn,v in var.items():
    for n in nails:
        p=dict(d[n]); s=1.15 if 'thumb' in n else 1.0
        q=dict(v); 
        for kk in ('root','depth','ext','hook','arch','r0'): q[kk]=v[kk]*s
        p.update(q); L=float(np.linalg.norm(np.array(h[n]['T'])-np.array(h[n]['C'])))
        p.update(half=2.4,h=0.04,c0back=round(0.3*L,3)); out[vn+'__'+n]=p
json.dump(out,open('mock2_sdf.json','w'),indent=1); print(len(out))
