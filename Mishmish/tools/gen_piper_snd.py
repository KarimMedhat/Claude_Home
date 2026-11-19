"""Phonics sounds in the game's own English voice (Piper en_US-lessac-medium), built to be clear:
- vowels, m n l r ng and vowel teams: the voice says them as before (clean, no creak)
- popping letters (b d t g p k j ch h w y qu): several spellings tried, kept only when Whisper hears the right letter
- hiss letters (s sh f th z v): cut from the voice's own words (sun, ship...), lengthened by smooth overlapping loops
usage: gen_piper_snd.py <old sounds dir (mp3 per key)> <voice_dir>"""
import os, sys, io, wave, json, base64, subprocess, numpy as np
from piper import PiperVoice, SynthesisConfig
from faster_whisper import WhisperModel
HERE = os.path.dirname(os.path.abspath(__file__))
old_dir, vdir = sys.argv[1], sys.argv[2]
V = PiperVoice.load(os.path.join(HERE, 'en_US-lessac-medium.onnx')); SR = V.config.sample_rate
WM = WhisperModel('small', device='cpu', compute_type='int8')

def say_text(t, ls=1.1):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf: V.synthesize_wav(t, wf, syn_config=SynthesisConfig(length_scale=ls))
    buf.seek(0)
    with wave.open(buf) as wf: return np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
def say_ph(ph, ls=1.1):
    a = np.asarray(V.phoneme_ids_to_audio(V.phonemes_to_ids(list(ph)), SynthesisConfig(length_scale=ls)))
    return a.astype(np.float32) / (32768 if a.dtype == np.int16 else 1)
def trim(a, thr=.02):
    idx = np.where(np.abs(a) > thr * np.abs(a).max())[0]
    return a[max(0, idx[0] - int(.01 * SR)): idx[-1] + int(.03 * SR)] if len(idx) else a
def hear(a):
    pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0', '-af', 'apad=pad_dur=0.6', '-ar', '16000', '-f', 'f32le', 'pipe:1'],
                                       input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32)
    segs, _ = WM.transcribe(pcm, language='en', beam_size=5, initial_prompt='Phonics sounds: buh, duh, tuh, guh, puh, kuh, juh, chuh, huh, wuh, yuh, kwuh.')
    return ' '.join(s.text.strip() for s in segs).strip()
def mp3(a):
    return subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0', '-af', 'apad=pad_dur=0.05', '-ar', '22050', '-b:a', '48k', '-f', 'mp3', 'pipe:1'],
                          input=np.clip(a, -.98, .98).astype(np.float32).tobytes(), capture_output=True, check=True).stdout
def hiss_share(a):
    n = 1024; fr = [a[i:i + n] * np.hanning(n) for i in range(0, len(a) - n, 256)]
    S = np.mean([np.abs(np.fft.rfft(x)) ** 2 for x in fr], axis=0); f = np.fft.rfftfreq(n, 1 / SR); return S[f > 3500].sum() / S.sum()
def hnr(x):
    n, hop = int(.04 * SR), int(.01 * SR); lo, hi = int(SR / 400), int(SR / 75); vals = []
    e = [np.sqrt((x[i:i + n] ** 2).mean()) for i in range(0, len(x) - n, hop)]
    for k, i in enumerate(range(0, len(x) - n, hop)):
        if e[k] < .3 * max(e): continue
        f = (x[i:i + n] - x[i:i + n].mean()) * np.hanning(n); ac = np.correlate(f, f, 'full')[n - 1:]
        w = np.correlate(np.hanning(n), np.hanning(n), 'full')[n - 1:]; ac = ac / (w + 1e-9); ac /= ac[0] + 1e-12
        r = min(ac[lo:hi].max(), .9999)
        if r > .3: vals.append(10 * np.log10(r / (1 - r)))
    return float(np.median(vals)) if vals else float('nan')

snd, log = {}, []
# 1) keep the clean ones from the first recording
KEEP = {'a', 'e', 'i', 'o', 'u', 'm', 'n', 'l', 'r', 'ng', 'x', 'ee', 'ai', 'oa', 'oo', 'ow', 'ar', 'or', 'er', 'A', 'E', 'I', 'O', 'U'}
for k in KEEP:
    snd[k] = base64.b64encode(open(os.path.join(old_dir, ('U_' if k.isupper() else '') + k + '.mp3'), 'rb').read()).decode()
