# sheets3.py : v003 audit-closure sheets. STRICT: every panel must exist (no blank cells).
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
R='/tmp/claude-0/rt'; O=R+'/ev3/sheets'; os.makedirs(O,exist_ok=True)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',27)
def load(p,w):
    if not os.path.exists(p): raise SystemExit('MISSING PANEL '+p)
    im=Image.open(p).convert('RGB'); return im.resize((w,int(im.height*w/im.width)))
def sheet(name,title,rows,w=300,notes=()):
    ims=[[(load(p,w),lab) for p,lab in r] for r in rows]
    H=80+sum(max(i.height for i,_ in r)+34 for r in ims)+34*len(notes)+20; Wd=20+max(len(r) for r in ims)*(w+10)
    S=Image.new('RGB',(Wd,H),'white'); d=ImageDraw.Draw(S); d.text((20,20),title,fill='black',font=FB); y=80
    for r in ims:
        x=20
        for im,lab in r: d.text((x,y),lab,fill=(40,40,40),font=F); S.paste(im,(x,y+28)); x+=w+10
        y+=max(i.height for i,_ in r)+34
    for n in notes: d.text((20,y),n,fill=(20,20,90),font=F); y+=34
    S.save(os.path.join(O,name)); print(name,S.size)
C=R+'/ev3/cmp'
T=[('src','v005 source'),('v001','v001 (x3)'),('v002','v002 (x2)'),('v003','v003 selected (x2)')]
views=[('body','front'),('body','left'),('body','back'),('body','q3'),('head','front'),('head','left'),('shoulder','front'),('shoulder','q3'),('hand','left'),('hand','right'),('foot','top'),('foot','left')]
for k,(a,b) in enumerate(((0,4),(4,8),(8,12))):
    sheet('S1_density_visual_%d.png'%(k+1),'Identical cameras: v005 / v001 / v002 / v003 (clay)',[[('%s/%s_%s_%s.png'%(C,t,g,v),'%s  %s %s'%(lab,g,v)) for t,lab in T] for g,v in views[a:b]],w=330)
WT=[('cage','authored cage (v001/v002 cage21)'),('x1','x1'),('x2','x2 raw'),('v002','v002'),('v003','v003')]
sheet('S2_density_wire.png','Wireframe: cage / x1 / x2 raw / v002 / v003',[[('%s/w_%s_%s.png'%(C,t,r),'%s  %s'%(lab,r)) for t,lab in WT] for r in ('face','shoulder','hand','groin','knee','foot')],w=300)
reg=[('ear','ear helix / rim'),('axilla','axillary fan'),('shoulder','shoulder'),('web_index_middle','index-middle web'),('web_thumb','thumb web'),('web_toe4_5_r','toe4-5 web R'),('hallux_toe2_l','hallux-toe2 L'),('groin','groin')]
sheet('Q1_quad_quality_repairs.png','Quad quality at repair regions - v001 vs v003 (red = hard limit, orange = outside 45-135 deg or aspect > 4)',
  [[('%s/q_v001_%s.png'%(R+'/ev2/cmp',k),'v001 '+l) for k,l in reg[:4]],[('%s/q_v003_%s.png'%(C,k),'v003 '+l) for k,l in reg[:4]],
   [('%s/q_v001_%s.png'%(R+'/ev2/cmp',k),'v001 '+l) for k,l in reg[4:]],[('%s/q_v003_%s.png'%(C,k),'v003 '+l) for k,l in reg[4:]]],w=340,
   notes=['v001: 712 hard-limit quads. v003: 0 hard-limit quads (angles 20.1-160.0 deg); opposite-edge-sum aspect max 7.07; longest/shortest edge max 8.07 (1 face).'])
P=[('head','head / face'),('shoulder_axilla','shoulder / axilla'),('hand_dorsal','hand dorsal'),('hand_palmar','hand palmar'),('pelvis_groin','pelvis / groin'),('foot_top','foot top'),('foot_sole','foot sole')]
sheet('P_pole_audit.png','Pole audit - v003 poles labelled id:valence (red v3, blue v5, black v6); 166 authored-cage poles; none within 2 loops of an audited crease',
  [[('%s/pole_v003_%s.png'%(C,k),l) for k,l in P[:4]],[('%s/pole_v003_%s.png'%(C,k),l) for k,l in P[4:]]],w=420)
RG=R+'/ev3/rings'; ev=json.load(open(RG+'/ring_evidence.json'))
nts=[]
for k,v in ev.items():
    nts.append('%s: %d distinct closed rings in the +-%d mm band (required %d); offsets %s mm; path count by side %s'%(k,v['distinct_closed_rings_in_band'],v['band_mm'][1],v['required'],', '.join('%+.1f'%r['offset_mm'] for r in v['rings']),v['path_count_by_side']))
sheet('R_ring_evidence.png','Closed-ring evidence: both ankles, right elbow, left toe-5 MTP (rings coloured, offset from the joint plane; red solid = joint plane, dashed = band)',
  [[(RG+'/rings_%s_%s.png'%(j,v),'%s %s'%(j,v)) for v in ('front','side')] for j in ('ankle_l','ankle_r')]+[[(RG+'/rings_%s_%s.png'%(j,v),'%s %s'%(j,v)) for j in ('elbow_r','toe5_j0_l') for v in ('front','side')][:2],
   [(RG+'/rings_%s_%s.png'%(j,v),'%s %s'%(j,v)) for j in ('toe5_j0_l',) for v in ('front','side')]],w=560,notes=nts)
FV=R+'/fv'; vv=['top','front','sole','lateral','medial','webs','nails']
for s,nm in (('l','LEFT'),('r','RIGHT')):
    sheet('E_feet_%s_unobstructed.png'%nm.lower(),'%s foot isolated (no hands / legs in view): v005 source (row 1), v003 clay (row 2), v003 wire (row 3)'%nm,
      [[('%s/%s_%s_%s.png'%(FV,t,s,v),'%s %s'%(lab,v)) for v in vv] for t,lab in (('src','source'),('v003','v003'),('v003w','v003 wire'))],w=300,
      notes=['Views: top, front, sole, lateral, medial, toe-web close-up, toenail close-up. Ground-level crop (u < 13 cm) so the leg does not hide the foot.'])
WV=R+'/wv'; hv=['im_d','mr_d','rp_d','im_p','mr_p','rp_p','thumb']; hn={'im_d':'index-middle dorsal','mr_d':'middle-ring dorsal','rp_d':'ring-pinky dorsal','im_p':'index-middle palmar','mr_p':'middle-ring palmar','rp_p':'ring-pinky palmar','thumb':'thumb web'}
for s,nm in (('l','LEFT'),('r','RIGHT')):
    sheet('W_webs_%s_hand.png'%nm.lower(),'%s hand web spaces close-up (3.6 cm field): v005 source / v002 / v003'%nm,
      [[('%s/%s_%s_%s.png'%(WV,t,s,v),'%s %s'%(lab,hn[v])) for v in hv] for t,lab in (('src','source'),('v002','v002'),('v003','v003'))],w=250)
