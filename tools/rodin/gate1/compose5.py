import sys; sys.path.insert(0,'/tmp/claude-0/rodin/adopt')
from compose import *
from PIL import Image, ImageDraw
import json
G='/tmp/claude-0/rodin/g1/'; O=G+'sheets5/'; A=json.load(open(G+'acct5.json'))
def tile(p,cell):
    im=Image.open(p).convert('RGBA').resize((cell,cell),Image.LANCZOS); bg=Image.new('RGB',im.size,PANEL); bg.paste(im,(0,0),im); return bg
def row(items,title,sub,out,cell=760):
    W=20+len(items)*(cell+20); img=Image.new('RGB',(W,cell+60+40*len(sub)+60),BG); d=ImageDraw.Draw(img)
    d.text((20,16),title,font=F(30,True),fill=TXT)
    for i,s in enumerate(sub): d.text((20,62+30*i),s,font=F(20),fill=SUB)
    top=100+30*len(sub)
    for i,(p,lab) in enumerate(items):
        x=20+i*(cell+20); img.paste(tile(p,cell),(x,top)); d.text((x+6,top-32),lab,font=F(22,True),fill=SUB)
    img.save(out,quality=90)
T=" — DIAGNOSTIC / NOT FINAL"
strip(G+'E5',"Saurin Gate 5 — forelimb / wrist / hand reconstruction on the accepted Gate 4 body"+T,
 ["Arms and hands only (shoulder root → upper arm → elbow → forearm → wrist → carpal/metacarpal palm → five digits → claws). Gate 1 / 2A / 3A / 4, TS6.1 head, height and shoulder placement locked.",
  "Removed: B1/Rodin arm surface map (deltoid cap, biceps/triceps bellies, human hand). Kept: B1 limb mass, length and shoulder position (low-pass), which preserves the silhouette."],O+'g5_01_five_views.jpg')
row([(G+'E5_shF.png','Front'),(G+'E5_shL.png','Lateral'),(G+'E5_shF34.png','Front 3/4'),(G+'E5_shR34.png','Rear 3/4'),(G+'E5_shLF34.png','Front 3/4 (left side)')],
 "Gate 5 — shoulder / upper arm"+T,["No deltoid ball: the upper arm grows out of the thoracic/scapular mass. Clavicular, acromial and scapular fans overlap and converge onto the lateral humerus.",
 "Upper arm: long anterior flexor plane (continuing into the medial forearm), posterior extensor plane with a lateral slip. No biceps/triceps bellies."],O+'g5_02_shoulder_upper_arm.jpg',cell=620)
row([(G+'E5_elL.png','Lateral'),(G+'E5_elR.png','Rear'),(G+'E5_elF.png','Front'),(G+'E5_elR34.png','Rear 3/4')],
 "Gate 5 — elbow"+T,["Upper-arm termination into a posterior extension ridge (olecranon line), medial and lateral epicondylar stabilisers, and a soft anterior hinge hollow.",
 "Below the hinge the two forearm paths split: flexor (palmar/medial) and extensor (dorsal/lateral). No spikes or ornament."],O+'g5_03_elbow.jpg',cell=700)
row([(G+'E5_fwF.png','Forearm front'),(G+'E5_fwL.png','Forearm lateral'),(G+'E5_fwR.png','Forearm rear'),(G+'E5_wrL.png','Wrist close')],
 "Gate 5 — forearm / wrist"+T,["Forearm: flexor and extensor masses, a spiral rotational band crossing from the lateral elbow to the radial wrist, an ulnar load ridge, and two distal tendon paths.",
 "Wrist: forearm narrows (controlled, not a stalk) and overlaps a distinct carpal block, which then widens into the metacarpal palm."],O+'g5_04_forearm_wrist.jpg',cell=700)
row([(G+'H5_hD.png','Dorsal'),(G+'H5_hP.png','Palmar'),(G+'H5_hR.png','Radial (thumb side)'),(G+'H5_hU.png','Ulnar'),(G+'H5_h34.png','Front 3/4 (palmar)'),(G+'H5_h34d.png','Front 3/4 (dorsal)')],
 "Gate 5 — isolated right hand, hand frame"+T,["Chain: carpal block → metacarpal palm (thenar mass, hypothenar ridge) → knuckle row → phalanges (2-3-3-3-3) → claws grown from the terminal phalanx. Wrist to claw tip ≈ 21 cm (0.11H).",
 "Digit lengths differ (III longest) with uneven spacing and splay; relaxed natural curl. Opposable thumb set palmar to the palm plane. Cropped at the wrist for clarity."],O+'g5_05_hand_isolated.jpg',cell=560)
