# sa_immutables.py RECORD OUT : re-hash every immutable listed in RECORD (repo paths in the clone; PC: canonical files from the staged copies of
# E:/UnrealProjects/Wayfarer 5.8/RaceBodies/out in /tmp/claude-0/rt/sa/src) and compare with the recorded sha256.
import sys, hashlib, os
REC, OUT = sys.argv[1:3]; ROOT = '/home/claude/wayfarer-design'; SRC = '/tmp/claude-0/rt/sa/src'; out = []; bad = 0
for line in open(REC):
    p = line.split()
    if len(p) < 2: continue
    h, path = p[0], p[1]; f = os.path.join(SRC, os.path.basename(path)) if path.startswith('PC:') else os.path.join(ROOT, path)
    if not os.path.exists(f): out.append('%s  %s  MISSING' % (h, path)); bad += 1; continue
    h2 = hashlib.sha256(open(f, 'rb').read()).hexdigest(); ok = h2 == h; bad += (not ok); out.append('%s  %s  %s' % (h2, path, 'UNCHANGED' if ok else 'CHANGED (record %s)' % h))
open(OUT, 'w').write('\n'.join(out) + '\n'); print(len(out) - bad, '/', len(out), 'unchanged')
