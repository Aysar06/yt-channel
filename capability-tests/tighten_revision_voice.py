"""Conservative silence edits on the new continuous scene takes; preserve speech samples."""
import json,re,wave,subprocess,sys
from production_runtime import media_tool, portable_path, project_path, video_encoder_args
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
from synthesize import captions
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';A=P/'03_AUDIO/revision_02';Q=P/'09_REPORT/revision_02';FF=media_tool('ffmpeg');SR=48000
M=json.loads((A/'narration_manifest.json').read_text(encoding='utf8'));allwords=[];audio=[];cursor=0;edits=[]
for row in M['lines']:
 with wave.open(str(project_path(row['clean'])),'rb') as f:x=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()
 r=subprocess.run([FF,'-hide_banner','-i',str(project_path(row['clean'])),'-af','silencedetect=noise=-42dB:d=0.28','-f','null','-'],capture_output=True,text=True,check=True)
 spans=[];start=None
 for line in r.stderr.splitlines():
  if 'silence_start:' in line:start=float(line.split('silence_start:')[1].split()[0])
  elif 'silence_end:' in line and start is not None:
   end=float(line.split('silence_end:')[1].split()[0]);spans.append((start,end));start=None
 if start is not None:spans.append((start,len(x)/SR))
 # Alter only measured non-speech intervals. Keep at least 120ms at both word edges.
 cuts=[]
 for a,b in spans:
  duration=b-a
  if a<.025:keep=.035;cut=(0,max(0,b-keep))
  elif b>len(x)/SR-.025:keep=.10;cut=(a+keep,len(x)/SR)
  elif duration>.46:
   prior=[w for w in row['words'] if w['end']<=a+.09]
   punct=bool(prior and re.search(r'[.!?]["\x27)]*$',prior[-1]['text']))
   # Preserve natural variation; reduce excess rather than impose one pause length.
   keep=min(.42 if punct else .30,.24+(duration-.46)*.30)
   cut=(a+keep/2,b-keep/2)
  else:continue
  if cut[1]-cut[0]>.015:cuts.append(cut)
 def remap(t):return t-sum(max(0,min(t,b)-a) for a,b in cuts if t>a)
 pieces=[];last=0
 for a,b in cuts:
  ia,ib=round(a*SR),round(b*SR);pieces.append(x[last:ia]);last=ib
 pieces.append(x[last:]);y=np.concatenate(pieces)
 # Short fades occur in retained silence, never over speech phonemes.
 n=min(192,len(y)//2);y[:n]=(y[:n]*np.linspace(0,1,n)).astype(np.int16);y[-n:]=(y[-n:]*np.linspace(1,0,n)).astype(np.int16)
 dest=A/'voice_clean'/f"{row['id']}_connected.wav"
 with wave.open(str(dest),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes(y.tobytes())
 row['original_clean']=row['clean'];row['clean']=portable_path(dest);row['source_duration']=row['duration'];row['duration']=len(y)/SR;row['start']=cursor/SR;row['words']=[{**w,'start':round(remap(w['start']),6),'end':round(remap(w['end']),6)} for w in row['words']];row['end']=row['start']+row['duration']
 for w in row['words']:allwords.append({**w,'line_id':row['id'],'start':w['start']+row['start'],'end':w['end']+row['start']})
 audio.append(y);cursor+=len(y);edits.append({'section':row['id'],'removed_seconds':sum(b-a for a,b in cuts),'cuts_in_original_seconds':cuts,'speech_samples_processed':False})
 # No added fixed inter-scene gaps. Visual pauses, if needed, are explicit timeline events.
joined=np.concatenate(audio)
with wave.open(str(A/'connected_narration.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes(joined.tobytes())
M.update(duration=len(joined)/SR,audio=portable_path(A/'connected_narration.wav'),timing_source='Original word boundaries remapped through measured non-speech cuts')
(A/'connected_manifest.json').write_text(json.dumps(M,indent=2,ensure_ascii=False),encoding='utf8');(A/'connected.words.json').write_text(json.dumps(allwords,indent=2,ensure_ascii=False),encoding='utf8');(A/'connected.srt').write_text(captions(allwords),encoding='utf8');(Q/'voice_timing_edits.json').write_text(json.dumps(edits,indent=2),encoding='utf8');print('Connected narration:',len(joined)/SR,'seconds; removed:',sum(e['removed_seconds'] for e in edits),'seconds of measured silence')
