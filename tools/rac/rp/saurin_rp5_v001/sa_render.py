# sa_render.py : RP5 Saurin board helper -- reuses the RP4 board machinery (pipkin_rp4_v001/pk_sheets.py: job / img / sheet, workbench clay renders via
# halvren_rp3_v001/hv_ear_quick render_attr.py). Import, then call R.job(tag, V, F, col, views, wire=...), R.run(), R.sheet(...). Views: (name, dir, centre, ortho height).
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
_W = os.environ.get('SA_W', '/tmp/claude-0/rt/sa'); _OUT = os.environ.get('SA_OUT', _W + '/sheets')
sys.argv = [sys.argv[0], _W, _OUT]; os.environ['BOARDS'] = ''
_src = open('/home/claude/wayfarer-design/tools/rac/rp/pipkin_rp4_v001/pk_sheets.py').read()
exec(_src.split('# ---------- A / C')[0]); exec('def sheet' + _src.split('def sheet', 1)[1].split("if 'A' in SEL")[0])
TMP = _W + '/render_r'; os.makedirs(TMP, exist_ok=True); globals()['TMP'] = TMP
def run(par=2):
    with ThreadPoolExecutor(par) as ex: list(ex.map(lambda j: subprocess.run(j, env=ENV, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
    del jobs[:]
