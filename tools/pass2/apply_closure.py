# Pass 2 author closure: apply the approved conforming-edit rows (with author-decision adjustments),
# then the AD-1..AD-5 / AC-1..AC-10 additions. Every replacement asserts its exact occurrence count.
import json, sys, collections
R='/home/claude/wayfarer-design/'
rows=json.load(open(R+'tools/pass2/conforming_rows.json'))
SKIP={'E7-08':'already applied (PROJECT_RULES Reviews section rewritten in the resolution sequence)',
      'E7-09':'superseded: STATUS is written by the closure audit',
      'E2-11':'referent of "robust humans" not explicitly resolved by the author order (AUTHOR CONFIRM row); left unchanged',
      'E2-12':'same as E2-11'}
ADJ={
 'E2-09':'| Thoracic breadth | Trends high: greater than Grask at matched height and, at equal height, greater axial breadth than Skarn (§80–87 comparative tests; Large-Race Comparative Anatomy Review),',
 'E2-10':'greater lower-limb contribution to standing height than the Marchfolk Human Reference Population and Skarn at matched normalized height (as stated in Part 2 §14–20),',
 'E13-04':'a relatively slender skeletal silhouette for its stature (a skeletal proportion, not low body fat; §6–7),',
 'E6-02':'| Applied | Tattoos, makeup, paint, decorative markings |\n| Acquired | Scars |',
 'E6-06':'| Applied | Tattoos, paint, makeup, decorative markings |\n| Acquired | Scars |',
 'E6-08':'The universal four layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (sun and tanning, weathering, roughness, dryness, calluses, localized wear, dirt), applied (tattoos, body paint, makeup, ceremonial markings) and acquired (scars).',
 'E6-09':'The universal four layers stay: natural (pigmentation, undertone, complexion, freckles, moles, birthmarks), environmental (tanning, sun, weathering, dryness, roughness, calluses, dirt), applied (tattoos, makeup, paint, markings) and acquired (scars).',
 'E7-23':'| Future Large-Race Comparative Anatomy Review | (Performed and accepted in Pass 2: `reviews/claude-pass2-r2-large-race-comparative-review.md`, author decisions AD-1–AD-5, October 5, 2026; see Part 5 comparative tests.) Once Gorrund is designed, compare',
 'E10-16':'pending the universal system (OPEN; the universal rule is now R-SEX in `decisions/PROJECT_RULES.md` — Durrim magnitudes stay OPEN).',
}
files={}; log=[]; applied=0
def get(f):
    if f not in files: files[f]=open(R+f).read()
    return files[f]
def rep(f,cur,new,n=1,tag=''):
    t=get(f); c=t.count(cur)
    assert c==n, (tag,f,c,n,cur[:80])
    files[f]=t.replace(cur,new); log.append((tag,f))
for x in rows:
    if x['id'] in SKIP: continue
    new=ADJ.get(x['id'],x['new'])
    rep(x['f'],x['cur'],new,x.get('n',1),x['id']); applied+=1
# AC-3: dirt -> Environmental in the Marchfolk / Skarn tables
rep('specs/marchfolk/MARCHFOLK_V1.md','| Environmental | Sun exposure, tanning, weathering, dryness, roughness, calluses, minor discoloration |',
    '| Environmental | Sun exposure, tanning, weathering, dryness, roughness, calluses, minor discoloration, dirt |',tag='AC-3a')
rep('specs/skarn/SKARN_V1.md','| Environmental | Sun exposure, wind and weather, dryness, roughness, calluses, localized wear |',
    '| Environmental | Sun exposure, wind and weather, dryness, roughness, calluses, localized wear, dirt |',tag='AC-3b')
# AD-1, AD-3(GOR side), AD-4: Gorrund
G='specs/gorrund/GORRUND_V1.md'
rep(G,'| Feet (Fenn added) | Fenn: gracile, extremity-emphasized elven architecture. Gorrund: large, substantial plantigrade architecture supporting massive scale |',
 '| Feet (Fenn added) | Fenn: gracile, extremity-emphasized elven architecture. Gorrund: large, substantial plantigrade architecture supporting massive scale |\n'
 '| Gorrund / Skarn (208 cm Gorrund minimum vs Broad Skarn at equal and greater valid Skarn height through 229 cm; added by Pass 2 author decision AD-1) | **Cross-Population Boundary Test.** Passes only on proportional and architectural carriers: thoracic depth relative to stature and breadth, Axial Load-Path Continuity, craniofacial identity (Transverse Structural Continuity) and ear architecture. Fails if it relies on absolute size or Current Muscularity |',tag='AD-1')
