"""Launch the pinned renderer from any working directory. GPU is optional."""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'capability-tests'))
from production_runtime import media_tool


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', action='store_true', help='Use the tested NVIDIA configuration; default is software encoding')
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--output', default='07_EXPORT/revision_02.mp4')
    args = parser.parse_args()
    env = dict(os.environ)
    env['PATH'] = str(Path(media_tool('ffmpeg')).parent) + os.pathsep + env.get('PATH', '')
    env.update(HF_CAPTURE_PARALLEL_STREAM='true', PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS='900', PRODUCER_EXPERIMENTAL_FAST_CAPTURE='false')
    npx = shutil.which('npx.cmd' if os.name == 'nt' else 'npx')
    if not npx:
        raise SystemExit('Install Node.js and run tools/setup.py first.')
    cmd = [npx, '--no-install', 'hyperframes', 'render', '--fps', '24', '--quality', 'high', '--workers', str(args.workers), '--crf', '18', '--output', args.output]
    if args.gpu:
        cmd.append('--gpu')
    subprocess.run(cmd, cwd=ROOT / 'VIDEO_PROJECT', env=env, check=True)


if __name__ == '__main__':
    main()
