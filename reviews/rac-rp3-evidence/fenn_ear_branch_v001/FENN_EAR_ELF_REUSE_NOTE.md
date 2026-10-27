# Fenn ear branch — reuse note for later elf branches (order bdcd6a6 §15; note only, no elf-family freeze)

The Fenn ear branch is **Fenn-only**. Aelari and Vael ear geometry is not authored here, and nothing in this note is a universal elf ear.

These parts of the topology look reusable when Aelari / Vael ear branches are ordered.

## 1. Root interface

- The v005 root loop (52 vertices per side) with the valence-preserving root band: every root vertex keeps v005 valence 4.
- One bounded transition ring for the posterior sulcus lip.
- The DP-matched cuff from ring 1 (52) to the junction ring (70).

These depend only on v005, not on Fenn anatomy. A race with a different attachment length or notch would reuse them, with a new canonical cuff band list.

## 2. Structural loops

- The junction ring composition: attachment line A + attached helix-root and lobe edges + rim ends + notch curve U behind the concha.
- The block layout:
  - bridge (attached concha floor / tragus);
  - crescent F1 (antihelix / scapha band behind the concha);
  - upper-extension block F2;
  - a K_r-row rim strip round the free outline.

## 3. Helix / antihelix topology

- The rim strip (helix roll) runs continuously from the lobe front round the posterior rim and the tip to the helix root.
- Crescent rows run parallel to the posterior rim: antihelix stem, superior and inferior crura.
- The anatomy is carried by the fixed (s, t) ear parameters, so other outlines and relief laws can drive the same vertices.

## 4. Tip-support architecture

- The tip is a single corner of the upper-extension block, with the rim strip wrapping it. This keeps a clean, non-fanned point.
- The current kite-shaped upper block gives rhombic cells near acute tips, which is the main T-4 cost; gate §8 lists it as a refinement item.
- Races with longer tapers (Aelari) would load this block harder. Races with broader bases (Vael) would load it less.

## 5. Not reusable as-is

- The Fenn outline and relief parameters (W1e FN-elven), the projection / tilt / sweep values, and the attachment angle.
- These are race identity and must be authored per race (Elf Comparative Review).
