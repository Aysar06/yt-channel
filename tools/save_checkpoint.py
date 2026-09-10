"""Record hashes of tracked LFS media after an intentional checkpoint update."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
suffixes = {'.mp4', '.mp3', '.wav', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.zip', '.exe', '.pdf'}
names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf8').split('\0')
files = []
for name in sorted(n for n in names if n and Path(n).suffix.lower() in suffixes):
    p = ROOT / name
    with p.open('rb') as f:
        header = f.read(128)
        if header.startswith(b'version https://git-lfs.github.com/spec/v1'):
            raise SystemExit('Fetch full media before checkpointing: ' + name)
        f.seek(0)
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    files.append({'path': name, 'bytes': p.stat().st_size, 'sha256': digest})
out = ROOT / 'handoff/media-manifest.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({'schema': 1, 'total_bytes': sum(f['bytes'] for f in files), 'files': files}, indent=2) + '\n', encoding='utf8')
print(f'Recorded {len(files)} media files, {sum(f["bytes"] for f in files)/1024**3:.2f} GiB')
