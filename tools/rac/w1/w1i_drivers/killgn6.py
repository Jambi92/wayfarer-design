# kill running gn6 / sens6 solver processes without matching this script or its shell
import os, sys, signal
me = {os.getpid(), os.getppid()}
pat = sys.argv[1] if len(sys.argv) > 1 else 'gn6.py'
for p in os.listdir('/proc'):
    if not p.isdigit() or int(p) in me: continue
    try: cmd = open('/proc/%s/cmdline' % p, 'rb').read().replace(b'\0', b' ').decode()
    except Exception: continue
    if cmd.startswith('python3') and pat in cmd and 'killgn6' not in cmd: os.kill(int(p), signal.SIGTERM); print('killed', p, cmd[:80])
