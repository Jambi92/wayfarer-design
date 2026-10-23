import numpy as np, sys
def vdihedral(V,Q):
    T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
    # use quad normals (average of 2 tris)
    n1=np.cross(V[Q[:,1]]-V[Q[:,0]],V[Q[:,2]]-V[Q[:,0]]); n2=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,0]]); N=n1+n2; N/=np.linalg.norm(N,axis=1)[:,None]
    E=np.vstack([np.c_[Q[:,[i,(i+1)%4]],np.arange(len(Q))] for i in range(4)]); key=np.sort(E[:,:2],1)
    o=np.lexsort((key[:,1],key[:,0])); k=key[o]; f=E[o,2]; same=(k[1:]==k[:-1]).all(1)
    a=f[:-1][same]; b=f[1:][same]; ed=k[:-1][same]
    ang=np.degrees(np.arccos(np.clip((N[a]*N[b]).sum(1),-1,1)))
    vd=np.zeros(len(V)); np.maximum.at(vd,ed[:,0],ang); np.maximum.at(vd,ed[:,1],ang)
    return vd, ed, ang
if __name__=='__main__':
    z=np.load(sys.argv[1]); vd,_,_=vdihedral(z['V'],z['Q']); np.save(sys.argv[2],vd)
