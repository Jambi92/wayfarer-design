import sys,re,glob
pat=re.compile(sys.argv[1], re.I if len(sys.argv)>3 and sys.argv[3]=='i' else 0)
ctx=int(sys.argv[4]) if len(sys.argv)>4 else 70
files=[]
for g in sys.argv[2].split(','):
    files+=sorted(glob.glob('/home/claude/wayfarer-design/'+g))
for f in files:
    lines=open(f).read().split('\n'); text='\n'.join(lines)
    h1=h2=''
    for i,l in enumerate(lines,1):
        if l.startswith('# '): h1=l[2:60]; h2=''
        elif l.startswith('##'): h2=l.lstrip('#').strip()[:60]
        for m in pat.finditer(l):
            s=max(0,m.start()-ctx); e=min(len(l),m.end()+ctx)
            snip=l[s:e]
            n=text.count(snip)
            print(f"{f.split('wayfarer-design/')[1]}:{i} [{h1} > {h2}] (x{n}) «{snip}»")
