import json, numpy as np, sys
from featpts import tip_and_walls
D=json.load(open(sys.argv[2] if len(sys.argv)>2 else 'pdesign5.json')); S=float(sys.argv[1]) if len(sys.argv)>1 else 0.4
axes=[2,2,2,1,1,1,1,1]; arms=[True,True,True,True,True,True,False,False]
rows=[]
for k,(rw,ax,arm) in enumerate(zip(D['rows'],axes,arms)):
    P=[np.array(p) for p in rw['pts']]; lAR,tR,lBR,C,lBL,tL,lAL=P
    val=P[3][ax]
    new=[]
    for lA,t,lB in ((lAR,tR,lBR),(lAL,tL,lBL)):
        if arm:
            tip,w1,w2,_=tip_and_walls(ax,val,t,s=S)
            oth=[i for i in range(3) if i!=ax]; v=(0.5*(lA+lB)-tip)[oth]
            cr=lambda w:(w-tip)[oth][0]*v[1]-(w-tip)[oth][1]*v[0]
            lo,hi=(w1,w2) if np.sign(cr(w1))==np.sign(cr(lA)) else (w2,w1)
        else:
            lo=t+0.35*(lA-t); hi=t+0.35*(lB-t)
        new.append((lA,lo,hi,lB))
    (a1,b1,c1,d1),(a2,b2,c2,d2)=new
    pts=[a1,b1,c1,d1,C,d2,c2,b2,a2]
    cols=[11,11,9,9,9,9,9,10,10]
    rows.append(dict(pts=[p.round(3).tolist() for p in pts],cols=cols,sub=rw.get('sub',False)))
D['rows']=rows; json.dump(D,open('pdesign6.json','w'),indent=0)
for r in rows: print(np.array(r['pts'])[[0,1,2,3,4]].round(2).tolist())
