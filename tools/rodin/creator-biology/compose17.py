import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt'); sys.path.insert(0,'/tmp/claude-0/rodin/v1')
from compose import BG,PANEL,TXT,SUB,F
from PIL import Image, ImageDraw
import json, os, sets, evaluate as EV
D='/tmp/claude-0/rodin/v1/'; R=D+'R3/'; O=D+'sheets17/'; os.makedirs(O,exist_ok=True)
S=json.load(open(D+'sweep.json')); T=" (DIAGNOSTIC)"
STAT=json.load(open(D+'status.json')) if os.path.exists(D+'status.json') else {}
RED=(235,110,100); YEL=(235,200,90); GRN=(120,200,120)
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,fn,lw=230,capfont=17,extra_img=None,notes=None):
    W=lw+len(cols)*(cell+12)+10+(370 if notes else 0); top=92+26*len(sub)+32
    H=top+len(rows)*(cell+12)+20
    if extra_img: ex=Image.open(extra_img); sc=(W-40)/ex.width; ex=ex.resize((int(ex.width*sc),int(ex.height*sc))); H+=ex.height+20
    img=Image.new('RGB',(max(W,1400),H),BG); d=ImageDraw.Draw(img)
    d.text((20,14),title,font=F(28,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,56+26*i),s,font=F(18),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.text((lw+c*(cell+12)+4,top-26),cl,font=F(capfont,True),fill=SUB)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+12); d.multiline_text((14,y+8),rl,font=F(17,True),fill=TXT,spacing=5)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if p and os.path.exists(p): img.paste(tile(p,cell),(lw+c*(cell+12),y))
        if notes and rk in notes:
            st,txt=notes[rk]; col={'PASS':GRN,'CONSTRAIN':YEL,'FAIL':RED}.get(st,TXT)
            x0=lw+len(cols)*(cell+12)+6; d.text((x0,y+6),st,font=F(20,True),fill=col); d.multiline_text((x0,y+36),txt,font=F(14),fill=SUB,spacing=4)
    if extra_img: img.paste(ex,(20,top+len(rows)*(cell+12)+10))
    img.save(O+out,quality=88); print(out,img.size)
lab={j:d['label'] for j,d in S.items()}
def met(j):
    m=EV.derived(S[j]['metrics']); return m
f=lambda r,c:R+'%s_%s.png'%(r,c)
BODYV=[('Front','front'),('Profile','profile'),('Rear 3/4','rear34')]
# 01 reference
sheet("Saurin creator biology — 1. frozen reference (identical cameras used throughout)"+T,
 ["Frozen closure reference (aff1b52): standing height 187.9 cm, tail 121.4 cm along the relaxed centreline (64.6 % H), head length 31.9 cm (0.170 H), body volume 136.9 L,",
  "free-tail volume 21.2 L (15.5 %). Every variant in this package is DERIVED from this mesh by smooth region warps; the reference itself is never modified."],
 [('Reference\nbody','ref')],BODYV,430,'v17_01_reference.jpg',f)
sheet("Saurin creator biology — 1b. reference tail and naked skull close views"+T,[" "],
 [('Tail','ref'),('Head','ref')],[('Tail profile','tprof'),('Tail top','ttop'),('Tail rear 3/4','tr34'),('—','x')],400,'v17_01b_reference_close.jpg',
 lambda r,c: f(r,{'tprof':'tprof','ttop':'ttop','tr34':'tr34','x':'none'}[c]) )
def pair_rows(ids):
    rows=[]
    for a in ids:
        lo,hi=a+'_lo',a+'_hi'; rows.append(('%s\n%s'%(lab[lo].split(' -')[0].split(' +')[0],'lo | hi'),a))
    return rows
def pf(view):
    def g(r,c):
        side,v=c.split(':'); return R+'%s_%s_%s.png'%(r,side,v) if r!='ref' else R+'ref_%s.png'%v
    return g
def rowsLH(ids):
    return [('%s\n(low | high)'%(lab[a+'_lo'].rsplit(' ',2)[0] if not lab[a+'_lo'].startswith('Stature') else 'Stature'),a) for a in ids]
