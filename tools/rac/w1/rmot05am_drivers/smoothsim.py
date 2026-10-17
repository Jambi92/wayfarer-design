# Diagnostic replica of Blender Mesh Filter "Smooth": every modal mouse-move event re-applies
# co = orig + fade*(avg_current_neighbours - orig), fade = clamp(f_event*(1-mask), -1, 1); events act as Jacobi iterations.
import numpy as np
def run(V, Avg, mask, fades):
    orig = V.copy(); co = V.copy()
    for f in fades:
        fade = np.clip(f * (1 - mask), -1, 1)[:, None]; co = orig + (Avg @ co - orig) * fade
    return co
