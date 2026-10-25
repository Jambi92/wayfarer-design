# symm.py PROD.npz OUT.json : side-split deviation (left x>0 / right x<0) and source-asymmetry preservation
# (distance of each mesh to its own mirror image, source vs production; the production must keep the source asymmetry)
import numpy as np, sys, json, igl
sys.path.insert(0,'/tmp/claude-0/rt'); from common import load_src
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
SV,SF=load_src(); dsp=np.load(sys.argv[1].replace('.npz','_dsp.npy')); dps=np.load(sys.argv[1].replace('.npz','_dps.npy'))
PS=np.vstack([V,V[Q].mean(1)])
st=lambda v: [float(np.median(v)),float(np.percentile(v,95)),float(v.max())]
R={}
for nm,ms,mp in (('left (x>0)',SV[:,0]>0,PS[:,0]>0),('right (x<0)',SV[:,0]<0,PS[:,0]<0)):
    R[nm]=dict(src_to_prod=st(dsp[ms]),prod_to_src=st(dps[mp]))
M=SV*np.array([-1,1,1.0])            # mirrored source vertices: distance to the source vs to the production surface
ds=np.sqrt(igl.point_mesh_squared_distance(M,SV,SF)[0])*10; dp=np.sqrt(igl.point_mesh_squared_distance(M,V,T)[0])*10
R['asymmetry_mirror_distance_mm']=dict(source=st(ds),production=st(dp),diff_p95_mm=float(np.percentile(np.abs(ds-dp),95)),diff_max_mm=float(np.abs(ds-dp).max()),note='mirrored source vertices measured against the source and against the production surface; matching statistics = source asymmetry preserved (no symmetrisation)')
json.dump(R,open(sys.argv[2],'w'),indent=1); print(json.dumps(R))
