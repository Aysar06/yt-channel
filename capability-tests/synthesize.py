"""Credential-free Edge neural TTS production helper.

python capability-tests/synthesize.py request.json --out VIDEO_PROJECT/03_AUDIO
request: {voice?, rate?, pitch?, lines:[{id,text,voice?,rate?,pitch?,gap_after?}]}
Writes raw MP3, clean 48 kHz WAV, word timings, joined narration.wav and SRT.
No paid service, account credential, arbitrary SSML, or voice cloning is used.
"""
import argparse
import asyncio
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import wave
from pathlib import Path

import edge_tts
import imageio_ffmpeg

from production_runtime import ROOT, media_tool, portable_path, project_path
FFMPEG = media_tool("ffmpeg")


def run_ffmpeg(args):
    result = subprocess.run([FFMPEG, "-hide_banner", "-nostdin", *args],
                            capture_output=True, text=True, encoding="utf8", errors="replace")
    if result.returncode:
        raise RuntimeError(result.stderr[-6000:])
    return result.stderr


def norm(s):
    return re.sub(r"[^\w]", "", s.lower())


def restore_punctuation(words, source):
    """Restore original punctuation only for verified exact token matches."""
    tokens = source.split()
    matcher = difflib.SequenceMatcher(a=[norm(w["text"]) for w in words],
                                     b=[norm(t) for t in tokens], autojunk=False)
    for block in matcher.get_matching_blocks():
        for n in range(block.size):
            words[block.a + n]["text"] = tokens[block.b + n]
    return matcher.ratio()


