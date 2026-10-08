import subprocess, json
T='/home/claude/wayfarer-design/tools/rac/w1'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
N4={"bone_scales":{"LR:clavicle":[1,0.95,1],"spine_02":[0.95,1,1],"spine_03":[0.95,1,1],"pelvis":[0.98,1,1],"LR:thigh":[0.98,1,0.98]},"kb_nodes":[0.98,0.98,0.965,0.95,0.95,0.95]}
J=[("GON5","0.8369140625",N4),("GON5_218","0.7503",N4)]
ps=[subprocess.Popen(['python3','w2d_drivers/go_body.py',n,m,json.dumps(f)],cwd=T,stdout=open(S+'/w2d/logs/%s.log'%n,'w'),stderr=subprocess.STDOUT) for n,m,f in J]
for p in ps: p.wait()
print('N4_DONE')
