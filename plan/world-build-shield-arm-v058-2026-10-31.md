# Wayfarer shield-arm continuity correction

October 31, 2026. Player review found that the broader sword attacks were closer to the desired motion, but the shield arm moved awkwardly. The preceding attack poses held the shield hand at a fixed position relative to the character root while the chest turned underneath it, with a separate forearm-facing solve. This kept the sword clear but produced an unconvincing arm motion.

The four isolated attack copies now carry the shield arm with the chest from the established ready pose. The elbow and forearm retain that local relationship instead of swiveling around a stationary hand target. The wider sword paths remain unchanged in animation measurements. Ready, guard and block-catch asset files, native combat code, input timing and gameplay damage reach remain unchanged.

Checks cover both arm lengths and conservative shield clearance through 3,527 keyed/interpolated poses, live attack blends and native front/rear-quarter review. The attack-chain, moving-attack and guard-transition scenarios are retested, along with an equipped-pawn smoke check of the copied route. Earlier general control and world-clearance results are retained rather than represented as newly rerun. The revision has a compressed E-drive backup with verified archive readback and a preservation check against the preceding full checkpoint.

The next choreography target is coordinated footwork, hip-led rotation, momentum between cuts and recovery into defense. These are future animation goals. This correction remains a stock-mannequin prototype; it does not establish a finished naturalistic fighting style, final character retargeting, named abilities or physical blade traces. Public updates remain prose only.
