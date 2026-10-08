# RAC S7 normalization: re-run an existing evaluation script UNCHANGED except for its input / output locations.
#   base mode: outputs redirected to a scratch mirror of reviews/ (reproduction control: must equal the committed evidence);
#   norm mode: the same, and every skeletal-proxy (SKP) input directory replaced by its S7-normalized copy (s7_normalize.py).
# Usage: python3 remap_run.py base|norm MIRROR_ROOT NORM_ROOT SCRIPT [script args...]
import sys, os, re, runpy
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
mode, RO, N, script = sys.argv[1:5]; args = sys.argv[5:]
blk = {"w2a_eval.py": "w2a", "w2a1_eval.py": "w2a1", "w2b_eval.py": "w2b"}.get(os.path.basename(script))

def label(p):        # scratch SKP dir -> normalized copy
    p = os.path.normpath(p)
    if p.endswith('/w1l/probe/skp_GRL925_1200'): return N + '/w1l_GR'
    if p.endswith('/w1g/true208/skp_GO-H208'): return N + '/w1g_true208'
    if p == os.path.normpath('/home/claude/wayfarer-design/reviews/rac-w1i-evidence/skeletal'): return N + '/w1i_base'
    rel = os.path.relpath(p, S)
    assert rel.endswith('/skp'), p
    return N + '/' + rel[:-4].replace('/', '_')

src = open(script).read()
if mode == 'norm':
    src = src.replace("R + '/reviews/rac-w1i-evidence/skeletal'", repr(N + '/w1i_base'))
    src = src.replace("S + '/w1l/probe/skp_GRL925_1200'", repr(N + '/w1l_GR')).replace("S + '/w1g/true208/skp_GO-H208'", repr(N + '/w1g_true208'))
    src = re.sub(r"S \+ '/(w1[a-z]/[^']+?)/skp'", lambda m: repr(N + '/' + m.group(1).replace('/', '_')), src)
    src = re.sub(r"A2 \+ '/g/([^']+?)/skp'", lambda m: repr(N + '/w2a_g_' + m.group(1)), src)
    if blk: src = re.sub(r"W \+ '/g/([^']+?)/skp'", lambda m: repr(N + '/%s_g_' % blk + m.group(1)), src)
    args = [a.split('=', 1)[0] + '=' + (label(a.split('=', 1)[1]) if a.split('=', 1)[1] != 'BASE' else 'BASE') if '=' in a and '/skp' in a else
            (label(a) if a.rstrip('/').endswith('/skp') or a.rstrip('/').endswith('rac-w1i-evidence/skeletal') else a) for a in args]
    for e in ('MFSKP',):
        if os.environ.get(e): os.environ[e] = label(os.environ[e])
    for e in ('W2B1_M229', 'W2B1_F229'):
        if os.environ.get(e):
            p, g, k = os.environ[e].split('|'); os.environ[e] = '|'.join((p, label(g), k))
src = src.replace("R + '/reviews/", repr(RO + '/reviews/') + " + '")
# mirror inputs read through the mirror (e.g. frames_X.json) stay consistent within one mode
sys.argv = [script] + args
code = compile(src, script, 'exec')
g = {"__name__": "__main__", "__file__": script}
sys.path.insert(0, os.path.dirname(os.path.abspath(script))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
exec(code, g)
