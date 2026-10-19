import numpy as np, json, sys
# usage: hidebox.py side cx cy cxw czw sx sz  (cursor at world (cxw,czw) -> pixel (cx,cy) in Front view)
side=sys.argv[1]; cx,cy,cxw,czw,sx,sz=map(float,sys.argv[2:8])
z=np.load('ui_cur.npz');U=z['V']
mv={int(k) for k in json.load(open('ui_moves_e30.json'))}
ids=[k for k in mv if (U[k,0]>0)==(side=='L')]
px=cx+(U[:,0]-cxw)*sx; pz=cy-(U[:,2]-czw)*sz
p=px[ids];q=pz[ids]
def edge(vals, lo, hi, other, olo, ohi):
    best=None
    for e in np.arange(lo,hi+0.01,1.0):
        m=(other>olo-30)&(other<ohi+30)
        d=np.abs(vals[m]-e).min()
        if best is None or d>best[0]: best=(d,e)
    return best
bx0=edge(px,p.min()-40,p.min()-3,pz,q.min(),q.max())
bx1=edge(px,p.max()+3,p.max()+40,pz,q.min(),q.max())
by0=edge(pz,q.min()-40,q.min()-3,px,p.min(),p.max())
by1=edge(pz,q.max()+3,q.max()+40,px,p.min(),p.max())
print('margins px',bx0[0],bx1[0],by0[0],by1[0])
B=[bx0[1],by0[1],bx1[1],by1[1]]; print('box',B)
ins=(px>B[0])&(px<B[2])&(pz>B[1])&(pz<B[3])
print('visible',ins.sum(),'median',U[ins].mean(0).round(3))
json.dump(dict(box=B,vis=np.where(ins)[0].tolist()),open('hide_%s.json'%side,'w'))
