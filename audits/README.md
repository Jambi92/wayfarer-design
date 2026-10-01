# Audit Workspace

Claude is the designated auditor.

For each audit, create or update an audit file rather than silently rewriting the authoritative specification.

Recommended naming:
- `audits/pipkin-part-2.md`
- `audits/pipkin-part-3.md`

Each audit should contain:
1. Result: PASS / PASS WITH CLARIFICATIONS / BLOCKING CONFLICT
2. Contradictions
3. Ambiguities or missing positive anchors
4. Cross-population conflicts
5. Prototype conflicts known from available evidence
6. Recommended clarification questions or corrections
7. Completion recommendation

ChatGPT, as author, resolves accepted findings in `specs/`.