LH=[('Low · front','lo:front'),('Low · profile','lo:profile'),('Reference · profile','ref:profile'),('High · front','hi:front'),('High · profile','hi:profile')]
def gLH(r,c):
    s,v=c.split(':'); return R+('ref_%s.png'%v if s=='ref' else '%s_%s_%s.png'%(r,s,v))
LABELS={'h':'Stature 168 | 208 cm','hd':'Head proportion -8 | +8 %','nk':'Neck length -15 | +15 %','tl':'Axial trunk length -10 | +10 %','ll':'Leg length -6 | +6 %','al':'Arm length -6 | +6 %',
 'nd':'Neck depth -10 | +10 %','td':'Thoracic depth -8 | +8 %','tw':'Thoracic width -7 | +7 %','sh':'Shoulder breadth -8 | +8 %','pw':'Pelvic width -7 | +7 %','ha':'Hand size -8 | +8 %','fo':'Foot size -8 | +8 %',
 'tn':'Tail length 55 | 80 % H','tb':'Tail base -15 | +15 %','tt':'Tail mid/distal fullness\n-15 | +15 %','tc':'Tail carriage\nlift 8° | droop 10°','tx':'Tail section\ndeeper | broader',
 'rl':'Rostrum length\n-15 | +20 %','rw':'Rostral base width\n-12 | +12 %','ra':'Anterior rostral width\n-15 | +15 %','rd':'Rostral depth\n-12 | +12 %','jd':'Posterior jaw depth\n-12 | +15 %','cl':'Cranial length\n-8 | +8 %','cw':'Cranial width\n-8 | +8 %','cd':'Cranial depth\n-7 | +7 %','ob':'Orbit size\n-8 | +8 %'}
for _k,_v in list(LABELS.items()):
    if '\n' not in _v:
        i=_v.find(' -'); i=_v.find(' 1') if i<0 else i; i=_v.find(' 5') if i<0 else i
        LABELS[_k]=_v[:i]+'\n'+_v[i+1:] if i>0 else _v
def note_single(a):
    out={}
    return out
def notes_for(ids):
    n={}
    for a in ids:
        st=[];  txt=[]
        for s_ in ('lo','hi'):
            j=a+'_'+s_; d,h,sf=EV.classify(S[j]['metrics'],S[j]['params']); ss_=STAT.get(j,{}).get('status','FAIL' if h else 'PASS'); st.append(ss_)
            txt.append('%s: %s'%(s_,STAT.get(j,{}).get('short',('; '.join(h) if h else 'within hard bounds'))))
        worst='FAIL' if 'FAIL' in st else ('CONSTRAIN' if 'CONSTRAIN' in st else 'PASS'); n[a]=(worst,'\n'.join(txt))
    return n
fn2=lambda r,c: R+('ref_%s.png'%c.split(':')[1] if c.split(':')[0]=='ref' else '%s_%s_%s.png'%(r,c.split(':')[0],c.split(':')[1]))
for out,ids,ttl,sub in [('v17_02_body_proportion.jpg',['h','hd','nk','tl','ll','al'],'2. single-variable extremes — stature and segment proportions',
                          ["Identical cameras. Stature changes absolute size; every other row is at constant standing height (187.9 cm)."]),
                         ('v17_03_body_breadth.jpg',['nd','td','tw','sh','pw','ha','fo'],'3. single-variable extremes — breadth, depth and extremities',
                          ["Constant standing height. Thoracic depth/width is protected (deep narrow-to-moderate shell, 0.80–1.00; ref 0.88)."])]:
    sheet("Saurin creator biology — "+ttl+T,sub,[(LABELS[a],a) for a in ids],LH,250,out,fn2,notes=notes_for(ids))
FC=[('Narrow','fr_n'),('Balanced (ref)','ref'),('Broad','fr_b'),('Muscle low','mu_lo'),('Muscle high','mu_hi'),('Fat low','fa_lo'),('Fat high','fa_hi')]
sheet("Saurin creator biology — 4. frame and composition"+T,
 ["Frame changes skeletal breadth and joint girth only (lengths, head, sacral-caudal organization protected).",
  "Composition adds soft-tissue volume: muscle on limbs, girdle, epaxial neck/trunk, proximal-mid tail; fat ventral-abdominal,",
  "flank/hip, graded caudal-proximal, minor gular. No pectoral blocks, no abdominal segmentation, no gluteal mass."],
 [('Front','front'),('Profile','profile'),('Rear 3/4','rear34'),('Torso\nfront','tfront'),('Torso\n3/4','t34')],FC,250,'v17_04_frame_composition.jpg',lambda r,c: R+'%s_%s.png'%(c,r),lw=110)