def clean_audio(raw, clean):
    """Two-pass loudness only; natural pauses and timing stay intact."""
    report = run_ffmpeg(["-i", str(raw), "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    measurements = json.loads(re.findall(r"\{[^{}]+\}", report)[-1])
    filt = ("loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
            f"measured_I={measurements['input_i']}:measured_TP={measurements['input_tp']}:"
            f"measured_LRA={measurements['input_lra']}:measured_thresh={measurements['input_thresh']}:"
            f"offset={measurements['target_offset']}:print_format=json")
    clean_report = run_ffmpeg(["-y", "-i", str(raw), "-af", filt,
                              "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(clean)])
    return {"input": measurements, "output": json.loads(re.findall(r"\{[^{}]+\}", clean_report)[-1])}


async def synth_line(line, request, out, sem):
    line_id = str(line["id"])
    if not re.fullmatch(r"[A-Za-z0-9_-]+", line_id):
        raise ValueError(f"Unsafe line id: {line_id!r}")
    text = re.sub(r"\[(?:CURIOUS|EXCITED|SERIOUS|QUIET|CONFUSED|SARCASTIC|DISBELIEF|FAST|SLOW|EMPHASIS)\]", "", line["text"])
    text = re.sub(r"\s+", " ", text).strip()
    voice = line.get("voice", request.get("voice", "en-US-AndrewMultilingualNeural"))
    rate = line.get("rate", request.get("rate", "-8%"))
    pitch = line.get("pitch", request.get("pitch", "+0Hz"))
    raw = out / "voice_raw" / f"{line_id}.mp3"
    clean = out / "voice_clean" / f"{line_id}.wav"
    metadata_path = out / "voice_clean" / f"{line_id}.json"
    fingerprint = hashlib.sha256(json.dumps([text, voice, rate, pitch], ensure_ascii=False).encode()).hexdigest()
    if metadata_path.exists() and clean.exists() and raw.exists():
        old = json.loads(metadata_path.read_text(encoding="utf8"))
        if old.get("fingerprint") == fingerprint:
            print(f"cached {line_id}", flush=True)
            old["raw"] = portable_path(raw)
            old["clean"] = portable_path(clean)
            return old
    async with sem:
        words = []
        for attempt in range(3):
            try:
                words = []
                communicate = edge_tts.Communicate(text, voice=voice, rate=rate,
                                                   pitch=pitch, boundary="WordBoundary")
                with raw.open("wb") as audio:
                    async for item in communicate.stream():
                        if item["type"] == "audio":
                            audio.write(item["data"])
                        elif item["type"] == "WordBoundary":
                            words.append({"id": f"w{len(words)}", "text": item["text"],
                                          "start": item["offset"] / 10_000_000,
                                          "end": (item["offset"] + item["duration"]) / 10_000_000})
                if not words or raw.stat().st_size < 1000:
                    raise RuntimeError("TTS returned no usable audio or words")
                break
            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 * (attempt + 1))
        punctuation_match = restore_punctuation(words, text)
        levels = await asyncio.to_thread(clean_audio, raw, clean)
        with wave.open(str(clean), "rb") as wav:
            duration = wav.getnframes() / wav.getframerate()
        result = {"id": line_id, "text": text, "voice": voice, "rate": rate, "pitch": pitch,
                  "raw": portable_path(raw), "clean": portable_path(clean), "duration": duration,
                  "words": words, "gap_after": float(line.get("gap_after", .12)),
                  "punctuation_match": punctuation_match, "loudness": levels,
                  "fingerprint": fingerprint}
        metadata_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
        print(f"synthesized {line_id}: {duration:.2f}s, punctuation match {punctuation_match:.3f}", flush=True)
        return result


def timestamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"


def captions(words):
    groups = []
    group = []
    for word in words:
        prospective = " ".join(w["text"] for w in [*group, word])
        if group and (len(prospective) > 78 or word["end"] - group[0]["start"] > 5.0
                      or word["start"] - group[-1]["end"] > .75):
            groups.append(group)
            group = []
        group.append(word)
        if re.search(r"[.!?][\"')]*$", word["text"]):
            groups.append(group)
            group = []
    if group:
        groups.append(group)
    blocks = []
    for index, group in enumerate(groups):
        content = " ".join(w["text"] for w in group)
        if len(content) > 42:
            spaces = [m.start() for m in re.finditer(" ", content)]
            cut = min(spaces, key=lambda n: abs(n - len(content)/2))
            content = content[:cut] + "\n" + content[cut+1:]
        end = group[-1]["end"] + .12
        if index + 1 < len(groups):
            end = min(end, groups[index+1][0]["start"] - .02)
        end = max(end, group[0]["start"] + .15)
        blocks.append(f"{index+1}\n{timestamp(group[0]['start'])} --> {timestamp(end)}\n{content}\n")
    return "\n".join(blocks)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("request", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8-sig"))
    out = args.out.resolve()
    for folder in ("voice_raw", "voice_clean"):
        (out / folder).mkdir(parents=True, exist_ok=True)
    if len({str(l["id"]) for l in request["lines"]}) != len(request["lines"]):
        raise ValueError("Duplicate line IDs")
    sem = asyncio.Semaphore(2)
    results = await asyncio.gather(*(synth_line(l, request, out, sem) for l in request["lines"]))
    words = []
    cursor_samples = 0
    with wave.open(str(out / "narration.wav"), "wb") as joined:
        joined.setnchannels(1)
        joined.setsampwidth(2)
        joined.setframerate(48000)
        for i, result in enumerate(results):
            result["start"] = cursor_samples / 48000
            with wave.open(str(project_path(result["clean"])), "rb") as source:
                if source.getparams()[:3] != (1, 2, 48000):
                    raise RuntimeError("Unexpected PCM source format")
                joined.writeframes(source.readframes(source.getnframes()))
                cursor_samples += source.getnframes()
            result["end"] = cursor_samples / 48000
            first_word_id = len(words)
            words.extend({**w, "id": f"w{first_word_id+n}", "line_id": result["id"],
                          "start": round(w["start"] + result["start"], 6),
                          "end": round(w["end"] + result["start"], 6)}
                         for n, w in enumerate(result["words"]))
            if i < len(results)-1:
                silence_samples = round(result["gap_after"] * 48000)
                joined.writeframes(b"\0\0" * silence_samples)
                cursor_samples += silence_samples
    manifest = {"provider": "Microsoft Edge online neural TTS via edge-tts", "duration": cursor_samples/48000,
                "sample_rate": 48000, "audio": portable_path(out / "narration.wav"),
                "timing_source": "TTS word boundary metadata; verify at final QC", "lines": results}
    (out / "narration_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf8")
    (out / "narration.words.json").write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf8")
    (out / "narration.srt").write_text(captions(words), encoding="utf8")
    print(f"DONE: {len(results)} lines, {len(words)} words, {cursor_samples/48000:.2f}s", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
