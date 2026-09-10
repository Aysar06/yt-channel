import json,html,re,subprocess,wave,math
from production_runtime import media_tool, portable_path, project_path, video_encoder_args
from pathlib import Path
import numpy as np
from PIL import Image
from synthesize import captions
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';A=P/'03_AUDIO/revision_02';E=P/'05_EDIT/revision_02';C=P/'compositions/revision_02';C.mkdir(exist_ok=True);V=P/'04_MEDIA/video';CUT=V/'cuts';CUT.mkdir(exist_ok=True);FF=media_tool('ffmpeg')
M=json.loads((A/'connected_manifest.json').read_text(encoding='utf8'));rows={x['id']:x for x in M['lines']};shots=[]
def shot(ch,a,b,kind,source='',source_in=0,purpose='',**kw):
 if b is None:b=rows[ch]['duration']+(12 if ch=='r04' else 0)
 shots.append(dict(chapter=ch,start_local=a,end_local=b,kind=kind,source=source,source_in=source_in,purpose=purpose,**kw))
G='I5IogZtvJyI';L='AYSFN6UiVA8';TR='VYI-maF6xMI';TE='ByNhd5SoSU8';DT='zAQlWpcs8nE'
# Every source range is finite, forward, at original speed. Changes follow spoken ideas or source events.
shot('r01',0,10.9,'storage',purpose='Deleting an installation is an ordinary storage decision; selected tile disappears.')
shot('r01',10.9,27.4,'error',purpose='The actual PS4 download error documented in May 2015; focus on Cannot download.')
shot('r01',27.4,42,'installed',purpose='One drive retains the installation while another has an empty slot; no remote wipe implied.')
shot('r01',42,None,'poster',purpose='Identify the precise teaser as narration turns back to the experience.')
shot('r02',0,8.4,'video',G,19.2,purpose='Original waking camera looking from the floor toward the opening door.')
shot('r02',8.4,18.5,'video',G,45.5,purpose='Original corridor furnishings while the narrator describes learning the room.')
shot('r02',18.5,26.2,'video',G,82.4,purpose='A door transition returns the player to the corridor; the loop is the subject.')
shot('r02',26.2,31.7,'video',G,515,purpose='Specific changing picture clue; not unrelated hallway filler.')
shot('r02',31.7,37.1,'video',G,771,purpose='The red-light state shows a familiar route changing appearance.')
shot('r02',37.1,50.5,'video',G,997,purpose='Return to recognizable corridor geometry as familiarity is discussed.')
shot('r02',50.5,None,'video',G,395,purpose='Closed-door hesitation, checking the bathroom, then returning to the corridor.')
shot('r03',0,16.5,'web','playstation_tips_full.png',purpose='The actual official guide is the evidence for close inspection and trial-and-error.',focus='tips')
shot('r03',16.5,24.6,'video',G,1288,purpose='The radio/telephone clue objects being discussed in the puzzle conversation.')
shot('r03',24.6,33.4,'web','gameinformer_full.png',purpose='The real contemporary reader-discussion headline, author and date.',focus='discussion')
shot('r03',33.4,44.3,'video',TE,28.1,purpose='Actual Gamescom teaser preserves its concealed identity and P.T. title.')
shot('r03',44.3,52.1,'video',TE,44.7,purpose='Original AVAILABLE NOW / PS4 announcement matches immediate availability.')
shot('r03',52.1,None,'video',G,1321,purpose='Telephone puzzle payoff contextualizes players sharing how to reach an ending.')
# A 12-second editorial hold after the first reveal sentence gives the original title animation time to finish.
shot('r04',0,10.7,'video',TR,44,purpose='The original figure turns into the Norman Reedus face reveal.')
shot('r04',10.7,24.7,'video',TR,64,purpose='Let the complete Silent Hills title reveal play; narration intentionally clears the payoff.')
shot('r04',24.7,29.9,'video',TR,25.4,purpose='Original Hideo Kojima credit as the collaboration is named.')
shot('r04',29.9,34.6,'video',TR,38.9,purpose='Original Guillermo del Toro credit; a complete name reveal.')
shot('r04',34.6,41.8,'video',TR,55.2,purpose='Original Reedus credit and street pullback support the reveal-as-sales-pitch analysis.')
shot('r04',41.8,55.1,'video',DT,8.5,purpose='The actual KONAMI del Toro message identifies the collaborator and his discussion.',identify='Guillermo del Toro · KONAMI message, 2014')
shot('r04',55.1,68,'disclaimer',purpose='Original teaser disclaimer, shown as evidence rather than invented quotation.')
shot('r04',68,None,'two_works',purpose='A running teaser and the advertised future remain distinct artifacts.')
shot('r05',0,19.5,'web','cancellation_full.png',purpose='Cancellation date, original report and embryonic project wording.',focus='cancel')
shot('r05',19.5,31.4,'video',DT,119,purpose='Original collaborator discussing the project provides context for what audiences imagined.')
shot('r05',31.4,42.9,'two_works',purpose='The particular promised project ends; the released teaser remains visible.',cancel=True)
shot('r05',42.9,54.3,'video',G,236.5,purpose='A playable demonstration someone could show a friend, before access becomes the issue.')
shot('r05',54.3,None,'web','distribution_full.png',purpose='The notice introducing a distribution deadline.',focus='distribution')
shot('r06',0,14.5,'calendar',purpose='Separate the Apr 27 cancellation, Apr 29 distribution end, and May 6 report without duplicating narration as a headline.')
shot('r06',14.5,23.5,'web','gamespot_full.png',purpose='Original May 6 reporting on the loss of re-download access.',focus='gamespot')
shot('r06',23.5,32.5,'error',purpose='Actual test screenshot; follow the failed library recovery control.')
shot('r06',32.5,52.9,'network',purpose='Demonstrate installed storage surviving while the download path breaks.')
shot('r06',52.9,None,'drive',purpose='A file remains on a specific drive; replaceability is no longer automatic.')
shot('r07',0,26.2,'web','forum_full.png',purpose='Actual thread title and drive-upgrade testimony; retain author and personal-account context.',focus='forum')
shot('r07',26.2,39.1,'drive',purpose='A storage upgrade exchanges the drive while the playable file stays on the old one.',swap=True)
shot('r07',39.1,51,'choice',purpose='A recording fixes one camera path; interaction offers multiple directions, illustrated explicitly.')
shot('r07',51,None,'video',L,90,purpose='Original-software investigation introduces the source examined next.')
shot('r08',0,7.8,'video',L,117.8,purpose='Normal Lisa encounter and disappearance, directly preceding the patched comparison.',identify='Lance McDonald · original software investigation, 2019')
shot('r08',7.8,13.6,'video',L,103.2,purpose='Normal disappearance, followed by the altered version in the next shot.')
shot('r08',13.6,31.6,'video',L,131,purpose='Patched visibility: approach Lisa and inspect the model that normally disappears.')
shot('r08',31.6,39.2,'video',L,194,purpose='Original opening-room viewpoint toward the cracked door.')
shot('r08',39.2,55.2,'video',L,232,purpose='Patched opening-room investigation reveals the model beside the doorway.')
shot('r08',55.2,None,'video',L,248,purpose='The continued original-software inspection supports preservation as future discovery.')
shot('r09',0,15.7,'web','ps5_full.png',purpose='Dated source report of early PS5 review-hardware compatibility.',focus='ps5')
shot('r09',15.7,27,'compatibility',purpose='A historical compatibility path changes to PS4-only, anchored in the source report.')
shot('r09',27,None,'network',purpose='The older installed copy retains its significance; no current workaround is demonstrated.',historical=True)
shot('r10',0,16.5,'two_works',purpose='Distinguish the imagined Silent Hills from the actual P.T. experience.',editorial=True)
shot('r10',16.5,26.4,'video',G,502,purpose='Concrete picture/clue design is visible while the narrator describes examinable choices.')
shot('r10',26.4,40.4,'video',G,1067,purpose='The real interactive corridor continues beyond its role as an advertisement.')
shot('r10',40.4,54.1,'video',G,1346,purpose='A previously unused telephone sequence recalls sharing and reaching the game.')
shot('r10',54.1,None,'video',G,1249,purpose='Finish on a complete movement toward the corridor door; no padding loop.')
# Insert the deliberate reveal hold into voice data and remap every later cue.
audio=[];words=[];cursor=0;chapters=[]
for row in M['lines']:
 with wave.open(str(project_path(row['clean'])),'rb') as f:x=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()
 hold=12 if row['id']=='r04' else 0
 if hold:
  at=round(12.44*48000);x=np.concatenate([x[:at],np.zeros(hold*48000,dtype=np.int16),x[at:]])
 start=cursor/48000
 for w in row['words']:
  shift=hold if w['start']>=12.44 and hold else 0;words.append({**w,'line_id':row['id'],'start':start+w['start']+shift,'end':start+w['end']+shift})
 end=start+len(x)/48000;chapters.append({'id':row['id'],'start':start,'end':end,'duration':end-start,'title':json.loads((P/'02_SCRIPT/revision_02_request.json').read_text(encoding='utf8'))['lines'][len(chapters)]['title']});audio.append(x);cursor+=len(x)
