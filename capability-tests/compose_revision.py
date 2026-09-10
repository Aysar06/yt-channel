"""Author revision 02: finite real footage, native evidence pages, subject-specific diagrams."""
import json,html,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';E=P/'05_EDIT/revision_02';C=P/'compositions/revision_02';A=P/'04_MEDIA/evidence'
S=json.loads((E/'shots.json').read_text(encoding='utf8'));CH=json.loads((E/'chapters.json').read_text());D=CH[-1]['end']
Image.open(A/'reveal_99.jpg').crop((0,0,1920,865)).save(A/'disclaimer.jpg',quality=98)
im=Image.open(A/'cancel_quote.png');im.crop((0,63,im.width,163)).save(A/'cancel_statement.png')
CSS='''*{box-sizing:border-box;margin:0}#root{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:Arial,sans-serif;color:#18232b}.shot{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}.footage{object-fit:contain;background:#090b09}.photo{position:absolute;object-fit:contain}.note{position:absolute;padding:14px 24px;font-size:30px;background:#f8f8f2;color:#17252b;max-width:1700px}.label{font-size:38px}.disk{position:absolute;width:550px;height:610px;background:linear-gradient(135deg,#647783,#27353c);border:9px solid #a4b1b8;border-radius:22px;box-shadow:18px 30px 35px #06121e55}.platter{position:absolute;width:375px;height:375px;border:40px solid #c6cfd2;border-radius:50%;left:78px;top:105px;background:radial-gradient(circle,#44565e 0 18%,#9ba8ad 19% 20%,#d1d7d8 21% 40%,#aeb9bc 41% 70%)}.drive-label{position:absolute;top:32px;left:34px;font-size:32px;color:#fff}.drive-tile{position:absolute;left:165px;top:215px;width:205px;height:205px;object-fit:cover;border:4px solid #f6f6ec}.screw{position:absolute;width:17px;height:17px;border:4px solid #ccd5d8;border-radius:50%}.page{position:absolute;object-fit:contain}.control{position:absolute;border:3px solid #9aafb8;background:#f8fafb;padding:24px;font-size:38px}.arrow{position:absolute;width:190px;height:6px;background:#94adbb}.arrow:after{content:'';position:absolute;right:-2px;top:-11px;border-left:24px solid #94adbb;border-top:14px solid transparent;border-bottom:14px solid transparent}.calendar{position:absolute;background:#fffdf5;width:420px;height:465px;box-shadow:14px 19px 0 #cad4d1;border-radius:8px;text-align:center;top:300px}.month{padding:28px;background:#245d66;color:white;font-size:42px}.day{font-family:Georgia,serif;font-size:160px;line-height:1.3}.event{font-size:30px;padding:0 22px}.path{fill:none;stroke:#51b4d7;stroke-width:8;stroke-linecap:round}.branch{fill:none;stroke:#d9c583;stroke-width:7;stroke-linecap:round}'''
PT='04_MEDIA/images/official_psblog_pt.jpg';ERR='04_MEDIA/images/gs_download_error.jpg';TITLE='04_MEDIA/evidence/silent_hills_title.jpg'
def img(src,x,y,w,h,id='',cl='photo',extra=''):
 return f'<img class="{cl}" '+(f'id="{id}" ' if id else '')+f'src="{src}" alt="Original source imagery" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{extra}">'
def ev(name,x,y,w,h,id=''):return img('04_MEDIA/evidence/'+name+'.png',x,y,w,h,id)
def text(t,x,y,size=38,color='',id='',extra=''):
 return f'<div '+(f'id="{id}" ' if id else '')+f'style="position:absolute;left:{x}px;top:{y}px;font-size:{size}px;'+(f'color:{color};' if color else '')+extra+'">'+t+'</div>'
def disk(id,x,y,label,tile=True):
 return f'<div class="disk" id="{id}" style="left:{x}px;top:{y}px"><div class="drive-label">{label}</div><div class="platter"></div>'+(''.join(f'<i class="screw" style="left:{a}px;top:{b}px"></i>' for a,b in [(15,15),(499,15),(15,558),(499,558)]))+ (f'<img id="{id}-tile" class="drive-tile" src="{PT}" alt="P.T. installation symbol">' if tile else '')+'</div>'
