# W2I: rebuild the Saurin creator-biology working copies (deleted /tmp/claude-0/rodin/*) in the scratchpad from the repo sources + the PC-staged frozen mesh
import os, shutil, numpy as np, igl, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; W = S + '/w2i/rodin'; R = '/home/claude/wayfarer-design/tools/rodin'
for d in ('v1', 'v5', 'c12', 'g8', 'rb'): os.makedirs(W + '/' + d, exist_ok=True)
def cp(src, dst):
    t = open(src).read().replace('/tmp/claude-0/rodin', W).replace('/tmp/claude-0/rb', W + '/rb'); open(dst, 'w').write(t)
for f in glob.glob(R + '/creator-biology/*.py'): cp(f, W + '/v1/' + os.path.basename(f))
shutil.copy(R + '/creator-biology/ref_metrics.json', W + '/v1/ref_metrics.json')
for f in glob.glob(R + '/female/closure/*.py'): cp(f, W + '/v5/' + os.path.basename(f))
cp(R + '/gate1/wf_saurin_head63.py', W + '/rb/wf_saurin_head63.py')
A = '/mnt/attach/outputs/racebodies_v35/'
b = np.load(A + 'saurin_final_base.npz'); np.savez(W + '/c12/g15_body.npz', V=b['v'], F=b['f'])
V, F = igl.upsample(b['v'].astype(np.float64), b['f'].astype(np.int64)); V = V + np.load(A + 'saurin_final_surface_delta.npz')['d'].astype(np.float64)
np.savez(W + '/c12/g15_surf.npz', V=V.astype(np.float32), F=F.astype(np.int32))
print('ok', b['v'].shape, V.shape)
