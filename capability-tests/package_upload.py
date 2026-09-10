import json,re,shutil,html
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent.parent;P=R/'VIDEO_PROJECT';U=P/'08_YOUTUBE'
M=json.loads((P/'03_AUDIO/narration_manifest.json').read_text());C=json.loads((P/'05_EDIT/project_files/chapter_timing.json').read_text());L={x['id']:x for x in M['lines']}
def stamp(s):return f'{int(s)//60:02d}:{int(s)%60:02d}'
def write(name,text):(U/name).write_text(text,encoding='utf8')
title='The Horror Game You Could Lose Forever'
write('title.txt',title+'\n');write('backup_titles.txt',"P.T.: The Horror Game You Could Lose Forever\nThe Game That Outlived Its Own Cancellation\n\nSuggested title test: Why People Are Afraid to Delete This Game\nNo experiment has been run.\n")
chapters='\n'.join(stamp(c['start'])+' '+c['title'] for c in C)
write('chapters.txt',chapters+'\n')
tags='P.T., PT Silent Hills, Silent Hills, Silent Hill, Hideo Kojima, Guillermo del Toro, Norman Reedus, Lisa PT, cancelled games, horror games, gaming mysteries, lost media, game preservation, PlayStation 4, PT download, Lance McDonald'
write('tags.txt',tags+'\n');write('keywords.txt','Primary: P.T. Silent Hills\nSecondary: PT download, Silent Hills cancellation, P.T. Lisa, game preservation\n');write('hashtags.txt','#SilentHills #PT #HorrorGaming\n')
sources=re.findall(r'^- URL: (https?://\S+)',(P/'01_RESEARCH/sources.md').read_text(),re.M)
source_names=['Reveal (Gematsu)','Contemporary reveal (Ars Technica)','Release record (Guinness)','Official Konami gameplay tips','Puzzle expectations','Cancellation statement','Cancellation cross-check','Distribution deadline','Re-download failure','Re-download cross-check','PS5 review hardware','PS5 compatibility report','Lance McDonald original post','Camera investigation','Flashlight qualifier']
music=json.loads((P/'04_MEDIA/licenses/music.json').read_text());credits='\n'.join(x['attribution']+'\n'+x['source_page'] for x in music)
description="A free horror game became something players were afraid to delete. The strange story of P.T. is about what happens when the hallway survives, but the way back disappears.\n\nFrom its disguised 2014 launch to Silent Hills' cancellation, the loss of normal re-download access, and Lance McDonald's camera discovery: this is the story of the teaser people actually played. Existing installed copies were not all remotely erased; P.T. and the cancelled Silent Hills are distinct projects.\n\nSources:\n"+'\n'.join(n+': '+u for n,u in zip(source_names,sources))+"\nGameSpot's 2015 download test: https://www.gamespot.com/articles/p-t-can-no-longer-be-downloaded-even-from-your-ps4/1100-6427124/\nCommunity discussion: https://gamefaqs.gamespot.com/boards/691087-playstation-4/74324135\nPuzzle discussion: https://gameinformer.com/b/news/archive/2014/08/16/reader-discussion-have-you-finished-the-silent-hills-playable-teaser-p-t.aspx\n\nVisuals: P.T. game imagery © Konami, via Silent Hill Memories (https://www.silenthillmemories.net/silent_hills/screens_en.htm), PlayStation Blog and GameSpot; brief stills accompany contextual analysis. Original explanatory diagrams are labeled. No AI images used. Narration is synthetic.\n\nMusic:\n"+credits+"\nLicense: https://creativecommons.org/licenses/by/4.0/\nMusic excerpts edited with fades and dialogue ducking. Original procedural sound effects.\n\nChapters:\n"+chapters+"\n\n#SilentHills #PT #HorrorGaming\n"
write('description.txt',description)
write('pinned_comment.txt','If you could preserve only one, would you keep the original playable P.T. or a perfect recording of everything we currently know is in it? Which moment would be lost by giving up the controller?\n')
shorts=[('c01p01','c01p03','You deleted a free game. Now you cannot get it back.','The Free Game You Should Never Delete'),('c03p01','c03p02','Knowing this map makes the game scarier.','The Hallway That Uses Your Memory Against You'),('c05p01','c05p02','This unknown horror game ended with Norman Reedus.','The Reveal Hidden Inside P.T.'),('c07p02','c07p03','Owning the download and keeping the installation became different things.','P.T. Closed Two Different Doors'),('c09p01','c09p02','Move the camera, and the ghost is right behind the player.','What P.T. Hid Behind the Camera')]
out=['# Suggested Shorts from the completed timeline\n\nReframe into 9:16 manually within this project; preserve source attribution and the flashlight qualifier. These are extraction plans, not exported vertical videos.\n']
for a,b,hook,t in shorts:
    selected=[l['text'] for l in M['lines'] if L[a]['start']<=l['start']<=L[b]['start']]
    out.append(f'## {t}\n\nSource: {stamp(L[a]["start"])}–{stamp(L[b]["end"])} ({L[b]["end"]-L[a]["start"]:.1f}s).\n\nHook/caption: {hook}\n\nEdit: start immediately on the focal source image; crop around the relevant detail, then cut to a readable source/keyword panel. Use compact subtitles below the subject.\n\nScript: '+ ' '.join(selected)+'\n')
