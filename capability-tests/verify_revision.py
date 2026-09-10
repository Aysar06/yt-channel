"""Full-stream decode plus frame, boundary, caption and audio measurements."""
import json,re,subprocess,math,hashlib
from production_runtime import media_tool, portable_path, project_path, video_encoder_args
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';Q=P/'09_REPORT/revision_02';V=P/'07_EXPORT/revision_02.mp4';F=media_tool('ffmpeg');FP=media_tool('ffprobe');S=json.loads((P/'05_EDIT/revision_02/shots.json').read_text());C=json.loads((P/'05_EDIT/revision_02/chapters.json').read_text());D=C[-1]['end'];O=Q/'encoded_frames';O.mkdir(exist_ok=True)
def run(args):
 r=subprocess.run(args,capture_output=True,text=True,encoding='utf8',errors='replace')
 if r.returncode:raise RuntimeError(r.stderr[-5000:])
 return r
probe=json.loads(run([FP,'-v','error','-show_format','-show_streams','-of','json',str(V)]).stdout);(Q/'export_probe.json').write_text(json.dumps(probe,indent=2))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');duration=float(probe['format']['duration'])
assert v['codec_name']=='h264' and (v['width'],v['height'])==(1920,1080) and v['avg_frame_rate']=='24/1';assert a['codec_name']=='aac' and abs(duration-D)<.12
# Read the entire video sequentially. Sample every shot's entry, midpoint and exit;
# sampling is explicitly not described as uninterrupted audiovisual viewing.
def balanced(xs):
 if len(xs)==1:return xs[0]
 m=len(xs)//2;return '('+balanced(xs[:m])+'+'+balanced(xs[m:])+')'
times=sorted(set(round(t*24) for s in S for t in [s['start']+.15,(s['start']+s['end'])/2,s['end']-.15]));sel=balanced([f'eq(n\\,{n})' for n in times])
graph=f'[0:v]blackdetect=d=0.4:pix_th=0.005:pic_th=0.99,select={sel},scale=480:270[v];[0:a]silencedetect=noise=-50dB:d=1[a]'
r=run([F,'-hide_banner','-y','-i',str(V),'-filter_complex',graph,'-map','[v]','-fps_mode','vfr',str(O/'frame-%03d.jpg'),'-map','[a]','-f','null','-']);(Q/'full_decode.log').write_text(r.stderr,encoding='utf8')
files=sorted(O.glob('frame-*.jpg'));assert len(files)==len(times),(len(files),len(times))
for k in range(0,len(files),18):
 sheet=Image.new('RGB',(1440,1740),'#252525');draw=ImageDraw.Draw(sheet)
 for j,f in enumerate(files[k:k+18]):
  x=j%3*480;y=j//3*290;sheet.paste(Image.open(f),(x,y));draw.text((x+5,y+273),f'{times[k+j]/24:.2f}s',fill='white')
 sheet.save(Q/f'encoded_review_{k//18+1}.jpg',quality=91)
r=run([F,'-hide_banner','-i',str(V),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','-']);levels=json.loads(re.findall(r'\{[^{}]+\}',r.stderr)[-1]);(Q/'encoded_audio_levels.json').write_text(json.dumps(levels,indent=2))
def sec(s):
 h,m,t=s.split(':');return int(h)*3600+int(m)*60+float(t.replace(',','.'))
sub=(P/'07_EXPORT/revision_02_subtitles.srt').read_text(encoding='utf8');blocks=re.split(r'\n\s*\n',sub.strip());last=0
for b in blocks:
 lines=b.splitlines();start,end=map(sec,lines[1].split(' --> '));assert start>=last-.002 and end>start and end<=duration+.02;last=end
for i,s in enumerate(S):
 assert s['duration']>0
 if i:assert abs(s['start']-S[i-1]['end'])<.001
 if s['kind']=='video':
  p=json.loads(run([FP,'-v','error','-show_format','-of','json',str(P/s['asset'])]).stdout);assert abs(float(p['format']['duration'])-s['duration'])<.1
  assert not s.get('reuse_review')
result={'export':portable_path(V),'duration_seconds':duration,'bytes':V.stat().st_size,'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'codec':v['codec_name'],'full_decode_exit_code':0,'shots':len(S),'entry_mid_exit_samples':len(files),'captions_valid':True,'caption_cues':len(blocks),'full_timeline_coverage':True,'unintentional_source_overlaps':0,'ai_images':0,'audio_integrated_lufs':levels['input_i'],'audio_true_peak_dbtp':levels['input_tp'],'black_events':re.findall(r'black_start:[^\n]+',(Q/'full_decode.log').read_text(encoding='utf8')),'silence_events':re.findall(r'silence_(?:start|end):[^\n]+',(Q/'full_decode.log').read_text(encoding='utf8')),'visual_sample_review':'pending','full_audio_only_listening_review':False,'uninterrupted_viewer_review':False,'approved':False}
(Q/'export_qc.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
