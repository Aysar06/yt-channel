import subprocess,json,re
from production_runtime import media_tool, portable_path, project_path, video_encoder_args
from pathlib import Path
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';A=P/'03_AUDIO/revision_02';W=A/'mix_work';W.mkdir(exist_ok=True);F=media_tool('ffmpeg')
C=json.loads((P/'05_EDIT/revision_02/chapters.json').read_text());S=json.loads((P/'05_EDIT/revision_02/shots.json').read_text());D=C[-1]['end']
def run(args):
 r=subprocess.run([F,'-hide_banner','-nostdin','-y',*args],capture_output=True,text=True,encoding='utf8',errors='replace');
 if r.returncode:raise RuntimeError(r.stderr[-4000:])
 return r.stderr
music=sorted((P/'03_AUDIO/music').glob('*.mp3'));parts=[]
for i,c in enumerate(C):
 p=W/f'music_{i:02d}.wav';parts.append(p);dur=c['duration'];cue=[0,0,1,2,1,0,0,1,0,2][i]
 run(['-ss',str((i%3)*40),'-i',str(music[cue]),'-t',str(dur),'-af',f'loudnorm=I=-29:TP=-8:LRA=9,afade=t=in:d=1.2,afade=t=out:st={dur-1.5}:d=1.5','-ar','48000','-ac','2',str(p)])
(W/'parts.txt').write_text('\n'.join("file '"+p.as_posix()+"'" for p in parts))
run(['-f','concat','-safe','0','-i',str(W/'parts.txt'),'-c','copy',str(W/'music.wav')])
inputs=['-i',str(A/'timeline_narration.wav'),'-i',str(W/'music.wav')];filters=['[0:a]highpass=f=65,asplit=2[voice][side]','[1:a][side]sidechaincompress=threshold=0.015:ratio=5:attack=12:release=380[bed]'];labels=['[voice]','[bed]'];n=2
for s in S:
 if s['kind']=='video' and s['source']=='I5IogZtvJyI':
  p=W/(s['id']+'_ambience.wav');run(['-ss',str(s['source_in']),'-i',str(P/'04_MEDIA/video/I5IogZtvJyI.mp4'),'-t',str(s['duration']),'-vn','-af',f'loudnorm=I=-34:TP=-9:LRA=8,afade=t=in:d=0.12,afade=t=out:st={s["duration"]-.18}:d=0.18','-ar','48000','-ac','2',str(p)])
  inputs+=['-i',str(p)];filters.append(f'[{n}:a]adelay={round(s["start"]*1000)}:all=1[a{n}]');labels.append(f'[a{n}]');n+=1
inputs+=['-i',str(P/'03_AUDIO/sfx/archive-click.wav')];filters.append(f'[{n}:a]volume=0.35,adelay=3500:all=1[click]');labels+=['[click]']
filters.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=first:normalize=0,alimiter=limit=0.84:level=0[mix]')
run(inputs+['-filter_complex',';'.join(filters),'-map','[mix]','-t',str(D),'-ar','48000','-ac','2',str(A/'final_mix.wav')])
r=run(['-i',str(A/'final_mix.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']);(P/'09_REPORT/revision_02/audio_levels.json').write_text(re.findall(r'\{[^{}]+\}',r)[-1]);print('Revision audio mixed:',D,'seconds')


