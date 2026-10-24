# digit_radii.py MESH : median radius and visible length per finger (left/right hands) + toe forefoot width/height
import sys,numpy as np; sys.path.insert(0,'/tmp/claude-0/src3d/tools')
from digits import segment, frames
d=np.load(sys.argv[1]); V=d['V']; F=d['Q'].astype(np.int64)
out=[]
for sg,seed in ((1,(28.5,2.0,104.0)),(-1,(-29.5,2.0,104.0))):
    idx=np.nonzero((sg*V[:,0]>18)&(V[:,2]<108)&(V[:,2]>60))[0]
    D,_=segment(V,F,idx,np.array(seed),min_pers=1.0)
    for g in sorted(D,key=lambda g:-V[g['idx']][np.argmax(g['d'])][1]):
        fr=frames(V,g); out.append('%.2f/%.1f'%(np.median(fr['R'][(fr['s']>0.15)&(fr['s']<0.85)]),g['L']))
for sg in (1,-1):
    m=(sg*V[:,0]>3)&(V[:,2]<16)&(V[:,1]>17)
    out.append('toes L%s: vol-proxy %.0f zmax %.2f fmax %.2f'%('L' if sg>0 else 'R',m.sum(),V[m,2].max(),V[m,1].max()))
print(' '.join(out))
