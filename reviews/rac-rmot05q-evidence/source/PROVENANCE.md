# RM-OT-05Q source provenance and extraction

## Source GLB: three copies, one hash

All three copies have sha256 `78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b`.

| Location | Size |
|---|---|
| Session upload `base.glb` | 43,012,652 bytes |
| Container copy `/mnt/user-data/outputs/gorrund_source/Gorrund-Male_Rodin_base.glb` | 43,012,652 bytes |
| Author's machine: `E:\UnrealProjects\Wayfarer 5.8\RaceBodies\source\Gorrund-Male\Gorrund-Male_Rodin_base.glb.zip` | zip is 22,764,144 bytes, zip sha256 `b3fbfb2a381e5300239227c4ceb533d40aa53e057ccfacf8eb0740bdb4bb482e`; the GLB inside has the hash above |

The GLB contains one mesh: 969,107 vertices and 1,000,000 faces. Welding vertices at 1e-5 gives 11 islands.

## F1 extraction

F1 is the 05N `c0s_1` detailed surface, the same surface used for GO-RD0-SOURCE. It is taken **before** any 05N SDF, blur or field step.

1. Island 0 (290,800 faces) holds both figures, F1 and F2, which touch at a contact slab.
2. 05N `split.py` removed the slab and re-assigned its faces to the nearest figure. **The slab bounds were not recorded in 05N.**
3. 05Q therefore recovered F1's exact GLB face indices by matching face centroids against `c0s_1`: maximum distance 7.2e-5 GLB units, 140,960 unique faces, all from island 0. They are committed as `F1_face_indices.npz`, index sha256 `f1b46e6b499816d08d7943e6bf58971533d185a6b24096e1138df5780b3d9f72`. This list, not the slab rule, is now the authoritative definition of F1.
4. `q_extract.py` rebuilds F1 from base.glb and this list:
   - `F1_glb_units.obj`: untouched GLB coordinates;
   - `F1_rac_frame.obj`: RAC frame;
   - `F1_working.obj`: welded working copy.

   It also writes `extraction_record.json`, which holds the transform and its constants.
5. **Transform:**
   - `W = (x, −z, y)·100`
   - `X = −(Wx − XC)·S`
   - `Y = −Wy·S − yshift`
   - `Z = (Wz − floor)·S`

   with XC = −76.1, floor = 34.884, S = 229/(119.5 − floor) = 2.70634 and yshift = −7.6422. This is a rotation of 180° about Z plus a scale; **it is not a mirror**. The 05N `field.py` step mirrored later. Mirroring is not part of the extraction, and nothing in 05Q is mirrored.
6. The F1 RAC-frame copy matches the committed GO-RD0-SOURCE to within 0.00028 cm. This is float rounding of S and yshift.

## Boundaries of F1, all inherited from the source split

- **320 open boundary edges in total.** Most lie on the −X arm and hand, which are open where the slab was cut at the F1/F2 seam. The +X arm is closed and clean.
- **Four tiny floating fragments** (168 + 42 + 8 + 1 faces) near the −X hand at z 93–104. These are slab leftovers. They are kept and not repaired.

## Rules followed

- No stance, lengthening, stature normalization, composition, head/tail or muscle edits.
- The reference frame is the 05N RAC frame. The 229 cm crown is a scale convention, not a measurement.
