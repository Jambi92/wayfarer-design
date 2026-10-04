import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json, os
R='/tmp/claude-0/rodin/g8/r/'; O='/tmp/claude-0/rodin/g8/sheets12/'; os.makedirs(O,exist_ok=True); A=json.load(open('/tmp/claude-0/rodin/g8/acct12.json'))
T=" — DIAGNOSTIC / NOT FINAL"
def tile(p,cell,bgc=PANEL):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,bgc); bg.paste(im,(0,0),im); return bg
def sheet(title,sub,rows,cols,cell,out,lw=230,fn=None,capfont=19):
    """rows: [(label,key)], cols: [(label,key)], fn(rowkey,colkey)->path or None"""
    W=lw+len(cols)*(cell+14)+10; top=96+28*len(sub)+30; img=Image.new('RGB',(W,top+len(rows)*(cell+14)+20),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,60+28*i),s,font=F(19),fill=SUB)
    for c,(cl,ck) in enumerate(cols): d.multiline_text((lw+c*(cell+14)+4,top-30 if '\n' not in cl else top-52),cl,font=F(capfont,True),fill=SUB,spacing=2)
    for r,(rl,rk) in enumerate(rows):
        y=top+r*(cell+14); d.multiline_text((16,y+cell//2-36),rl,font=F(20,True),fill=TXT,spacing=6)
        for c,(cl,ck) in enumerate(cols):
            p=fn(rk,ck)
            if p and os.path.exists(p): img.paste(tile(p,cell),(lw+c*(cell+14),y))
    img.save(O+out,quality=90); print(out,img.size)
from g8lib import PH
K=list(PH.keys()); short=lambda k:k.split('_')[0]
nice={k:k.split('_',1)[1].replace('_',' ') for k in K}
# 1 material calibration
sheet("Saurin Gate 8 — 1. neutral material calibration (matte → satin)"+T,
 ["Neutral grey pigment, identical lights/cameras; only the base roughness changes (per-region offsets kept: articulation +0.05, ventral +0.04, contact +0.18, interstitial skin +0.15).",
  "Accepted natural envelope = 0.45–0.72 (dry satin → matte); 0.30 is the upper limit for 'modest localized sheen'. Scale relief stays readable at every level; nothing reads wet or plastic."],
 [('Roughness 0.30\nsheen limit','30'),('Roughness 0.45\nsatin','45'),('Roughness 0.55\nDEFAULT\ndry satin','55'),('Roughness 0.72\nmatte','72')],
 [('Whole body','f34'),('Mid (torso)','mid'),('Dorsal scales close','dorsC')],560,'g8_01_material_calibration.jpg',fn=lambda r,c:R+'C_cal%s_%s.png'%(r,c))
# 2 pigmentation families
desc={'P1':'warm earth brown\nmid value, mid contrast','P2':'slate grey (cool)\nmid value, high contrast','P3':'ochre (warm)\nlight, high contrast','P4':'charcoal\ndark, low contrast',
 'P5':'muted olive\nmid, low-mid contrast','P6':'rust/terracotta (warm)\nmid, high sat.','P7':'subdued blue-grey (cool)\nmid, mid contrast','P8':'sand / stone\nlight, low sat.',
 'P9':'muted green\nmid-dark, mixed','P10':'cool brown\nlow contrast, low sat.'}
cols=[(short(k)+' '+desc[short(k)],k) for k in K]
img_cols=cols[:5]; img_cols2=cols[5:]
sheet("Saurin Gate 8 — 2. pigmentation families (10 natural phenotypes)"+T,
 ["Each individual = dominant hue family + secondary pigment + dorsal/ventral value relationship + saturation jitter + facial accent + distal shift + keratin + iris + asymmetry.",
  "Families from spec §87 (earth browns, ochre, olive, slate, charcoal, rust, blue-grey, sand, muted green, cool brown); no neon, metallic or emissive pigment; names carry no sex/culture/class meaning."],
 [('',0),('',1)],[('',i) for i in range(5)],520,'g8_02_pigmentation_families.jpg',lw=20,fn=lambda r,c:R+'A_%s_mid.png'%K[r*5+c])
im=Image.open(O+'g8_02_pigmentation_families.jpg'); d=ImageDraw.Draw(im)
for r in range(2):
    for c in range(5):
        k=K[r*5+c]; d.multiline_text((20+c*534+8,96+56+30+r*534+8),short(k)+'  '+desc[short(k)],font=F(18,True),fill=(240,240,240),spacing=2)
im.save(O+'g8_02_pigmentation_families.jpg',quality=90)
# 3 pattern families
PAT=['uniform','mottled','blotched','banded','broken_banded','axial','speckled','regional','mixed']
pn={'uniform':'near-uniform','mottled':'dorsal mottling','blotched':'lateral blotching','banded':'banding','broken_banded':'broken banding','axial':'axial striping','speckled':'speckling','regional':'regional contrast','mixed':'mixed / asymmetric'}
sheet("Saurin Gate 8 — 3. biological pattern families (same pigments, same individual)"+T,
 ["Patterns live in girth-normalized anatomical coordinates (body axis + limb axes), so elements scale with local girth, wrap the body, continue trunk → tail and fade (not stop) across the ventral field;",
  "edges can follow scale cells. Identical primary/secondary pigment in every column isolates the pattern logic."],
 [('Profile','prof'),('Rear 3/4','r34')],[(pn[p],p) for p in PAT],400,'g8_03_pattern_families.jpg',lw=130,fn=lambda r,c:R+'B_%s_%s.png'%(c,r),capfont=17)
# 4 whole organism
sheet("Saurin Gate 8 — 4. whole-organism phenotypes (10 individuals, identical pose/camera/light)"+T,
 ["One population: subdued earth, cool and warm ranges, dark and light, high and low contrast, strongly and minimally patterned. Pattern reaches head, trunk, limbs and tail.",
  "No individual is labelled by geography, culture, ancestry, sex or temperament."],
 [('Front 3/4','f34'),('Rear 3/4','r34')],[(short(k)+'\n'+nice[k],k) for k in K],360,'g8_04_whole_organism.jpg',lw=120,fn=lambda r,c:R+'A_%s_%s.png'%(c,r),capfont=15)
# 5 heads
HK=[k for k in K if short(k) in ('P1','P2','P3','P4','P5','P7','P8','P9')]
sheet("Saurin Gate 8 — 5. head close-ups: planes read through pigmentation"+T,
 ["Facial pattern contrast is reduced (×0.5, ×0.3 on the rostrum) and limited to plane-following accents: post-orbital stripe eye → tympanic recess, darker dorsal cranium, lighter gular/labial field.",
  "Brow shelf, orbital platform, rostral planes, jugal/quadrate and hinge stay readable in every phenotype. Vertical pupil legible in every iris colour."],
 [('Front 3/4','hF34'),('Profile','hP')],[(short(k)+' '+nice[k],k) for k in HK],440,'g8_05_heads.jpg',lw=120,fn=lambda r,c:R+'A_%s_%s.png'%(c,r),capfont=15)
# 6 tail flow
TP=['banded','broken_banded','axial','blotched','mottled','mixed']
sheet("Saurin Gate 8 — 6. tail / root pattern flow (sacral base → root → free tail)"+T,
 ["The body-axis coordinate runs continuously from the trunk through the sacral base into the tail; band period and blotch size shrink with tail girth.",
  "No pattern starts at the root, and the root articulation band carries no separate colour (see failure control 'tail seam')."],
 [('Tail profile','tailP'),('Root rear 3/4','trc')],[(pn[p],p) for p in TP],440,'g8_06_tail_flow.jpg',lw=140,fn=lambda r,c:R+'B_%s_%s.png'%(c,r))
# 7 RSA material
items=[(R+'C_rsa_dors.png','Protective structural\n(dorsal trunk) rough 0.55'),(R+'C_rsa_elb.png','Transitional articulation\n(elbow) +0.05'),(R+'C_rsa_fx.png','Fine expressive\n(orbit/rostrum) +0.02'),
 (R+'C_rsa_vent.png','Ventral (transverse)\n+0.04, lighter value'),(R+'D_hand_P1_hPal.png','Contact: palm\nmatte +0.18, paler'),(R+'D_foot_P1_fPl.png','Contact: sole\nmatte +0.18, paler'),
 (R+'D_foot_P1_fcl.png','Claw keratin\nrough 0.32–0.40, banded'),(R+'C_rsa_eyec.png','Eye\ncornea coat, slit pupil')]
cell=420; img=Image.new('RGB',(20+8*(cell+12),cell+230),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Saurin Gate 8 — 7. Regional Scale Architecture material response (phenotype P1)"+T,font=F(30,True),fill=TXT)
d.text((20,60),"Material follows the Gate 7 families without separating them: roughness offsets are small, interstitial skin is slightly paler and rougher, contact fields are matte and paler, keratin is smoother with growth bands.",font=F(19),fill=SUB)
for i,(p,l) in enumerate(items):
    x=20+i*(cell+12); d.multiline_text((x+4,112),l,font=F(17,True),fill=SUB,spacing=2); img.paste(tile(p,cell),(x,170))
img.save(O+'g8_07_rsa_material.jpg',quality=90)
# 8 display keratin
DV=[('minimal_ridges','Minimal ridges'),('low_hornlets','Low hornlets'),('swept_paired','Swept-back paired'),('mixed_asym','Mixed / asymmetric'),('crest','Restrained crest\n(2.43 cm)')]
KC=[('P1_horn','P1 · neutral horn'),('P1_matched','P1 · body-matched'),('P1_dark','P1 · dark keratin'),('P7_horn','P7 · neutral horn'),('P7_matched','P7 · body-matched'),('P7_dark','P7 · dark keratin')]
sheet("Saurin Gate 8 — 8. Cranial Keratin Display material"+T,
 ["Keratin differs from scale: smoother (0.32–0.40), slight translucency toward tips, faint growth banding along the growth axis. Three keratin/pigment relationships per phenotype:",
  "independent neutral horn, partially body-matched, dark. None is bright, sexually coded, decorated, magical or weapon-like; display attachments unchanged from Gate 7."],
 [(l,k) for k,l in DV],[(l,k) for k,l in KC],330,'g8_08_display_keratin.jpg',lw=200,fn=lambda r,c:R+'E_%s_%s_hF34.png'%(r,c),capfont=17)
# 9 eyes
EI=[('P1','P1 amber'),('P2','P2 pale\nyellow-grey'),('P4','P4 copper'),('P7','P7 grey-green')]
sheet("Saurin Gate 8 — 9. eye / nictitating membrane"+T,
 ["Iris: two-tone radial fibre pattern + limbal darkening; vertical pupil stays legible; cornea = clear coat (glint only, no glow).",
  "Membrane = diagnostic shading state on the Gate 7 eye (no geometry change): retracted fold → half-drawn",
  "→ fully drawn. Translucent milky film; iris tint and the pupil outline stay faintly visible beneath it."],
 [(l,k) for k,l in EI],[('Open (fold retracted)','0'),('Membrane half-drawn','5'),('Membrane drawn','10')],400,'g8_09_eyes.jpg',lw=220,fn=lambda r,c:R+'C_eye_%s_m%s_eyec.png'%(r,c))
# 10 failure controls
FL=[('wet_plastic','Wet / plastic','A_P1_umber_mottled_mid'),('metallic','Metallic','A_P1_umber_mottled_mid'),('gem','Gem / translucent','A_P5_olive_axial_mid'),('pale_belly','Cartoon pale belly','A_P1_umber_mottled_f34'),
 ('paint_mask','Paint-mask borders','A_P1_umber_mottled_f34'),('joint_rings','Joint rings','A_P1_umber_mottled_f34'),('face_noise','Face-obscuring noise','A_P1_umber_mottled_hF34'),('tail_seam','Tail-seam pattern','B_banded_tailP'),('dragon','Dragon colouring','A_P6_terracotta_blotched_f34')]
import glob
def fpath(r,c):
    nm=[x for x in FL if x[0]==c][0]
    if r=='rej': return glob.glob(R+'C_fail_%s_*.png'%c)[0]
    return R+nm[2]+'.png'
rj=A['_REJECT']
sheet("Saurin Gate 8 — 10. failure controls: rejected (top) vs accepted (bottom)"+T,
 ["Top row is deliberately wrong. Measured safeguards (accepted library vs rejected): scaly roughness ≥ 0.43 (wet 0.06), metallic 0 (1.0), sat. p99 ≤ %.2f (dragon %.2f), ventral boundary step ≤ %.2f (cartoon belly %.2f),"%(
   max(v['sat_p99'] for k,v in A.items() if not k.startswith('_')),rj['dragon']['sat_p99'],max(v['ventral_boundary_max_step'] for k,v in A.items() if not k.startswith('_')),rj['pale_belly']['ventral_boundary_max_step']),
  "joint-ring index %.2f–%.2f (rings %.2f), face/trunk cell contrast ≤ %.2f (face noise %.2f), tail-root luminance jump ≤ %.2f (tail seam %.2f). Full table in the report."%(
   min(v['joint_ring_index'] for k,v in A.items() if not k.startswith('_')),max(v['joint_ring_index'] for k,v in A.items() if not k.startswith('_')),rj['joint_rings']['joint_ring_index'],
   max(v['face_cell_contrast']/max(v['trunk_cell_contrast'],1e-6) for k,v in A.items() if not k.startswith('_')),rj['face_noise']['face_cell_contrast']/max(rj['face_noise']['trunk_cell_contrast'],1e-6),
   max(v['tail_root_luminance_jump'] for k,v in A.items() if not k.startswith('_')),rj['tail_seam']['tail_root_luminance_jump'])],
 [('REJECTED','rej'),('Accepted\ncontrol','ok')],[(l,k) for k,l,_ in FL],380,'g8_10_failure_controls.jpg',lw=140,fn=fpath,capfont=17)
