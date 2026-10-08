import subprocess
T='/home/claude/wayfarer-design/tools/rac/w1'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
J=[]
for src,h in (("GO208","208"),("GO218","218")):
    for n,m,w in (("06",0.0,0.5),("07",1.0,0.5),("09",0.5,1.0),("10",1.0,1.0),("16",0.25,0.25)): J.append(("GOR-BODY-%s_%s"%(n,h),src,m,w))
ps=[]
for n,src,m,w in J:
    ps.append(subprocess.Popen(['python3','w2d_drivers/go_comp.py',n,src,str(m),str(w)],cwd=T,stdout=open(S+'/w2d/logs/comp2.log','a'),stderr=subprocess.STDOUT))
    if len(ps)>=2: ps.pop(0).wait()
for p in ps: p.wait()
print('COMP2_DONE')
