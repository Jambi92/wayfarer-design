import subprocess
from concurrent.futures import ThreadPoolExecutor
T='/home/claude/wayfarer-design/tools/rac/w1'; S='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W=S+'/w2e'
B=[('st','SG152-NAT'),('st','SG163'),('st','SG173'),('st','SG190'),('st','SG203'),('st','SG208'),('mf','MF163'),('mf','MF178'),
   ('fr','SGB178'),('fr','SGN178'),('fr','SGN208'),('fr','SGB208'),('fr','SGB152'),('fr','SGN152'),('nm','SG04'),('nm','SG09'),('nm','SG10'),('st','SG181')]
def g(x):
    d,n=x
    with open(W+'/logs/grid_%s.log'%n,'w') as f: rc=subprocess.run(['python3','w2a_drivers/mfm_grid.py',W+'/%s/%s_build.json'%(d,n),W+'/g/'+n],cwd=T,stdout=f,stderr=subprocess.STDOUT).returncode
    print('GRID',n,rc,flush=True)
with ThreadPoolExecutor(2) as ex: list(ex.map(g,B))
print('GRIDS_DONE',flush=True)
