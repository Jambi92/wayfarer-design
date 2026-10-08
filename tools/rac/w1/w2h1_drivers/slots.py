# RAC W2H1: W1 slot reference dirs with the D1-corrected Durrim (DU137C skin + W2 grid) in the DU slot; every other slot = the W2H dirs (cand0 / skb0)
import shutil, os
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2h1'
for d in ('cand1', 'skb1'):
    if os.path.exists(W + '/' + d): shutil.rmtree(W + '/' + d)
shutil.copytree(S + '/w2h/cand0', W + '/cand1'); shutil.copy(W + '/st/DU137C-NAT_meas.json', W + '/cand1/DU_meas.json')
shutil.copytree(S + '/w2h/skb0', W + '/skb1', symlinks=True)
for t in ("0.0", "0.5", "1.0"):
    d = W + '/skb1/t%s/DU_meas.json' % t
    if os.path.lexists(d): os.remove(d)
    shutil.copy(W + '/g/DU137C-NAT/skp/t%s/MF-M-R_meas.json' % t, d)
print('slots ready')
