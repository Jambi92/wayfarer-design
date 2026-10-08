import subprocess, json, sys
T='/home/claude/wayfarer-design/tools/rac/w1'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
M=sys.argv[1]; suf=sys.argv[2]; which=sys.argv[3].split(',')
def br(f): return {"bone_scales":{"LR:clavicle":[1,f,1],"spine_02":[f,1,1],"spine_03":[f,1,1]},"kb_nodes":[1,1,1,f,f,f]}
def dp(g): return {"ka":g,"kp":g,"kd_from":0.3}
F={}
for f in json.loads(sys.argv[4]): F["GOX12_%s%s"%(str(f)[2:],suf)]=br(f)
for g in json.loads(sys.argv[5]): F["GOD14_%s%s"%(str(g)[2:],suf)]=dp(g)
F={k:v for k,v in F.items() if any(k.startswith(w) for w in which)}
ps=[]
for n,f in F.items():
    ps.append(subprocess.Popen(['python3','w2d_drivers/go_body.py',n,M,json.dumps(f)],cwd=T,stdout=open(S+'/w2d/logs/%s.log'%n,'w'),stderr=subprocess.STDOUT))
    if len(ps)>=2: ps.pop(0).wait()
for p in ps: p.wait()
print('EXT_DONE', list(F))
