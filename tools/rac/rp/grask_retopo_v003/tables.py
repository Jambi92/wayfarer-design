# tables.py TAG EVDIR : G tables image (deviation by zone, identity zones, IoU, landmark drift, loop audit summary)
import json, sys, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
T,E=sys.argv[1],sys.argv[2]; R='/tmp/claude-0/rt/'
dev=json.load(open(R+T+'_dev.json')); iou=json.load(open(E+'/iou.json')); lm=json.load(open(R+T+'_lmdrift.json'))
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',20); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
L=['Deviation (mm)            src->retopo med/p95/max      retopo->src med/p95/max   limit']
lim={'head_face':'T-2 0.3/0.8/1.5','ears':'T-2','hand_l':'T-2','hand_r':'T-2','foot_l':'T-2','foot_r':'T-2','body_general':'T-1 0.5/1.5/3.0'}
for k,v in dev.items():
    a=v['src_to_prod']; b=v['prod_to_src']
    L.append('%-14s %6.3f/%6.3f/%6.3f        %6.3f/%6.3f/%6.3f     %s'%(k,a['median'],a['p95'],a['max'],b['median'],b['p95'],b['max'],lim[k]))
L.append(''); L.append('Silhouette IoU (3 px/cm, body only)   limit 0.995 front/profile/rear')
for k,v in iou['views'].items(): L.append('  %-16s %.5f'%(k,v['iou']))
L.append(''); L.append('Landmark drift: n=%d  median %.3f mm  max %.3f mm   >1.0 mm: %s   >1.5 mm: %s'%(lm['n'],lm['median_mm'],lm['max_mm'],', '.join('%s %.2f'%(k,v['drift_mm']) for k,v in lm['over_1mm'].items()) or 'none',', '.join(lm['over_1_5mm']) or 'none'))
W=1700; H=40+30*len(L); im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im); y=20
for l in L: d.text((20,y),l,fill='black',font=F); y+=30
im.save(E+'/G_tables.png'); print('\n'.join(L))
