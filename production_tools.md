# Production capabilities audit

Verified locally on 2026-09-06 and 2026-09-07. This audit is evidence of tool operation, not a claim that the final video has passed perceptual review.

| Capability | Working route | Evidence / limit |
|---|---|---|
| Runtime | Node.js 24.18.0; Python 3.11.9 | Installed on PATH |
| Video/audio processing | Portable FFmpeg + ffprobe 9.0.1, `tools/ffmpeg/bin` | Both executable; downloaded official-linked Gyan essentials build, SHA256 verified |
| Existing fallback FFmpeg | Python imageio-ffmpeg 0.6.0 ships FFmpeg 7.1 | Fallback used successfully before portable setup |
| Neural narration | edge-tts 7.2.8, `en-US-AndrewMultilingualNeural` and `en-US-GuyNeural` | Both produced complete samples with no paid call or account credentials |
| Timings/captions | Edge word-boundary metadata + original source punctuation | Sample aligned all 31 source words exactly; SRT emitted |
| Loudness normalization | Two-pass FFmpeg loudnorm | 10.8 s sample output measured -16.2 LUFS, -1.5 dBTP |
| Speech verification | faster-whisper 1.2.1, `small.en`, CPU int8, cached model | 10.056 s sample transcribed in 3.24 s, no missing speech; normalized twenty to 20 |
| GPU transcription | CTranslate2 detects RTX 4060 | CUDA ASR failed: cublas64_12.dll missing; use verified CPU route |
| Music | Three Scott Buckley original MP3 files | CC BY 4.0 pages verified; files saved in `VIDEO_PROJECT/03_AUDIO/music`; required description credits in music.md |
| Original sound effects | NumPy/SciPy PCM synthesis | No borrowed recordings or samples |
| HeyGen | CLI and credential directory not present at audit | No external credentials printed or generated; not required for working narration route |
| Optional voice models | Torch/Kokoro absent in default Python; cached Chatterbox model exists | Cached weights alone do not demonstrate a working inference route |
| Perceptual listening | Not established for this agent | Do not equate ASR or a waveform/loudness scan with listening to voice naturalness, breaths or clicks |

The sample voice comparison produced Andrew and Guy alternatives, but no direct auditory ranking is claimed. Andrew is the production default with restrained per-paragraph rate and pitch changes. Arbitrary emotion tags are not supported by edge-tts; they must guide punctuation and bounded performance settings. Performance tags are stripped before speech/caption generation. The Edge route is an online Microsoft service accessed through the installed client, not an offline model; no independent commercial-rights guarantee for its output is asserted here.

## Working commands

```powershell
# Enable portable binary discovery for one shell / HyperFrames invocation.
$env:PATH = (Join-Path (Get-Location) 'tools\ffmpeg\bin') + ';' + $env:PATH
ffmpeg -version
ffprobe -v error -show_format -show_streams -of json 'VIDEO_PROJECT\03_AUDIO\narration.wav'

# Full narration from a request containing voice/rate/pitch and lines [{id,text,...}].
python 'capability-tests\synthesize.py' request.json --out 'VIDEO_PROJECT\03_AUDIO'

# Reproducible sample; helper writes raw MP3, clean WAV, per-line JSON,
# joined narration.wav, narration_manifest.json, narration.words.json, narration.srt.
python 'capability-tests\synthesize.py' 'capability-tests\sample-request.json' --out 'capability-tests\synth-test'

# Music source links are frozen from their actual official download links.
python 'capability-tests\fetch_music.py'
python 'capability-tests\create_sfx.py'
```

The narration helper resumes unchanged paragraphs using a text/voice/rate/pitch fingerprint. It preserves the audio duration and pauses. It only normalizes loudness; it does not silently gate breath candidates, apply broad denoising, or compress normal expressive declination.

Available FFmpeg filters tested include loudnorm, adeclick, afftdn, deesser, sidechaincompress, silencedetect and ebur128. Their presence is not evidence that every filter should be applied. Broad breath/click suppression needs a confirmed problem; synthetic silence and low background energy are measured first.

## Portable binary provenance

- FFmpeg project Windows download page: https://ffmpeg.org/download.html#build-windows
- Build provider linked by FFmpeg: https://www.gyan.dev/ffmpeg/builds/
- ZIP: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
- ZIP SHA256: `fec81ae03971d9dd4be3ebe02e263bd2ec1d789483f931bdba5f5715e65da2e9`
- Provider checksum checked before extraction. GPLv3 license retained at `tools/ffmpeg/LICENSE`.
- Built-in H.264/H.265/AAC encoding and probing are available. No cloud-render fees or public publishing actions were used.

## Samples and evidence

- `capability-tests/edge-andrew-sample.mp3` and matching SRT
- `capability-tests/edge-guy-sample.mp3` and matching SRT
- `capability-tests/synth-test/narration.wav` and timed outputs
- `capability-tests/whisper-small-en-test.json`
- `VIDEO_PROJECT/04_MEDIA/licenses/music.md` and machine-readable music.json
