# sw_maps.py WORKDIR : Track S2 weight / field maps (order 28dd8d3 §20) on the rest v003 mesh, front / back / lateral per side:
#   row 1: max |W_SW1 - W0| over the girdle columns (grey 0 -> blue >= 0.4)   row 2: SW1 upper-arm weight (0 -> 1)   row 3: LBS-DQS blend mask b (SW3, 0 -> 0.5)
import sys, os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
W = sys.argv[1]; T = os.path.dirname(os.path.abspath(__file__)); BP = '/home/claude/stc/bin/python3'
fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13); fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
Z = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V0 = Z['V'].astype(float); Q = np.asarray(Z['Q'])
z0 = np.load('/tmp/claude-0/rt/rd/rig/weights_v001c.npz'); z1 = np.load(W + '/sw1/weights_S2.npz'); nm = [str(x) for x in z0['names']]
b = np.load(W + '/sw3/blend_mask.npy'); LM = json.load(open('/tmp/claude-0/rt/rd/out/GR_U_REF_RP2_rigprep_landmarks_v002.json'))['joints']
OV = W + '/ov'; SH = W + '/sheets'; os.makedirs(OV, exist_ok=True); os.makedirs(SH, exist_ok=True)
def col(v, vmax, c1):
    t = np.clip(v / vmax, 0, 1)[Q].mean(1)[:, None]; return (1 - t) * np.array([0.85, 0.83, 0.8]) + t * np.array(c1)
cell = 240; S = Image.new('RGB', (6 * cell + 20, 50 + 3 * (cell + 22)), (255, 255, 255)); dr = ImageDraw.Draw(S)
dr.text((10, 8), 'Track S2 maps on rest v003 — row 1: max |W_SW1 - W0| (girdle columns, blue >= 0.4); row 2: SW1 upper-arm weight; row 3: SW3 LBS-DQS blend mask b (red = 0.5)', fill=(0, 0, 0), font=fb)
for si, s in enumerate('lr'):
    g = [nm.index(k) for k in ('clavicle_' + s, 'scapula_' + s, 'upperarm_' + s)]; dW = np.abs(z1['W'][:, g] - z0['W'][:, g]).max(1); ua = z1['W'][:, nm.index('upperarm_' + s)] / np.maximum(z1['W'].sum(1), 1e-9)
    gh = np.array(LM['glenohumeral_' + s]['position_source_frame_cm']); c = gh + np.array([0, 0, -6]); sg = 1 if s == 'l' else -1
    vs = 'f:0,1,0.1:%.3f,%.3f,%.3f:24;b:0,-1,0.1:%.3f,%.3f,%.3f:24;x:%d,0.2,0.1:%.3f,%.3f,%.3f:24' % (*c, *c, sg, *c)
    for ri, (tag, cc) in enumerate((('dw', col(dW, 0.4, (0.1, 0.35, 0.9))), ('ua', col(ua, 1.0, (0.9, 0.5, 0.1))), ('bm', col(b, 0.5, (0.85, 0.1, 0.1))))):
        o = '%s/swm_%s_%s.npz' % (OV, tag, s); np.savez(o, V=V0, Q=Q); np.save(o[:-4] + '_c.npy', cc.astype(np.float32))
        subprocess.run([BP, T + '/render_attr.py', '--', o, o[:-4] + '_c.npy', OV, 'swm_%s_%s' % (tag, s), vs, '0', '420'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        for j, v in enumerate(('f', 'b', 'x')): S.paste(Image.open('%s/swm_%s_%s_%s.png' % (OV, tag, s, v)).convert('RGB').resize((cell, cell)), (10 + (3 * si + j) * cell, 40 + ri * (cell + 22)))
    dr.text((10 + 3 * si * cell, 40 + 3 * (cell + 22) - 18), '%s side: changed rows %d, max |dW| %.2f' % (s, int((dW > 1e-6).sum()), dW.max()), fill=(0, 0, 0), font=fn)
S.save(SH + '/SW_maps.jpg', quality=85); print('maps')
