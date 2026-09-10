import json,re,html
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT'
def write(path,s):(P/path).write_text(s,encoding='utf8')
write('01_RESEARCH/competitor_analysis.md', '''# Competitor and audience evidence — 8 September 2026

## Verified reference
[GVMERS: Kojima's Cancelled Masterpiece — Investigating Silent Hills](https://www.youtube.com/watch?v=_P7wHolvfH0). Title and description retrieved through YouTube search; 15 top comments and replies saved from vidIQ in `vidiq_comments.json`. The title emphasizes the cancelled collaboration and an investigation. The description promises a history of Silent Hills. These are packaging observations, not a complete viewing audit. Reliable first-30-second, pacing and thumbnail observations were not retained; they are not invented here. No private retention, CTR, impressions or revenue data is available.

Comment evidence: @electricbayonet2 reacts to the disappointment surrounding the cancelled collaboration (2,622 likes in the retrieved snapshot); @KitsGravity imagines the unrealized creative lineup (1,399); @Fourloko45 expresses frustration through a Silent Hill reference (1,383). This small, ranked, old-comment sample suggests disappointment is a useful emotional entry point. It does not establish current demand or represent all viewers. No comment is fabricated for the edit.

Our angle begins with the installed copy and the consequences of deleting it, then earns the cancellation context. Later camera discoveries and the 2020 compatibility report give the story movement beyond the initial announcement. Distinguishing the released teaser from the unrealized full game keeps the payoff grounded. These are creative decisions, not measured predictions.

## Keyword research
Raw response: `vidiq_keyword.json`. Seed: P.T. Silent Hills. Estimated monthly searches: 5,073; volume score 55.31/100; competition 44/100; overall opportunity 55.59/100. Metrics timestamp: 6 September 2026, retrieved 8 September. No related suggestions, regional estimates, growth baseline or search-growth percentage were returned. Treat this as an evergreen topic with a documented search signal, not a demonstrated rising trend.

## Scope
The 17-topic matrix and 22-title matrix use editorial scores. Only one directly relevant competing YouTube package and its comment sample have been verified for this report. A broader competitor viewing study remains incomplete. Channel performance is unknown until this production is published and real analytics are supplied.
''')
C=json.loads((P/'05_EDIT/project_files/chapter_timing.json').read_text())
T=json.loads((P/'05_EDIT/project_files/visual_timeline.json').read_text())
write('02_SCRIPT/outline.md','# Final narrative outline\n\nPromise: explain how a free teaser became an experience someone could lose.\n\n'+'\n'.join(f"{i+1}. **{x['title']}** — {int(x['start'])//60:02}:{int(x['start'])%60:02}" for i,x in enumerate(C))+'\n\nThe opening establishes deletion stakes; the middle separates cancellation, distribution and re-download; the camera investigation shows why preserving executable software matters; the ending returns to the difference between watching a recording and holding the controller. Full manuscript: final_script.md. Exact shots and timings: ../05_EDIT/project_files/visual_timeline.csv.\n')
f=P/'06_THUMBNAIL/concepts/concepts.md';s=f.read_text()
s=s.replace('This is concept development only; no image has been generated or visually inspected yet.','Six concepts were scored. Concepts A and B are now rendered in ../final using an authentic P.T. screenshot, native typography and an editorial deletion symbol. No AI imagery is used. Other concepts remain unrendered proposals.')
s=s.replace('a large, isolated P.T. game card showing an original illustrated dark hallway.','an authentic P.T. hallway still sourced from Silent Hill Memories, cropped into a large left-side panel.')
s=s.replace('this is a designed illustration.','the screenshot is genuine; typography and the deletion symbol are editorial additions.')
s=s.replace('one large vacant game-card silhouette with a ghosted P.T. identifier and a broken downward arrow.','the same authentic hallway image and P.T. identifier as concept A, with the alternative NO DOWNLOAD wording.')
s=s.replace('one original horror hallway','one sourced P.T. hallway still')
s+='\n\n## Final implementation\nA: `../final/thumbnail.jpg` and PNG, 1280×720. B: `../final/thumbnail_alternative.jpg` and PNG. The alternative uses the same source photograph to isolate the wording change. Neither is a real PlayStation deletion dialog. Source: https://www.silenthillmemories.net/silent_hills/screens_en.htm — `silent_hills_pt_screen_20140821_02.jpg`, game imagery © Konami. Editable HTML retained. Scores are editorial; no CTR test has run.\n'
f.write_text(s,encoding='utf8')
write('04_MEDIA/licenses/community_sources.md','''# Additional source receipts used in the edit

- GameSpot, 6 May 2015: https://www.gamespot.com/articles/p-t-can-no-longer-be-downloaded-even-from-your-ps4/1100-6427124/ — actual PS4 download-error screenshot saved as `../images/gs_download_error.jpg`. Direct original: https://www.gamespot.com/wp-content/uploads/original/280/2802776/2860565-20150506144042.jpg . Copyrighted screenshot; credited in the relevant frames and description. Availability is not a license grant.
- Game Informer reader discussion, 16 August 2014: https://gameinformer.com/b/news/archive/2014/08/16/reader-discussion-have-you-finished-the-silent-hills-playable-teaser-p-t.aspx — brief attributed headline excerpt on a native source card.
- GameFAQs, Firehawk030: https://gamefaqs.gamespot.com/boards/691087-playstation-4/74324135 — 20-word attributed excerpt describing an installed copy and a drive upgrade. Personal testimony, not a verified universal outcome. Native excerpt card; not a fabricated website screenshot.

No Reddit or Twitter screenshot is claimed in this cut. The sourcing preference is fulfilled with real game stills, a contemporary test image, and actual community discussion. Original explanatory diagrams are labeled; AI images: zero.
''')
write('05_EDIT/project_files/animation_map.md','''# Motion map

12 chapter subcompositions; 142 timed shots. 121 photo placements (including two contemporary error-screen placements); 21 native title, excerpt or explanatory cards. Ordinary photo shots move continuously from scale 1.01 to 1.10 with a 17px horizontal and 8px vertical drift, reversing direction between shots. Error screenshots ease from 0.97 to 1.00 while remaining contained. The camera schematic draws its connection over two seconds; the loop diagram draws over three seconds. Cards enter over 0.38 seconds, then hold. Hard cuts follow actual paragraph timings. Runtime uses paused GSAP timelines and framework-owned audio playback.

Checks: no runtime errors, no layout errors or warnings. Layout info findings are intentional image overflow during the contained crop. Lint warnings identify reused image sources and 9–15 shots per chapter; each timed section has its own identifier. No automated motion assertions were configured. All 23 source/graphic placements were inspected via timed HyperFrames snapshots. Final exported shot contact sheets provide a separate encoded-frame check.
''')
# Mobile-sized thumbnail comparison, for visual QA rather than image editing.
im=Image.new('RGB',(420,175),'#242424');draw=ImageDraw.Draw(im)
for i,name in enumerate(['thumbnail','thumbnail_alternative']):
 x=20+i*200;src=Image.open(P/f'06_THUMBNAIL/final/{name}.jpg');src.thumbnail((160,90));im.paste(src,(x,30));draw.text((x,130),'A: DON\'T DELETE' if i==0 else 'B: NO DOWNLOAD',fill='white')
im.save(P/'09_REPORT/thumbnail_mobile.jpg')
write('NEXT_SESSION.md','''# Current checkpoint — 8 September 2026

Production 001, P.T.: The Horror Game You Could Lose Forever. Narration and edit completed, 831.246 seconds, 12 chapters, 142 shots, zero AI images. Full mix measured -16.12 LUFS / -4.43 dBTP. Independent full-narration ASR similarity 97.8%, no low-confidence segments flagged. Human listening review not performed. Real game stills and community/source excerpts are credited; music is Scott Buckley CC BY 4.0. Descriptions retain attribution.

HyperFrames updated to 0.8.31. Full check passed: zero lint errors, zero runtime errors/warnings, zero layout errors/warnings; known maintainability warnings and intentional cropped-image overflow documented. All 23 cards checked visually. Full 1080p24 render started in session 93821, output 07_EXPORT/final_video.mp4. Check process/file before restarting. Next: verify encoded output, inspect every shot contact sheet, finish report and delivery package. Thumbnail A/B, SRT, upload metadata and five Shorts plans are already saved. No publishing authorized. Conserve account usage; no redundant research or image generation.
''')
print('Research scope, outline, sourcing, motion map, concepts and checkpoint updated.')
