import subprocess, os
from concurrent.futures import ThreadPoolExecutor
T='/home/claude/wayfarer-design/tools/rac/w1'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W=S+'/w2f'
B=[(W+'/mf/MF157-NAT_build.json',W+'/g/MF157-NAT'),(W+'/mf/MF168_build.json',W+'/g/MF168'),(S+'/w2e/mf/MF181_build.json',W+'/g/MF181')]+[(W+'/nm/%s_build.json'%n,W+'/g/'+n) for n in ('FN15','FN16','FN09','FN08','AE19','AE20','AE11','VA09','VA10')]
def g(x):
    p,o=x
    with open(W+'/logs/grid2_%s.log'%os.path.basename(o),'w') as f: rc=subprocess.run(['python3','w2a_drivers/mfm_grid.py',p,o],cwd=T,stdout=f,stderr=subprocess.STDOUT).returncode
    print('GRID',os.path.basename(o),rc,flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(g,B))
print('GRIDS2_DONE')