TV=[('Low · tail profile','lo:tprof'),('Low · top','lo:ttop'),('High · tail profile','hi:tprof'),('High · top','hi:ttop')]
sheet("Saurin creator biology — 5. tail single-variable extremes (each alone, nothing coupled)"+T,
 ["Each row changes ONE tail variable with everything else at reference — deliberately what the creator must NOT allow freely;","see the coupling sheets for the rule."],
 [(LABELS[a],a) for a in ['tn','tb','tt','tc','tx']],TV,300,'v17_05_tail_singles.jpg',fn2,notes=notes_for(['tn','tb','tt','tc','tx']))
for nm,img,ttl in [('v17_06a_tail_profiles.jpg',D+'P_tail_profiles.png','6a. tail cross-section profiles (normalized)'),('v17_06b_tail_envelope.jpg',D+'P_tail_envelope.png','6b. tail length x base x fullness validity envelope'),('v17_06c_balance.jpg',D+'P_balance.png','6c. counterbalance (lean needed to stand over the feet)')]:
    ex=Image.open(img); W=ex.width+40; im=Image.new('RGB',(W,ex.height+130),BG); d=ImageDraw.Draw(im); d.text((20,14),"Saurin creator biology — "+ttl+T,font=F(26,True),fill=TXT)
    d.text((20,56),{'v17_06a_tail_profiles.jpg':"Area / root area along normalized tail length; red bar = mid-tail validity band (0.27–0.48).",
                    'v17_06b_tail_envelope.jpg':"Each dot = one measured variant (length x base, three fullness levels); number = size-normalized root-sufficiency index (1 = reference).",
                    'v17_06c_balance.jpg':"Uniform-density centre of mass vs feet. The reference itself needs 8.8° of forward lean in the frozen pose (see report); limit = reference + 3°."}[nm],font=F(18),fill=SUB)
    im.paste(ex,(20,100)); im.save(O+nm,quality=88); print(nm)
CT=[('Tail profile','tprof'),('Tail top','ttop'),('Body profile','profile')]
CC=['x03','x26','x28','x27','x04','x22','x21','x25']
sheet("Saurin creator biology — 6d. tail coupling cases"+T,["Long tails need a proportionally larger base (root sufficiency) but the added mass costs balance;","Broad frames carry the 80 % canon end, the reference body tops out near 78 %."],
 [(lab[j].replace(' + ','\n+ '),j) for j in CC],CT,300,'v17_06d_tail_coupling_cases.jpg',f,notes={j:(STAT.get(j,{}).get('status','?'),STAT.get(j,{}).get('short','')) for j in CC})
HV=[('Low · front','lo:hF'),('Low · profile','lo:hP'),('Low · top','lo:hT'),('High · front','hi:hF'),('High · profile','hi:hP'),('High · top','hi:hT')]
for out,ids,ttl in [('v17_07a_cranial_rostral.jpg',['rl','rw','ra','rd','jd'],'7a. cranial identity — rostral and jaw extremes, displays OFF'),('v17_07b_cranial_vault.jpg',['cl','cw','cd','ob'],'7b. cranial identity — vault and orbit extremes, displays OFF')]:
    sheet("Saurin creator biology — "+ttl+T,["Neutral naked skull (no display anatomy). Every valid head keeps: compact projecting rostrum, layered rostral-cranial","integration, brow -> temporal/postorbital transition, embedded orbit, deep jaw base, no human chin/lips/nose/pinnae."],
          [(LABELS[a],a) for a in ids],HV,240,out,fn2,notes=notes_for(ids))
