import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';S=json.loads((P/'05_EDIT/revision_02/shots.json').read_text());C=json.loads((P/'05_EDIT/revision_02/chapters.json').read_text());U=P/'08_YOUTUBE/revision_02';U.mkdir(exist_ok=True)
pages={
'tips':'https://blog.playstation.com/2014/10/31/p-t-on-ps4-survival-tips-for-konamis-horror-hit/',
'discussion':'https://gameinformer.com/b/news/archive/2014/08/16/reader-discussion-have-you-finished-the-silent-hills-playable-teaser-p-t.aspx',
'cancel':'https://www.gematsu.com/2015/04/silent-hills-officially-cancelled',
'distribution':'https://www.gematsu.com/2015/04/p-t-distribution-end-april-29',
'gamespot':'https://www.gamespot.com/articles/p-t-can-no-longer-be-downloaded-even-from-your-ps4/1100-6427124/',
'forum':'https://gamefaqs.gamespot.com/boards/691087-playstation-4/74324135',
'ps5':'https://www.gematsu.com/2020/11/p-t-was-playable-on-ps5-until-publisher-decision-made-it-ps4-only'}
rights='Copyrighted source used for contextual commentary and analysis. Public availability does not grant a blanket reuse license; no permission or clearance is claimed.'
ledger=[]
for s in S:
 row=dict(s)
 if s['kind']=='video':
  i=json.loads((P/f'04_MEDIA/video/{s["source"]}.info.json').read_text(encoding='utf8'));row.update(creator=i.get('uploader'),title=i.get('title'),rights=rights,original_speed=True,loop=False,reverse=False,padding_freeze=False)
 elif s['kind']=='web':row.update(source_url=pages[s['focus']],rights=rights,capture='Actual browser pixels; evidence crops in 04_MEDIA/evidence; native text is not reconstructed.')
 elif s['kind']=='error':row.update(source_url=pages['gamespot'],rights=rights,asset='04_MEDIA/images/gs_download_error.jpg')
 else:row.update(rights='Original explanatory layout; any embedded game or page imagery retains its source copyright.',ai_generated=False)
 ledger.append(row)
(P/'04_MEDIA/licenses/revision_02_asset_ledger.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False),encoding='utf8')
def stamp(t):return f'{int(t)//60:02}:{int(t)%60:02}'
chapters='\n'.join(stamp(c['start'])+' '+c['title'] for c in C)+'\n';(U/'chapters.txt').write_text(chapters,encoding='utf8');(U/'title.txt').write_text('The Horror Game You Could Lose Forever\n',encoding='utf8')
desc="""A free horror game became something players were afraid to delete. P.T. survived on installed consoles while its ordinary download path disappeared.

From the disguised 2014 announcement to Silent Hills' cancellation, failed re-downloads, and Lance McDonald's 2019 investigation of visibility and unseen objects, this follows the teaser people actually played. The 2020 PS5 segment describes historical review hardware.

Original footage and imagery:
P.T. gameplay — Shirrako: https://www.youtube.com/watch?v=I5IogZtvJyI
2014 Gamescom P.T. announcement — Silent Hill Memories: https://www.youtube.com/watch?v=ByNhd5SoSU8
Silent Hills ending/reveal — Silent Hill Memories: https://www.youtube.com/watch?v=VYI-maF6xMI
Guillermo del Toro's official KONAMI message: https://www.youtube.com/watch?v=zAQlWpcs8nE
Lance McDonald's September 2019 original-software investigation: https://www.youtube.com/watch?v=AYSFN6UiVA8
P.T. / Silent Hills game imagery © Konami. Additional original stills: https://www.silenthillmemories.net/silent_hills/screens_en.htm

Research and captured evidence:
"""+'\n'.join(k+': '+v for k,v in pages.items())+"""

Music:
'Eyes In The Void' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au
https://www.scottbuckley.com.au/library/eyes-in-the-void/
'Incredulity' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au
https://www.scottbuckley.com.au/library/incredulity/
'Unraveling' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au
https://www.scottbuckley.com.au/library/unraveling/
License: https://creativecommons.org/licenses/by/4.0/
Music edited with fades and narration ducking. Game ambience from the credited gameplay; original interface click.

Narration is synthetic. No AI images. Some storage and compatibility explanations use original diagrams; those are not recordings of a console interface.

Chapters:
"""+chapters+'\n#PT #SilentHills #HorrorGaming\n';(U/'description.txt').write_text(desc,encoding='utf8')
(P/'01_RESEARCH/revision_02_sources.md').write_text('# Revision 02 source changes\n\nThe 2019 sequence now analyzes the actual September 26 visibility investigation. The earlier September 9 following-camera Twitter claim is removed from the cut. Do not reinsert it on the basis of the old manuscript.\n\n'+'\n'.join(f'- [{k}]({v})' for k,v in pages.items())+'\n\nOriginal footage and exact in/out ranges are recorded in `04_MEDIA/licenses/revision_02_asset_ledger.json`. No blanket reuse license or creator permission is asserted.\n',encoding='utf8')
edits=json.loads((P/'09_REPORT/revision_02/voice_timing_edits.json').read_text());stats={'duration_seconds':C[-1]['end'],'shots':len(S),'real_video_seconds':sum(s['duration'] for s in S if s['kind']=='video'),'web_evidence_seconds':sum(s['duration'] for s in S if s['kind']=='web'),'ai_images':0,'permanent_source_footers':0,'voice_takes':10,'removed_measured_silence_seconds':sum(e['removed_seconds'] for e in edits),'intentional_title_reveal_hold_seconds':12,'unintentional_overlapping_source_ranges':sum(bool(s.get('reuse_review')) for s in S),'hyperframes_version':'0.8.32'};(P/'09_REPORT/revision_02/change_statistics.json').write_text(json.dumps(stats,indent=2))
print(json.dumps(stats,indent=2))
