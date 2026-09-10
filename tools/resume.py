"""Verify the saved production state before continuing on another computer."""
import argparse
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'capability-tests'))
from production_runtime import media_tool, project_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files-only', action='store_true', help='Check transferred files without installed production dependencies')
    args = parser.parse_args()
    errors = []
    manifest = json.loads((ROOT / 'handoff/media-manifest.json').read_text(encoding='utf8'))
    for item in manifest['files']:
        p = ROOT / item['path']
        if not p.is_file():
            errors.append('Missing: ' + item['path'])
            continue
        with p.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        if digest != item['sha256']:
            errors.append('Changed or Git LFS pointer: ' + item['path'])
    # Check all original and connected narration inputs, including historical path compatibility.
    audio = ROOT / 'VIDEO_PROJECT/03_AUDIO/revision_02'
    for name in ('narration_manifest.json', 'connected_manifest.json'):
        data = json.loads((audio / name).read_text(encoding='utf8'))
        for row in data['lines']:
            for key in ('raw', 'clean'):
                if not project_path(row[key]).is_file():
                    errors.append(f'{name}: {row[key]} does not resolve')
    # The mounted revision must resolve its local images, footage, audio and chapters.
    for p in [ROOT / 'VIDEO_PROJECT/index.html', *sorted((ROOT / 'VIDEO_PROJECT/compositions/revision_02').glob('*.html'))]:
        for url in re.findall(r'(?:src|data-composition-src)=[\"\x27]([^\"\x27]+)', p.read_text(encoding='utf8')):
            if url.startswith(('http:', 'https:', 'data:', '#')):
                continue
            # HyperFrames resolves child composition media against the project root.
            target = ROOT / 'VIDEO_PROJECT' / unquote(url.split('?', 1)[0].split('#', 1)[0])
            if not target.is_file():
                errors.append(f'{p.name}: missing {url}')
    if not args.files_only:
        for tool in ('ffmpeg', 'ffprobe'):
            try:
                subprocess.run([media_tool(tool), '-version'], check=True, capture_output=True)
            except Exception as exc:
                errors.append(str(exc))
        for package in ('edge-tts', 'imageio-ffmpeg', 'numpy', 'Pillow'):
            try:
                importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                errors.append('Missing dependency: ' + package + '; run tools/setup.py')
        for command in ('node', 'npm', 'git'):
            if not shutil.which(command):
                errors.append('Missing command: ' + command)
        if not (ROOT / 'VIDEO_PROJECT/node_modules/hyperframes/package.json').is_file():
            errors.append('Run tools/setup.py (HyperFrames dependency is not installed).')
    if errors:
        print('\n'.join(errors[:30]))
        raise SystemExit(f'{len(errors)} checks failed. If files are missing, run git lfs pull.')
    state = json.loads((ROOT / 'handoff/checkpoint.json').read_text(encoding='utf8'))
    print(f"Verified {len(manifest['files'])} frozen media files ({manifest['total_bytes'] / 1024**3:.2f} GiB).")
    print('Current export:', state['current_export'])
    print('Status:', state['status'])
    print('Next:', state['next_action'])
    print('Open RESUME.md in Codex and continue from it. Do not regenerate cached narration.')


if __name__ == '__main__':
    main()