HC=[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Top','hT')]
sheet("Saurin creator biology — 8. coupled cranial extremes, displays OFF"+T,["Coupled extremes of the head controls (single-variable extremes all pass; these combinations test the relationships)."],
 [('Reference','ref')]+[(lab[j].replace(' + ','\n+ '),j) for j in ['x05','x06','x19','x24']],HC,300,'v17_08_cranial_coupled.jpg',f,notes={j:(STAT.get(j,{}).get('status','?'),STAT.get(j,{}).get('short','')) for j in ['x05','x06','x19','x24']})
CM=[c[0] for c in sets.COMBO]
half=[CM[:13],CM[13:]]
for i,ids in enumerate(half):
    sheet("Saurin creator biology — 9%s. combined-proportion stress matrix"%('ab'[i])+T,["Identical cameras; PASS / CONSTRAIN / FAIL against the candidate relationship rules (report §8).","CONSTRAIN = the creator adapts a dependent control; FAIL = the requested combination is itself an invalid shape."],
          [(lab[j].replace(' + ','\n+ ').replace(', ',',\n').replace(': ',':\n'),j) for j in ids],BODYV+[('Detail (head 3/4 or tail)','det')],250,'v17_09%s_combined_matrix.jpg'%('ab'[i]),
          lambda r,c: f(r,c) if c!='det' else (f(r,'hF34') if os.path.exists(f(r,'hF34')) else f(r,'tprof')),notes={j:(STAT.get(j,{}).get('status','?'),STAT.get(j,{}).get('short','')) for j in ids})
# displays
DS=json.load(open(D+'display_metrics.json')) if os.path.exists(D+'display_metrics.json') else {}
DV=[('Neutral naked','d00'),('Minimal ridges','d13'),('Low hornlets (ref)','dlh'),('Hornlets: 1 pair','d01'),('Hornlets: length x1.5','d02'),('Hornlets: x0.7,\nbase x0.85','d03'),('Hornlets: x1.5,\nbase x0.7','d04'),
    ('Swept (ref)','dsw'),('Swept: length x0.75','d05'),('Swept: length x1.25','d06'),('Swept: +10° lower','d07'),('Swept: -12° raised','d08'),('Swept: x1.25,\nbase x0.8','d09'),
    ('Mixed/asym (ref)','dmx'),('Mixed: asym 0.70','d10'),('Crest 2.43 (ref)','dcr'),('Crest 1.6 cm','d11'),('Crest 3.0 cm','d12')]
dv=lambda r,c: D+'dv/DN_%s_%s.png'%(r,c)
DVV=[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Top','hT'),('Attachment','att'),('Rear 3/4','hR34')]
for i,rows in enumerate([DV[:9],DV[9:]]):
    sheet("Saurin creator biology — 10%s. cranial display family range"%('ab'[i])+T,["Display = biological phenotype in the creator's hair-selection slot (not hair). Same frozen naked skull; only display","parameters change: count, length, base footprint, sweep, asymmetry, crest height."],
          rows,DVV,230,'v17_10%s_display_range.jpg'%('ab'[i]),dv,lw=250,notes={k:(DS.get(k,{}).get('status','?'),DS.get(k,{}).get('short','')) for _,k in rows})
DX=json.load(open(D+'dispx.json')) if os.path.exists(D+'dispx.json') else {}
XR=[('Mixed x long rostrum\n+ narrow cranium','mx_x05'),('Mixed x short rostrum\n+ broad cranium','mx_x06'),('Swept x long rostrum\n+ narrow cranium','sw_x05'),('Swept x short rostrum\n+ broad cranium','sw_x06'),('Near-naked x long\nrostrum + narrow cranium','mr_x05'),('Near-naked x short\nrostrum + broad cranium','mr_x06')]
sheet("Saurin creator biology — 11. displays on extreme crania"+T,["Strongest allowed displays and near-naked expression on the coupled cranial extremes.","Displays re-seat on the warped skull; they never rescue the skull read."],
      XR,[('Front','hF'),('Profile','hP'),('Front 3/4','hF34'),('Top','hT')],260,'v17_11_display_cranial.jpg',lambda r,c:D+'dx/%s_%s.png'%(r,c),lw=270,notes={k:(DX.get(k,{}).get('status','?'),DX.get(k,{}).get('short','')) for _,k in XR})
