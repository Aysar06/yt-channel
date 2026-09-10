# Long-form YouTube production

Editable production workspace for **The Horror Game You Could Lose Forever** (P.T. / Silent Hills).

**Start with [RESUME.md](RESUME.md).** It records the current edit, the user's corrections, completed checks and the exact next work. The current 10:22 revision is rendered but **not approved**.

## Continue on another computer

Install Git with [Git LFS](https://git-lfs.com/), Python 3.11 and Node.js 24. Sign in to GitHub as an account with access to this private repository. On macOS/Linux, also install FFmpeg including `ffprobe`. Windows FFmpeg 9.0.1 is included through LFS.

```sh
git lfs install
git clone https://github.com/Aysar06/yt-channel.git
cd yt-channel
python tools/setup.py
```

Use `python3` if your computer names Python that way. Setup downloads LFS media, creates `.venv`, installs pinned production dependencies and verifies the saved media hashes. It does not regenerate narration or render another video. Add `--review-tools` only when automatic transcription is needed; its speech model downloads on first use.

Open this folder as a project in Codex on the other computer, and say:

> Read AGENTS.md and RESUME.md, verify the checkpoint, then continue production from the next unfinished step. Preserve the user's revision requirements and use real sourced media. Do not restart research or regenerate unchanged narration.

For an existing clone:

```sh
git pull --ff-only
git lfs pull
python tools/setup.py
```

Keep local work committed before pulling. Git transfers the saved project and handoff notes; the old chat, signed-in browser sessions and running processes are not transferred. The existing export is preserved byte for byte. New renders on different operating systems may differ in font rendering or encoding.

## Preview and render

After setup, run `npm run dev --prefix VIDEO_PROJECT` for the editable preview. The saved video is `VIDEO_PROJECT/07_EXPORT/revision_02.mp4`; its captions are beside it.

Use `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on macOS/Linux for production commands. `tools/render.py` defaults to software encoding; `--gpu --workers 4` selects the original NVIDIA render setup. Cached source cuts need no GPU. New cuts automatically fall back to software H.264 if NVIDIA encoding is unavailable.

See [the rebuild instructions](VIDEO_PROJECT/05_EDIT/revision_02/REBUILD.md) for individual stages. Run `tools/resume.py` with the virtual-environment Python to verify the saved checkpoint, or `python tools/resume.py --files-only` to verify media without installing production dependencies.

## What is saved

The repository includes the current and rejected edits, original downloaded footage, source screenshots, voice takes, music, captions, thumbnails, research, source/usage records, automated QA and ten local workflow skills. Large binary assets use Git LFS. Do not use GitHub's Download ZIP as the migration method; use the clone commands above to retrieve all media.

Only regenerable mixing intermediates, duplicate FFmpeg downloads, dependency caches and the ZIP duplicating the rejected V1 upload package are excluded. The rejected V1 MP4 itself is retained for comparison. No accounts, credentials or API keys are included.

This is a private production backup. Source availability is not a reuse license; per-asset provenance and usage notes remain in `VIDEO_PROJECT/04_MEDIA/licenses`. YouTube publishing and purchases require separate user authorization.
