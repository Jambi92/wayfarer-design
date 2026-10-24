# Grask extracted 3D source handoff

## Files

- `GRASK_front_reference_proxy_v001.glb.gz`
  - Cleanly isolated **left/front-derived figure** from Tyler's uploaded Grask GLB.
  - This is intentionally a **coarse macro-shape transport proxy**, not production topology and not the detailed anatomical authority.
  - Approx. 649 vertices / 1,424 triangles.
  - Generated height: ~1.898 m before canonical rescale.
  - Centered laterally/depth-wise and grounded vertically.
  - gzip SHA-256: `b22eea7ee8d7a1aab05e8723a52c2881e8c019d62948de707fb8104cc03b77f1`
  - decompressed GLB SHA-256: `38856fd771f0540d030492ca11bc126871d898760712c7cb12874fcc2e26c62a`

## Dense extraction provenance

ChatGPT also produced an exact dense standalone extraction of the same left/front-derived figure from Tyler's uploaded GLB:

- local handoff name: `GRASK_front_reference_extracted_v3.glb`
- approx. 196,873 vertices / 314,892 triangles
- size: 6,141,968 bytes
- SHA-256: `03aed1aad8f134720e448feab54301d99dbc6bf8fa61583f671a2906878bceb2`

The GitHub connector could not directly stream that 6.1 MB binary into the repo from local storage, so **do not mistake the coarse proxy for the full-detail source**. Tyler/ChatGPT retain the dense extraction for direct transfer if needed.

## Reconstruction

Decompress the proxy before import:

```python
import gzip, shutil
with gzip.open("GRASK_front_reference_proxy_v001.glb.gz", "rb") as src, \
     open("GRASK_front_reference_proxy_v001.glb", "wb") as dst:
    shutil.copyfileobj(src, dst)
```

or:

```bash
gzip -dk GRASK_front_reference_proxy_v001.glb.gz
```

## Authority

Use the proxy only for **3D macro massing and spatial relationships**.

Detailed shape authority remains:
1. Tyler's approved Grask troll turnaround image;
2. the dense extracted figure when available;
3. Grask biological canon.

Do not use the proxy's low-resolution topology or faceting as anatomical detail.
