#!/bin/bash
# hash_parents.sh OUT.txt : SHA-256 of every immutable Grask RP2 parent (freshly staged PC copies) + blend geometry hashes
D=/mnt/user-data/uploads/RaceBodies/production/Grask/RP2; T=$(cd "$(dirname "$0")" && pwd); O=$1; : > "$O"
for f in GR_U_REF_RP2_retopo_v003.blend GR_U_REF_RP2_retopo_v003.json GR_U_REF_RP2_retopo_v003_landmarks.json \
         GR_U_REF_RP2_retopo_v003_FREEZE.json GR_U_REF_RP2_retopo_v002.blend GR_U_REF_RP2_retopo_v002.json \
         GR_U_REF_RP2_retopo_v002_landmarks.json GR_U_REF_RP2_retopo_v001.blend GR_U_REF_RP2_retopo_v001.json \
         GR_U_REF_RP2_retopo_v001_landmarks.json SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend \
         SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.json SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005_naturalization_masks.npz \
         SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.glb; do
  echo "$(sha256sum "$D/$f" | cut -c1-64)  $f" >> "$O"
done
for f in GR_U_REF_RP2_retopo_v003.blend SOURCE_3D/GR_U_REF_RP2_SOURCE_3D_v005.blend; do
  echo "== $f" >> "$O"
  ${BP:-/home/claude/stc/bin/python3} "$T/geomhash.py" -- "$D/$f" 2>/dev/null | grep -E '^(FILESHA|GEOMHASH|OBJ)' >> "$O"
done
