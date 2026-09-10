# Resume production 001 from this checkpoint

Checkpoint saved 2026-09-10 for migration to `Aysar06/yt-channel`. Read this before older status reports. The user's latest request was to push the complete resumable workspace to that private repository.

## Current state

**Revision 02 is rendered, technically checked, and still awaiting final review.** Continue this production; do not start another topic. The current edit is `VIDEO_PROJECT/index.html`, mounting ten chapters in `VIDEO_PROJECT/compositions/revision_02/`. The current movie is `VIDEO_PROJECT/07_EXPORT/revision_02.mp4`, 622.25 seconds, 1920×1080, 24 fps, H.264/AAC, 344,510,060 bytes.

SHA-256: `78d537dc6dd859b7a8cb3072dd6a02eacefdca4dc41e1bc438c9f3332383f085`.

The **rejected V1** remains at `VIDEO_PROJECT/07_EXPORT/final_video.mp4` (13:51); that filename is historical and does not indicate approval. Its composition backup is `VIDEO_PROJECT/05_EDIT/revision_02/v1_project`. Do not use V1 packaging scripts or old root YouTube metadata to package revision 02. Revised metadata is in `VIDEO_PROJECT/08_YOUTUBE/revision_02/`.

## User requirements that govern the next work

Read `PRODUCTION_BRIEF.txt` and `VIDEO_PROJECT/REVISION_REQUIREMENTS.txt`. The user rejected the original film and requires a substantive rebuild, much less AI imagery and more actual sourced material, including community posts/forums. This revision uses **zero AI images**. Conserve usage; reuse completed research, unchanged narration and frozen assets.

Avoid generic black/red templates, permanent source/chapter footers, narration duplicated as headlines, repetitive stills, padding, reversed/looped footage and clipped speech. The film needs natural connected narration and relevant evidence matched to the spoken point. The user requires full audio-only listening and an uninterrupted whole-film viewer review. Neither has been completed; transcription and sampled frames cannot substitute for them. Do not claim approval or upload readiness prematurely. No public publishing or paid purchases are authorized.

## Exact next work

1. Run the setup/verification in README.md. All original footage and current audio are frozen locally; do not synthesize new voice takes just to resume.
2. Visually review the latest encode's 159 entry/midpoint/exit samples (`VIDEO_PROJECT/09_REPORT/revision_02/encoded_review_1.jpg` through `_9.jpg`) and affected shots in the actual MP4. The prior encode's 159 samples were inspected; **the latest encode's samples remain pending**. Its two changes are the complete official PlayStation guide heading and removal of an extra fan subtitle beneath the original teaser disclaimer.
3. Inspect the disclaimer around 247.45 seconds. The current original-image crop is `(0,0,1920,865)` in `compose_revision.py`. There was an unresolved concern that this asymmetric crop might place the text too low. Inspect first; a vertically balanced crop was only a possible idea, not an implemented or verified correction. Do not assume it is defective without viewing.
4. Complete the full audio-only and uninterrupted viewer reviews required by the user using actual supported listening/viewing. If those capabilities are unavailable, retain both fields as false and state the precise limitation. Fix identified issues, render only when needed, and repeat affected verification.
5. After quality passes, reconcile thumbnail and upload package with the revision's new length/script, update final reports and review status, and create a distinctly named revision 02 package. Preserve real source credits. Do not publish to YouTube without authorization.

## Completed evidence and decisions

- The latest render and full automated decode completed successfully; no render is pending. HyperFrames 0.8.32 was used. The media manifest verifies the actual frozen bytes.
- Ten continuous scene takes, 1,631 script words, Andrew Multilingual neural voice at +0% rate / +0 Hz pitch. Measured silence editing removed about 5.436 seconds, leaving 610.236 seconds of connected narration.
- A deliberate 12-second original title-reveal hold is inserted at **r04 local 12.44 seconds**, inside measured silence. A previous 12.7-second insertion split speech and was fixed. Preserve the corrected boundary and matching word/caption shifts.
- 53 purpose-mapped shots, about 311 seconds of actual motion footage, no overlapping source ranges in this edit, no loops/reverse/slow motion/padding freezes. Source in/out/purpose records are in `05_EDIT/revision_02/shots.json`.
- Current encoded QA: 194 valid caption cues; full timeline coverage; zero decode errors; -16.31 LUFS integrated, -4.27 dBTP peak; no detected whole-mix silence below -50 dB lasting at least one second.
- Three black-detector events are original source title/fade frames at approximately 167.71–168.58, 210.63–211.54 and 215.83–218.29 seconds. Inspect their context before treating them as missing footage.
- The previous full ASR check gave approximately 0.96675 text similarity, mostly punctuation/name/number differences; it is explicitly not a hearing review. A separate reveal-join check confirmed speech continuity after the silence-boundary correction.
- Original source footage: Shirrako walkthrough `I5IogZtvJyI`; Silent Hill Memories teaser `ByNhd5SoSU8` and ending reveal `VYI-maF6xMI`; KONAMI del Toro message `zAQlWpcs8nE`; Lance McDonald 2019 investigation `AYSFN6UiVA8`. The separately downloaded 2020 AV1 investigation `nJHg1gmySTs` is not used in this edit.
- r08 describes Lance McDonald's **September 26, 2019 visibility investigation**, not the distinct September 9 Lisa-following-camera claim from older research. Revised sourcing is in `01_RESEARCH/revision_02_sources.md`.
- The forum is an individual drive-upgrade account, not proof of every user's experience. PS5 material describes 2020 review hardware, not a verified current workaround. Cancellation, distribution ending and redownload failure are separate dated events.
- Source webpages/screenshots, creator URLs and per-shot editorial-use notes are retained. No invented rights clearance, analytics or completion claims. `channel_learning.json` has null unavailable analytics.

## Editing and environment notes

Use the copied skills in `.agents/skills/` for the HyperFrames workflow. The production Python scripts derive the checkout location automatically; active audio manifests now use repository-relative paths. `production_runtime.py` also recognizes the historical Windows manifest paths. Historical reports can contain old absolute paths as provenance; they are not required locations.

Use Python 3.11, Node.js 24, the pinned npm lockfile and requirements. Windows includes FFmpeg 9.0.1 through LFS. macOS/Linux need local FFmpeg/ffprobe; font differences may affect newly rendered layouts. Source footage cuts and the existing MP4 remain byte-identical after clone. Original render hardware was an RTX 4060; software encoding is available on other computers. Required renderer assets such as pinned GSAP may need internet access. Browser sessions, API sign-ins, ASR model caches and OS fonts are not Git state.

The detailed pipeline is `VIDEO_PROJECT/05_EDIT/revision_02/REBUILD.md`. `handoff/checkpoint.json` is the machine-readable checkpoint; `handoff/media-manifest.json` lists frozen binary hashes. After future intentional media edits, regenerate the manifest with `python tools/save_checkpoint.py` and update this document and review evidence before committing.