D=cursor/48000
with wave.open(str(A/'timeline_narration.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes(np.concatenate(audio).tobytes())
(E/'chapters.json').write_text(json.dumps(chapters,indent=2),encoding='utf8');(A/'timeline.words.json').write_text(json.dumps(words,indent=2,ensure_ascii=False),encoding='utf8');(P/'07_EXPORT/revision_02_subtitles.srt').write_text(captions(words),encoding='utf8')
chmap={x['id']:x for x in chapters}
for i,s in enumerate(shots):
 s['id']=f's{i+1:03}';s['start']=chmap[s['chapter']]['start']+s['start_local'];s['end']=chmap[s['chapter']]['start']+s['end_local'];s['duration']=s['end_local']-s['start_local']
 if s['kind']=='video':
  info=json.loads((V/f"{s['source']}.info.json").read_text(encoding='utf8'));assert s['source_in']+s['duration']<=info['duration'];s['source_url']=info['webpage_url'];s['source_out']=s['source_in']+s['duration'];s['asset']=f"04_MEDIA/video/cuts/{s['id']}.mp4"
  dst=P/s['asset']
  cache=dst.with_suffix('.json');signature={'source':s['source'],'source_in':s['source_in'],'duration':s['duration'],'fps':24,'source_bytes':(V/f"{s['source']}.mp4").stat().st_size}
  if not dst.exists() or not cache.exists() or json.loads(cache.read_text())!=signature:
   subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-ss',str(s['source_in']),'-i',str(V/f"{s['source']}.mp4"),'-t',str(s['duration']),'-an','-vf','fps=24',*video_encoder_args(),'-pix_fmt','yuv420p','-movflags','+faststart',str(dst)],check=True)
   cache.write_text(json.dumps(signature,indent=2))
 elif s['kind']=='web':s['asset']='04_MEDIA/web/'+s['source']
 else:s['asset']=''
 # Exact overlapping source reuse is prohibited except the named normal/altered comparison.
for i,s in enumerate(shots):
 if s['kind']!='video':continue
 for prev in shots[:i]:
  if prev['kind']=='video' and prev['source']==s['source'] and min(prev['source_out'],s['source_out'])>max(prev['source_in'],s['source_in']) and not s.get('comparison_replay'):
   s.setdefault('reuse_review',[]).append(prev['id'])
(E/'shots.json').write_text(json.dumps(shots,indent=2,ensure_ascii=False),encoding='utf8')
print('Prepared',len(shots),'purpose-mapped shots;',D,'seconds; finite source cuts saved.',flush=True)