# 2) popping letters
POP = {'b': ('b', ['buh', 'ˈbʌ', 'bʌː']), 'd': ('d', ['duh', 'ˈdʌ', 'dʌː']), 't': ('t', ['tuh', 'ˈtʌ', 'tʌː']), 'g': ('g', ['guh', 'ˈɡʌ', 'ɡʌː']),
       'p': ('p', ['puh', 'ˈpʌ', 'pʌː']), 'k': ('kcq', ['kuh', 'ˈkʌ', 'kʌː']), 'j': ('jg', ['juh', 'ˈdʒʌ', 'dʒʌː']), 'ch': ('c', ['chuh', 'ˈtʃʌ', 'tʃʌː']),
       'h': ('h', ['huh', 'ˈhʌ', 'hʌː']), 'w': ('w', ['wuh', 'ˈwʌ', 'wʌː']), 'y': ('y', ['yuh', 'ˈjʌ', 'jʌː']), 'qu': ('qk', ['kwuh', 'ˈkwʌ', 'kwʌː'])}
for k, (ok, cands) in POP.items():
    pick = None
    for c in cands:
        a = trim(say_ph(c) if not c.isascii() else say_text(c)); h = hear(a); good = bool(h) and h.lstrip('"\'.').lower()[:1] in ok
        log.append(f'{k:3} {c!r:8} -> {h!r:18} hnr {hnr(a):5.1f} {"OK" if good else ""}')
        if pick is None: pick = a
        if good: pick = a; break
    snd[k] = base64.b64encode(mp3(pick)).decode()
snd['q'] = snd['qu']
# 3) hiss letters: noise shaped with the exact spectrum of the hiss in the voice's own words (smooth, steady, natural)
SRC = {'s': ('sun', .5), 'sh': ('ship', .5), 'f': ('fan', .45), 'th': ('thumb', .45), 'z': ('zoo', .3), 'v': ('van', .3)}
rng = np.random.default_rng(7)
for k, (w, thr) in SRC.items():
    a = say_text(w, 2.0); n, hop = int(.025 * SR), int(.005 * SR); f = np.fft.rfftfreq(n, 1 / SR); hs = []
    for i in range(0, len(a) - n, hop):
        S = np.abs(np.fft.rfft(a[i:i + n] * np.hanning(n))) ** 2; hs.append(S[f > 3500].sum() / (S.sum() + 1e-12))
    pk = int(np.argmax(hs)); lo = hi = pk
    while lo > 0 and hs[lo - 1] >= thr: lo -= 1
    while hi < len(hs) - 1 and hs[hi + 1] >= thr: hi += 1
    seg = a[lo * hop: hi * hop + n]
    N = 2048; fr = [seg[i:i + N] * np.hanning(len(seg[i:i + N])) for i in range(0, max(1, len(seg) - N // 2), N // 4)]
    P = np.mean([np.abs(np.fft.rfft(x, N)) ** 2 for x in fr], axis=0)
    P = np.convolve(P, np.ones(9) / 9, 'same')                               # smooth envelope
    L = int(.6 * SR); spec = np.fft.rfft(rng.standard_normal(L)); fq = np.fft.rfftfreq(L, 1 / SR)
    out = np.fft.irfft(spec * np.sqrt(np.interp(fq, np.fft.rfftfreq(N, 1 / SR), P)), L)
    if k in ('z', 'v'):                                                       # voiced: add a soft hum from the voice's pitch
        t = np.arange(L) / SR; f0 = 190.0
        hum = sum(np.sin(2 * np.pi * f0 * h * t) / h ** 1.5 for h in range(1, 12))
        out = out / np.sqrt((out ** 2).mean()) * (.6 if k == 'z' else .35) + hum / np.sqrt((hum ** 2).mean()) * (.8 if k == 'v' else .55)
    fd = int(.06 * SR); out[:fd] *= np.linspace(0, 1, fd) ** 2; out[-fd:] *= np.linspace(1, 0, fd) ** 2
    out = out / (np.sqrt((out ** 2).mean()) + 1e-9) * .07
    snd[k] = base64.b64encode(mp3(out)).decode()
    log.append(f'{k:3} from {w!r}: hiss piece {len(seg) / SR:.2f}s -> {L / SR:.2f}s, hiss {hiss_share(out):.0%}')
json.dump(snd, open(os.path.join(vdir, 'v_snd.json'), 'w'), separators=(',', ':'))
print('\n'.join(log)); print(len(snd), 'sounds')
