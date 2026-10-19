import json, subprocess, sys, itertools, os
base=json.load(open('pR.json'))
res=[]
for p3x,p3z,p2x,ks in itertools.product([-33.0,-32.2],[104.2,104.8],[-28.6,-29.4],[0.6,0.75]):
    p=json.loads(json.dumps(base))
    p['palm_override']['P3']['p0'][0]=p3x; p['palm_override']['P3']['p1'][0]=p3x
    p['palm_override']['P3']['p0'][2]=p3z; p['palm_override']['P3']['p1'][2]=p3z
    p['palm_override']['P2']['p0'][0]=p2x; p['palm_override']['P2']['p1'][0]=p2x
    p['k_thumb']=ks
    json.dump(p,open('pR_sw.json','w'))
    subprocess.run('python3 handdesign.py R "$(cat pR_sw.json)" > /dev/null',shell=True)
    out=subprocess.run('./run_e.sh sw 2 | tail -1',shell=True,capture_output=True,text=True).stdout
    import re
    m=re.search(r"'hand_R': (\d+)",out); n=int(m.group(1)) if m else 0
    print(p3x,p3z,p2x,ks,'hand_R L2 selfx',n, flush=True)
