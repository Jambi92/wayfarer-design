# shading_audit.py : chest/abdomen band shading audit on identical workbench renders (front and back, centre z 135, half-size 22 cm).
import numpy as np, json
from PIL import Image; from scipy.ndimage import gaussian_filter, binary_erosion
R='/tmp/claude-0/rp2/ev/'; out={}
for v in ('front','back'):
    for m in ('e3_body','sstar','hstar','cand_v001'):
        a=np.array(Image.open(R+'tr_%s_%s.png'%(m,v)).convert('L'),float)
        bg=np.median(np.r_[a[:5].ravel(),a[-5:].ravel()]); mask=binary_erosion(np.abs(a-bg)>3,iterations=12)
        W=a.shape[1]; c=W//2; mask&=np.fliplr(mask)
        band=np.zeros_like(mask); band[int(a.shape[0]*0.15):int(a.shape[0]*0.85), int(W*0.3):int(W*0.7)]=True; mk=mask&band
        hf=a-gaussian_filter(a,4); lr=np.abs(gaussian_filter(a,3)-np.fliplr(gaussian_filter(a,3)))
        out['%s.%s'%(v,m)]=dict(hf_rms=float(np.sqrt((hf[mk]**2).mean())), lr_shading_asym_mean=float(lr[mk].mean()), lr_shading_asym_p95=float(np.percentile(lr[mk],95)), n_px=int(mk.sum()))
json.dump(out,open('/tmp/claude-0/rp2/evpkg/shading_audit.json','w'),indent=1)
for k,v in out.items(): print('%-20s hf_rms %.3f  L/R asym mean %.2f p95 %.2f'%(k,v['hf_rms'],v['lr_shading_asym_mean'],v['lr_shading_asym_p95']))
