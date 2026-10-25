# sheets.py EVDIR OUTDIR : compose evidence sheets A-G (PNG) from raw renders
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
E,O=sys.argv[1],sys.argv[2]; os.makedirs(O,exist_ok=True)
try: F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22); FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
except Exception: F=FB=ImageFont.load_default()
def load(p,w):
    im=Image.open(p).convert('RGB'); h=int(im.height*w/im.width); return im.resize((w,h))
def sheet(name,title,rows,w=420,notes=None):
    ims=[[(load(p,w) if p and os.path.exists(p) else Image.new('RGB',(w,w),'white'),lab) for p,lab in r] for r in rows]
    H=80+sum(max(i.height for i,_ in r)+36 for r in ims)+(40*len(notes) if notes else 0); Wd=20+max(len(r) for r in ims)*(w+10)
    S=Image.new('RGB',(Wd,H),'white'); d=ImageDraw.Draw(S); d.text((20,20),title,fill='black',font=FB); y=80
    for r in ims:
        x=20
        for im,lab in r:
            d.text((x,y),lab,fill=(40,40,40),font=F); S.paste(im,(x,y+30)); x+=w+10
        y+=max(i.height for i,_ in r)+36
    if notes:
        for n in notes: d.text((20,y),n,fill=(20,20,90),font=F); y+=40
    S.save(os.path.join(O,name)); print(name,S.size)
v=lambda t,n: os.path.join(E,'%s_%s.png'%(t,n))
sheet('A_whole_body.png','A  Whole body - v005 source vs retopo v001 (identical orthographic cameras)',
  [[(v('A_src',k),'source '+k) for k in ('front','left','back','q3','bq3')],[(v('A_prod',k),'retopo '+k) for k in ('front','left','back','q3','bq3')],
   [(os.path.join(E,'iou_%s.png'%k),'overlay %s (yellow=both)'%k) for k in ('front','profile_left','rear','q3_front_left','q3_rear_left')]],w=320)
sheet('B_head_face.png','B  Head / face - source clay, retopo clay, retopo wireframe',
  [[(v('B_src',k),'source '+k) for k in ('front','left','q3','q3r')],[(v('B_prod',k),'retopo '+k) for k in ('front','left','q3','q3r')],
   [(os.path.join(E,'Bw_front.png'),'wire front'),(os.path.join(E,'Bw_left.png'),'wire profile'),(os.path.join(E,'Bw_ear.png'),'wire ear')]],w=420)
sheet('C_girdle_torso_pelvis.png','C  Girdle / torso / pelvis',
  [[(v('C_src',k),'source '+k) for k in ('front','back','q3','left','bq3')],[(v('C_prod',k),'retopo '+k) for k in ('front','back','q3','left','bq3')],
   [(os.path.join(E,f),l) for f,l in (('Cw_shoulder.png','wire shoulder / clavicle'),('Cw_axilla.png','wire axilla (from below-front)'),('Cw_pelvis.png','wire pelvis / groin'),('Cw_glute.png','wire gluteal fold'))]],w=360)
sheet('D_hands.png','D  Hands (left; right in Dr_*) - clay comparison and wireframe',
  [[(v('D_src',k),'source '+k) for k in ('left','right','front','back','q3')],[(v('D_prod',k),'retopo '+k) for k in ('left','right','front','back','q3')],
   [(v('Dr_src',k),'source R '+k) for k in ('left','right','front','q3r')]+[(None,'')],[(v('Dr_prod',k),'retopo R '+k) for k in ('left','right','front','q3r')]+[(None,'')],
   [(os.path.join(E,f),l) for f,l in (('Dw_dorsal.png','wire dorsal / MCP row'),('Dw_palmar.png','wire palm / webs'),('Dw_thumb.png','wire thumb root / finger side'))]],w=360)
sheet('E_feet.png','E  Feet (left; right in Er_*) - clay comparison and wireframe',
  [[(v('E_src',k),'source '+k) for k in ('top','left','right','front','below')],[(v('E_prod',k),'retopo '+k) for k in ('top','left','right','front','below')],
   [(v('Er_src',k),'source R '+k) for k in ('top','left','right','front','below')],[(v('Er_prod',k),'retopo R '+k) for k in ('top','left','right','front','below')],
   [(os.path.join(E,f),l) for f,l in (('Ew_top.png','wire top / toe roots'),('Ew_lat.png','wire outer'),('Ew_med.png','wire inner / hallux'),('Ew_sole.png','wire sole'))]],w=360)
sheet('F_topology_diagnostics.png','F  Topology diagnostics - tagged identity/deformation loops (colour = family), poles (red v3, blue v5, black v6+); 0 triangles, 0 n-gons',
  [[(os.path.join(E,'F_body.png'),'whole body')],[(os.path.join(E,'F_zoom.png'),'head / shoulder-axilla / hand / foot / pelvis')]],w=1500)
sheet('G_deviation.png','G  Bidirectional deviation heat maps (0 - 1.5 mm, turbo) and tables',
  [[(v('G_src',k),'source->retopo '+k) for k in ('front','back','left')]+[(v('G_prod',k),'retopo->source '+k) for k in ('front','back','left')],
   [(v('Gh_src',k),'s->r head/hand '+k) for k in ('front',)]+[(None,'tables: see G2_tables.png')]],w=320)
fc=[(os.path.join(E,'Fc_%s.png'%k),k.replace('_',' ')) for k in ('face','shoulder_axilla','elbow','wrist','hand','hip_groin','glute','knee','ankle','foot')]
sheet('F2_edge_flow_cage.png','F2  Edge flow, readable density (cage x1 subdiv; production = x3, all quads)',
  [fc[0:4],fc[4:8],fc[8:10]],w=420)
