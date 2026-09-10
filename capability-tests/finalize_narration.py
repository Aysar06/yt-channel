import json,shutil,csv
from pathlib import Path
root=Path(__file__).resolve().parent.parent;p=root/'VIDEO_PROJECT'
m=json.loads((p/'03_AUDIO/narration_manifest.json').read_text(encoding='utf8'))
c=json.loads((p/'02_SCRIPT/chapters.json').read_text(encoding='utf8'))
lookup={l['id']:l for l in m['lines']}
for ch in c:
    ch['start']=lookup[ch['line_ids'][0]]['start'];ch['end']=lookup[ch['line_ids'][-1]]['end']
(p/'05_EDIT/project_files/chapter_timing.json').write_text(json.dumps(c,indent=2),encoding='utf8')
with (p/'05_EDIT/project_files/narration_timeline.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.writer(f);w.writerow(['id','start','end','narration']);w.writerows((l['id'],l['start'],l['end'],l['text']) for l in m['lines'])
shutil.copyfile(p/'03_AUDIO/narration.srt',p/'05_EDIT/subtitles/narration.srt')
summary={'duration_seconds':m['duration'],'paragraphs':len(m['lines']),'word_boundary_count':sum(len(l['words']) for l in m['lines']),'minimum_punctuation_match':min(l['punctuation_match'] for l in m['lines']),'status':'Narration and TTS-timed subtitles generated. Full listening review and final edit synchronization pending.'}
(p/'09_REPORT/narration_checkpoint.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(summary))
