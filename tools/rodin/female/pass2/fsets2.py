import sys; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); from sets import NARROW, BROAD, M
K10=1.019   # stature compensation for trunk +10 %: head and tail keep the reference absolute size / % H
STR={'trunk_len':1.10,'pelvis_w':1.055,'head':K10,'tail_len':K10}     # candidate A (structural)
VB=1.6; VC=3.0; BD=3.8; FE=2.0      # peak displacement (cm): B, C ventral fullness; D breast projection
def A(*d):
    o=M(STR,*d)
    if any('tail_len' in x for x in d): o['tail_len']=o['tail_len']*K10
    return o
JOBS=[
 ('m_ref','Male / reference','M',{}),
 ('p1','Pass-1 female (+6 % / +3 %)','F',{'trunk_len':1.06,'pelvis_w':1.03,'head':1.0114,'tail_len':1.0114}),
 ('a_tr','Trunk +10 % only','F',{'trunk_len':1.10,'head':K10,'tail_len':K10}),
 ('a_pv','Pelvic band +5.5 % only','F',{'pelvis_w':1.055}),
 ('A','A  structural','F',A()),
 ('B','B  ventral fullness, subtle','F',A({'vfull':VB})),
 ('C','C  ventral fullness, stronger','F',A({'vfull':VC})),
 ('D','D  breast-bearing (comparison only)','F',A({'breast':BD})),
 ('E','E  coelomic body wall (additional)','F',A({'flank':FE})),
 ('E2','E + B  body wall + subtle ventral','F',A({'flank':FE,'vfull':VB})),
 # overlap / anti-stereotype on the strongest non-mammalian candidates (C, and B as its lower setting)
 ('c_n','C, Narrow','F',A(NARROW,{'vfull':VC})),
 ('c_bm','C, Broad + high muscle','F',A(BROAD,{'muscle':1.0,'vfull':VC})),
 ('c_flo','C, fat low','F',A({'fat':-1.0,'vfull':VC})),
 ('c_fhi','C, fat high','F',A({'fat':1.0,'vfull':VC})),
 ('c_tall','C, 208 cm + Broad + high muscle','F',A(BROAD,{'height':208.0,'muscle':1.0,'vfull':VC})),
 ('c_t80','C, Broad + tail 80 % (base 1.16)','F',A(BROAD,{'tail_len':80/64.613,'tail_base':1.16,'vfull':VC})),
 ('c_t55','C, tail 55 % (base 0.83)','F',A({'tail_len':55/64.613,'tail_base':0.83,'vfull':VC})),
 ('e_n','E+B, Narrow','F',A(NARROW,{'flank':FE,'vfull':VB})),
 ('e_bm','E+B, Broad + high muscle','F',A(BROAD,{'muscle':1.0,'flank':FE,'vfull':VB})),
 ('e_flo','E+B, fat low','F',A({'fat':-1.0,'flank':FE,'vfull':VB})),
 ('e_fhi','E+B, fat high','F',A({'fat':1.0,'flank':FE,'vfull':VB})),
 ('m_ovE','Male inside the female range: trunk +10 %, pelvis +5.5 %, body wall at half E','M',A({'flank':1.0})),
 ('m_sn','Male, 168 cm + Narrow + low muscle','M',M(NARROW,{'height':168.0,'muscle':-1.0})),
 ('m_ovB','Male inside the female range: trunk +10 %, pelvis +5.5 %, fullness at B','M',A({'vfull':VB})),
 ('f_lo','Female low end: trunk +0 %, pelvis +0 %, fullness 0','F',{}),
 ('f_mid','Female individual: trunk +4 %, pelvis +2 %, fullness at B','F',{'trunk_len':1.04,'pelvis_w':1.02,'head':1.0076,'tail_len':1.0076,'vfull':VB}),
 ('c_over','Fullness requested at 1.5 x C (4.5 cm)','F',A({'vfull':4.5})),
 ('c_fhi_over','C + fat high + 1.5 x C','F',A({'fat':1.0,'vfull':4.5})),
 ('t16','Female individual above the mean: trunk +16 % requested','F',{'trunk_len':1.16,'pelvis_w':1.055,'head':1.03,'tail_len':1.03}),
]