write('shorts_ideas.md','\n'.join(out))
# Native designed thumbnail: the underlying authentic source photograph is unchanged.
font=next((Path('C:/Users/aysar/.cache/hyperframes/fonts/league-gothic')).glob('*.woff2'));dest=P/'05_EDIT/graphics/league-gothic.woff2';shutil.copyfile(font,dest)
photo=(P/'04_MEDIA/images/silent_hills_pt_screen_20140821_02.jpg').as_uri()
base="""<!doctype html><html><head><meta charset='utf-8'><style>@font-face{font-family:LG;src:url('FONT')}*{box-sizing:border-box}body{margin:0;width:1280px;height:720px;background:#10140f;color:#f2ebd9;overflow:hidden}.photo{position:absolute;left:0;top:0;width:720px;height:720px;object-fit:cover;object-position:48% 50%}.shade{position:absolute;left:645px;top:0;width:635px;height:720px;background:#10140f}.pt{position:absolute;left:50px;top:36px;font:150px LG;letter-spacing:3px;text-shadow:0 4px 12px #000}.copy{position:absolute;left:750px;top:185px;font-family:LG;line-height:.96}.one{font-size:112px}.two{font-size:153px;color:#f35b49}.x{position:absolute;left:553px;top:510px;width:125px;height:125px;background:#df4437;border-radius:50%;display:grid;place-items:center;font:100px Arial;color:white;border:8px solid #f2ebd9}</style></head><body><img class='photo' src='PHOTO'><div class='shade'></div><div class='pt'>P.T.</div><div class='copy'><div class='one'>ONE</div><div class='two'>TWO</div></div><div class='x'>×</div></body></html>""".replace('FONT',dest.as_uri()).replace('PHOTO',photo)
chrome='C:/Users/aysar/.cache/hyperframes/chrome/chrome-headless-shell/win64-152.0.7977.30/chrome-headless-shell-win64/chrome-headless-shell.exe'
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path=chrome);page=b.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
 for name,one,two in [('thumbnail','DON’T','DELETE'),('thumbnail_alternative','NO','DOWNLOAD')]:
    s=base.replace('ONE',one).replace('TWO',two)
    if name.endswith('alternative'):s=s.replace('font-size:153px','font-size:120px').replace('left:750px','left:716px')
    file=P/f'06_THUMBNAIL/final/{name}.html';file.write_text(s,encoding='utf8');page.goto(file.as_uri());page.evaluate('document.fonts.ready');page.screenshot(path=str(file.with_suffix('.png')));page.screenshot(path=str(file.with_suffix('.jpg')),type='jpeg',quality=95)
 b.close()
manifest=json.loads((P/'04_MEDIA/licenses/asset_manifest.json').read_text());manifest.append({'path':'04_MEDIA/images/gs_download_error.jpg','source_page':'https://www.gamespot.com/articles/p-t-can-no-longer-be-downloaded-even-from-your-ps4/1100-6427124/','image_url':'https://www.gamespot.com/wp-content/uploads/original/280/2802776/2860565-20150506144042.jpg','rights':'GameSpot test screenshot; copyrighted. Brief contextual commentary on download failure.'})
(P/'04_MEDIA/licenses/asset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print('Upload copy and two sourced thumbnails saved. Description characters:',len(description))
