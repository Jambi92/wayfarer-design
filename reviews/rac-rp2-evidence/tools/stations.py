# stations.py : identity station readings on identical front / profile silhouettes (10 px/cm), E3 vs H (adjudicated target) vs production.
import numpy as np, json, sys
fs=sys.argv[1:]; sys.argv=['x','cand_v001.npz','/tmp/t.json']
exec(open('/tmp/claude-0/rp2/tools/gate_t367.py').read().split('out = {}')[0])
H=np.load(R+'hstar.npz'); P=np.load(R+'cand_v001.npz')
def read(V,Q):
    s=sil(V,Q,'front',ppc=10,ss=4); p=sil(V,Q,'profile',ppc=10,ss=4); Hh=s.shape[0]
    row=lambda img,zc: img[int(Hh-(zc+2)*10)]
    out={}
    for zc in (100,110,120,135,150,165,180):           # front half-widths of the trunk band at the midline-connected run
        r=row(s,zc); c=600; L=c; Rr=c
        while r[L-1]: L-=1
        while r[Rr+1]: Rr+=1
        out['front_halfwidth_left_cm@%d'%zc]=round((c-L)/10,2); out['front_halfwidth_right_cm@%d'%zc]=round((Rr-c)/10,2)
        rp=row(p,zc); nz=np.nonzero(rp)[0]; out['profile_depth_cm@%d'%zc]=round((nz.max()-nz.min())/10,2)
    def top(xc): col=s[:,int((xc+60)*10)]; return (Hh-np.nonzero(col)[0].min())/10-2
    for sgn,side in ((1,'left'),(-1,'right')):
        z10,z20=top(sgn*10),top(sgn*20)
        out['girdle_slope_deg_%s'%side]=round(float(np.degrees(np.arctan2(z10-z20,10))),2)
        out['shoulder_top_cm_%s@x20'%side]=round(z20,2)
    cols=np.nonzero(s[int(Hh-(160+2)*10)])[0]; out['front_span_cm@160 (incl arms)']=round((cols.max()-cols.min())/10,2)
    out['stature_cm']=round(float(V[:,2].max()-V[:,2].min()),3)
    return out
res={'E3':read(E3['V'],E3['Q']),'H_adjudicated':read(H['V'],H['Q']),'S_star_bilateral':read(SS['V'],SS['Q']),'production_v001':read(P['V'],P['Q'])}
json.dump(res,open(R+'evpkg/stations.json','w'),indent=1)
for k in res['E3']: print('%-34s'%k, *['%8s'%res[m][k] for m in res])
