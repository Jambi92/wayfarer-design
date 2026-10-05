# Post-edit audit fixes (conforming/reconciliation only; no new biology).
R='/home/claude/wayfarer-design/'
def rep(f,cur,new,n=1):
    t=open(R+f).read(); c=t.count(cur); assert c==n,(f,c,cur[:70]); open(R+f,'w').write(t.replace(cur,new))
D='specs/durrim/DURRIM_V1.md'
# 1 restore quoted legacy trait; comparator note outside the quote
rep(D,'"Durrim hold their breath longer than the Marchfolk Human Reference Population" stay','"Durrim hold their breath longer than baseline humans" (comparator read as the Marchfolk Human Reference Population; PROJECT_RULES terminology) stay')
# 3 tier vs mode
rep(D,'menu hierarchy, Simple Mode or Advanced Mode controls,','menu hierarchy, Simple Mode or Advanced Mode controls (including quick and detailed controls),')
rep(D,'presets, Simple Mode and Advanced Mode editing,','presets, Simple Mode and Advanced Mode (including quick and detailed controls) editing,')
# 8 Durrim acquired states
rep(D,'sun exposure, weathering), which are acquired states.','sun exposure, weathering), which are transient environmental states (Environmental Skin Appearance Layer).')
# 15 Durrim short-race label
rep(D,'| Future Short-Race Comparative Anatomy Review |','| Short-Race Comparative Anatomy Review (originally future; now ACCEPTED / COMPLETE: `reviews/short-race-comparative-anatomy-v1.md`) |')
M='specs/marchfolk/MARCHFOLK_V1.md'
rep(M,'| Mode | Controls |','| Tier | Controls |')
rep(M,'## 5. Advanced body regions','## 5. Detailed body regions')
rep(M,'## 3. Natural asymmetry (Advanced)','## 3. Natural asymmetry (detailed controls)')
rep(M,'Advanced may add regional distribution','Detailed controls may add regional distribution')
S='specs/skarn/SKARN_V1.md'
rep(S,'## 5. Hands and feet (Advanced)','## 5. Hands and feet (detailed controls)')
rep(S,'\nAdvanced controls to explore:','\nDetailed controls to explore:')
rep(S,'The next race was Sagekin, whose scholarly culture must never','The next race was Sagekin, and scholarly culture must never')
rep(S,'Skarn hold their breath about 1.5× as long as the Marchfolk Human Reference Population.','Skarn hold their breath about 1.5× as long as the baseline (read as the Marchfolk Human Reference Population).')
K='specs/grask/GRASK_V1.md'
rep(K,'the final comparison waits for Gorrund.','the final comparison waits for Gorrund. (Gorrund is now first-pass complete; Grask–Gorrund relations are defined in the Gorrund spec and the Pass 2 Large-Race Comparative Anatomy Review. This placeholder text is retained as history.)')
rep(K,'| Future Large-Race Comparative Anatomy Review | (Performed','| Large-Race Comparative Anatomy Review (originally future) | (Performed')
G='specs/gorrund/GORRUND_V1.md'
rep(G,'| Large-Race Comparative Anatomy Review | After Gorrund first pass, at least Skarn, Grask and Gorrund, so all three have positive, independent identities |',
 '| Large-Race Comparative Anatomy Review | After Gorrund first pass, at least Skarn, Grask and Gorrund, so all three have positive, independent identities. (Performed and accepted in Pass 2: `reviews/claude-pass2-r2-large-race-comparative-review.md`; AD-1–AD-5.) |')
rep(G,'Presets may use internal proportion families (more axial, more balanced, slightly more limb-present),',
 'Presets may use internal proportion families (more axial, more balanced, slightly more limb-present; at matched height the limb-present family stays below the shortest-limbed valid Grask in relative limb contribution — Pass 2 AD-3),')
rep(G,'| ID | Target (internal validation only, not subraces) |','GOR-BODY-01…18 and GOR-STRESS-01…09 were cited with the prefix GRR- before Pass 2; historical GRR- citations refer to the same cases.\n\n| ID | Target (internal validation only, not subraces) |')
SA='specs/saurin/SAURIN_V1.md'
rep(SA,'These remain separate anatomical quantities.','These remain separate anatomical controls.')
rep(SA,'Expression ranges from subtle keratin ridges and low hornlets','Expression ranges from subtle ridges and low hornlets')
rep('specs/halvren/HALVREN_V1.md','Environment (sun, weathering, dryness, scarring)','Environment (sun, weathering, dryness; scarring is Acquired)')
rep('specs/pipkin/PIPKIN_V1.md','lighting, exposure, wetness, dirt, camera and color grading must not','lighting, exposure, camera and color grading (observation) and wetness or dirt (Environmental layer) must not')
A='specs/aelari/AELARI_V1.md'
rep(A,'The review isn\'t performed yet. It happens after','The review isn\'t performed yet (since performed and accepted: `reviews/elf-comparative-review.md`). It happens after')
rep(A,'The review isn\'t performed until Vael v1.0–v1.5 are complete.','The review isn\'t performed until Vael v1.0–v1.5 are complete (since performed and accepted: `reviews/elf-comparative-review.md`).')
print('ok')
