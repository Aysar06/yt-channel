"""Build the sourced P.T. edit, its storyboard and portable metadata."""
import json,math,html,csv,shutil
from pathlib import Path
R=Path(__file__).resolve().parent.parent; P=R/'VIDEO_PROJECT'
M=json.loads((P/'03_AUDIO/narration_manifest.json').read_text(encoding='utf8'))
C=json.loads((P/'05_EDIT/project_files/chapter_timing.json').read_text(encoding='utf8'))
L={x['id']:x for x in M['lines']};D=M['duration'];E=html.escape
(P/'compositions').mkdir(exist_ok=True)
def pic(n,early=False):
    prefix='silent_hills_pt_screen_20140814_' if early else 'silent_hills_pt_screen_20140821_'
    return next((P/'04_MEDIA/images').glob(prefix+f'{n:02d}*.jpg')).relative_to(P).as_posix()
groups=[[pic(2),pic(3),pic(7)], [pic(1),pic(2),pic(3),pic(4),pic(6)], [pic(7),pic(8),pic(29),pic(6),pic(23)],
 [pic(9),pic(13),pic(15),pic(19),pic(28),pic(10)], [pic(7,True),pic(6,True),pic(8,True),pic(24)],
 [pic(8,True),pic(7,True),pic(1),pic(3)], [pic(1),pic(27),pic(21),pic(4)], [pic(23),pic(7),pic(2),pic(29)],
 [pic(34),pic(35),pic(30),pic(31),pic(33)], [pic(3),pic(23),pic(1),pic(26)],
 [pic(6),pic(28),pic(9),pic(7,True),pic(21)], [pic(2),pic(3),pic(23),pic(1)]]
# Each special is tied to a paragraph whose narration directly discusses it.
special={
 'c01p01':('photo','04_MEDIA/images/gs_download_error.jpg','THE DOWNLOAD IS GONE','GameSpot / PS4 test / 6 May 2015'),
 'c01p02':('title','P.T.','A HALLWAY YOU COULD LOSE'),
 'c02p01':('title','12 AUG 2014','7780s Studio / PlayStation 4'),
 'c03p01':('loop','SAME CORRIDOR.','DIFFERENT RULES.'),
 'c04p02':('quote','Have You Finished The Silent Hills Playable Teaser, P.T.?','Game Informer reader discussion / 16 Aug 2014'),
 'c04p04':('title','ONE WEEK?','Solved within hours / reported at Gamescom 2014'),
 'c05p01':('title','SILENT HILLS','Hideo Kojima · Guillermo del Toro · Norman Reedus'),
 'c05p03':('quote','no direct relation to the main title','P.T. ending disclaimer / reported by Gematsu, 12 Aug 2014'),
 'c06p01':('quote','will not be continued','Konami statement / via Gematsu / 27 Apr 2015'),
 'c06p03':('title','SILENT HILLS','That project ends. The series continues.'),
 'c07p01':('dates','27 APR / 29 APR / 6 MAY','Cancellation / Distribution ends / Re-download failure reported'),
 'c07p02':('photo','04_MEDIA/images/gs_download_error.jpg','CANNOT DOWNLOAD','GameSpot / tested on PS4 / 6 May 2015'),
 'c07p04':('compare','STILL INSTALLED','NO NORMAL RE-DOWNLOAD'),
 'c08p01':('quote','I had the P.T. demo installed on my PS4 until recently when I upgraded my harddrive to a bigger one','Firehawk030 / GameFAQs PS4 discussion / personal account'),
 'c08p03':('compare','WATCHING','PLAYING'),
 'c09p01':('camera','THE PLAYER','THE VIEWPOINT'),
 'c09p02':('camera','AFTER THE FLASHLIGHT','Lisa follows behind the player'),
 'c09p04':('title','2019','A new discovery in old software'),
 'c10p01':('title','2020','PS5 review hardware: first playable, then blocked'),
 'c10p02':('quote','was a publisher decision','Sony statement / reported by Polygon; via Gematsu / 6 Nov 2020'),
 'c11p01':('compare','P.T. / RELEASED','SILENT HILLS / CANCELLED'),
 'c12p02':('title','IT STILL EXISTED.','That did not mean everyone could reach it.'),
 'c12p04':('compare','THE RECORDING','THE CONTROLLER')}
