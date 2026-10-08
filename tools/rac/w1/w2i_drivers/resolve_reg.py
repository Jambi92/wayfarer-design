# resolve the g7regs import chain from the repo tools/ and the earlier racebodies outputs (latest copy wins), rewriting /tmp paths into the scratchpad
import subprocess, re, glob, os
W='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/w2i/rodin'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
def find(mod):
    c=glob.glob('/home/claude/wayfarer-design/tools/**/%s.py'%mod, recursive=True)
    if c: return c[0]
    c=sorted(glob.glob('/mnt/attach/outputs/racebodies*/%s.py'%mod), key=lambda p: int(re.sub(r'\D','',p.split('/')[-2]) or 0))
    return c[-1] if c else None
for it in range(15):
    r=subprocess.run(['python3','g7regs.py',W+'/c12/g15up.npz',W+'/c12/g15reg.npz'],cwd=W+'/g1',capture_output=True,text=True,env={**os.environ,'HEAD_SCALE':'1.08'})
    m=re.search(r"No module named '([^']+)'",r.stderr)
    if r.returncode==0: print('OK'); break
    if not m: print(r.stderr[-1500:]); break
    src=find(m.group(1)); print('need',m.group(1),'->',src)
    if not src: break
    t=open(src).read().replace('/tmp/claude-0/rodin',W).replace('/tmp/claude-0/rb',W+'/rb'); open(W+'/g1/%s.py'%m.group(1),'w').write(t)