row([(G+'H5_gTip.png','Right hand from the fingertips'),(G+'H5_gPal.png','Right hand, palmar oblique'),(G+'H5L_gPal.png','Left hand, palmar oblique'),(G+'H5L_gTip.png','Left hand from the fingertips')],
 "Gate 5 — grasp readiness / thumb opposition"+T,["Relaxed pose. The thumb metacarpal sits palmar to the palm plane and its tip points across the palm toward digits II–III: a pinch/grip can close without re-rigging the thumb.",
 "The fingers keep a relaxed flexion arc, with joint swellings at each joint so articulation reads in clay."],O+'g5_06_grasp_readiness.jpg',cell=700)
# before/after
views=[('front','Full front'),('front34','Full front 3/4'),('profile','Full profile'),('shF34','Shoulder front 3/4'),('elR34','Elbow rear 3/4'),('fwF','Forearm front')]
cell=520; W=240+len(views)*(cell+20); img=Image.new('RGB',(W,150+2*(cell+20)+60+2*(cell+20)),BG); d=ImageDraw.Draw(img)
d.text((20,16),"Gate 5 before/after — accepted Gate 4 vs Gate 5, identical cameras"+T,font=F(30,True),fill=TXT)
d.text((20,62),"Rows 1-2: identical orthographic cameras on the two meshes. Rows 3-4: the isolated right hand (B1/Gate 4 hand vs the Gate 5 hand) in the same hand frame and camera.",font=F(20),fill=SUB)
for r,(lab,tag) in enumerate((("Gate 4\n(before)",'E4'),("Gate 5\n(after)",'E5'))):
    y=130+r*(cell+20); d.multiline_text((20,y+cell//2-30),lab,font=F(24,True),fill=TXT,spacing=8)
    for c,(v,vl) in enumerate(views):
        x=240+c*(cell+20); img.paste(tile(G+'%s_%s.png'%(tag,v),cell),(x,y))
        if r==0: d.text((x+6,y-28),vl,font=F(19,True),fill=SUB)
hv=[('hD','Hand dorsal'),('hP','Hand palmar'),('hR','Hand radial'),('h34','Hand front 3/4'),('gPal','Palmar oblique'),('gTip','From fingertips')]
for r,(lab,tag) in enumerate((("Gate 4\nhand",'H4'),("Gate 5\nhand",'H5'))):
    y=130+2*(cell+20)+60+r*(cell+20); d.multiline_text((20,y+cell//2-30),lab,font=F(24,True),fill=TXT,spacing=8)
    for c,(v,vl) in enumerate(hv):
        x=240+c*(cell+20); img.paste(tile(G+'%s_%s.png'%(tag,v),cell),(x,y))
        if r==0: d.text((x+6,y-28),vl,font=F(19,True),fill=SUB)
img.save(O+'g5_07_before_after.jpg',quality=88)
# accounting
o=A['_out']
img=strip(G+'AC5',"Gate 5 accounting — provenance relative to the accepted Gate 4 mesh",
 ["Green: identical Gate 4 vertices (%d). Amber: copied and relaxed at the seam (%d, ≤ %.2f cm). Red: re-surfaced in Gate 5 (%d new vertices)."%(o['identical'],o['relaxed'],o['relaxed_max'],o['new']),
  "Free tail, torso/pelvis/head/neck (|x| < 19.5), legs/feet and hips/thighs: 100%% vertex-identical. %d Gate 4 vertices replaced, all within 3.0 cm of B1's own arm/hand surface."%A['_changed_gate4_verts']],O+'g5_08_accounting.jpg')
cell=760; rowi=Image.new('RGB',(img.width,cell+40),BG)
for i,p in enumerate((G+'AC5_shF34.png',G+'AC5_elR34.png',G+'AC5_fwF.png')): rowi.paste(tile(p,cell),(20+i*(cell+20),20))
leg=Image.new('RGB',(img.width,80),BG); d=ImageDraw.Draw(leg); x=20
for lab,c in (("Identical to Gate 4",COL["PRESERVE"]),("Copied, relaxed ≤0.93 cm at the seam",COL["MODIFY"]),("Re-surfaced in Gate 5",COL["REBUILD"])):
    d.rectangle((x,22,x+34,56),fill=c); d.text((x+46,26),lab,font=F(21,True),fill=TXT); x+=46+d.textlength(lab,font=F(21,True))+50
out=Image.new('RGB',(img.width,img.height+rowi.height+leg.height),BG); out.paste(img,(0,0)); out.paste(rowi,(0,img.height)); out.paste(leg,(0,img.height+rowi.height)); out.save(O+'g5_08_accounting.jpg',quality=88)
print('ok')
