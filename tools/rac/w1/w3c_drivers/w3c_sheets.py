# RAC W3C: neutral-material matched-camera head sheets (rclose Workbench; one grey material, no hair / beard / scars / texture).
import os, sys, json, numpy as np
from PIL import Image, ImageDraw
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w3b_drivers'))
import w3b_common as C, w3b_sheet as SS
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
M = json.load(open(S + '/w3c/metrics.json')); R = S + '/w3c/rend'; SH = S + '/w3c/sheets'; os.makedirs(R, exist_ok=True); os.makedirs(SH, exist_ok=True)
def views(bid, kind):
    m = M[bid]; L = m['landmarks']; d = np.load(m['path'] + '_r6.npz'); e = 0.5 * (d['eye_l'] + d['eye_r'])
    me = L['Me']; vt = L['V']; sto = L['sto']; cu = 0.5 * (vt[2] + me[2]) - 1.5; cf = e[1] - 5.0
    if kind == 'head': return "F:0:0:0:%.2f:%.2f:36;P:90:0:0:%.2f:%.2f:36;Q:35:6:0:%.2f:%.2f:36" % ((cf, cu) * 3)
    if kind == 'close': return ("brow:90:0:0:%.2f:%.2f:13;jaw:40:-12:0:%.2f:%.2f:20;mid:0:0:0:%.2f:%.2f:16;top:0:89:0:%.2f:%.2f:30"
                                % (e[1] - 1, e[2] + 0.5, e[1] - 6, sto[2] - 2, e[1], e[2] - 3.5, e[1] - 9, vt[2]))
def ensure(bid, kind):
    tag = '%s_%s' % (bid, kind); v = views(bid, kind); names = [x.split(':')[0] for x in v.split(';')]
    if all(os.path.exists('%s/%s_%s.png' % (R, tag, n)) for n in names): return
    d = np.load(M[bid]['path'] + '_r6.npz'); V = d['V'].astype(float); F = d['F']; keep = d['keep'].astype(bool)
    me = M[bid]['landmarks']['Me']; box = lambda P: keep & (P[:, 2] > me[2] - 7)
    C.save_head_npz(R + '/%s.npz' % tag, V, F, box); C.render(R + '/%s.npz' % tag, R + '/' + tag, v, 700); os.remove(R + '/%s.npz' % tag)
