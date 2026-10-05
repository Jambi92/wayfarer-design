import sys; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); from sets import NARROW, BROAD, M
# stature compensation so head and tail keep the reference absolute size / % H when the trunk lengthens
def K(tr): return 1.0+(tr-1.0)*0.19
FE=2.0; VB=1.6; VC=3.0
def fem(tr,pel=1.055,fe=FE,vb=VB):
    k=K(tr); return {'trunk_len':tr,'pelvis_w':pel,'head':k,'tail_len':k,'flank':fe,'vfull':vb}
REF=fem(1.10)      # final reference female (visual body)
CEN=fem(1.07)      # female sampling centre
def R(*d,base=REF):
    o=M(base,*d)
    if any('tail_len' in x for x in d): o['tail_len']=o['tail_len']*base['tail_len']
    return o
JOBS=[
 ('m_ref','Male / reference (male mean)','M',{}),
 ('p1','Pass-1 female (+6 % / +3 %)','F',{'trunk_len':1.06,'pelvis_w':1.03,'head':K(1.06),'tail_len':K(1.06)}),
 ('fref','Final reference female (trunk +10, pelvis +5.5, E 2.0, B 1.6)','F',REF),
 ('fcen','Female sampling centre (trunk +7, pelvis +5.5, E 2.0, B 1.6)','F',CEN),
 # frame / composition on the reference female
 ('fr_n','Female ref, Narrow','F',R(NARROW)),('fr_b','Female ref, Broad','F',R(BROAD)),
 ('fr_mlo','Female ref, muscle low','F',R({'muscle':-1.0})),('fr_mhi','Female ref, muscle high','F',R({'muscle':1.0})),
 ('fr_flo','Female ref, fat low','F',R({'fat':-1.0})),('fr_fhi','Female ref, fat high','F',R({'fat':1.0})),
 # stature
 ('fr_h168','Female ref, 168 cm','F',R({'height':168.0})),('fr_h208','Female ref, 208 cm','F',R({'height':208.0})),
 # tail
 ('fr_t55','Female ref, tail 55 % (base 0.83)','F',R({'tail_len':55/64.613,'tail_base':0.83})),
 ('fr_t78','Female ref, tail 78 % (base 1.15)','F',R({'tail_len':78/64.613,'tail_base':1.15})),
 ('fr_b80','Female ref, Broad + tail 80 % (base 1.16)','F',R(BROAD,{'tail_len':80/64.613,'tail_base':1.16})),
 # overlap
 ('m_in','Male at the female sampling centre (trunk +7, pelvis +5.5, E 2.0, B 1.6)','M',CEN),
 ('m_mid','Male individual inside the female range (trunk +5, pelvis +3, E 1.0, B 0.8)','M',fem(1.05,1.03,1.0,0.8)),
 ('f_mean','Female at the male mean (all tendencies 0)','F',{}),
 ('f_near','Female near the male mean (trunk +2, pelvis +1, E 0.5, B 0.4)','F',fem(1.02,1.01,0.5,0.4)),
 # anti-stereotype
 ('as_bm','Female: Broad + high muscle','F',R(BROAD,{'muscle':1.0})),
 ('as_nl','Female: Narrow + low muscle','F',R(NARROW,{'muscle':-1.0})),
 ('as_mn','Male: Narrow with female-shifted trunk/pelvis/body wall/ventral','M',R(NARROW)),
 # clamps
 ('cl_nC','Narrow + C-level ventral 3.0 cm requested','F',R(NARROW,{'vfull':VC})),
 ('cl_fC','Fat high + C-level ventral 3.0 cm (valid individual)','F',R({'fat':1.0,'vfull':VC})),
 ('cl_nCk','Narrow + C requested, clamped to 2.1 cm','F',R(NARROW,{'vfull':2.1})),
 ('cl_nf','Narrow + fat high (B 1.6 requested)','F',R(NARROW,{'fat':1.0})),
 ('cl_nfk','Narrow + fat high, B clamped to 1.5 cm','F',R(NARROW,{'fat':1.0,'vfull':1.5})),
 ('m_fhi','Male, fat high (control for C6)','M',{'fat':1.0}),
 ('cl_t16','Trunk +16 % requested','F',fem(1.16)),
]
