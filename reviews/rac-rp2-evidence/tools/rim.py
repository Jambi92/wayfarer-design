import numpy as np, igl, sys
S=np.load('sstar.npz'); SV=S['V'].astype(float); ST=np.r_[S['Q'][:,[0,1,2]],S['Q'][:,[0,2,3]]]
for f in sys.argv[1:]:
    D=np.load(f); V=D['V'].astype(float); T=np.r_[D['Q'][:,[0,1,2]],D['Q'][:,[0,2,3]]]
    N=igl.per_vertex_normals(V,T); d2,fi,cp=igl.point_mesh_squared_distance(V,SV,ST); FN=-igl.per_face_normals(SV,ST,np.array([0.,0,1])); d=10*np.sqrt(d2)*np.sign(((V-cp)*FN[fi]).sum(1))
    rim=np.abs(N[:,1])<0.1
    # outward sign: compare to stature change sign; report raw
    print(f,'all med %.3f | rim med %.3f p10 %.3f p90 %.3f | mean curvature-ish'%(np.median(d),np.median(d[rim]),np.percentile(d[rim],10),np.percentile(d[rim],90)))
