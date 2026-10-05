import sys; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); from sets import NARROW, BROAD, M
K=1.0114   # stature-normalization compensation: head and tail keep the reference absolute size / % H (no head or tail dimorphism)
FEM={'trunk_len':1.06,'pelvis_w':1.03,'head':K,'tail_len':K}   # candidate sex-correlated tendency (mean shift; strong overlap)
def F(*d):
    o=M(FEM,*d)
    if any('tail_len' in x for x in d): o['tail_len']=o['tail_len']*K
    return o
JOBS=[  # id, label, sex, params
 ('m_ref','Male / reference','M',{}),
 ('f_ref','Female reference','F',F()),
 ('f_n','Female Narrow','F',F(NARROW)),('f_b','Female Broad','F',F(BROAD)),
 ('f_mlo','Female muscle low','F',F({'muscle':-1.0})),('f_mhi','Female muscle high','F',F({'muscle':1.0})),
 ('f_flo','Female fat low','F',F({'fat':-1.0})),('f_fhi','Female fat high','F',F({'fat':1.0})),
 ('f_t55','Female tail 55 % (coupled base 0.83)','F',F({'tail_len':55/64.613,'tail_base':0.83})),
 ('f_t78','Female tail 78 % (coupled base 1.15)','F',F({'tail_len':78/64.613,'tail_base':1.15})),
 ('f_b80','Female Broad + tail 80 % (base 1.16)','F',F(BROAD,{'tail_len':80/64.613,'tail_base':1.16})),
 # overlap: male with long trunk / wide pelvis within individual range vs female with short trunk
 ('m_ov','Male, trunk +6 %, pelvis +3 % (individual)','M',{'trunk_len':1.06,'pelvis_w':1.03,'head':K,'tail_len':K}),
 ('f_ov','Female, trunk -6 %, pelvis -3 % vs female mean (individual)','F',{'trunk_len':1.0,'pelvis_w':1.0}),
 # anti-stereotype
 ('a1','Female: tallest + Broad + high muscle','F',F({'height':208.0,'muscle':1.0},BROAD)),
 ('a2','Male: shortest + Narrow','M',M({'height':168.0},NARROW)),
 ('a5','Female: high fat (no hourglass)','F',F({'fat':1.0})),
 ('a6','Female: low fat, reference muscle','F',F({'fat':-1.0})),
 ('a7m','Equal height/frame pair: male 180 cm Balanced','M',{'height':180.0}),
 ('a7f','Equal height/frame pair: female 180 cm Balanced','F',F({'height':180.0})),
 ('a8','Male: low muscle + high fat + Narrow','M',M(NARROW,{'muscle':-1.0,'fat':1.0})),
 ('a9','Female: trunk at the hard maximum (+10 %)','F',{'trunk_len':1.10,'pelvis_w':1.03,'head':1.019,'tail_len':1.019}),
 ('a10','Female: trunk mean shift stacked past the bound (+16 %)','F',{'trunk_len':1.16,'pelvis_w':1.03,'head':1.03,'tail_len':1.03}),
 ('a11','Female: pelvis stacked past the bound (+10 %)','F',F({'pelvis_w':1.10})),
]
