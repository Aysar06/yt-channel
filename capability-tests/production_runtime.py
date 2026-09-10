"""Paths and media tools that survive moving this checkout to another computer."""
import os
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def project_path(value):
    """Resolve current relative paths and the historical Windows manifest format."""
    value = str(value).replace('\\', '/')
    marker = '/VIDEO_PROJECT/'
    if marker in value:
        value = 'VIDEO_PROJECT/' + value.split(marker, 1)[1]
    p = Path(value)
    if not p.is_absolute():
        p = ROOT / p
    return p.resolve()


def portable_path(value):
    p = project_path(value)
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        # synthesize.py can also be used with an explicitly supplied external output.
        return str(p)


@lru_cache(maxsize=None)
def media_tool(name):
    override = os.environ.get(name.upper() + '_BINARY')
    if override:
        resolved = shutil.which(override) or (override if Path(override).is_file() else None)
        if not resolved:
            raise RuntimeError(f'{name.upper()}_BINARY does not point to a usable executable')
        return str(resolved)
    if os.name == 'nt':
        bundled = ROOT / 'tools/ffmpeg/bin' / (name + '.exe')
        if bundled.is_file():
            with bundled.open('rb') as f:
                if f.read(2) != b'MZ':
                    raise RuntimeError('Media tools are Git LFS pointers. Run git lfs pull.')
            return str(bundled)
    found = shutil.which(name)
    if found:
        return found
    if name == 'ffmpeg':
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    raise RuntimeError('Install FFmpeg (including ffprobe) and put it on PATH.')


@lru_cache(maxsize=1)
def video_encoder_args():
    """Probe actual NVENC operation; computers without NVIDIA use software H.264."""
    requested = os.environ.get('VIDEO_ENCODER', 'auto').lower()
    if requested not in ('auto', 'cpu', 'nvenc'):
        raise ValueError('VIDEO_ENCODER must be auto, cpu or nvenc')
    if requested != 'cpu':
        check = subprocess.run(
            [media_tool('ffmpeg'), '-hide_banner', '-loglevel', 'error',
             '-f', 'lavfi', '-i', 'color=size=64x64:rate=24', '-frames:v', '1',
             '-c:v', 'h264_nvenc', '-f', 'null', '-'], capture_output=True)
        if check.returncode == 0:
            return ['-c:v', 'h264_nvenc', '-preset', 'p4', '-cq', '18']
        if requested == 'nvenc':
            raise RuntimeError('NVENC was requested but is unavailable on this computer')
    return ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18']
