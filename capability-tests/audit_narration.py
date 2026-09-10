import json,re,difflib,time
from pathlib import Path
from faster_whisper import WhisperModel
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT'
model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4)
segments,info=model.transcribe(str(P/'03_AUDIO/narration.wav'),beam_size=3,language='en',vad_filter=True)
rows=[]
for s in segments:
 rows.append({'start':s.start,'end':s.end,'text':s.text,'average_log_probability':s.avg_logprob})
(P/'09_REPORT/asr_full.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
def norm(t):return re.findall(r'[a-z0-9]+',t.lower())
M=json.loads((P/'03_AUDIO/narration_manifest.json').read_text());reference=norm(' '.join(x['text'] for x in M['lines']));observed=norm(' '.join(x['text'] for x in rows));score=difflib.SequenceMatcher(a=reference,b=observed,autojunk=False).ratio()
report={'coverage':'Full narration processed with independent local ASR; not a human listening review.','model':'faster-whisper small.en / CPU int8','source_tokens':len(reference),'asr_tokens':len(observed),'token_sequence_similarity':score,'review_segments':[x for x in rows if x['average_log_probability']<-.6]}
(P/'09_REPORT/asr_audit.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('Full ASR completed. Token sequence similarity:',round(score,4))
