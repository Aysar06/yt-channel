import json,zipfile,re
from pathlib import Path
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';Q=P/'09_REPORT'
qc=json.loads((Q/'export_qc.json').read_text(encoding='utf8'));T=json.loads((P/'05_EDIT/project_files/visual_timeline.json').read_text(encoding='utf8'))
M=json.loads((P/'03_AUDIO/narration_manifest.json').read_text(encoding='utf8'))
unique=len(set(x['asset'] for x in T if x['asset']));photo_sec=sum(x['end']-x['start'] for x in T if x['kind']=='photo')
report=f'''# Production 001 — P.T.

**Selected title:** The Horror Game You Could Lose Forever

**Final export:** `../07_EXPORT/final_video.mp4` — {qc['duration_seconds']:.3f} seconds (13:51), 1920×1080, 24fps, H.264/AAC, {qc['file_bytes']/1000000:.1f} MB. Synthetic English narration: Microsoft Edge Andrew Multilingual Neural. Twelve chapters, 142 shots. Zero AI images. {unique} unique sourced images appear in {photo_sec/qc['duration_seconds']:.1%} of the timeline; the remaining shots are native source excerpts, title cards and explanatory diagrams.

## Deliverables
- Main video and synchronized SRT: `../07_EXPORT/`.
- Primary thumbnail: `../06_THUMBNAIL/final/thumbnail.jpg`; PNG and alternate NO DOWNLOAD thumbnail included. Both 1280×720. Editable HTML retained. Main design uses an authentic P.T. still, P.T. identifier, DON’T DELETE wording and an editorial deletion symbol.
- Two backup titles, 22 scored title options, description, tags, keywords, hashtags, final chapters, pinned comment and five Shorts extraction plans: `../08_YOUTUBE/`. Shorts are plans, not rendered vertical clips.
- Seventeen topic candidates and 15 factual source records, additional community receipts, one competitor package review, saved vidIQ keyword/comment responses: `../01_RESEARCH/` and `../04_MEDIA/licenses/`.
- Final manuscript, performance script, narrative outline, paragraph/audio timing, full visual timeline, original diagrams and editable HyperFrames project retained.

## Validation actually completed
- HyperFrames upgraded from 0.8.30 to 0.8.31 before checking/rendering. Lint: zero errors, 34 warnings for reused media sources and chapter timeline density. Runtime: zero errors or warnings. Layout: zero errors or warnings; reported information concerns intentional photo cropping. Ten automated contrast checks passed. No motion assertions were configured.
- All 23 source/graphic placements inspected in timed snapshots. Both thumbnail variants inspected at 160×90. Encoded output yielded {qc['sampled_shots']} midpoint frames covering every shot; visual-review status: {qc['contact_sheet_visual_review']}.
- Full export decoded successfully with FFmpeg. Resolution, H.264/AAC, 24fps and duration verified with ffprobe. {qc['subtitle_cues']} SRT cues validated for increasing, nonoverlapping times within the film.
- Final encoded audio: {qc['audio']['integrated_lufs']:.2f} LUFS integrated, {qc['audio']['true_peak_dbtp']:.2f} dBTP. Music changes by chapter, is faded and ducked under dialogue, and includes restrained original sound effects.
- Independent full-narration transcription: 97.8% normalized token similarity, no low-confidence segments flagged. Most differences concern P.T., written numbers and inflections. This is an automated intelligibility check, not a human listening pass or a pronunciation guarantee.
- Black/silence detector results are retained in `export_qc.json` and `full_decode.log`; naturally dark gameplay and short intentional pauses must be interpreted in context.

## Practical limits and editorial notes
No human end-to-end listening review has occurred; a final listening pass remains before an unqualified upload-ready signoff. Competitor research is limited to one verified package and its ranked comment sample; broader visual/hook benchmarking is incomplete. No claim of professional voice acting, manually removed breaths, or measured retention is made. The cut uses motion-treated stills, not captured gameplay video.

The game images are copyrighted source material used with contextual commentary and attribution; their availability does not establish a blanket reuse license. Scott Buckley music is CC BY 4.0; preserve the supplied description credits. Community testimony is labeled as such. No post or screenshot is fabricated. Lisa-following claims include the flashlight qualifier; cancellation, distribution removal and re-download failure have distinct dates. Historical 2020 PS5 reports are not current compatibility instructions.

## Packaging and experiment
Primary thumbnail: DON’T DELETE. First alternative: NO DOWNLOAD. Backup title 1: P.T.: The Horror Game You Could Lose Forever. Backup title 2: The Game That Outlived Its Own Cancellation. Suggested later test: Why People Are Afraid to Delete This Game. All concept scores are editorial estimates; no experiment has run.

vidIQ estimated 5,073 monthly searches for P.T. Silent Hills, competition 44/100 and opportunity 55.59/100, with metrics dated 6 September 2026. Growth was unavailable. The topic is treated as evergreen. Nothing has been published; CTR, retention, views and revenue remain null in `../../channel_learning.json`.

The first render was stopped by a temporary-disk estimate. The next single-worker stream was superseded by four-worker parallel streaming to reduce render time; the composition and quality settings stayed the same. Render diagnostics are retained. No purchases or public uploads were performed.
'''
(Q/'production_report.md').write_text(report,encoding='utf8')
d=json.loads((R/'channel_learning.json').read_text(encoding='utf8'));d['productions'][0].update(status='rendered_unpublished',export='VIDEO_PROJECT/07_EXPORT/final_video.mp4',duration_seconds=qc['duration_seconds'],AI_images=0,human_listening_review=False);(R/'channel_learning.json').write_text(json.dumps(d,indent=2),encoding='utf8')
(P/'NEXT_SESSION.md').write_text('''# Production 001 checkpoint

Final video is rendered and technically verified: 07_EXPORT/final_video.mp4, 13:51 at 1080p24. Zero AI images; sourced stills, a real download-error screenshot, actual community/source excerpts and labeled original diagrams. Two sourced thumbnails, SRT, metadata and five Shorts plans are complete. See 09_REPORT/production_report.md and export_qc.json for actual QA and limitations. Full human listening review and broader competitor viewing study remain incomplete. Nothing published; no purchases. Analytics remain null. Do not regenerate narration or redo research. Preserve the user’s remaining usage.

Full project remains editable in HyperFrames 0.8.31. Upload files are also collected in 07_EXPORT/UPLOAD_PACKAGE_001.zip. Public publishing requires authorization. Preserve all music credits in the supplied description.
''',encoding='utf8')
target=P/'07_EXPORT/UPLOAD_PACKAGE_001.zip'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED) as z:
 for path in [P/'07_EXPORT/final_video.mp4',P/'07_EXPORT/final_subtitles.srt',P/'06_THUMBNAIL/final/thumbnail.jpg',P/'06_THUMBNAIL/final/thumbnail_alternative.jpg',Q/'production_report.md',Q/'export_qc.json',*sorted((P/'08_YOUTUBE').glob('*'))]:
  if path.is_file():z.write(path,path.relative_to(P))
print('Upload package saved:',target,'bytes:',target.stat().st_size)
