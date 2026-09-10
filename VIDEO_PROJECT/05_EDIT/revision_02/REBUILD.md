# Revision 02 production files

Start with the repository-root `README.md` and `RESUME.md` after moving computers. Run all Python commands with the virtual environment created by `tools/setup.py`. The following inputs are already cached; rebuilding is only needed after intentional edits. For a portable render from the root, use `python tools/render.py` (software), or add `--gpu --workers 4` for the original NVIDIA setup.

The revised project starts at `VIDEO_PROJECT/index.html`. Ten new compositions live in `compositions/revision_02`. The rejected composition is preserved in `v1_project`.

Run these from the workspace root, in this order, if changing the manuscript or edit:

```powershell
python capability-tests/synthesize.py VIDEO_PROJECT/02_SCRIPT/revision_02_request.json --out VIDEO_PROJECT/03_AUDIO/revision_02
python capability-tests/tighten_revision_voice.py
python capability-tests/build_revision.py
python capability-tests/compose_revision.py
python capability-tests/mix_revision.py
python capability-tests/document_revision.py
```

Synthesis caches unchanged takes. Finite footage cuts use source/time/duration signatures. Web evidence is frozen locally; its pixels are captured from the actual pages. Re-capture source pages through the browser when needed, retaining the original capture and its URL. Avoid reconstructing page text as a fake screenshot.

The reveal hold is inserted at scene time 12.44 seconds, within measured silence. It is a deliberate 12-second title-animation payoff. Caption words and all subsequent chapter positions use the resulting timeline. Do not move that hold into speech.

The edit uses 24 fps. Each video element owns its local timing once. No video loops, reverse playback, slow motion or padding freezes are used. Static diagrams repeat the P.T. installation symbol for an explicit comparison; this is separate from repeating a source video excerpt.

From `VIDEO_PROJECT`, add `../tools/ffmpeg/bin` to PATH and run `npx --yes hyperframes@0.8.32 check`. The project was upgraded from 0.8.31 to 0.8.32. Snapshot previews and the finished encode need visual checks after edits.

For the existing local streaming render configuration:

```powershell
$env:PATH = (Join-Path (Get-Location).Path '../tools/ffmpeg/bin') + ';' + $env:PATH
$env:HF_CAPTURE_PARALLEL_STREAM='true'
$env:PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS='900'
$env:PRODUCER_EXPERIMENTAL_FAST_CAPTURE='false'
npx.cmd --yes hyperframes@0.8.32 render --fps 24 --quality high --workers 4 --gpu --crf 18 --output 07_EXPORT/revision_02.mp4
```

Then, from the workspace root, run `python capability-tests/verify_revision.py`. Automated transcription, signal measurements, full decoding and visual samples do not establish that a person has listened to or watched the entire finished film. Keep those review fields false unless that review actually occurs. Publishing remains unauthorized.
