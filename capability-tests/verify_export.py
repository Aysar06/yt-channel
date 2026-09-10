import json,re,subprocess,math
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';Q=P/'09_REPORT';V=P/'07_EXPORT/final_video.mp4';FF=str(R/'tools/ffmpeg/bin/ffmpeg.exe');FP=str(R/'tools/ffmpeg/bin/ffprobe.exe')
def run(args):
 r=subprocess.run(args,capture_output=True,text=True,encoding='utf8',errors='replace')
 if r.returncode:print(r.stderr[-6000:]);r.check_returncode()
 return r
probe=json.loads(run([FP,'-v','error','-show_format','-show_streams','-of','json',str(V)]).stdout)
(Q/'export_probe.json').write_text(json.dumps(probe,indent=2),encoding='utf8')
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');duration=float(probe['format']['duration'])
assert v['codec_name']=='h264' and (v['width'],v['height'])==(1920,1080) and v['avg_frame_rate']=='24/1'
assert a['codec_name']=='aac' and abs(duration-831.246)<.1
T=json.loads((P/'05_EDIT/project_files/visual_timeline.json').read_text(encoding='utf8'));O=Q/'encoded_shots';O.mkdir(exist_ok=True)
frames=[round((s['start']+s['end'])/2*24) for s in T]
def balanced(items):
 if len(items)==1:return items[0]
 m=len(items)//2;return '('+balanced(items[:m])+'+'+balanced(items[m:])+')'
selection=balanced([f'eq(n\\,{f})' for f in frames])
graph=f'[0:v]blackdetect=d=0.4:pix_th=0.005:pic_th=0.99,select={selection},scale=400:225[v];[0:a]silencedetect=noise=-50dB:d=1[a]'
if not (Q/'full_decode.log').exists() or len(list(O.glob('shot-*.jpg')))!=len(T):
 r=run([FF,'-hide_banner','-y','-i',str(V),'-filter_complex',graph,'-map','[v]','-fps_mode','vfr',str(O/'shot-%03d.jpg'),'-map','[a]','-f','null','NUL'])
 (Q/'full_decode.log').write_text(r.stderr,encoding='utf8')
shots=sorted(O.glob('shot-*.jpg'));assert len(shots)==len(T),(len(shots),len(T))
for group in range(math.ceil(len(shots)/20)):
 im=Image.new('RGB',(1640,1265),'#242424');draw=ImageDraw.Draw(im)
 for j in range(20):
  n=group*20+j
  if n>=len(shots):break
  x=10+j%4*410;y=10+j//4*250;im.paste(Image.open(shots[n]),(x,y));draw.text((x,y+229),f"{n+1:03} / {(T[n]['start']+T[n]['end'])/2:.1f}s / {T[n]['kind']}",fill='white')
 im.save(Q/f'encoded_contact_{group+1}.jpg',quality=90)
r=run([FF,'-hide_banner','-i',str(V),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-f','null','NUL'])
audio=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])[0];(Q/'encoded_audio_levels.json').write_text(json.dumps(audio,indent=2),encoding='utf8')
srt=(P/'07_EXPORT/final_subtitles.srt').read_text(encoding='utf8');blocks=re.split(r'\n\s*\n',srt.strip());prev=0
def sec(s):
 h,m,t=s.split(':');return int(h)*3600+int(m)*60+float(t.replace(',','.'))
for b in blocks:
 line=b.splitlines();start,end=map(sec,line[1].split(' --> '));assert start>=prev-.002 and end>start and end<=duration+.01;prev=end
assert not re.search(r'\[(?:pause|whisper|excited|serious)',srt,re.I)
result={'duration_seconds':duration,'video':{'codec':v['codec_name'],'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'pixel_format':v.get('pix_fmt'),'bit_rate':v.get('bit_rate')},'audio':{'codec':a['codec_name'],'sample_rate':a['sample_rate'],'channels':a['channels'],'integrated_lufs':float(audio['input_i']),'true_peak_dbtp':float(audio['input_tp'])},'full_decode_exit_code':0,'sampled_shots':len(shots),'subtitle_cues':len(blocks),'subtitle_timing_valid':True,'black_events':re.findall(r'black_start:[^\n]+',(Q/'full_decode.log').read_text(encoding='utf8')),'silence_events':re.findall(r'silence_(?:start|end):[^\n]+',(Q/'full_decode.log').read_text(encoding='utf8')),'contact_sheet_visual_review':'pending','human_listening_review':False,'file_bytes':V.stat().st_size}
(Q/'export_qc.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
