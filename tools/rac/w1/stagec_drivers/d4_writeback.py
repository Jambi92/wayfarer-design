import re
R='/home/claude/wayfarer-design/specs/'
SRC="`reviews/claude-rac-rm-ot-05-world-scale-author-gate.md` §1; reference assets `reviews/reference-assets/manifest.json`; D4 order `reviews/chatgpt-rac-d4-race-spec-stature-writeback-execute-order.md`"
def block(env, ref, extra=""):
    return ("**Accepted stature envelope (RAC D4 writeback, October 18, 2026; "+SRC+"):** "
            "**accepted W2 / RM-OT-05 envelope "+env+"**; reference "+ref+". "
            "The first-pass / provisional / preliminary stature labels in this spec are historical; they now read as this accepted envelope. "
            "Stature is DIR inside the envelope, never uniform scaling; no interval midpoint is an average; **frequency / distribution OPEN**."
            +(" "+extra if extra else "")+" No bound, reference or distribution is changed by this writeback.")
# race: (file, list of (heading_old, heading_new)), anchor-line-prefix after which to insert, block
J=[
 ('marchfolk/MARCHFOLK_V1.md',[('## 3. Height (preliminary)','## 3. Height (preliminary; accepted W2 / RM-OT-05 envelope per D4, §4–5)')],
  'This is the approved first-pass playable envelope.', block('147–203 cm (W2A; both configurations, bounds identical)','173 cm (MF-M-R 173.14 / MF-F-R 172.99)')),
 ('skarn/SKARN_V1.md',[('## 2. Height (provisional)','## 2. Height (accepted W2 / RM-OT-05 envelope; first-pass label: provisional)')],
  'The overlap with tall Marchfolk (up to 203 cm) is intentional', block('183–229 cm (W2B / W2B1 / W2C1; both configurations)','208 cm (SK 208.01; central face C1R)','Configuration 2 at 229 cm = macro 1.0 + native extension.')),
 ('sagekin/SAGEKIN_V1.md',[('## 2. Height (provisional)','## 2. Height (accepted W2 / RM-OT-05 envelope; first-pass label: provisional)')],
  'Height overlaps heavily with Marchfolk and is never the main racial marker.', block('152–208 cm (W2E; both configurations)','178 cm (SG 177.99)','Configuration-2 bounds are SGF152-NAT / SGF208 (author-accepted, RM-OT-05A §2; see the configuration-2 acceptance block).')),
 ('fenn/FENN_V1.md',[('## 2. Height (provisional)','## 2. Height (accepted W2 / RM-OT-05 envelope; first-pass label: provisional)')],
  "There's substantial overlap with Marchfolk and Sagekin", block('157–211 cm (W2F)','181 cm (FNL4 181.16)')),
 ('aelari/AELARI_V1.md',[('## 3. Height (provisional)','## 3. Height (accepted W2 / RM-OT-05 envelope; first-pass label: provisional)')],
  'Height supports Aelari identity but doesn', block('168–221 cm (W2F)','190 cm (AEL1 190.01)','168 cm is realized on the native route (R2).')),
 ('vael/VAEL_V1.md',[('## 3. Height (provisional)','## 3. Height (accepted W2 / RM-OT-05 envelope; first-pass label: provisional)')],
  'Height never defines Vael', block('157–203 cm (W2F)','178 cm (VAL4 178.00)')),
 ('halvren/HALVREN_V1.md',[],
  'This is a **provisional first-pass range**, revised by the consistency resolution', block('central population envelope 152–213 cm (W2G; outer bound > 147 / < 229 cm, H-5)','178 cm (HVC1 177.73, diagnostic anchor)','**Preserved qualifier:** ancestry-conditional outer reach 147.2 cm (Marchfolk-supported, bound-limited), 228.8 cm (Skarn-supported) and 221.0 cm (Aelari-supported, source ceiling) per W3A1 (§10–14 below); tails are minority outcomes (H-6) and their conditional frequency is a named dependency. The W3A1 block below is unchanged; this line only retires the stale \"provisional\" label.')),
 ('durrim/DURRIM_V1.md',[],
  'This is the **provisional first-pass Durrim height range**', block('122–152 cm (W2H / W2H1)','137 cm (DU137C, current W2 Durrim reference realization with the D1 pelvis rebuild)','Durrim-local \"distribution left for later\" stays OPEN.')),
 ('grask/GRASK_V1.md',[],
  'This is a **FIRST-PASS BIOLOGICAL RANGE — SUBJECT TO CROSS-RACE VALIDATION**', block('198–239 cm (W2C)','218 cm; the accepted reference-anatomy direction is **Grask E3** (Stage C ACCEPT, October 18, 2026; reference mesh geometry `a452bf6e…`), with the W2 GR218R (217.99) kept as constraint / provenance','The earlier RM-OT-05 \"neutralized-readability FAIL open\" note is superseded by the Stage C ACCEPT.')),
 ('gorrund/GORRUND_V1.md',[],
  'This is a **FIRST-PASS BIOLOGICAL RANGE — SUBJECT TO CROSS-RACE AND WORLD VALIDATION**, genuinely large', block('208–251 cm (W1i / W1j / W2D)','**229 cm nominal design reference; GOREF 230.9 cm accepted ARM realization** (RM-OT-05 D1, kept distinct)','**Preserved qualifier:** 251 cm is the current accepted world-validation / creator upper end for the present design state, **not a permanent project-wide maximum** (RM-OT-05 D5); no race is inferred above it. The frozen reference sculpt `GO-05AW4_nails_final` stands at native 204.5225 cm (Stage C D2(c)): this is **not** an envelope revision, and uniform scaling is never stature construction. The earlier \"neutralized-readability FAIL open\" note is superseded by RM-OT-05 closure and the Stage C ACCEPT.')),
 ('pipkin/PIPKIN_V1.md',[],
  'This is a **FIRST-PASS BIOLOGICAL RANGE — SUBJECT TO CROSS-RACE AND WORLD VALIDATION**. The Pipkin maximum', block('91–122 cm (W2H)','107 cm (PK-NAT)')),
 ('cogling/COGLING_V1.md',[],
  "- **Maximum:** ~107 cm / 3'6\"", block('76–107 cm (W2H)','91 cm (CGJ7 90.99)','The 76 cm realization is **CG76H-NAT** (adult head 11.04 cm, author-accepted RM-OT-05A §2; head ≥ 11.0 cm fix preserved).')),
 ('saurin/SAURIN_V1.md',[],
  'Saurin are not defined by exceptional height.', block('168–208 cm, tail excluded (W2I D1 regional route; canonical W2 reference W2I6)','188 cm (W2 reference 187.88)','No sex shift and no sex-specific bound (§263). The W2I6 blocks later in this spec are unchanged.')),
]
for f,heads,anchor,blk in J:
    p=R+f; s=open(p).read(); n0=s
    for a,b in heads:
        assert s.count(a)==1,(f,a); s=s.replace(a,b)
    lines=s.split('\n'); idx=[i for i,l in enumerate(lines) if l.startswith(anchor)]
    assert len(idx)==1,(f,anchor,idx)
    i=idx[0]
    lines.insert(i+1,''); lines.insert(i+2,blk)
    open(p,'w').write('\n'.join(lines))
    print('ok',f)
