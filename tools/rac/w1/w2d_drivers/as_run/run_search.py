import sys, subprocess
out, argf, log = sys.argv[1:4]
args = [l.strip() for l in open(argf) if l.strip()]
with open(log, 'w') as f:
    subprocess.run(['python3', 'w2d_drivers/go_search.py', out] + args, stdout=f, stderr=subprocess.STDOUT, cwd='/home/claude/wayfarer-design/tools/rac/w1')
    f.write('SEARCH_DONE\n')
