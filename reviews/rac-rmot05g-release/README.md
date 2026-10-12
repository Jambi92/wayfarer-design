# RM-OT-05G sculptor release

| | |
|---|---|
| Release id | `gorrund-sculpt-release-8b76d2eae245` |
| Source commit | `8b76d2eae245d2adce3f228a8a11f7b616b6b825` (folder `reviews/rac-rmot05f-handoff/`) |
| Archive | `gorrund-sculpt-release-8b76d2eae245.zip` |
| Archive SHA-256 | `287884f0da90df18cc9bd51e2291b8c602d88df0517fcfb8556513ce2f191bcd` |
| Size | 9 571 289 bytes, 81 files plus the manifest |
| Entry point | `rac-rmot05f-handoff/START_HERE.md` |

The archive is **not committed**: it would only duplicate committed files. It is deterministic, so rebuilding from the source commit gives the same SHA-256 (this was checked twice). To rebuild and check it:

```
git checkout 8b76d2eae245d2adce3f228a8a11f7b616b6b825
python3 tools/rac/w1/rmot05g_blender/g_release.py build --out <dir>
python3 tools/rac/w1/rmot05g_blender/g_release.py verify <dir>/gorrund-sculpt-release-8b76d2eae245.zip
```

Contents of this folder:

| File | What |
|---|---|
| `RELEASE_MANIFEST.json` | Byte-identical to the manifest inside the archive: full SHA-256 and size of every file, the required paths and the frozen hashes |
| `RELEASE_VERIFY.json` | Result of the clean-copy check: COMPLETE |
| `*.zip.sha256` | Archive hash |

A built copy was also placed on the author's machine at `E:/UnrealProjects/Wayfarer 5.8/RaceBodies/sheets/racebodies_v111/`.
