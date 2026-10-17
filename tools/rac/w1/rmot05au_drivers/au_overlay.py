import json, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
V=np.load('/home/claude/at/final/ac3.npz')['V'].astype(float); F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; z0=V[:,2].min()
W=np.load('/home/claude/wayfarer-design/reviews/rac-w1i-evidence/geometry/GO_r6.npz',allow_pickle=True); Vw=W['V'].astype(float)/100; keep=W['keep'].astype(bool); Fw=W['F'][keep[W['F']].all(1)]; Vw[:,1]*=-1   # W1 faces +Y; flip to face -Y like AC3
J=json.loads(str(W['joints']))
R=json.load(open('au_measure_head_feet.json')); Hs=R['stature']['vertex_height_cm']/100
gm=json.load(open('/home/claude/wayfarer-design/reviews/rac-w1i-evidence/candidates/GO_meas.json'))['r6']; Hw_vertex=gm['cranio']['V'][2]/100  # kept geometry sole z = 0
s=Hs/Hw_vertex; Vw=Vw*s; Vw[:,2]+=z0
# horizontal alignment: front = body midline x; profile = pelvis centre y (AC3: mean of the two hip-blend rings; W1: pelvis joint)
Wv=np.load('/home/claude/ao/vgroups.npz'); names=list(Wv['names']); Wt=Wv['W']
ring=lambda a,b: V[(Wt[:,names.index(a)]>0.25)&(Wt[:,names.index(a)]<0.75)&(Wt[:,names.index(b)]>0.2)].mean(0)
pel=(ring('thigh_L','trunk')+ring('thigh_R','trunk'))/2
pw=np.array(J['pelvis'][0])/100; pw[1]*=-1; pw=pw*s
Vw[:,0]+= (0.007 - 0)               # AC3 body midline x = 0.70 cm (au_tail), W1 midline x = 0
Vw[:,1]+= pel[1]-pw[1]
def raster(Vx,Fx,ax2,box,res):
    img=Image.new('L',res,0); d=ImageDraw.Draw(img); (u0,u1),(v0,v1)=box
    U=(Vx[:,ax2[0]]-u0)/(u1-u0)*res[0]; Y=res[1]-(Vx[:,ax2[1]]-v0)/(v1-v0)*res[1]
    for f in Fx: d.polygon([(U[f[0]],Y[f[0]]),(U[f[1]],Y[f[1]]),(U[f[2]],Y[f[2]])],fill=255)
    return img
def outline(img): return ImageChops.difference(img.filter(ImageFilter.MaxFilter(5)),img)
for nm,ax2,box in [('front',(0,2),((-0.75,0.75),(z0-0.02,z0+2.1))),('profile',(1,2),((-1.05,0.95),(z0-0.02,z0+2.1)))]:
    res=(int(800*(box[0][1]-box[0][0])/ (box[1][1]-box[1][0])*1.0),800); res=(res[0]*2,res[1]*2)
    rng=np.random.default_rng(0)
    a=raster(V,F,ax2,box,res); b=raster(Vw,Fw,ax2,box,res)
    canvas=Image.new('RGB',res,(255,255,255)); canvas.paste((215,215,215),mask=a)
    canvas.paste((0,0,0),mask=outline(a)); canvas.paste((220,40,40),mask=outline(b))
    d=ImageDraw.Draw(canvas); d.text((10,10),'grey fill + black outline = GO-05AT_AC3 (accepted body). red outline = accepted W1 GO guide (GO_r6), scaled to equal vertex stature, aligned at floor (sole), midline and pelvis centre; helper geometry excluded',fill=(0,0,0))
    canvas.save(f'r/overlay_{nm}.png')
    # head/shoulder crop (top 32% of stature)
    hc=canvas.crop((0,0,res[0],int(res[1]*0.36))); hc.save(f'r/overlay_{nm}_headcrop.png')
print('scale W1->AC3',s)
