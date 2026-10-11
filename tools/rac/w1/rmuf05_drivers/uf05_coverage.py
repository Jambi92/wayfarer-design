# RAC RM-UF-05: evidence coverage by population (structural facial DIR in slots 2-9; counts from the UFCA / race-spec inventory).
import json
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad/rmuf05'
C = {  # pop: (DIR count, NUM, ANCH-scaled, QUAL/CEN/ND remainder note, numeric-batch status, Tier-G tests)
 'Marchfolk': (22, 0, 9, 'QUAL regions; projection ANCH (MF-FACE-PROJ-MAX); granular control list not enumerated', 'ANCHOR-SCALE BATCH (shared human anchor scale) - CONSTRAINED', 'identity stress MF L253; randomization sample MF L261'),
 'Skarn': (44, 0, 9, 'QUAL; C1R / C2 / six overlap anchors; mandibular-body and anterior maxillary depth ND', 'ANCHOR-SCALE BATCH (C1R centre) - CONSTRAINED', 'anti-stereotype SK L294-296; relationship-aware randomization SK L282-284; SK-12; W3C overlap validators (no UFCA-06 Tier-G row)'),
 'Sagekin': (53, 0, 0, 'QUAL ("detailed ranges come later", SG L105)', 'NOT FULLY CALIBRATABLE (profile-only diagnostic)', 'clone / stereotype SG L370-383; SG-14; population-sample tests'),
 'Fenn': (46, 0, 0, 'QUAL; ORB delta and ear centres CEN; envelopes OPEN', 'NOT FULLY CALIBRATABLE', 'FN-34; population-randomization test FN L553'),
 'Aelari': (45, 0, 0, 'QUAL; ear centres CEN', 'NOT FULLY CALIBRATABLE', 'generic-elf convergence AE L479-481; AE-48/49/50'),
 'Vael': (41, 0, 0, 'QUAL; VL-35/36 ND', 'NOT FULLY CALIBRATABLE', 'cliche convergence VA L505-507; VL-55/56/57'),
 'Halvren': (50, 0, 0, 'QUAL inside ancestry envelope B; no face anchor (ND)', 'NOT FULLY CALIBRATABLE (synthetic-source diagnostic only)', 'anti-generic-half-elf HV L223; anti-beauty L222; anti-50/50 L60 / L361 / L381; HV-FAMILY-01/02; source passing L145 / L383 / L504'),
 'Durrim': (50, 0, 0, 'QUAL ("no numerical thresholds yet", DU L331); DU-FACE / DU-DEPTH ND', 'NOT FULLY CALIBRATABLE', 'population sampling DU L233; Part 5 L521'),
 'Grask': (37, 0, 0, 'QUAL; maxillary / mandibular projection CEN; GR-FACE-14 ND', 'NOT FULLY CALIBRATABLE', 'anti-caricature GR L739; biological diversity GR L740'),
 'Gorrund': (41, 0, 0, 'QUAL; projection CEN; GOR-FACE-05 ND', 'NOT FULLY CALIBRATABLE', 'minimum-stereotype GO L713; biological diversity GO L716'),
 'Pipkin': (49, 0, 0, 'QUAL; aperture / orbit CLAMP relational', 'NOT FULLY CALIBRATABLE', 'PIP-INT-15 (L1622); PIP-INT-14'),
 'Cogling': (39, 0, 0, 'QUAL; head height VAL only', 'NOT FULLY CALIBRATABLE', 'COG-SURF-14; COG-CC-04 / 06 (13 / 14 relevant); surface cannot rescue structure (L1612)'),
 'Saurin': (30, 11, 0, 'NUM 11 axes (head scale, cranial L/W/D, ridge m, orbit, IOD*, rostrum L / base W / anterior W / depth, posterior jaw depth); ~19 QUAL; *IOD binding conflict (UFCA s4 Bound-locked vs SA s267.2)', 'NUMERIC BATCH (10 axes, IOD excluded) - SUPPORTED', 'SAU-CC-01/03/05/17/18/24/25/26; s74 preset diversity; s264 driver -> dependent -> reject')}
out = {k: dict(dir_total=v[0], numeric_axes=v[1], anchor_scaled_axes=v[2], scaled_fraction=round((v[1] + v[2]) / v[0], 3), remainder=v[3], batch_status=v[4], tier_g=v[5], frequency='OPEN') for k, v in C.items()}
json.dump(out, open(S + '/coverage.json', 'w'), indent=1)
for k, v in out.items(): print(k.ljust(10), v['dir_total'], v['numeric_axes'], v['anchor_scaled_axes'], v['scaled_fraction'], v['batch_status'])
