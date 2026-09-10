from pathlib import Path
import subprocess,json,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';V=P/'04_MEDIA/video';Q=P/'09_REPORT/revision_02/source_sheets';Q.mkdir(exist_ok=True,parents=True);FF=str(R/'tools/ffmpeg/bin/ffmpeg.exe')
for vid,step in [('I5IogZtvJyI',15),('ByNhd5SoSU8',5),('VYI-maF6xMI',5),('zAQlWpcs8nE',15)]:
 d=json.loads((V/f'{vid}.info.json').read_text(encoding='utf8'));dest=Q/vid;dest.mkdir(exist_ok=True)
 subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-i',str(V/f'{vid}.mp4'),'-vf',f'fps=1/{step},scale=320:180','-q:v','3',str(dest/'%04d.jpg')],check=True)
 frames=sorted(dest.glob('*.jpg'))
 for g in range(math.ceil(len(frames)/24)):
  im=Image.new('RGB',(1320,1240),'#333333');dr=ImageDraw.Draw(im)
  for j in range(24):
   n=g*24+j
   if n>=len(frames):break
   x=10+(j%4)*330;y=10+(j//4)*205;im.paste(Image.open(frames[n]),(x,y));dr.text((x,y+182),f'{vid} | ~{(n+.5)*step:.1f}s',fill='white')
  im.save(Q/f'{vid}_{g+1}.jpg',quality=90)
 print(vid,d['duration'],'seconds;',len(frames),'inspection frames',flush=True)
