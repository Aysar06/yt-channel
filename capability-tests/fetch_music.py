import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parent.parent
music = root / 'VIDEO_PROJECT/03_AUDIO/music'
licenses = root / 'VIDEO_PROJECT/04_MEDIA/licenses'
music.mkdir(parents=True, exist_ok=True)
licenses.mkdir(parents=True, exist_ok=True)
ledger = []
verified_downloads = {
    'eyes-in-the-void': 'https://www.scottbuckley.com.au/library/wp-content/uploads/2025/06/EyesInTheVoid.mp3',
    'incredulity': 'https://www.scottbuckley.com.au/library/wp-content/uploads/2025/04/Incredulity.mp3',
    'unraveling': 'https://www.scottbuckley.com.au/library/wp-content/uploads/2026/05/Unraveling.mp3',
}
for slug, title in [('eyes-in-the-void', 'Eyes In The Void'), ('incredulity', 'Incredulity'), ('unraveling', 'Unraveling')]:
    page = f'https://www.scottbuckley.com.au/library/{slug}/'
    # These exact hrefs were retrieved from each official page by the web tool.
    # The HTML server rejects requests with 406; this uses its public audio href.
    download = verified_downloads[slug]
    file = music / f'scott-buckley-{slug}.mp3'
    # Windows curl handles this public host's content negotiation correctly.
    if not file.exists() or file.stat().st_size < 10000:
        subprocess.run(['curl.exe', '-L', '--fail', '--silent', '--show-error', download, '-o', str(file)], check=True)
    audio_bytes = file.read_bytes()
    metadata = json.loads(subprocess.check_output([str(root / 'tools/ffmpeg/bin/ffprobe.exe'), '-v', 'error',
                                                   '-show_format', '-show_streams', '-of', 'json', str(file)]))
    record = {'title': title, 'creator': 'Scott Buckley', 'source_page': page, 'download': download,
              'file': str(file.relative_to(root / 'VIDEO_PROJECT')), 'license': 'CC BY 4.0',
              'license_url': 'https://creativecommons.org/licenses/by/4.0/',
              'attribution': f"'{title}' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au",
              'sha256': hashlib.sha256(audio_bytes).hexdigest(), 'metadata': metadata,
              'usage': 'Edited excerpts, fades, level reduction and dialogue ducking; credit in YouTube description.',
              'retrieved': '2026-09-07'}
    ledger.append(record)
    print(json.dumps({k: record[k] for k in ['title', 'download', 'file']}) + f" duration={metadata['format']['duration']}", flush=True)
(licenses / 'music.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf8')
text = '# Music licenses\n\nRetrieved 2026-09-07 from the composer’s own library. Each source page expressly allows commercial use under CC BY 4.0 and requires the creator credit in the YouTube description. These sources are edited in the production by excerpting, fades, reduced volume and dialogue ducking.\n\n'
for record in ledger:
    text += f"## {record['title']}\n\n- Creator: Scott Buckley\n- Source: {record['source_page']}\n- Audio: {record['download']}\n- File: `{record['file']}`\n- License: CC BY 4.0 — {record['license_url']}\n- SHA256: `{record['sha256']}`\n- Required description credit: {record['attribution']}\n\n"
text += 'The Unraveling page has a trailing hyphen in its sample attribution (Unraveling-); this ledger uses the displayed track title and links the exact source. No WAV subscription or paid license was purchased.\n'
(licenses / 'music.md').write_text(text, encoding='utf8')
