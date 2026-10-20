import numpy as np, igl
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); F=w['F'].astype(np.int64)
c=np.array([-33,-40.8,93.2]); m=(np.linalg.norm(S[F].mean(1)-c,axis=1)<6); Fl=F[m]
xs=np.arange(-34.2,-31.9,0.05); zs=np.arange(91.6,94.6,0.05); ys=np.arange(-41.6,-40.0,0.02)
G=np.array([[x,y,z] for x in xs for z in zs for y in ys])
wn=igl.fast_winding_number(S,F,G).reshape(len(xs),len(zs),len(ys))
out=wn<0.5
tip=[]
for j,z in enumerate(zs):
    # columns x where some y in the band is outside (air) AND both y ends are inside or near walls: the slit
    opn=[i for i in range(len(xs)) if out[i,j,:].any() and not out[i,j,0] and not out[i,j,-1]]
    if not opn: continue
    # slit tip at this z: the largest x of a contiguous run starting from the smallest open x
    run=[opn[0]]
    for i in opn[1:]:
        if i==run[-1]+1: run.append(i)
        else: break
    i=run[-1]; ycol=ys[out[i,j,:]]; tip.append((round(z,2),round(xs[i],3),round(ycol.mean(),3),round(np.ptp(ycol)*10+0.2,2),round(xs[run[0]],2)))
for t in tip: print(t)
