"""Build a restrained licensed score with speech-driven ducking and original SFX."""
import json,subprocess,re
from pathlib import Path
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';F=str(R/'tools/ffmpeg/bin/ffmpeg.exe')
C=json.loads((P/'05_EDIT/project_files/chapter_timing.json').read_text());D=C[-1]['end'];out=P/'03_AUDIO';tmp=out/'mix_work';tmp.mkdir(exist_ok=True)
def run(args):
 r=subprocess.run([F,'-hide_banner','-nostdin','-y',*args],capture_output=True,text=True,encoding='utf8',errors='replace');
 if r.returncode:raise RuntimeError(r.stderr[-3000:])
 return r.stderr
music=list(sorted((out/'music').glob('*.mp3')));choice=[0,1,0,1,1,2,0,2,0,1,2,2]
parts=[]
for i,c in enumerate(C):
 end=C[i+1]['start'] if i+1<len(C) else D;dur=end-c['start'];p=tmp/f'{i:02d}.wav';parts.append(p)
 # Reposition within full tracks; change cue per chapter with gentle fades.
 run(['-ss',str((i%3)*35),'-i',str(music[choice[i]]),'-t',str(dur),'-af',f'loudnorm=I=-27:TP=-6:LRA=9,afade=t=in:d=1.5,afade=t=out:st={max(0,dur-2)}:d=2','-ar','48000','-ac','2',str(p)])
concat=tmp/'parts.txt';concat.write_text('\n'.join("file '"+p.as_posix()+"'" for p in parts))
run(['-f','concat','-safe','0','-i',str(concat),'-c','copy',str(tmp/'music_bed.wav')])
inputs=['-i',str(out/'narration.wav'),'-i',str(tmp/'music_bed.wav')]
sfx=[('low-door-hit',0),('archive-click',C[1]['start']),('low-door-hit',C[5]['start']),('soft-page-sweep',C[6]['start']),('quiet-discovery',C[8]['start'])]
filters=['[0:a]asplit=2[voice][side]','[1:a][side]sidechaincompress=threshold=0.018:ratio=5:attack=8:release=700[duck]']
labels=['[voice]','[duck]']
for i,(name,t) in enumerate(sfx,2):
 inputs+=['-i',str(out/f'sfx/{name}.wav')];filters.append(f'[{i}:a]adelay={round(t*1000)}:all=1[fx{i}]');labels.append(f'[fx{i}]')
filters.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=first:normalize=0,alimiter=limit=0.84:level=0[mix]')
run(inputs+['-filter_complex',';'.join(filters),'-map','[mix]','-ar','48000','-ac','2',str(out/'final_mix.wav')])
report=run(['-i',str(out/'final_mix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','NUL'])
(P/'09_REPORT/audio_levels.json').write_text(re.findall(r'\{[^{}]+\}',report)[-1]);print('Mixed licensed score, speech ducking and 5 restrained SFX cues.')
