import sys; sys.path.insert(0,'/home/claude/an'); import numpy as np, maskemu as E
S=np.load('/home/claude/an/start_VF.npz'); V,F=S['V'],S['F']
W=np.load('/home/claude/af/weights_05AE.npz'); names=[str(x) for x in W['names']]; o2n=np.load('/home/claude/af/old_to_new_05AE_to_05AF.npy'); lab=np.full(len(V),-1); lab[o2n]=W['W'].argmax(1)
Z=(V[:,2]-V[:,2].min())*100
E_=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]])
HARD=[(540,43,661,368),(485,43,708,226),(510,219,540,247),(661,219,691,247),(524,357,668,426),(446,366,549,448),(644,366,752,448),(452,653,752,722),(525,239,541,274),(660,239,676,274)]
JOINT=[(500,311,547,332),(663,302,709,322),(487,365,534,386),(674,354,721,375),(525,516,582,537),(628,515,685,536),(517,636,569,657),(641,636,693,656)]
def trans(e_sh,e_hip,e_tor):
    return [(540-e_tor,43,661+e_tor,368+e_tor),(510-e_sh,219-e_sh,540+e_sh,247+e_sh),(661-e_sh,219-e_sh,691+e_sh,247+e_sh),(524-e_hip,357-e_hip,668+e_hip,426+e_hip),(525-e_tor,239,541+e_tor,274+e_tor),(660-e_tor,239,676+e_tor,274+e_tor)]
def build(e_sh,e_hip,e_tor,nops,k=5,joint=True):
    e=E.Emu(V,F)
    for b in [(418,243,540,405),(661,243,791,405),(491,359,708,678)]: e.box(*b)
    e.invert()
    if joint:
        for b in JOINT: e.box(*b)
    for b in trans(e_sh,e_hip,e_tor): e.box(*b)
    e.smooth(nops*k)
    for b in HARD: e.box(*b)
    e.box(566,418,780,515,'right'); e.box(430,645,500,660,'right'); return e.M
def report(M):
    hard=M>=0.9999; a,b=E_[:,0],E_[:,1]; edge=hard[a]!=hard[b]; jump=np.abs(M[a]-M[b])[edge]
    bel={}
    for k,(zlo,zhi,parts) in {'biceps_L':(140,150,['upperarm_L']),'biceps_R':(137,147,['upperarm_R']),'forearm_L':(122,132,['forearm_L']),'forearm_R':(118,128,['forearm_R']),'thigh_L':(62,90,['thigh_L']),'thigh_R':(62,90,['thigh_R']),'calf_L':(22,45,['shin_L']),'calf_R':(22,45,['shin_R'])}.items():
        m=np.isin(lab,[names.index(p) for p in parts])&(Z>zlo)&(Z<zhi); bel[k]=round(float(M[m].mean()),3)
    limb=np.isin(lab,[names.index(k) for k in names if k.split('_')[0] in ('upperarm','forearm','thigh','shin')])
    return dict(max_jump_at_hard_edge=round(float(jump.max()),3),p99_jump=round(float(np.percentile(jump,99)),3),bellies=bel)
