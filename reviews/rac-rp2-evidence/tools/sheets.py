import numpy as np
from PIL import Image, ImageDraw, ImageFont
E='/tmp/claude-0/rp2/ev/'
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22); Fs=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
except: F=Fs=ImageFont.load_default()
def crop(n, box=None):
    a=Image.open(E+n+'.png').convert('RGB'); 
    if box: return a.crop(box)
    g=np.array(a.convert('L'),int); bg=np.median(g[:4]); m=np.abs(g-bg)>4; ys,xs=np.nonzero(m)
    return a.crop((max(xs.min()-10,0),max(ys.min()-10,0),min(xs.max()+10,a.width),min(ys.max()+10,a.height)))
def grid(rows, cols, cellh, title, out, rowlab, collab=None, box=None):
    ims=[[crop(n,box) for n in r] for r in rows]
    sc=[[cellh/i.height for i in r] for r in ims]; cw=max(int(i.width*s) for r,ss in zip(ims,sc) for i,s in zip(r,ss))
    W=180+cw*len(cols); H=70+cellh*len(rows)+30; o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); d.text((10,10),title,fill='black',font=F)
    for j,c in enumerate(cols): d.text((180+j*cw+10,42),c,fill='black',font=Fs)
    for i,r in enumerate(ims):
        d.text((8,70+i*cellh+cellh//2),rowlab[i],fill='black',font=Fs)
        for j,im in enumerate(r):
            im=im.resize((int(im.width*cellh/im.height),cellh)); o.paste(im,(180+j*cw+(cw-im.width)//2,70+i*cellh))
    o.save(out,quality=88); return out
V=['front','left','back','q3']
grid([['mv_%s_%s'%(m,v) for v in V] for m in ('e3_body','e3_mirrored','sstar','hstar','w2_body')]+[['heat_e3_'+v for v in V],['heat_w2_'+v for v in V]],
     ['front','profile (left)','back','three-quarter'],520,'RP2 Grask asymmetry diagnostics (identical cameras; heat = mirror deviation 0-10 mm)',
     '/tmp/claude-0/rp2/evpkg/sheet_asymmetry.jpg',['E3 source','E3 mirrored','S* bilateral avg','H adjudicated','W2 GR218R','E3 heat','W2 heat'],None)
grid([['mv_%s_%s'%(m,v) for v in V] for m in ('e3_body','cand_v001b')],['front','profile (left)','back','three-quarter'],900,
     'RP2 Grask identity: E3 source vs production v001 (identical cameras)','/tmp/claude-0/rp2/evpkg/sheet_identity.jpg',['E3 source','production v001'])
names=[('cu1','front','crotch front'),('cu1','q3','crotch 3/4'),('cu2','below','crotch below'),('cu3','front','axilla front'),('cu3','q3','axilla 3/4'),
       ('cu4','front','girdle front'),('cu4','back','girdle back'),('cu4','q3','girdle 3/4'),('cu5','front','chest/abdomen band front'),('cu5','back','band back')]
grid([['%s_%s_%s'%(a,m,v) for a,v,_ in names] for m in ('e3_body','cand_v001b')],[l for *_,l in names],420,
     'RP2 Grask close-ups: E3 source (top) vs production v001 (bottom), identical cameras','/tmp/claude-0/rp2/evpkg/sheet_closeups.jpg',['E3 source','production v001'],box=None)