def compose(s):
 id=s['id'];start=s['start_local'];dur=s['duration'];k=s['kind'];js=[];initialized=set()
 def anim(sel,a,b,t,length=.65,ease='power2.inOut'):
  if sel not in initialized:
   js.append(f'tl.set("#{id}{sel}",{json.dumps(a)},0);');initialized.add(sel)
  js.append(f'tl.fromTo("#{id}{sel}",{json.dumps(a)},'+json.dumps({**b,'duration':length,'ease':ease,'immediateRender':False})+f',{start+t:.6f});')
 def show(sel,t):anim(sel,{'opacity':0},{'opacity':1},t,.25)
 bg='#edf0eb';body=''
 if k=='video':
  markup=f'<video id="{id}" class="clip shot footage" src="{s["asset"]}" data-start="{start:.6f}" data-duration="{dur:.6f}" data-track-index="1" muted playsinline preload="auto"></video>'
  if s.get('identify'):markup+=f'<div id="{id}-id" class="clip note" data-start="{start+.35:.6f}" data-duration="3.2" data-track-index="3" style="top:62px;left:70px">{html.escape(s["identify"])}</div>'
  return markup,js
 if k=='storage':
  bg='#124b7a';body=text('System storage',155,110,52,'#fff')+text('Applications',155,210,35,'#c9e2f4')
  for n in range(4):body+=f'<div style="position:absolute;left:{155+n*410}px;top:315px;width:360px;height:360px;border:3px solid #73a8c7;background:#{["183e56","285e78","255b79","2c6580"][n]}"></div>'
  body+=img(PT,165,325,340,340,id+'-tile','photo','object-fit:cover')+f'<div id="{id}-select" style="position:absolute;left:143px;top:303px;width:384px;height:384px;border:7px solid white"></div>'+text('Delete',195,760,47,'#fff',id+'-delete')+f'<div id="{id}-bar" style="position:absolute;left:155px;top:922px;height:14px;width:1180px;background:#95dff0"></div>'+text('Illustrated storage decision',1350,944,25,'#d5e8f1',id+'-explain')
  anim('-tile',{'opacity':1,'scale':1},{'opacity':0,'scale':.85},3.5,.35);anim('-select',{'opacity':1},{'opacity':0},3.5,.2);anim('-delete',{'opacity':1},{'opacity':0},3.5,.2);anim('-bar',{'scaleX':1},{'scaleX':.82},3.5,.7);anim('-explain',{'opacity':1},{'opacity':0},2.8,.3)
 elif k=='error':
  bg='#073971';body=img(ERR,0,0,1920,1080,id+'-screen');anim('-screen',{'scale':1,'x':0,'y':0},{'scale':1.9,'x':864,'y':350},3,1.1);anim('-screen',{'scale':1.9,'x':864,'y':350},{'scale':1.2,'x':192,'y':108},max(6,dur-4),1)
 elif k=='installed':
  bg='#e4ecef';body=disk(id+'-a',240,230,'Installed copy')+disk(id+'-b',1120,230,'Empty drive',False)+text('▶',440,890,67,'#24606b',id+'-play')+text('↻',1340,880,75,'#81919a',id+'-retry');show('-play',1);anim('-retry',{'rotation':0},{'rotation':240},3,1.2);anim('-retry',{'opacity':1},{'opacity':.25},4.2,.4)
 elif k=='poster':
  bg='#263a2c';body=img(PT,0,0,1920,1080,id+'-poster','photo','object-fit:cover');anim('-poster',{'scale':1.04},{'scale':1},0,min(dur,5),'none')
 elif k=='web':
  focus=s['focus'];bg='#181a1b'
  if focus=='tips':
   bg='#080909';body=ev('tips_head',65,90,660,900)+ev('tips_body',800,230,1040,610,id+'-body');show('-body',3)
  elif focus=='discussion':
   bg='#f5f5f5';body=ev('discussion_head',110,180,1700,330)+ev('discussion_body',440,530,1040,540,id+'-body');show('-body',2.5)
  elif focus=='cancel':
   body=ev('cancel_native',160,50,1600,1954,id+'-article');anim('-article',{'y':0},{'y':-1120},6.2,1.4)
  elif focus=='distribution':body=ev('distribution',200,60,1460,1520,id+'-article');anim('-article',{'y':0},{'y':-430},1.3,1.2)
  elif focus=='gamespot':
   bg='#fff';body=ev('gamespot_head',120,150,1680,310)+ev('gamespot_body',380,490,1160,490,id+'-body');show('-body',2.4)
  elif focus=='forum':
   bg='#f2f3ee';body=ev('forum',50,100,1820,950,id+'-full')+ev('forum_post',65,300,1790,540,id+'-post');anim('-full',{'opacity':1},{'opacity':0},7,.3);show('-post',7.2);anim('-post',{'scale':1,'y':0},{'scale':1.055,'y':-28},10,1.2)
  elif focus=='ps5':body=ev('ps5_head',120,75,1100,980)+ev('ps5_body',1130,300,710,400,id+'-body');show('-body',5)
 elif k=='disclaimer':
  bg='#e7e8e6';body=img('04_MEDIA/evidence/disclaimer.jpg',0,0,1920,1080,id+'-source');anim('-source',{'scale':1},{'scale':3.1},1,1.4);anim('-source',{'scale':3.1},{'scale':1.5},dur-2.8,1.1)
 elif k=='two_works':
  if s.get('editorial'):
   bg='#e8ece7';body=img(TITLE,0,0,1920,1080,id+'-future')+img(PT,0,0,1920,1080,id+'-actual','photo','object-fit:cover');show('-actual',10.7);anim('-future',{'opacity':1},{'opacity':0},10.7,.5)
  elif s.get('cancel'):
   body=img(TITLE,70,155,1040,670,id+'-future')+ev('cancel_statement',1030,380,790,300)+text('27 April 2015',1070,735,36,'#49626c');anim('-future',{'opacity':1},{'opacity':.35},2,.7)
  else:
   body=img(PT,100,125,770,680,'','photo','object-fit:cover')+img(TITLE,960,125,850,680)+text('The playable teaser',150,855,43)+text('The announced project',1030,855,43)
 elif k=='calendar':
  bg='#e8eeec'
  for i,(m,d,e) in enumerate([('APRIL 2015','27','Project cancelled'),('APRIL 2015','29','Distribution ends'),('MAY 2015','6','Re-download failure reported')]):
   body+=f'<div id="{id}-d{i}" class="calendar" style="left:{210+i*550}px"><div class="month">{m}</div><div class="day">{d}</div><div class="event">{e}</div></div>'
   if i:show('-d'+str(i),[0,1.8,7][i])
 elif k=='network' and not s.get('historical'):
  bg='#113b60';body=img(PT,130,140,415,350,'','photo','object-fit:cover')+text('Library',130,535,44,'#fff')+f'<div class="control" style="left:790px;top:235px;width:345px">Download</div>'+disk(id+'-drive',1320,215,'Local installation')+text('Already installed',1270,910,38,'#fff')
  body+=f'<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0"><path id="{id}-route" class="path" d="M565 310 H755 M1160 310 H1290" pathLength="1"/><path id="{id}-break" d="M938 372 l55 55 m0 -55 l-55 55" stroke="#f3bf75" stroke-width="9"/></svg>'
  anim('-route',{'strokeDasharray':1,'strokeDashoffset':1},{'strokeDashoffset':0},1,1.4,'none');show('-break',4);anim('-drive-tile',{'scale':1},{'scale':1.18},dur-6,.7)
 elif k=='network':
  bg='#181a1b';body=ev('ps5_ui',0,0,1920,1080)+ev('ps5_decision',260,750,1400,280,id+'-decision');show('-decision',2)
 elif k=='drive':
  if s.get('swap'):
   bg='#dcdad0';body=disk(id+'-old',250,220,'Old drive')+disk(id+'-new',1120,220,'Replacement',False)+f'<div id="{id}-arrow" class="arrow" style="left:830px;top:545px"></div>';anim('-old',{'x':0},{'x':-160},2.5,1);anim('-new',{'x':160,'opacity':.2},{'x':0,'opacity':1},3,1);show('-arrow',2)
  else:
   bg='#dce7e9';body=disk(id+'-only',660,230,'One surviving installation');anim('-only',{'scale':.95},{'scale':1.1},0,dur-1,'none')
 elif k=='choice':
  bg='#273634';body=img('04_MEDIA/images/silent_hills_pt_screen_20140821_02.jpg',90,180,740,680,'','photo','object-fit:cover')+text('A recorded viewpoint',120,865,38,'#eef3e9')+text('A choice of viewpoints',1030,865,38,'#eef3e9')
  body+=f'<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0"><circle cx="1320" cy="680" r="42" fill="#ebe7cc"/><path id="{id}-p1" class="branch" d="M1320 628 V355 L1080 215" pathLength="1"/><path id="{id}-p2" class="branch" d="M1320 355 L1550 215" pathLength="1"/><path id="{id}-p3" class="branch" d="M1320 355 V150" pathLength="1"/></svg>'
  for n in range(1,4):anim('-p'+str(n),{'strokeDasharray':1,'strokeDashoffset':1},{'strokeDashoffset':0},1+n*.7,1,'none')
 elif k=='compatibility':
  bg='#e6e9e5';body=text('Review hardware · 2020',170,120,38,'#42535b')+text('P.T.',170,430,135)+text('PS4',720,430,115)+text('PS5',1410,430,115,id=id+'-ps5')+f'<div class="arrow" style="left:410px;top:506px"></div><div id="{id}-route" class="arrow" style="left:1120px;top:506px"></div>'+f'<div id="{id}-status" class="control" style="left:620px;top:690px;width:690px;text-align:center">Playable on PS4</div>'
  anim('-route',{'opacity':1},{'opacity':0},2.6,.45);anim('-ps5',{'opacity':1},{'opacity':.25},2.6,.45);show('-status',2.8)
 return f'<section id="{id}" class="clip shot" data-start="{start:.6f}" data-duration="{dur:.6f}" data-track-index="1" style="background:{bg}">{body}</section>',js

