import numpy as np, igl, json, sys
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); F=w['F'].astype(np.int64)
target=float(sys.argv[1]) if len(sys.argv)>1 else 0.6
xs=np.arange(-34.0,-31.9,0.02); zs=np.array([92.45,92.75,93.1,93.45,93.85]); ys=np.arange(-41.6,-40.0,0.01)
G=np.array([[x,y,z] for x in xs for z in zs for y in ys])
out=(igl.fast_winding_number(S,F,G)<0.5).reshape(len(xs),len(zs),len(ys))
res=[]
for j,z in enumerate(zs):
    cols=[]
    for i in range(len(xs)):
        o=out[i,j,:]
        if o.any() and not o[0] and not o[-1]:
            yy=ys[o]; cols.append((xs[i],(np.ptp(yy)+0.01)*10,yy.mean()))
    # contiguous from the smallest x; find the largest x whose gap >= target
    cols=sorted(cols); run=[cols[0]]
    for cc in cols[1:]:
        if abs(cc[0]-run[-1][0]-0.02)<1e-6: run.append(cc)
        else: break
    cols=run; good=[c for c in cols if c[1]>=target]
    tipx=max(c[0] for c in cols); pick=max(good,key=lambda c:c[0]) if good else None
    res.append(dict(z=float(z),tip_x=round(float(tipx),3),crease=[round(float(pick[0]),3),round(float(pick[2]),3),float(z)] if pick else None,gap_mm=round(float(pick[1]),2) if pick else None))
    print(res[-1])
json.dump(res,open('/tmp/claude-0/crease06.json','w'))
