import json,re,subprocess,shutil
from pathlib import Path
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';Q=P/'09_REPORT/revision_02';Q.mkdir(exist_ok=True,parents=True)
FF=str(R/'tools/ffmpeg/bin/ffmpeg.exe')
T=json.loads((P/'05_EDIT/project_files/visual_timeline.json').read_text(encoding='utf8'));M=json.loads((P/'03_AUDIO/narration_manifest.json').read_text(encoding='utf8'))
issues=[]
for x in T:
 issues.append({'start':x['start'],'end':x['end'],'severity':'high','issue':'Persistent chapter/source decoration; remove from corrected composition.','shot_kind':x['kind']})
for i,x in enumerate(T):
 if i and x['asset'] and x['asset']==T[i-1]['asset']:
  issues.append({'start':T[i-1]['start'],'end':x['end'],'severity':'high','issue':'Same source immediately repeated with a restarted crop/zoom. Replace with one meaningful continuous shot or a different exact source.'})
 if x['kind'] in ('title','quote','compare','dates'):
  issues.append({'start':x['start'],'end':x['end'],'severity':'high','issue':'Repeated display-card grammar. Replace with original source/UI/object-driven sequence.'})
r=subprocess.run([FF,'-hide_banner','-i',str(P/'03_AUDIO/narration.wav'),'-af','silencedetect=noise=-42dB:d=0.22','-f','null','NUL'],capture_output=True,text=True)
sil=[];a=None
for line in r.stderr.splitlines():
 if 'silence_start:' in line:a=float(line.split('silence_start:')[1].split()[0])
 elif 'silence_end:' in line and a is not None:
  b=float(line.split('silence_end:')[1].split()[0]);sil.append({'start':a,'end':b,'duration':b-a});a=None
for x in sil:
 if x['duration']>.65:issues.append({'start':x['start'],'end':x['end'],'severity':'high','issue':'Measured narration silence exceeds 650ms; inspect linguistic boundary and shorten unless an intentional visual reveal needs it.'})
(Q/'v1_silences.json').write_text(json.dumps(sil,indent=2),encoding='utf8');(Q/'v1_issues.json').write_text(json.dumps(issues,indent=2),encoding='utf8')
backup=P/'05_EDIT/revision_02/v1_project';backup.mkdir(parents=True,exist_ok=True)
for name in ['index.html','STORYBOARD.md','design.md','BRIEF.md']:
 if not (backup/name).exists():shutil.copyfile(P/name,backup/name)
if not (backup/'compositions').exists():shutil.copytree(P/'compositions',backup/'compositions')
d=json.loads((R/'channel_learning.json').read_text(encoding='utf8'));d['productions'][0]['status']='rejected_revision_in_progress';d['productions'][0]['approved']=False;(R/'channel_learning.json').write_text(json.dumps(d,indent=2),encoding='utf8')
(P/'NEXT_SESSION.md').write_text('# Revision 02 in progress\n\nThe user rejected V1. The previous MP4 and ZIP are NOT approved/final. Apply REVISION_REQUIREMENTS.txt in full. Existing project backed up under 05_EDIT/revision_02/v1_project. Rebuild using original inspected gameplay, announcement and camera-investigation footage, real article/forum captures, purposeful UI and varied subject-led layouts. Remove all permanent labels. Repair narration gaps first; unlock all timings. No new AI images. No human listening or uninterrupted viewer review has been completed; never claim otherwise.\n',encoding='utf8')
print({'shots':len(T),'consecutive_duplicate_images':sum(bool(i and x['asset'] and x['asset']==T[i-1]['asset']) for i,x in enumerate(T)),'silences_over_650ms':sum(s['duration']>.65 for s in sil),'longest_narration_silence':max(x['duration'] for x in sil),'total_measured_silence':sum(x['duration'] for x in sil),'status':'rejected_revision_in_progress'})
