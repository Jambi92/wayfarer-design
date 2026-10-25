# iou.py PROD.npz OUT.json [pxcm] : orthographic silhouette IoU source vs retopo (front, profile L/R, rear, 3/4 views)
import numpy as np, sys, json
from PIL import Image, ImageDraw
sys.path.insert(0,'/tmp/claude-0/rt'); from common import load_src
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
SV,SF=load_src(); px=float(sys.argv[3]) if len(sys.argv)>3 else 3.0
def sil(V,F,yaw):
    a=np.radians(yaw); R=np.array([[np.cos(a),-np.sin(a),0],[np.sin(a),np.cos(a),0],[0,0,1]])
    P=V@R.T; u=(P[:,0]+60)*px; v=(225-P[:,2])*px
    W,H=int(120*px),int(230*px); im=Image.new('1',(W,H),0); d=ImageDraw.Draw(im)
    for t in F:
        d.polygon([(u[t[0]],v[t[0]]),(u[t[1]],v[t[1]]),(u[t[2]],v[t[2]])],fill=1)
    return np.array(im,bool)
out={}
for name,yaw in (('front',0),('rear',180),('profile_left',90),('profile_right',-90),('q3_front_left',45),('q3_front_right',-45),('q3_rear_left',135),('q3_rear_right',-135)):
    a=sil(SV,SF,yaw); b=sil(V,T,yaw); i=(a&b).sum(); u=(a|b).sum()
    out[name]=dict(iou=float(i/u),src_px=int(a.sum()),prod_px=int(b.sum()),xor_px=int((a^b).sum()))
    Image.fromarray(np.stack([a*255,b*255,np.zeros_like(a,np.uint8)],2).astype(np.uint8)).save(sys.argv[2].replace('.json','_%s.png'%name))
    print(name,round(out[name]['iou'],5))
json.dump(dict(px_per_cm=px,views=out),open(sys.argv[2],'w'),indent=1)
