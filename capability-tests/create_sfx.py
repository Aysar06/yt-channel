"""Create four restrained original editorial sound effects; no sampled media."""
import json
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

root = Path(__file__).resolve().parent.parent
out = root / 'VIDEO_PROJECT/03_AUDIO/sfx'
out.mkdir(parents=True, exist_ok=True)
sr = 48000
rng = np.random.default_rng(914217)


def save(name, sound, peak_db, description):
    sound = np.asarray(sound, dtype=np.float64)
    sound -= sound.mean()
    fade = min(len(sound)//2, int(.008*sr))
    sound[:fade] *= np.linspace(0, 1, fade)
    sound[-fade:] *= np.linspace(1, 0, fade)
    sound *= 10**(peak_db/20) / max(np.abs(sound).max(), 1e-10)
    file = out / f'{name}.wav'
    with wave.open(str(file), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(np.rint(sound*32767).astype('<i2').tobytes())
    return {'name': name, 'file': str(file.relative_to(root / 'VIDEO_PROJECT')),
            'duration': len(sound)/sr, 'peak_dbfs': peak_db,
            'description': description, 'source': 'Original procedural synthesis',
            'third_party_samples': False, 'seed': 914217}


records = []
t = np.arange(int(.12*sr))/sr
noise = sosfilt(butter(2, [800, 7200], btype='bandpass', fs=sr, output='sos'), rng.normal(size=len(t)))
click = noise*np.exp(-t*95) + .18*np.sin(2*np.pi*1250*t)*np.exp(-t*75)
records.append(save('archive-click', click, -22, 'Short muted file/card click for date and source reveals.'))
t = np.arange(int(.65*sr))/sr
noise = sosfilt(butter(2, [300, 3000], btype='bandpass', fs=sr, output='sos'), rng.normal(size=len(t)))
whoosh = noise * np.sin(np.pi*t/t[-1])**2
records.append(save('soft-page-sweep', whoosh, -26, 'Soft filtered sweep for one major document transition.'))
t = np.arange(int(1.2*sr))/sr
phase = 2*np.pi*(48*t + 44*.18*(1-np.exp(-t/.18)))
hit = np.sin(phase)*np.exp(-4.5*t) + .12*np.sin(2*np.pi*97*t)*np.exp(-9*t)
records.append(save('low-door-hit', hit, -23, 'Subtle falling low hit for removal/cancellation reveals.'))
t = np.arange(int(.9*sr))/sr
tone = np.sin(2*np.pi*440*t)*np.exp(-5*t) + .42*np.sin(2*np.pi*660*t)*np.exp(-6*t)
records.append(save('quiet-discovery', tone, -28, 'Quiet two-tone discovery marker.'))
(out / 'sfx_manifest.json').write_text(json.dumps(records, indent=2), encoding='utf8')
licenses = root / 'VIDEO_PROJECT/04_MEDIA/licenses'
licenses.mkdir(parents=True, exist_ok=True)
(licenses / 'original_sfx.md').write_text('# Original sound effects\n\nFour mono 48 kHz WAV effects were synthesized for this production with NumPy and SciPy using oscillators, seeded noise, filtering and smooth envelopes. No third-party recordings, melodies, samples or media were used.\n\n' + '\n'.join(f"- `{r['file']}` — {r['description']}" for r in records) + '\n', encoding='utf8')
print(json.dumps(records, indent=2))
