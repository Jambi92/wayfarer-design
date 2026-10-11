# RAC RM-OT-05B §9 blind readability: same protocol as RM-OT-05A (a_blind.py) on the 05B set (code prefix Q, new seed).
import os, sys, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/rmot05a_drivers')
import a_blind as AB
S = AB.S; AB.OUT = S + '/rmot05b/blind'; os.makedirs(AB.OUT, exist_ok=True); AB.PK.R = S + '/rmot05b/rend_blind'; os.makedirs(AB.PK.R, exist_ok=True)
AB.SETS['B05'] = dict(AB.HUM, **{'GR-ref': 'w2c/b/GR5B218/GR5B218', 'GR-nar': 'w2c/b/GR5BN/GR5BN', 'GR-brd': 'w2c/b/GR5BB/GR5BB', 'GR-low': 'w2c/b/B_GR-BODY-06/B_GR-BODY-06',
                                  'GO-ref': 'w2d/b/GO5BREF/GO5BREF', 'GO-nar': 'w2d/b/GO5BN/GO5BN', 'GO-brd': 'w2d/b/GO5BB/GO5BB', 'GO-low': 'w2d/b/B_GOR-BODY-06/B_GOR-BODY-06'})
AB.SEED['B05'] = 20261013
if __name__ == '__main__':
    for m in ('grey', 'sil'): AB.sheet('B05', m)
