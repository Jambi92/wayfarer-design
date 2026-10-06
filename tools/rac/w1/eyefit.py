"""D-4c eye-placement verification: landmark globe vs the generator orbit/aperture."""
import numpy as np
def eyefit(d, diam):
    V = d["V"].astype(float); k = d["keep"]; out = {}
    for s in ("l", "r"):
        e = d["eye_" + s].astype(float); R = diam / 2
        dist = np.linalg.norm(V[k] - e, axis=1)
        inside = int((dist < R - 0.02).sum())
        near = V[k][dist < R + 1.0]
        # lid margin proxy: skin verts within 0.8 cm laterally of the globe's anterior pole
        apex = e + np.array([0, R, 0]); lat = np.linalg.norm((V[k] - apex)[:, [0, 2]], axis=1)
        lid = V[k][(lat < 1.0) & (np.abs(V[k][:, 1] - apex[1]) < 1.5)]
        out[s] = {"globe_diam_cm": diam, "skin_verts_inside_globe": inside, "min_skin_clearance_cm": float(dist.min() - R),
                  "anterior_pole_f": float(apex[1]), "lid_front_f_max": float(lid[:, 1].max()) if len(lid) else None,
                  "pole_behind_lid_front_cm": float(lid[:, 1].max() - apex[1]) if len(lid) else None}
    return out