rep(G,'| Composition-neutral recognition (GOR-BODY-16, neutral pose and presentation) | Fails if it needs muscle bulk or fat volume to read Gorrund |',
 '| Composition-neutral recognition (GOR-BODY-16, neutral pose and presentation) | Fails if it needs muscle bulk or fat volume to read Gorrund |\n'
 '| Lower-breadth / lower-depth Gorrund (GOR-BODY-12, GOR-BODY-14) vs Broad Grask at matched height (Pass 2 author decision AD-3) | The Gorrund stays Gorrund through body architecture: lower relative limb contribution than the Grask distribution, greater axial contribution, joint presence and Axial Load-Path Continuity. Ears, face, surface phenotype, muscle and absolute height never rescue an otherwise collapsed body architecture. Numeric validator deferred to approved reference meshes (RM-LR-04) |',tag='AD-3g')
rep(G,'Gorrund completion provides enough anatomy for a future dedicated **Large-Race Comparative Anatomy Review** (Skarn, Grask, Gorrund), not performed here.',
 'Gorrund completion provided enough anatomy for the dedicated **Large-Race Comparative Anatomy Review** (Skarn, Grask, Gorrund), performed and accepted in Pass 2 (`reviews/claude-pass2-r2-large-race-comparative-review.md`; author decisions AD-1–AD-5, October 5, 2026). **Skarn–Gorrund torso and limb proportional separation is undetermined by design (AD-4):** their distinction is architectural — the human skeletal family versus Gorrund Axial Load-Path Continuity and load-bearing non-human architecture, plus the established craniofacial and auricular differences — and no Gorrund torso-share or limb-share relationship to Skarn is defined.',tag='AD-4')
# AD-2, AD-3 (Grask side)
K='specs/grask/GRASK_V1.md'
rep(K,'GR-BODY-10 (shorter-limbed extreme) keeps enough limb contribution to read Grask',
 'GR-BODY-10 (shorter-limbed extreme) keeps enough limb contribution to read Grask — at matched height it must still trend above the Gorrund limb-present proportion family in relative limb contribution (Pass 2 author decision AD-3: a directional biological boundary; the numeric validator comes from approved reference meshes, RM-LR-04) —',tag='AD-3k')
rep(K,'| Future Large-Race review | After Gorrund is independently designed: Skarn, Grask and Gorrund; no Gorrund anatomy set now |',
 '| Large-Race review | Performed and accepted in Pass 2 (`reviews/claude-pass2-r2-large-race-comparative-review.md`; author decisions AD-1–AD-5, October 5, 2026); Grask–Gorrund relations are defined in the Gorrund spec and that review |\n'
 '| Shortest-limbed Grask (GR-BODY-10) vs Skarn (Pass 2 author decision AD-2) | The Grask stays Grask through non-limb carriers: thoracic and shoulder breadth relative to stature, non-human girdle and pelvic organization, neck relationship, hand and digit relationships, craniofacial verticality and ear architecture |\n'
 '| Shortest-limbed Grask (GR-BODY-10) vs the Gorrund limb-present proportion family at matched height (Pass 2 author decision AD-3) | GR-BODY-10 still trends above the Gorrund limb-present family in relative limb contribution. Ears, face, surface phenotype, muscle and absolute height never rescue an otherwise collapsed body architecture. Numeric validator deferred (RM-LR-04) |',tag='AD-2/3')
rep(K,'> **Do not allow Grask variation to pre-design or presume the anatomy of an unfinished population.**',
 '> **Do not allow Grask variation to pre-design or presume the anatomy of an unfinished population.**\n\n(Gorrund is now first-pass complete; Grask–Gorrund relations are defined in the Gorrund spec and the Pass 2 Large-Race Comparative Anatomy Review. This placeholder note is retained as history.)',tag='AD-3p')
# AD-5 + AC-4 Skarn
S='specs/skarn/SKARN_V1.md'
rep(S,'Even extreme Skarn settings must not recreate Gorrund anatomy.',
 'Even extreme Skarn settings must not recreate Gorrund anatomy.\n\nSkarn–Grask separation is carried by the Grask spec (Part 1 §60–70 and Part 5 comparative tests) and the Pass 2 Large-Race Comparative Anatomy Review (`reviews/claude-pass2-r2-large-race-comparative-review.md`). This pointer adds no Skarn anatomy (Pass 2 AD-5).',tag='AD-5')