css='''*{box-sizing:border-box;margin:0}#root{position:relative;width:1920px;height:1080px;overflow:hidden;color:#F2EBD9;font-family:"IBM Plex Mono",monospace}.shot{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden}.fill{position:absolute;inset:0;background:#11150F}.photo{position:absolute;width:1920px;height:1080px;object-fit:cover}.contain{object-fit:contain;width:1500px;height:830px;left:210px;top:95px}.credit{position:absolute;bottom:38px;left:80px;font-size:24px;padding:10px 16px;background:#11150F;color:#F2EBD9;max-width:1760px}.label{position:absolute;top:56px;left:80px;padding:10px 16px;background:#11150F;font-size:25px;color:#F2EBD9}.stage{position:absolute;inset:0;padding:160px 130px 155px;display:flex;flex-direction:column;justify-content:center;gap:32px}.display{font-family:"League Gothic",sans-serif;font-size:156px;font-weight:400;line-height:1;max-width:1620px}.accent{color:#E84C3D}.support{font-size:36px;line-height:1.45;max-width:1530px}.rule{width:210px;height:8px;background:#E84C3D;transform-origin:left}.paper{background:#F2EBD9;color:#11150F}.paper .label{background:#F2EBD9;color:#11150F}.paper .credit{background:#F2EBD9;color:#11150F}.quotation{font-family:"League Gothic",sans-serif;font-size:110px;line-height:1.06;max-width:1550px}.twocol{display:flex;gap:90px;width:1620px}.col{flex:1;min-width:0;padding:34px 0;border-top:8px solid #E84C3D}.col .display{font-size:100px;line-height:1.05}.schematic{width:1450px;height:520px;display:block}.small{font-size:28px;line-height:1.4;color:#F2EBD9}.date{font-family:"League Gothic";font-size:105px}.date-item{width:30%}.motion{will-change:transform}'''
timeline=[];boards=['# P.T. — sourced documentary storyboard\n\nActual narration: %.3f seconds. No AI images. Transitions are hard cuts unless noted.\n'%D];slots=[]
for ci,ch in enumerate(C):
    sid=f'ch{ci+1:02d}';start=ch['start'];end=C[ci+1]['start'] if ci+1<len(C) else D;duration=end-start
    content=[];anim=[];localshots=[]
    boards.append(f'## Frame {ci+1}\nstatus: animated\nsrc: compositions/{sid}.html\nduration: {duration:.3f}\nrules: multi-phase-camera, svg-path-draw, kinetic-beat-slam\n\n{ch["title"]}: authentic stills and source receipts. Photograph holds use slow push and a new crop or subject every 2–8s. Source credits stay legible.\n')
    for pi,lid in enumerate(ch['line_ids']):
        ln=L[lid];ls=ln['start'];le=L[ch['line_ids'][pi+1]]['start'] if pi+1<len(ch['line_ids']) else end
        count=max(2,math.ceil((le-ls)/7));span=(le-ls)/count
        for j in range(count):
            a=ls+j*span;b=ls+(j+1)*span;local=a-start;ident=f'{sid}-p{pi+1}s{j+1}'
            spec=special.get(lid) if j==min(1,count-1) else None
            asset=groups[ci][(pi*2+j)%len(groups[ci])];kind='photo';heading='';credit='P.T. © Konami / via Silent Hill Memories';paper=False
            if spec:kind=spec[0]
            label=f'{ci+1:02d} / {E(ch["title"].upper())}'
            if kind=='photo':
                if spec:asset=spec[1];heading=spec[2];credit=spec[3]
                inner=f'<div class="fill"></div><img class="photo motion {"contain" if spec else ""}" id="{ident}-image" src="{asset}" alt="Sourced P.T. image"><div class="label">{label}</div>'
                if heading:inner+=f'<div class="label" style="top:870px;left:250px;font-family:League Gothic;font-size:76px">{E(heading)}</div>'
                if not spec:
                    anim.append(f'tl.fromTo("#{ident}-image",{{scale:1.01,x:0,y:0}},{{scale:1.10,x:{(-1 if j%2 else 1)*17},y:{(-1 if pi%2 else 1)*8},duration:{span:.6f},ease:"none",immediateRender:false}},{local:.6f});')
                else:anim.append(f'tl.fromTo("#{ident}-image",{{scale:.97}},{{scale:1,duration:{span:.6f},ease:"power2.out",immediateRender:false}},{local:.6f});')
            else:
                paper=kind in ('quote','dates');heading=spec[1]
                inner='<div class="fill '+('paper' if paper else '')+'"></div><div class="label">'+label+'</div><div class="stage" id="'+ident+'-stage">'
                if kind=='quote':
                    inner+=f'<div class="rule" id="{ident}-rule"></div><div class="quotation">“{E(spec[1])}”</div><div class="support">{E(spec[2])}</div>';credit='ATTRIBUTED EXCERPT / original source linked in description'
                elif kind=='title':inner+=f'<div class="rule" id="{ident}-rule"></div><div class="display">{E(spec[1])}</div><div class="support">{E(spec[2])}</div>';credit='P.T. / a story of access and preservation'
                elif kind in ('compare','dates'):
                    vals=spec[1].split(' / ') if kind=='dates' else [spec[1],spec[2]]
                    subs=spec[2].split(' / ') if kind=='dates' else ['','']
                    inner+='<div class="twocol">'+''.join(f'<div class="col"><div class="{ "date" if kind=="dates" else "display" }">{E(v)}</div><div class="support">{E(subs[k])}</div></div>' for k,v in enumerate(vals))+'</div>';credit='2015 chronology / sources: Gematsu; Siliconera; GameSpot' if kind=='dates' else 'COMMENTARY / conceptual comparison'
                elif kind=='camera':
                    inner+=f'<div class="display" style="font-size:95px">{E(spec[1])}</div><svg class="schematic" viewBox="0 0 1450 520"><path d="M80 80H1360V430H80Z" stroke="#798568" stroke-width="5" fill="none"/><path id="{ident}-line" d="M950 255H600L360 255" stroke="#E84C3D" stroke-width="10" fill="none"/><circle cx="600" cy="255" r="34" fill="#F2EBD9"/><circle cx="950" cy="255" r="34" fill="#E84C3D"/><path d="M600 255L240 120V390Z" fill="#798568" fill-opacity=".2"/><text x="520" y="355" font-size="30" fill="#F2EBD9">PLAYER</text><text x="890" y="355" font-size="30" fill="#F2EBD9">LISA</text><text x="150" y="465" font-size="29" fill="#F2EBD9">Normal viewpoint faces away from the following model</text></svg><div class="small">{E(spec[2])} / after the flashlight encounter</div>'
                    credit='EXPLANATORY SCHEMATIC / Lance McDonald investigation, Sept 2019';anim.append(f'tl.fromTo("#{ident}-line",{{strokeDasharray:590,strokeDashoffset:590}},{{strokeDashoffset:0,duration:2,ease:"none",immediateRender:false}},{local:.6f});')
                elif kind=='loop':
                    inner+=f'<div class="display">{E(spec[1])}</div><svg class="schematic" viewBox="0 0 1450 520"><path id="{ident}-line" d="M150 150H1230V370H150Z" fill="none" stroke="#E84C3D" stroke-width="12"/><text x="330" y="290" font-size="68" fill="#F2EBD9">WALK → LOOK → RETURN</text></svg><div class="support">{E(spec[2])}</div>';credit='CONCEPTUAL LOOP / layout is illustrative';anim.append(f'tl.fromTo("#{ident}-line",{{strokeDasharray:2600,strokeDashoffset:2600}},{{strokeDashoffset:0,duration:3,ease:"none",immediateRender:false}},{local:.6f});')
                inner+='</div>'
                anim.append(f'tl.fromTo("#{ident}-stage",{{y:24,opacity:0}},{{y:0,opacity:1,duration:.38,ease:"power3.out",immediateRender:false}},{local:.6f});')
            inner+=f'<div class="credit">{E(credit)}</div>'
            content.append(f'<section id="{ident}" class="clip shot {"paper" if paper else ""}" data-start="{local:.6f}" data-duration="{span:.6f}" data-track-index="1">{inner}</section>')
            timeline.append({'start':a,'end':b,'chapter':ch['title'],'paragraph':lid,'kind':kind,'asset':asset if kind=='photo' else '', 'text':heading,'credit':credit,'narration':ln['text'] if j==0 else '', 'camera':'slow push' if kind=='photo' else 'timed reveal','sfx':'chapter punctuation only','music':'ducked licensed score','transition':'hard cut'})
    body='<!doctype html><html><body><template><style>'+css+'</style><div id="root" data-composition-id="'+sid+'" data-width="1920" data-height="1080" data-start="0" data-duration="'+str(duration)+'">'+''.join(content)+'</div><script>const tl=gsap.timeline({paused:true});'+''.join(anim)+'window.__timelines["'+sid+'"]=tl;</script></template></body></html>'
    (P/f'compositions/{sid}.html').write_text(body,encoding='utf8')
    slots.append(f'<div id="slot-{sid}" class="clip" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-width="1920" data-height="1080" data-start="{start:.6f}" data-duration="{duration:.6f}" data-track-index="1"></div>')
