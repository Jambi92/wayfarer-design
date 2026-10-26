# twsheet.py : thumb-index hollow inspection sheets (one per hand) with arrows at the questioned hollow
import json, os, numpy as np
from PIL import Image, ImageDraw, ImageFont
D='/tmp/claude-0/rt/tw'; F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
H={'R':np.array([-27.23,6.89,94.89]),'L':np.array([27.35,7.4,94.81])}
def panel(tag,view,w,h_pt,arrow=True):
    p='%s/%s_%s.png'%(D,tag,view); im=Image.open(p).convert('RGB'); C=json.load(open(p.replace('.png','.json')))
    c=np.array(C['c']); x=np.array(C['x']); y=np.array(C['y']); hh=C['h']; px=C['px']
    u=((h_pt-c)@x/(2*hh)+0.5)*px; v=(0.5-(h_pt-c)@y/(2*hh))*px
    d=ImageDraw.Draw(im)
    if arrow:
        L=110 if view.startswith('cu') else 70; a=np.array([u,v]); b=a+np.array([-L,-L])*0.75
        d.line([tuple(b),tuple(a-np.array([-8,-8])*0)],fill=(230,40,20),width=7)
        d.polygon([tuple(a),tuple(a+np.array([-26,-6])),tuple(a+np.array([-6,-26]))],fill=(230,40,20))
    return im.resize((w,w))
VN={'ctx_dorsal':'back of hand','ctx_palmar':'palm','ctx_q3':'3/4 front (questioned angle)','ctx_front':'thumb side','cu_front':'close-up, thumb side','cu_q3':'close-up, 3/4 front','cu_dorsal':'close-up, back of hand','cu_palmar':'close-up, palm'}
for S,name in (('R','RIGHT'),('L','LEFT')):
    rows=[('v005 SOURCE (frozen) %s hand - clay'%name,'src_'+S,['ctx_dorsal','ctx_palmar','ctx_q3','ctx_front']),
          ('v002 RETOPOLOGY %s hand - clay'%name,'v002_'+S,['ctx_dorsal','ctx_palmar','ctx_q3','ctx_front']),
          ('v002 RETOPOLOGY %s hand - clay + wireframe'%name,'v002w_'+S,['ctx_dorsal','ctx_palmar','ctx_q3','ctx_front']),
          ('v005 SOURCE close-up - clay','src_'+S,['cu_front','cu_q3','cu_dorsal','cu_palmar']),
          ('v005 SOURCE close-up - its own triangle wireframe','srcw_'+S,['cu_front','cu_q3','cu_dorsal','cu_palmar']),
          ('v002 RETOPOLOGY close-up - clay','v002_'+S,['cu_front','cu_q3','cu_dorsal','cu_palmar']),
          ('v002 RETOPOLOGY close-up - clay + wireframe','v002w_'+S,['cu_front','cu_q3','cu_dorsal','cu_palmar'])]
    w=400; Wd=20+4*(w+10); Ht=110+len(rows)*(w+70)+230
    Sh=Image.new('RGB',(Wd,Ht),'white'); d=ImageDraw.Draw(Sh)
    d.text((20,20),'%s HAND - thumb-index hollow (red arrow): frozen v005 source vs v002 retopology'%name,fill='black',font=FB)
    d.text((20,62),'Hand isolated (no other limb). Identical orthographic cameras, framing, lighting and scale; v002 read back from the exported blend with the production-origin translation undone.',fill=(40,40,40),font=F)
    y=110
    for title,tag,views in rows:
        d.text((20,y),title,fill=(10,10,120),font=F); y+=30; x=20
        for v in views:
            Sh.paste(panel(tag,v,w,H[S]),(x,y)); d.text((x,y+w+2),VN[v],fill=(60,60,60),font=F); x+=w+10
        y+=w+40
    notes=['What you are seeing: the hollow is the first dorsal web space - the soft gap between the thumb metacarpal and the index metacarpal, where the thumb',
           'web meets the back of the hand. It is part of the frozen v005 sculpt (rows 1, 4, 5): the source surface itself dips there.',
           'v002 keeps the hollow: it follows the source within median 0.06 mm / p95 0.22-0.25 mm / max 0.65-0.67 mm in a 2.5 cm radius around the arrow',
           '(sections: TW4). BUT v002 has irregular quad spacing at the web saddle that shades as faint rumples (close-up rows 6-7) - a retopology defect, see TW3.',
           'Nothing was changed. Softening this hollow would be a SOURCE anatomy change and needs your explicit approval of an illustrated proposal.']
    for n in notes: d.text((20,y),n,fill=(20,20,90),font=F); y+=36
    Sh.save('%s/TW%d_%s_hand_thumb_index_hollow.png'%(D,1 if S=='R' else 2,name.lower())); print(S,Sh.size)
