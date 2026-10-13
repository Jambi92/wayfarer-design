# RM-OT-05R: render several meshes with IDENTICAL camera / material via q_render.py and stack them as rows.
# Usage: python3 r_compare.py --out OUT.png --rows "TITLE|mesh.obj|labels.npy-or-none" ... -- <q_render camera args (--box --center --scale --views --res --wire)>
import argparse, os, subprocess, sys, tempfile
from PIL import Image
argv = sys.argv[1:]; cut = argv.index('--'); ap = argparse.ArgumentParser(); ap.add_argument('--out'); ap.add_argument('--rows', nargs='+'); a = ap.parse_args(argv[:cut]); cam = argv[cut + 1:]
here = os.path.dirname(os.path.abspath(__file__)); qr = os.path.join(here, '..', 'rmot05q_drivers', 'q_render.py'); tmp = tempfile.mkdtemp(); ims = []
for i, row in enumerate(a.rows):
    title, mesh, labels = row.split('|'); o = os.path.join(tmp, 'r%d.png' % i)
    cmd = [sys.executable, qr, '--mesh', mesh, '--out', o, '--title', title] + cam + (['--labels', labels] if labels != 'none' else [])
    subprocess.run(cmd, check=True, capture_output=True); ims.append(Image.open(o))
W = max(im.width for im in ims); H = sum(im.height for im in ims); C = Image.new('RGB', (W, H), (34, 35, 42)); y = 0
for im in ims: C.paste(im, (0, y)); y += im.height
C.save(a.out); print(a.out, C.size)