rep(S,'Race changes the supported ranges, not how the editor works.',
 'Race changes the supported ranges, not how the editor works.\n\n**Ears (Pass 2 AC-4):** Skarn follow the Marchfolk human-family auricular anatomical foundation (Marchfolk Part 2 §3–4) unless this spec explicitly modifies a tendency. This does not make Skarn head anatomy Marchfolk-equivalent.',tag='AC-4s')
# AC-4, AC-6, AC-7 Sagekin
A='specs/sagekin/SAGEKIN_V1.md'
rep(A,'Pointed ears, exaggerated limbs, very light bones and other elven traits are never used to set Sagekin apart.',
 'Pointed ears, exaggerated limbs, very light bones and other elven traits are never used to set Sagekin apart.\n\n**Ears (Pass 2 AC-4):** Sagekin follow the Marchfolk human-family auricular anatomical foundation (Marchfolk Part 2 §3–4) unless this spec explicitly modifies a tendency. This does not make Sagekin head anatomy Marchfolk-equivalent.',tag='AC-4g')
rep(A,'None of this is exaggerated into elf-like anatomy.\n\n## 4. Skeletal frames',
 'None of this is exaggerated into elf-like anatomy.\n\n> **Clarified by v1.1 §1 (Pass 2 AC-6):** hands and feet remain human anatomy while the population may trend toward longer forearms, hands and fingers; the ribcage tendency is reduced depth, not an undefined global narrowing. The bullets above are kept as history.\n\n## 4. Skeletal frames',tag='AC-6')
rep(A,'## 9. Fenn and Aelari boundary (reserved test)\n\nOnce the elves are defined, the most extreme valid Sagekin are compared against Fenn and Aelari.',
 '## 9. Fenn and Aelari boundary (active test)\n\nActivated by Pass 2 AC-7: Fenn and Aelari are defined and carry their own Sagekin-boundary tests (FN-17, AE-21), so the most extreme valid Sagekin are compared against Fenn and Aelari.',tag='AC-7')
# AC-5 Fenn
rep('specs/fenn/FENN_V1.md','Fenn ears are their own external-ear anatomy, not human ears with stretched tips.',
 'Fenn ears are their own external-ear anatomy, not human ears with stretched tips. **Population tendency (Elf Comparative Review, final clarification §3; Pass 2 AC-5):** Fenn have the greatest average lateral (outward) ear projection of Fenn, Aelari and Vael, with individual overlap and the Fenn ear bounds (§9) preserved.',tag='AC-5')
# AC-8, AC-9 Cogling
C='specs/cogling/COGLING_V1.md'
rep(C,'- **FD-HAIR** — facial/scalp hair as relevant to facial analysis;','- **FD-HAIR** — scalp hair, facial hair and eyebrows as relevant to facial analysis (Pass 2 AC-8);',tag='AC-8')
rep(C,'Frame must not automatically determine height, muscle, fat, face, sex-related anatomy, culture or personality.',
 'Frame must not automatically determine height, muscle, fat, face, sex-related anatomy, culture or personality.\n\n**Clarification (Pass 2 AC-9):** Skeletal Frame may set starting correlated values or distribution tendencies for long-bone robusticity and joint dimensions inside the valid population envelope, but those parameters remain separately adjustable (§53, §69) and are never hard-determined by Narrow, Balanced or Broad. Combined-proportion validity governs the result.',tag='AC-9')
# AC-2 Saurin
rep('specs/saurin/SAURIN_V1.md','must be explicitly marked **non-baseline** and may not enter ordinary player presets, Biological Randomization, population distributions or NPC baseline generation.',
 'must be explicitly marked **non-baseline** and may not enter ordinary player presets, Biological Randomization, population distributions or NPC baseline generation.\n\nIn this specification **baseline** means canonical Saurin species anatomy (the normal species condition), not a comparator, population centre or design default (Pass 2 AC-2; `decisions/PROJECT_RULES.md` terminology).',tag='AC-2')
for f,t in files.items(): open(R+f,'w').write(t)
print('rows applied',applied,'skipped',len(SKIP),'additions',len([l for l in log if not l[0].startswith('E')]))
print('files',sorted(files))
