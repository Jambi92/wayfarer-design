import subprocess, json
T='/home/claude/wayfarer-design/tools/rac/w1'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
N3={"bone_scales":{"LR:clavicle":[1,0.95,1],"spine_02":[0.95,1,1],"spine_03":[0.95,1,1]},"kb_nodes":[1,1,1,0.95,0.95,0.95]}
B7={"bone_scales":{"LR:clavicle":[1,1.015,1],"pelvis":[1.05,1,1],"LR:thigh":[1.05,1,1.05]},"kb_nodes":[1.05,1.05,1,1,1,1]}
D98={"bone_scales":{"spine_03":[1,0.98,1]},"ka":0.98,"kp":0.98,"kd_from":0.3}
J=[("GO229","0.8241",None),("GON3_218","0.7503",N3),("GOB7_218","0.7503",B7),("GO14_218","0.7503",D98)]
ps=[]
for n,m,f in J:
    ps.append(subprocess.Popen(['python3','w2d_drivers/go_body.py',n,m]+([json.dumps(f)] if f else []),cwd=T,stdout=open(S+'/w2d/logs/%s.log'%n,'w'),stderr=subprocess.STDOUT))
    if len(ps)>=2: ps.pop(0).wait()
for p in ps: p.wait()
print('M218_DONE')
