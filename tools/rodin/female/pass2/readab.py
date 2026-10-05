# silhouette difference vs the male reference (identical orthographic cameras) and gameplay-distance thumbnails
import numpy as np, json
from PIL import Image
R='/tmp/claude-0/rodin/v4/R/'
J=['p1','a_tr','a_pv','A','B','C','D','E','E2']
V=['front','profile','rear34','tq']
def mask(j,v): return np.array(Image.open(R+'%s_%s.png'%(j,v)).convert('RGBA'))[:,:,3]>127
out={}
for v in V:
    m0=mask('m_ref',v); a0=m0.sum()
    for j in J:
        m=mask(j,v); out.setdefault(j,{})[v]=dict(xor_pct=100*float((m^m0).sum())/a0, area_pct=100*(float(m.sum())/a0-1))
for j in J: print(j,' '.join('%s xor %.2f%% area %+.2f%%'%(v,out[j][v]['xor_pct'],out[j][v]['area_pct']) for v in V))
json.dump(out,open('/tmp/claude-0/rodin/v4/readab.json','w'),indent=1)
# gameplay thumbnails: body ~ 96 px tall (front/rear: 187.9 cm in a 216 cm frame at 600 px -> 522 px tall; scale 0.184)
for j in ['m_ref']+J:
    for v in ('front','profile','rear34'):
        im=Image.open(R+'%s_%s.png'%(j,v)).convert('RGBA'); s=96/522.0 if v!='profile' else 96/522.0*268/216
        sm=im.resize((max(1,int(600*s)),max(1,int(600*s))),Image.LANCZOS)
        sm.resize((600,600),Image.NEAREST).save(R+'%s_g%s.png'%(j,v))
        a=np.array(sm)[:,:,3]; sil=np.zeros(a.shape+(4,),np.uint8); sil[...,3]=a; sil[...,:3]=235
        Image.fromarray(sil).resize((600,600),Image.NEAREST).save(R+'%s_s%s.png'%(j,v))