roothtml='<!doctype html><html lang="en"><head><meta charset="UTF-8"><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{margin:0;box-sizing:border-box}html,body,#root{width:1920px;height:1080px;overflow:hidden}#root{position:relative}.clip[data-composition-src]{position:absolute;inset:0}</style></head><body><div id="root" data-composition-id="pt-film" data-start="0" data-duration="'+str(D)+'" data-width="1920" data-height="1080" data-fps="24"><div style="position:absolute;inset:0;background:#11150F"></div>'+''.join(slots)+f'<audio id="final-mix" src="03_AUDIO/final_mix.wav" data-start="0" data-duration="{D}" data-track-index="10" data-volume="1"></audio></div><script>window.__timelines=window.__timelines||{{}};window.__timelines["pt-film"]=gsap.timeline({{paused:true}});</script></body></html>'
(P/'index.html').write_text(roothtml,encoding='utf8')
(P/'STORYBOARD.md').write_text('\n'.join(boards),encoding='utf8')
with (P/'05_EDIT/project_files/visual_timeline.csv').open('w',encoding='utf8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(timeline[0]));w.writeheader();w.writerows(timeline)
(P/'05_EDIT/project_files/visual_timeline.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2),encoding='utf8')
shutil.copyfile(P/'03_AUDIO/narration.srt',P/'07_EXPORT/final_subtitles.srt')
print(f'Built {len(C)} chapters, {len(timeline)} shots, {D:.3f}s; zero AI images.')
