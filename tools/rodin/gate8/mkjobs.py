import json, sys; sys.path.insert(0,'/tmp/claude-0/rodin/g8'); from g8lib import PH, NEUTRAL
G='/tmp/claude-0/rodin/g1/'; D='/tmp/claude-0/rodin/g8/'; R=D+'r/'
body=dict(mesh=G+'cs7c.npz',base=G+'g7up.npz',fields=D+'fld_body.npz',res=900,samples=40)
FB=["f34:45:0:0:0:94:198","r34:150:0:0:0:94:198","mid:35:5:0:0:120:80","hF34:40:12:0:8:181:24","hP:90:0:0:6:181:26"]
json.dump(dict(body,jobs=[dict(tag=R+'A_'+k,ph=v,views=FB) for k,v in PH.items()]),open(D+'jobA.json','w'))
base=dict(primary=(0.45,0.34,0.22),secondary=(0.17,0.12,0.08),ventral=(0.62,0.54,0.40),contrast=0.72,cs=0.3,face_accent=0.3,seed=31)
PAT=['uniform','mottled','blotched','banded','broken_banded','axial','speckled','regional','mixed']
PV=["prof:90:0:0:-50:94:200","r34:150:0:0:0:94:198","tailP:90:5:0:-70:84:120","trc:130:15:0:-26:90:34"]
jb=[]
for p in PAT:
    ph=dict(base,pattern=p)
    if p=='axial': ph.update(secondary=(0.66,0.56,0.38),contrast=0.6)
    if p=='speckled': ph.update(speckle=0.13,soft=0.1)
    if p=='mixed': ph.update(asym=0.55)
    jb.append(dict(tag=R+'B_'+p,ph=ph,views=PV))
json.dump(dict(body,jobs=jb),open(D+'jobB.json','w'))
jc=[]
for rb in (0.30,0.45,0.55,0.72): jc.append(dict(tag=R+'C_cal%02d'%int(rb*100),ph=dict(NEUTRAL,rough=rb),views=["f34:45:0:0:0:94:198","mid:35:5:0:0:120:80","dorsC:150:10:0:-6:132:16"]))
jc.append(dict(tag=R+'C_rsa',ph=PH['P1_umber_mottled'],views=["dors:160:10:0:-6:132:14","elb:100:0:29:-4:117:12","fx:60:5:4:9:182:8","vent:0:-5:0:8:124:14","eyec:70:5:3.6:10.3:183.5:4.2"]))
for k in ('P1_umber_mottled','P2_slate_banded','P4_charcoal_uniform','P7_bluegray_broken'):
    for st in (0.0,0.5,1.0): jc.append(dict(tag=R+'C_eye_%s_m%d'%(k.split('_')[0],int(st*10)),ph=PH[k],state=dict(membrane=st),views=["eyec:70:5:3.6:10.3:183.5:4.2"]))
P1=PH['P1_umber_mottled']
F=[('wet_plastic',dict(P1,pattern='uniform',contrast=0),dict(flat=(0.16,0.42,0.17),rough=0.06,coat=1.0),"mid:35:5:0:0:120:80"),
   ('metallic',P1,dict(metallic=1.0,rough=0.25),"mid:35:5:0:0:120:80"),
   ('gem',PH['P5_olive_axial'],dict(transmission=0.9,rough=0.02),"mid:35:5:0:0:120:80"),
   ('pale_belly',dict(P1,fail='pale_belly'),{},"f34:45:0:0:0:94:198"),
   ('paint_mask',dict(P1,fail='paint_mask'),{},"f34:45:0:0:0:94:198"),
   ('joint_rings',dict(PH['P2_slate_banded'],pattern='uniform',fail='joint_rings'),{},"f34:45:0:0:0:94:198"),
   ('face_noise',dict(P1,fail='face_noise'),{},"hF34:40:12:0:8:181:24"),
   ('tail_seam',dict(P1,pattern='uniform',fail='tail_seam'),{},"tailP:90:5:0:-70:84:120"),
   ('dragon',dict(P1,pattern='uniform',primary=(0.62,0.06,0.04),secondary=(0.3,0.02,0.02),belly=(0.95,0.72,0.18),keratin=(0.95,0.82,0.45),ker_rel=0.0,fail='dragon'),dict(metallic=0.35,rough=0.15,coat=1.0),"f34:45:0:0:0:94:198")]
for nm,ph,ov,v in F: jc.append(dict(tag=R+'C_fail_'+nm,ph=ph,override=ov,views=[v]))
json.dump(dict(body,jobs=jc),open(D+'jobC.json','w'))
jd=[dict(tag=R+'D_foot_'+k.split('_')[0],ph=PH[k],views=["fPl:0:-85:23:12:5:30","f34:35:25:23:12:5:30","fcl:15:15:24:22:3:11"]) for k in ('P1_umber_mottled','P3_ochre_speckled')]
json.dump(dict(body,crop=D+'crop_foot.npz',jobs=jd),open(D+'jobDf.json','w'))
jh=[dict(tag=R+'D_hand_'+k.split('_')[0],ph=PH[k],views=["hPal:-88:-9:37.1:9.7:88.4:27","hD:92:9:37.1:9.7:88.4:27"]) for k in ('P1_umber_mottled','P3_ochre_speckled')]
json.dump(dict(body,crop=D+'crop_hand.npz',jobs=jh),open(D+'jobDh.json','w'))
KR={'horn':dict(keratin=(0.55,0.48,0.38),ker_rel=0.1),'matched':dict(ker_rel=0.75),'dark':dict(keratin=(0.11,0.10,0.09),ker_rel=0.05,ker_tip=(0.35,0.30,0.24))}
for V in ('minimal_ridges','low_hornlets','swept_paired','mixed_asym','crest'):
    U='crest_c' if V=='crest' else V
    jobs=[]
    for pk in ('P1_umber_mottled','P7_bluegray_broken'):
        for kn,kv in KR.items(): jobs.append(dict(tag=R+'E_%s_%s_%s'%(V,pk.split('_')[0],kn),ph=dict(PH[pk],**kv),views=["hF34:40:12:0:6:183:32","hR34:145:15:0:-2:183:32"]))
    z=G+'hvcc_%s.npz'%V
    json.dump(dict(mesh=z,base=G+'hvu_%s.npz'%U,fields=D+'fld_hv_%s.npz'%V,res=800,samples=40,jobs=jobs),open(D+'jobE_%s.json'%V,'w'))
print('jobs ok')