for ch in CH:
 markup=[];motion=[]
 for s in S:
  if s['chapter']==ch['id']:
   m,j=compose(s);markup.append(m);motion+=j
 body=f'<!doctype html><html><body><template><style>{CSS}</style><div id="root" data-composition-id="{ch["id"]}" data-start="0" data-duration="{ch["duration"]:.6f}" data-width="1920" data-height="1080">'+''.join(markup)+'</div><script>const tl=gsap.timeline({paused:true});'+''.join(motion)+f'window.__timelines["{ch["id"]}"]=tl;</script></template></body></html>'
 (C/(ch['id']+'.html')).write_text(body,encoding='utf8')
root='<!doctype html><html lang="en"><head><meta charset="UTF-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{margin:0;box-sizing:border-box}html,body,#root{width:1920px;height:1080px;overflow:hidden}#root{position:relative;background:#152c37}.clip[data-composition-src]{position:absolute;inset:0}</style></head><body>'+f'<div id="root" data-composition-id="pt-revision-02" data-start="0" data-duration="{D:.6f}" data-width="1920" data-height="1080" data-fps="24">'
for ch in CH:root+=f'<div id="slot-{ch["id"]}" class="clip" data-composition-id="{ch["id"]}" data-composition-src="compositions/revision_02/{ch["id"]}.html" data-width="1920" data-height="1080" data-start="{ch["start"]:.6f}" data-duration="{ch["duration"]:.6f}" data-track-index="1"></div>'
root+=f'<audio id="final-mix-v2" src="03_AUDIO/revision_02/final_mix.wav" data-start="0" data-duration="{D:.6f}" data-track-index="10" data-volume="1"></audio></div><script>window.__timelines=window.__timelines||{{}};window.__timelines["pt-revision-02"]=gsap.timeline({{paused:true}});</script></body></html>'
(P/'index.html').write_text(root,encoding='utf8')
(P/'STORYBOARD.md').write_text('# Revision 02 — sourced footage and evidence\n\nNo permanent identifiers. No AI imagery. Finite excerpts at original speed.\n\n'+'\n'.join(f'## {c["id"]} — {c["title"]}\n\n'+ '\n'.join(f'- {s["start"]:.2f}–{s["end"]:.2f}: {s["kind"]}. {s["purpose"]}' for s in S if s['chapter']==c['id'])+'\n' for c in CH),encoding='utf8')
print('Authored',len(CH),'new chapter compositions;',D,'seconds')
