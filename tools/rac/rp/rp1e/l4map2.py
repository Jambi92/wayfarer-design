import numpy as np,sys
# map L4 quads -> cage faces assuming blender subsurf ordering (each cage n-gon -> n*4^(L-1) consecutive quads)
def l4face(cageF,L=4):
    n=(cageF>=0).sum(1); cnt=n*4**(L-1); return np.repeat(np.arange(len(cageF)),cnt)
if __name__=='__main__':
    c=np.load(sys.argv[1]); p=np.load(sys.argv[2]); fm=l4face(c['F'])
    print(len(fm), len(p['Q']))
    cen=p['V'][p['Q']].mean(1); cc=np.array([c['V'][f[f>=0]].mean(0) for f in c['F']])*np.array([1,-1,1])
    d=np.linalg.norm(cen-cc[fm],axis=1); print('dist med/max',np.median(d),d.max())
