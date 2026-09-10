"""Prepare the saved manuscript for real narration; no model/API generation here."""
import json, re, shutil
from pathlib import Path
root=Path(__file__).resolve().parent.parent
p=root/'VIDEO_PROJECT'
text=(p/'02_SCRIPT/final_script.md').read_text(encoding='utf8')
chapters=[]; lines=[]; performance=[]
moods=['CURIOUS','CURIOUS','QUIET','EXCITED','EXCITED','SERIOUS','SERIOUS','QUIET','CURIOUS','SERIOUS','QUIET','QUIET']
rates=['-6%','-4%','-8%','-2%','-4%','-6%','-5%','-8%','-6%','-5%','-6%','-8%']
for ci,part in enumerate(re.split(r'^## ',text,flags=re.M)[1:]):
    heading,body=part.split('\n',1)
    paragraphs=[x.strip() for x in body.strip().split('\n\n') if x.strip()]
    ids=[];performance.append('## '+heading+'\n')
    for pi,paragraph in enumerate(paragraphs):
        ident=f'c{ci+1:02d}p{pi+1:02d}';ids.append(ident)
        lines.append({'id':ident,'text':paragraph,'rate':rates[ci], 'pitch':'+0Hz','gap_after':.16 if pi<len(paragraphs)-1 else .45})
        performance.append('['+moods[ci]+'] '+paragraph+'\n')
    chapters.append({'id':ci+1,'title':heading.split(' — ',1)[-1],'line_ids':ids})
(p/'02_SCRIPT/narration_request.json').write_text(json.dumps({'voice':'en-US-AndrewMultilingualNeural','lines':lines},ensure_ascii=False,indent=2),encoding='utf8')
(p/'02_SCRIPT/chapters.json').write_text(json.dumps(chapters,ensure_ascii=False,indent=2),encoding='utf8')
(p/'02_SCRIPT/voice_performance_script.md').write_text('# Internal performance script\n\nEmotion tags guide delivery and editing. Edge TTS supports rate and pitch; these tags are not claimed to be native emotion controls and are not subtitles.\n\n'+'\n'.join(performance),encoding='utf8')
shutil.copyfile(root/'research/pt_sources.md',p/'01_RESEARCH/sources.md')
records=json.loads((p/'04_MEDIA/licenses/shm_download_records.json').read_text(encoding='utf8'))
for item in records:
    item['path']=str(Path(item['path']).relative_to(p)).replace('\\','/')
    item['rights']='Game imagery remains copyrighted; gallery availability is not a reuse license. Use only for specific contextual analysis, credited to Konami and the archive.'
(p/'04_MEDIA/licenses/asset_manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
(root/'channel_learning.json').write_text(json.dumps({'productions':[{'id':1,'topic':'P.T. and Silent Hills','status':'in_production','published':False,'CTR':None,'average_view_duration':None,'retention_drops':None,'traffic_sources':None}],'preferences':{'AI_images':'Avoid when real source material is available; aim for zero in current edit','sources':'Include documented community posts and forums'}},indent=2),encoding='utf8')
print(f'Prepared {len(lines)} paragraphs across {len(chapters)} chapters; {len(records)} sourced image records.')
