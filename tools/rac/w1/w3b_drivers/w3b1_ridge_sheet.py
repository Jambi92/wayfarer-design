# RAC W3B1: surfaced ridge-minimum sheet from the w3b_interact 'ix_S_m*' renders (matched cameras hF / hF34 / hP).
import os, sys; D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_sheet as SS
rows = [('ix_S_m1.0_1.0', 'reference\nm 1.0, relief x1\nminleg 1.18'),
        ('ix_S_m0.9_1.0', 'LOWEST VALID\ncanonical relief\nm 0.90, relief x1\ntemporal 1.00'),
        ('ix_S_m0.85_1.0', 'FIRST FAIL\ncanonical relief\nm 0.85, relief x1\ntemporal 0.91'),
        ('ix_S_m0.6_rmin', 'LOWEST VALID\nminimum relief\nm 0.60, min relief\ntemporal 1.11'),
        ('ix_S_m0.55_rmin', 'FIRST FAIL\nminimum relief\nm 0.55, min relief\ntemporal 0.91'),
        ('ix_S_m1.0_rC1', 'LOWEST VALID\nhigh relief (C-R1)\nm 1.0, capped max relief\ntemporal 1.00'),
        ('ix_S_m0.9_rC1', 'FIRST FAIL\nhigh relief\nm 0.90, capped max relief\ntemporal 0.85'),
        ('ix_S_m1.3_1.0', 'UPPER BOUND\ncanonical relief\nm 1.30, relief x1\ntemporal 1.69'),
        ('ix_S_m1.3_rC1', 'UPPER BOUND\nhigh relief (C-R1)\nm 1.30, capped max relief\ntemporal 1.43'),
        ('ix_S_m0.4_1.0', 'W3B naked min,\nsurfaced\nm 0.40, relief x1\ntemporal 0.13 FAIL')]
print(SS.sheet('w3b1_surfaced_ridge_minimum.jpg', 'W3B1 - surfaced structural-ridge lower bound (hidden strength m)',
    ['Surfaced head, canonical seeds. Legibility = ridge strength / scale relief within 1 cm of the core; >= 1.0 required (temporal line binds).',
     'Matched cameras: front / three-quarter / profile. Diagnostic copies; the canonical W2 asset is unchanged.'],
    rows, "hF:0:4:0:12:182:22;hF34:35:12:0:9:182:24;hP:90:0:0:6:181.5:26", ['front', 'three-quarter', 'profile'], cell=330))
