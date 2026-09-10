import json,re,difflib
from pathlib import Path
from faster_whisper import WhisperModel
P=Path(__file__).resolve().parent.parent/'VIDEO_PROJECT';Q=P/'09_REPORT/revision_02';model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4)
segments,info=model.transcribe(str(P/'03_AUDIO/revision_02/timeline_narration.wav'),beam_size=3,language='en',vad_filter=True)
rows=[{'start':s.start,'end':s.end,'text':s.text,'average_log_probability':s.avg_logprob} for s in segments];(Q/'asr_full.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
def norm(t):return re.findall('[a-z0-9]+',t.lower())
j=json.loads((P/'02_SCRIPT/revision_02_request.json').read_text(encoding='utf8'));a=norm(' '.join(x['text'] for x in j['lines']));b=norm(' '.join(x['text'] for x in rows));m=difflib.SequenceMatcher(a=a,b=b,autojunk=False)
report={'coverage':'Entire new narration independently transcribed. This is an automated intelligibility check, not an auditory review.','similarity':m.ratio(),'source_tokens':len(a),'observed_tokens':len(b),'differences':[{'expected':' '.join(a[i:j]),'observed':' '.join(b[k:l])} for op,i,j,k,l in m.get_opcodes() if op!='equal'],'low_confidence':[r for r in rows if r['average_log_probability']<-.6]};(Q/'asr_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('ASR similarity',report['similarity'])
