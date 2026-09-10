"""Prepare a fresh clone without changing any production media."""
import argparse
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--review-tools', action='store_true', help='Also install optional ASR tools')
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        raise SystemExit('Python 3.11 or newer is required; 3.11 is the recorded production version.')
    for command in ('git', 'node', 'npm'):
        if not shutil.which(command):
            raise SystemExit(f'Install {command} first. See README.md.')
    subprocess.run(['git', 'lfs', 'install', '--local'], cwd=ROOT, check=True)
    subprocess.run(['git', 'lfs', 'pull'], cwd=ROOT, check=True)
    envdir = ROOT / '.venv'
    venv.create(envdir, with_pip=True)
    python = envdir / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    req = 'requirements-review.txt' if args.review_tools else 'requirements.txt'
    subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(ROOT / req)], check=True)
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    subprocess.run([npm, 'ci'], cwd=ROOT / 'VIDEO_PROJECT', check=True)
    subprocess.run([str(python), str(ROOT / 'tools/resume.py')], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()