def grid(out, title, sub, rows, kind, cols, labels, cell=330):
    lw = 250; top = 70 + 22 * len(sub) + 30; img = Image.new('RGB', (lw + cell * len(cols), top + cell * len(rows) + 10), 'white'); dr = ImageDraw.Draw(img)
    dr.text((14, 12), title, font=SS.font(24), fill='black')
    for i, s in enumerate(sub): dr.text((14, 50 + 22 * i), s, font=SS.font(15), fill=(70, 70, 70))
    for j, l in enumerate(labels): dr.text((lw + j * cell + 6, top - 24), l, font=SS.font(15), fill=(70, 70, 70))
    for i, (bid, lab) in enumerate(rows):
        ensure(bid, kind); dr.multiline_text((10, top + i * cell + cell // 2 - 30), lab, font=SS.font(15), fill='black', spacing=4)
        for j, n in enumerate(cols):
            p = '%s/%s_%s_%s.png' % (R, bid, kind, n)
            if os.path.exists(p):
                im = Image.open(p).convert('RGBA').resize((cell, cell), Image.LANCZOS); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); img.paste(bg, (lw + j * cell, top + i * cell))
    img.save(SH + '/' + out, quality=88); print(SH + '/' + out, flush=True)
def lab(b, t): m = M[b]; return '%s\n%s\nH %.0f cm, HH %.1f cm' % (b, t, m['H'], m['HH'])
if __name__ == '__main__':
    sub0 = ['Neutral expression, one grey material, no hair / beard / scars / texture.', 'Matched camera: same ortho scale (36 cm) for every head, centred on each head.',
            'All rows are accepted anatomy (matched builds use accepted routes / frames).']
    grid('w3c_1_matched_stature.jpg', 'W3C - matched-stature Skarn vs Marchfolk (accepted anatomy, configuration 1)', sub0,
         [('SKM183', lab('SKM183', 'Skarn lower adult')), ('MFM183', lab('MFM183', 'Marchfolk matched')), ('SKM190', lab('SKM190', 'Skarn mid overlap')), ('MFM190', lab('MFM190', 'Marchfolk matched')),
          ('SKM203', lab('SKM203', 'Skarn at MF max')), ('MFM203', lab('MFM203', 'Marchfolk max')), ('SK208', lab('SK208', 'Skarn reference')),
          ('SKM190-NLOW', lab('SKM190-NLOW', 'Narrow, low muscle')), ('MFM190-NLOW', lab('MFM190-NLOW', 'Narrow, low muscle')), ('SKM190-B', lab('SKM190-B', 'Broad, ref. comp.')), ('MFM190-B', lab('MFM190-B', 'Broad, ref. comp.'))],
         'head', ['F', 'Q', 'P'], ['front', 'three-quarter', 'profile'], cell=280)
    grid('w3c_2_tendency_closeups.jpg', 'W3C - tendency-family close-ups at 190 cm (brow / jaw / midface / skull)', ['Close cameras matched per column (absolute scale). MF and SK rows: accepted anatomy; C1 / C2: builder-chosen tendency candidates.'],
         [('MFM190', lab('MFM190', 'Marchfolk (accepted)')), ('SKM190', lab('SKM190', 'Skarn (accepted)')), ('SKM190-C1', lab('SKM190-C1', 'restrained candidate')), ('SKM190-C2', lab('SKM190-C2', 'stronger candidate'))],
         'close', ['brow', 'jaw', 'mid', 'top'], ['brow / orbit (profile)', 'jaw / chin / ramus (3/4 low)', 'midface / cheek / nose', 'skull breadth / depth (top)'])
    grid('w3c_3_overlap.jpg', 'W3C - individual overlap / anti-stereotype (190 cm, builder-chosen diagnostics)', ['Each Skarn row stays inside the Skarn package except the named region; each Marchfolk row is the accepted MF face plus one region.'],
         [('SKM190-SKOV_BROW', lab('SKM190-SKOV_BROW', 'light-brow Skarn')), ('MFM190-MFOV_BROW', lab('MFM190-MFOV_BROW', 'strong-brow Marchfolk')),
          ('SKM190-SKOV_JAW', lab('SKM190-SKOV_JAW', 'lighter-jaw Skarn')), ('MFM190-MFOV_JAW', lab('MFM190-MFOV_JAW', 'robust-jaw Marchfolk')),
          ('SKM190-SKOV_MID', lab('SKM190-SKOV_MID', 'lighter-midface Skarn')), ('MFM190-MFOV_MID', lab('MFM190-MFOV_MID', 'substantial-midface MF'))],
         'head', ['F', 'Q', 'P'], ['front', 'three-quarter', 'profile'], cell=290)
    grid('w3c_4_complete_face.jpg', 'W3C - complete-face candidates (Skarn 190 cm; config-2 replication)', ['Tendency package k x (head breadth / depth, brow, jaw breadth / gonial drop, cheekbones, nose, neck). Builder-chosen diagnostics.'],
         [('SKM190', lab('SKM190', 'reference (accepted)')), ('SKM190-C1', lab('SKM190-C1', 'restrained k 1.0')), ('SKM190-C2', lab('SKM190-C2', 'stronger k 2.0')),
          ('SKM190-C3', lab('SKM190-C3', 'k 3.3 (first caricatured)')), ('SKF190', lab('SKF190', 'config 2 reference')), ('SKF190-C1', lab('SKF190-C1', 'config 2, k 1.0'))],
         'head', ['F', 'Q', 'P'], ['front', 'three-quarter', 'profile'], cell=290)
