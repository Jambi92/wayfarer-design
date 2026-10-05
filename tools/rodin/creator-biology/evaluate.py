# candidate validity rules (hard boundaries) and soft distributions; classify every variant
import json
REF=json.load(open('/tmp/claude-0/rodin/v1/ref_metrics.json'))
HREF=REF['height']
RULES=[ # key, hard_lo, hard_hi, soft_lo, soft_hi, label, source
 ('height',168.0,208.0,176.0,200.0,'Standing height (cm, excl. tail)','canon §4 (hard); soft = central 80 % candidate'),
 ('tail_len_pct',55.0,80.0,58.0,72.0,'Tail length (% standing height)','canon §10 (hard); soft candidate'),
 ('tail_RSI_n',0.75,1.20,0.85,1.10,'Tail root-sufficiency index (size-normalized, ref = 1)','derived: tail weight x lever / root section modulus'),
 ('tail_taper',0.0,1.25,0.0,1.12,'Peak area-loss rate (ref = 1)','derived: Gate-6 abrupt-taper failure guard'),
 ('tail_A50',0.27,0.48,0.31,0.44,'Area at mid-tail / root area','derived: threadlike (<) / cylindrical (>) guard'),
 ('tail_A25',0.065,0.16,0.075,0.13,'Area at 25 % from tip / root area','derived: distal continuity'),
 ('d_lean',-99.0,3.0,-99.0,1.5,'Extra lean needed to stand over the feet vs reference (deg)','derived: counterbalance (relative; reference itself needs 8.8 deg)'),
 ('rostral_index',0.255,0.335,0.268,0.315,'Rostral projection / head length (ref 0.288)','derived: §39 rostral floor (numeric cross-race check OPEN) / canine-dragon guard'),
 ('head_len_ratio',0.156,0.184,0.162,0.178,'Head length / standing height (ref 0.170)','derived: +-8 % around the +8 % head-scale decision'),
 ('thorax_d_over_w',0.80,1.00,0.83,0.95,'Thoracic depth / width (ref 0.88)','derived: deep narrow-to-moderate thoracic shell (§7-8)'),
]
def derived(m):
    import math
    d=dict(m); d['tail_RSI_n']=m['tail_RSI']*HREF/m['height']; sc=m['height']/HREF
    if 'heel_f' in m: d['lean_req_deg']=math.degrees(math.atan2((m['heel_f']+8.4*sc)-m['com_f'], m['com_u']-9.0*sc))   # foot offsets scale with stature
    d['d_lean']=d['lean_req_deg']-REF['lean_req_deg']; return d
def classify(m,params=None):
    d=derived(m); hard=[]; soft=[]
    for k,hl,hh,sl,sh,lab,src in RULES:
        v=d[k]
        if v<hl or v>hh: hard.append('%s %.3f outside [%g, %g]'%(k,v,hl,hh))
        elif v<sl or v>sh: soft.append(k)
    if params:
        rl=params.get('ros_len',1.0); jd=params.get('jaw_d',1.0); rd=params.get('ros_d',1.0)
        if rl>1.10 and (jd<1.0 or rd<1.0): hard.append('long rostrum (%.2f) on shallow jaw/rostral depth (%.2f/%.2f): §40 coupling'%(rl,jd,rd))
        if params.get('tail_fat_conc'): hard.append('caudal adipose concentrated at the base: abrupt mass step (tail_taper %.2f)'%d['tail_taper'])
    return d,hard,soft
