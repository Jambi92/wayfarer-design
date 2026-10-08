import subprocess, json
T='/home/claude/wayfarer-design/tools/rac/w1'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
M='0.8369140625'
F={"GON3":{"bone_scales":{"LR:clavicle":[1,0.95,1],"spine_02":[0.95,1,1],"spine_03":[0.95,1,1]},"kb_nodes":[1,1,1,0.95,0.95,0.95]},
   "GOB3":{"bone_scales":{"LR:clavicle":[1,1.05,1],"pelvis":[1.05,1,1],"LR:thigh":[1.05,1,1.05]},"kb_nodes":[1.05,1.05,1,1,1,1]},
   "GOB4":{"bone_scales":{"LR:clavicle":[1,1.05,1],"pelvis":[1.05,1,1],"LR:thigh":[1.05,1,1.05],"spine_02":[1.015,1,1],"spine_03":[1.015,1,1]},"kb_nodes":[1.05,1.05,1.015,1.015,1.015,1.015]}}
ps=[]
for n,f in F.items():
    ps.append(subprocess.Popen(['python3','w2d_drivers/go_body.py',n,M,json.dumps(f)],cwd=T,stdout=open(S+'/w2d/logs/%s.log'%n,'w'),stderr=subprocess.STDOUT))
    if len(ps)==2: ps[0].wait()
for p in ps: p.wait()
print('FR2_DONE')
