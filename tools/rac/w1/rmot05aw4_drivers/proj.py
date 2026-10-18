import numpy as np,sys,json; sys.path.insert(0,'/home/claude/aw1'); sys.path.insert(0,'/home/claude/aw1/aw4'); import aw1lib as L; from fields import multigeo
PL=np.load('plates.npy',allow_pickle=True).item(); FF=json.load(open('/home/claude/aw1/footframes.json'))
X2=np.load('/home/claude/aw1/aw2/real/GO-05AW2_nails_final_VF.npz')['V']
def proj(X):
    out={}
    for n,P in PL.items():
        a=np.array(FF[n[0]]['a']); nail=P['w']>0.3
        toe=P['dom']&(np.linalg.norm(X2-P['T'],axis=1)<0.03); d=multigeo(P['w']>0.03,0.003); pad=toe&~np.isfinite(d)
        out[n]=dict(projection_mm=round(float((X[nail]@a).max()-(X2[nail]@a).max())*1000,3), clear_mm=round(float((X[nail]@a).max()-(X[pad]@a).max())*1000,2))
    return out
if __name__=='__main__':
    for f in sys.argv[1:]: print(f,{k:v['projection_mm'] for k,v in proj(np.load(f)['V']).items()})
