# ident_targets.py : MakeHuman (CC0) hm08 morph targets as analysis-frame deltas on the 13 380-vertex Grask body.
import numpy as np, os
T='/tmp/claude-0/mh/mh/makehuman/data/targets/'
R='/tmp/claude-0/rp2/'
_s=np.load(R+'GR5DE3_r6.npz'); KEEP=np.nonzero(_s['keep'])[0]; INV=-np.ones(len(_s['keep']),int); INV[KEEP]=np.arange(len(KEEP))
_cache={}
def target(name, scale_cm=12.0):
    """delta (13380,3) in analysis cm for a target file name like 'ears/l-ear-scale-vert-incr'."""
    if name in _cache: return _cache[name]*scale_cm
    D=np.zeros((len(KEEP),3)); 
    for l in open(T+name+'.target'):
        if l.startswith('#') or not l.strip(): continue
        p=l.split(); i=INV[int(p[0])]
        if i>=0: D[i]=[float(p[1]),float(p[3]),float(p[2])]   # MH (x left, y up, z fwd) -> (x, f, u)
    _cache[name]=D; return D*scale_cm
def both(name, w, scale_cm=12.0):
    """apply an l-/r- pair (name contains {s})"""
    return w*(target(name.format(s='l'),scale_cm)+target(name.format(s='r'),scale_cm))
def compose(spec, scale_cm=12.0):
    D=0
    for name,w in spec.items():
        D = D + (both(name,w,scale_cm) if '{s}' in name else w*target(name,scale_cm))
    return D
