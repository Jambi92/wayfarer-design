# Gate 8 first-pass phenotype library (DIAGNOSTIC). Colours are sRGB 0-1. Names describe colour/pattern only:
# no phenotype is assigned to sex, culture, class, biome, ancestry or temperament.
FA=0.35
PH={
 'P1_umber_mottled':  dict(primary=(0.36,0.26,0.17),secondary=(0.16,0.11,0.07),ventral=(0.60,0.50,0.37),pattern='mottled',contrast=0.65,cs=0.35,face_accent=FA,keratin=(0.33,0.27,0.20),iris=(0.70,0.48,0.14),iris2=(0.35,0.20,0.06),seed=11,distal=0.15),
 'P2_slate_banded':   dict(primary=(0.37,0.39,0.41),secondary=(0.15,0.16,0.18),ventral=(0.57,0.57,0.55),pattern='banded',contrast=0.70,cs=0.30,face_accent=FA,keratin=(0.25,0.25,0.25),iris=(0.62,0.60,0.36),iris2=(0.30,0.30,0.18),seed=12),
 'P3_ochre_speckled': dict(primary=(0.66,0.51,0.29),secondary=(0.28,0.18,0.09),ventral=(0.79,0.70,0.53),pattern='speckled',speckle=0.13,contrast=0.75,soft=0.1,cs=0.30,face_accent=0.15,keratin=(0.55,0.45,0.32),iris=(0.55,0.35,0.12),iris2=(0.25,0.14,0.05),seed=13),
 'P4_charcoal_uniform':dict(primary=(0.13,0.12,0.115),secondary=(0.075,0.07,0.065),ventral=(0.25,0.23,0.21),pattern='uniform',contrast=0.4,cs=0.30,face_accent=0.0,keratin=(0.14,0.13,0.12),iris=(0.78,0.45,0.16),iris2=(0.40,0.18,0.05),seed=14),
 'P5_olive_axial':    dict(primary=(0.37,0.39,0.23),secondary=(0.63,0.59,0.41),ventral=(0.62,0.60,0.45),pattern='axial',contrast=0.55,soft=0.6,cs=0.30,face_accent=FA,keratin=(0.38,0.34,0.24),iris=(0.66,0.56,0.22),iris2=(0.30,0.26,0.08),seed=15),
 'P6_terracotta_blotched':dict(primary=(0.55,0.31,0.20),secondary=(0.24,0.13,0.09),ventral=(0.71,0.55,0.42),pattern='blotched',contrast=0.70,cs=0.32,face_accent=FA,keratin=(0.40,0.28,0.20),iris=(0.72,0.55,0.25),iris2=(0.38,0.24,0.08),seed=16),
 'P7_bluegray_broken':dict(primary=(0.34,0.40,0.45),secondary=(0.16,0.19,0.24),ventral=(0.62,0.64,0.63),pattern='broken_banded',contrast=0.70,cs=0.32,face_accent=FA,keratin=(0.30,0.31,0.32),iris=(0.48,0.55,0.42),iris2=(0.22,0.26,0.18),seed=17),
 'P8_sand_regional':  dict(primary=(0.72,0.62,0.46),secondary=(0.38,0.30,0.20),ventral=(0.80,0.74,0.62),pattern='regional',contrast=0.60,soft=0.85,cs=0.25,face_accent=0.25,keratin=(0.62,0.55,0.42),iris=(0.52,0.40,0.18),iris2=(0.24,0.17,0.07),seed=18,distal=0.1),
 'P9_green_mixed_asym':dict(primary=(0.30,0.36,0.24),secondary=(0.13,0.16,0.10),ventral=(0.55,0.56,0.42),pattern='mixed',asym=0.55,contrast=0.70,cs=0.32,face_accent=FA,keratin=(0.30,0.30,0.22),iris=(0.70,0.52,0.18),iris2=(0.32,0.22,0.06),seed=19),
 'P10_coolbrown_low': dict(primary=(0.33,0.28,0.25),secondary=(0.24,0.20,0.18),ventral=(0.45,0.40,0.36),pattern='mottled',contrast=0.35,cs=0.20,face_accent=0.15,keratin=(0.28,0.24,0.21),iris=(0.55,0.42,0.30),iris2=(0.26,0.18,0.12),seed=20,sat_jitter=0.02),
}
NEUTRAL=dict(primary=(0.50,0.50,0.50),secondary=(0.50,0.50,0.50),ventral=(0.50,0.50,0.50),pattern='uniform',contrast=0.0,cs=0.0,jitter=0.04,sat_jitter=0.0,face_accent=0,keratin=(0.42,0.40,0.37),iris=(0.55,0.50,0.40),iris2=(0.3,0.28,0.22),seed=1,dorsal_dark=0.0)
