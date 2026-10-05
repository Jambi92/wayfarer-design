import numpy as np, json
from PIL import Image
R='/tmp/claude-0/rodin/v4/R/'; PX=216/600.0   # cm per px in the front view
def runw(j):
    a=np.array(Image.open(R+'%s_front.png'%j).convert('RGBA'))[:,:,3]>127
    rows=np.where(a.any(1))[0]; top,bot=rows.min(),rows.max(); H=(bot-top)*PX
    cx=300; W=np.zeros(600)
    for r in range(600):
        if not a[r,cx]: continue
        l=cx
        while l>0 and a[r,l-1]: l-=1
        rr=cx
        while rr<599 and a[r,rr+1]: rr+=1
        W[r]=(rr-l+1)*PX
    u=(bot-np.arange(600))*PX*187.881/H
    return u,W
out={}
for j in ['m_ref','p1','a_tr','a_pv','A','B','C','D','E','E2']:
    u,W=runw(j); g=lambda a,b,f: f(W[(u>a)&(u<b)])
    sh=g(140,152,np.max); wa=g(104,124,np.min); hp=g(84,98,np.max); uw=u[(u>104)&(u<124)][np.argmin(W[(u>104)&(u<124)])]
    out[j]=dict(shoulder=sh,waist=wa,hip=hp,waist_u=float(uw),waist_sh=wa/sh,hip_sh=hp/sh,waist_hip=wa/hp)
    print(j,'sh %.1f waist %.1f @%.0f hip %.1f  w/sh %.3f hip/sh %.3f w/hip %.3f'%(sh,wa,uw,hp,wa/sh,hp/sh,wa/hp))
json.dump(out,open('/tmp/claude-0/rodin/v4/torsosil.json','w'),indent=1)
