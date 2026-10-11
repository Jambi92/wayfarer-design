# RAC W3C: normalized Skarn vs Marchfolk differences -> evidence tables.md + pairs.json
import os, sys, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3c_face as WF
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
M = json.load(open(S + '/w3c/metrics.json'))
FAM = {'skull': ['HH_H', 'HL_H', 'Eu_HH', 'HL_HH', 'LCB_HH'], 'brow': ['BGP', 'BSO', 'BOR'], 'jaw': ['BGB_HH', 'BGB_Zy', 'MDH', 'RAM', 'CW_Zy', 'NJT'],
       'midface': ['BZY', 'MAL', 'CHK', 'MPI', 'NH', 'NP', 'AB_Zy']}
PAIRS = [('SKM183', 'MFM183', 'lower overlap 183, config 1'), ('SKM190', 'MFM190', 'mid overlap 190, config 1'), ('SKM203', 'MFM203', '203, config 1'),
         ('SK208', 'MFM203', 'Skarn reference 208 vs MF 203 ENDPOINT (not matched height)'), ('SKM190-NLOW', 'MFM190-NLOW', '190 Narrow + low muscle'),
         ('SKM190-B', 'MFM190-B', '190 Broad, reference composition'), ('SKF190', 'MFF190', '190 config 2 (replication)'), ('SKF203', 'MFF203', '203 config 2 (replication)')]
CAND = [('SKM190-C1', 'MFM190'), ('SKM190-C2', 'MFM190'), ('SKM190-C3', 'MFM190'), ('SKF190-C1', 'MFF190')]
OVL = ['SKM190-SKOV_BROW', 'MFM190-MFOV_BROW', 'SKM190-SKOV_JAW', 'MFM190-MFOV_JAW', 'SKM190-SKOV_MID', 'MFM190-MFOV_MID']
pct = lambda a, b, k: 100.0 * (M[a][k] - M[b][k]) / abs(M[b][k])
out = {'pairs': {}, 'candidates': {}}
L = ['# RAC W3C - Skarn vs Marchfolk craniofacial tables', '', 'Metrics: `tools/rac/w1/w3c_drivers/w3c_face.py` (definitions in its header and the gate s2). Differences are % of the Marchfolk value.', '']
keys = sum(FAM.values(), [])
L += ['## 1. Accepted anatomy, matched pairs (SK - MF, %)', '', '| Pair | ' + ' | '.join(keys) + ' |', '|---|' + '---|' * len(keys)]
for a, b, nm in PAIRS:
    r = {k: pct(a, b, k) for k in keys}; out['pairs'][nm] = dict(sk=a, mf=b, pct=r, sk_vals={k: M[a][k] for k in keys}, mf_vals={k: M[b][k] for k in keys})
    L.append('| %s | ' % nm + ' | '.join('%+.1f' % r[k] for k in keys) + ' |')
L += ['', '## 2. Raw values (all bodies)', '', '| Body | class | H | HH cm | ' + ' | '.join(keys) + ' | FPI | MdPI |', '|---|---|---|---|' + '---|' * (len(keys) + 2)]
for b, m in M.items(): L.append('| %s | %s | %.1f | %.2f | ' % (b, m['class'], m['H'], m['HH']) + ' | '.join('%.4f' % m[k] for k in keys) + ' | %.4f | %.4f |' % (m['FPI'], m['MdPI']))
L += ['', '## 3. Builder-chosen candidates vs matched Marchfolk (%)', '', '| Candidate | vs | ' + ' | '.join(keys) + ' |', '|---|---|' + '---|' * len(keys)]
for a, b in CAND:
    r = {k: pct(a, b, k) for k in keys}; out['candidates'][a] = dict(vs=b, pct=r); L.append('| %s | %s | ' % (a, b) + ' | '.join('%+.1f' % r[k] for k in keys) + ' |')
L += ['', '## 4. Overlap cases (key metric per family)', '', '| Case | BGP | BSO | BGB_HH | RAM | MAL | NP | NH |', '|---|---|---|---|---|---|---|---|']
for b in ['MFM190', 'SKM190', 'SKM190-C1'] + OVL: L.append('| %s | ' % b + ' | '.join('%.4f' % M[b][k] for k in ['BGP', 'BSO', 'BGB_HH', 'RAM', 'MAL', 'NP', 'NH']) + ' |')
L += ['', '## 5. RM-CF-05 INPUT ONLY - FPI / MPI / MdPI on W3C faces', '', '| Body | FPI | MPI | MdPI |', '|---|---|---|---|']
for b, m in M.items(): L.append('| %s | %.4f | %.4f | %.4f |' % (b, m['FPI'], m['MPI'], m['MdPI']))
E = '/home/claude/wayfarer-design/reviews/rac-w3c-sk-evidence'; os.makedirs(E, exist_ok=True)
open(E + '/tables.md', 'w').write('\n'.join(L) + '\n'); json.dump(out, open(E + '/pairs.json', 'w'), indent=1)
print('\n'.join(L[:20])); print('\n'.join(L[-60:-30]))
