# hv_ear_quick.py OUT.png TAG:NPZ[:HEAD] ... : quick neutral-clay review strip (close 3/4 front, close profile, 3/4 rear, root / concha closeup) of ear
# realizations on one common head; camera = the left root frame of the common head (identical for every item). Builder review aid (not a gate sheet).
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D
BP = '/home/claude/stc/bin/python3'; REND = '/home/claude/wayfarer-design/tools/rac/rp/grask_rigprep_v001/render_attr.py'
TMP = os.environ.get('HV_QTMP', '/tmp/claude-0/rt/hv/ear/qr'); os.makedirs(TMP, exist_ok=True); GREY = np.array([0.80, 0.78, 0.76])
VIEWS = os.environ.get('HV_QVIEWS', 'etq,elat,etqr,root').split(',')
def cams(head):
    rd = D.frame(head, 'l'); O, n, b, u = rd['O'], rd['n'], rd['b'], rd['u']; Ce = O + 1.2 * b + 0.6 * u
    nb = lambda w: tuple(np.round(np.asarray(w, float), 4))
    return dict(etq=(nb(n + 0.45 * np.array([0, 1, 0]) + 0.25 * np.array([0, 0, 1])), Ce, 5.0), elat=(nb(n + 0.15 * np.array([0, 1, 0]) + 0.05 * np.array([0, 0, 1])), Ce, 5.4),
                etqr=(nb(0.6 * n - b + 0.15 * np.array([0, 0, 1])), Ce, 5.0), root=(nb(n + 0.2 * np.array([0, 1, 0])), O + 0.3 * b, 3.2),
                # NOTE: 'etqr' (used in the HVE / HE2C boards as '3/4 rear') looks BACKWARD at the ear from anterior-lateral (b is posterior, the camera sits on -b);
                # true posterior views (camera on +b): rq rear 3/4, rq2 stronger rear 3/4, rr direct rear, lr lower-rear 3/4 at the inferior root; aq = the etqr view
                aq=(nb(0.6 * n - b + 0.15 * np.array([0, 0, 1])), Ce, 5.0), aql=(nb(0.6 * n - b - 0.6 * np.array([0, 0, 1])), O - 1.0 * u + 0.6 * b, 3.6),
                rq=(nb(0.6 * n + b + 0.15 * np.array([0, 0, 1])), Ce, 5.0), rq2=(nb(0.3 * n + b + 0.1 * np.array([0, 0, 1])), Ce, 5.0),
                rr=(nb(b + 0.05 * n), Ce, 5.2), lr=(nb(0.6 * n + b - 0.7 * np.array([0, 0, 1])), O - 1.0 * u + 0.6 * b, 3.6), side=(nb(n), Ce, 5.4),
                front=((0, 1, 0.03), None, 15), prof=((1, 0, 0), None, 15), rear=((0, -1, 0), None, 15), tqf=((1, 1, 0.1), None, 15))
def run(tag, npz, head, views=VIEWS, px=520, col=None, wire=False):
    z = np.load(npz); V = z['V']; C = cams(head); hv = V[V[:, 2] > V[:, 2].max() - 25]; Hc = np.array([0.0, hv[:, 1].mean(), V[:, 2].max() - 12.0])
    vs = ';'.join('%s:%s:%s:%.2f' % (k, ','.join('%.4f' % x for x in C[k][0]), ','.join('%.3f' % x for x in (C[k][1] if C[k][1] is not None else Hc)), C[k][2]) for k in views)
    cf = os.path.join(TMP, tag + '_col.npy'); np.save(cf, np.asarray(col if col is not None else np.tile(GREY, (len(V), 1)), np.float32))
    return [BP, REND, '--', npz, cf, TMP, tag, vs, '1' if wire else '0', str(px)]
def font(sz, bold=False):
    f = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if bold else ''); return ImageFont.truetype(f, sz) if os.path.exists(f) else ImageFont.load_default()
if __name__ == '__main__':
    OUT = sys.argv[1]; items = [a.split(':') for a in sys.argv[2:]]; head0 = os.environ.get('HV_QHEAD', 'HVC1-HB2HF2-HPB')
    jobs = [run(t, p, h[0] if h else head0) for t, p, *h in items]
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: subprocess.run(j, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), jobs))
    cw = 360; Sh = Image.new('RGB', (130 + cw * len(VIEWS), 20 + len(items) * (cw + 6)), 'white'); d = ImageDraw.Draw(Sh)
    for r, (t, p, *h) in enumerate(items):
        d.text((6, 20 + r * (cw + 6) + cw // 2), t, fill=(0, 0, 0), font=font(15, True))
        for k, v in enumerate(VIEWS):
            q = os.path.join(TMP, '%s_%s.png' % (t, v)); im = Image.open(q).convert('RGB') if os.path.exists(q) else Image.new('RGB', (cw, cw), 'pink'); Sh.paste(im.resize((cw, cw)), (130 + k * cw, 20 + r * (cw + 6)))
    Sh.save(OUT)
