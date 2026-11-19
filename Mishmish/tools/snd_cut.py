"""Hiss sounds (s, sh, z, f, v, th) cut from the start of real words said by the same voice, then lengthened.
usage: snd_cut.py <voice_dir> [--dry]"""
import os, sys, json, base64, subprocess, numpy as np
from kokoro_onnx import Kokoro
HERE = os.path.dirname(os.path.abspath(__file__))
K = Kokoro(os.path.join(HERE, 'kok/kokoro-v1.0.onnx'), os.path.join(HERE, 'kok/voices-v1.0.bin'))
vdir, dry = sys.argv[1], '--dry' in sys.argv
SRC = {'s': 'sun', 'sh': 'ship', 'z': 'zoo', 'f': 'fan', 'v': 'van', 'th': 'thumb'}
TARGET = .65

def frames(a, sr, win=.025, hop=.01):
    n, h = int(win * sr), int(hop * sr); f = np.fft.rfftfreq(n, 1 / sr); out = []
    for i in range(0, len(a) - n, h):
        S = np.abs(np.fft.rfft(a[i:i + n] * np.hanning(n))) ** 2; tot = S.sum() + 1e-12
        out.append((i, np.sqrt((a[i:i + n] ** 2).mean()), S[f < 900].sum(), S[f > 3500].sum() / tot))
    return out
def hi_share(a, sr):
    n = 1024; fr = [a[i:i + n] * np.hanning(n) for i in range(0, len(a) - n, 256)]
    S = np.mean([np.abs(np.fft.rfft(x)) ** 2 for x in fr], axis=0); f = np.fft.rfftfreq(n, 1 / sr)
    return S[f > 3500].sum() / S.sum()
def stretch(a, sr, factor):
    chain = []
    while factor < .5: chain.append('atempo=0.5'); factor /= .5
    chain.append(f'atempo={factor:.3f}')
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', 'pipe:0', '-af', ','.join(chain), '-f', 'f32le', 'pipe:1'],
                                        input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32)
def mp3(a, sr):
    return subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', 'pipe:0', '-af', 'apad=pad_dur=0.05', '-ar', '22050', '-b:a', '48k', '-f', 'mp3', 'pipe:1'],
                          input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout

path = os.path.join(vdir, 'v_snd.json'); d = json.load(open(path))
for k, w in SRC.items():
    a, sr = K.create(w, voice='af_heart', speed=0.8, lang='en-us'); a = np.asarray(a, np.float32)
    fr = frames(a, sr); hs = [x[3] for x in fr]
    thr, ext = (.35, 4) if k in ('z', 'v') else (.5, 0)
    pk = int(np.argmax(hs)); lo = pk; hi = pk
    while lo > 0 and hs[lo - 1] >= thr: lo -= 1
    while hi < len(hs) - 1 and hs[hi + 1] >= thr: hi += 1
    lo = max(0, lo - ext)
    seg = a[fr[lo][0]: fr[hi][0] + int(.025 * sr)]
    out = stretch(seg, sr, len(seg) / sr / TARGET)
    fade = int(.04 * sr); env = np.ones(len(out)); env[:fade] = np.linspace(0, 1, fade); env[-fade:] = np.linspace(1, 0, fade)
    out = out * env; out = out / (np.sqrt((out ** 2).mean()) + 1e-9) * .07
    out = np.clip(out, -.98, .98)
    print(f'{k:3} from {w!r}: cut {len(seg)/sr:.2f}s -> {len(out)/sr:.2f}s, hiss >3.5k {hi_share(out, sr):.0%} (whole word {hi_share(a, sr):.0%})')
    if not dry: d[k] = base64.b64encode(mp3(out, sr)).decode()
if not dry: json.dump(d, open(path, 'w'), separators=(',', ':'))
