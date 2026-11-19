"""Voice clarity score: harmonics-to-noise ratio (dB) over voiced frames. Hoarse/breathy voices score low.
usage: hnr.py <json pack> <key>...   or   hnr.py <audio files>..."""
import sys, json, base64, subprocess, numpy as np
def pcm_of(b):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-ac', '1', '-ar', '16000', '-f', 'f32le', 'pipe:1'], input=b, capture_output=True, check=True).stdout, np.float32)
def hnr(x, sr=16000):
    n, hop = int(.04 * sr), int(.01 * sr); lo, hi = int(sr / 400), int(sr / 75); vals = []
    e = np.array([np.sqrt((x[i:i + n] ** 2).mean()) for i in range(0, len(x) - n, hop)])
    if not len(e): return float('nan')
    for k, i in enumerate(range(0, len(x) - n, hop)):
        if e[k] < .3 * e.max(): continue
        f = x[i:i + n] - x[i:i + n].mean(); f = f * np.hanning(n)
        ac = np.correlate(f, f, 'full')[n - 1:]; w = np.correlate(np.hanning(n), np.hanning(n), 'full')[n - 1:]
        ac = ac / (w + 1e-9); ac /= ac[0] + 1e-12
        r = ac[lo:hi].max()
        if r > .3: vals.append(10 * np.log10(min(r, .9999) / (1 - min(r, .9999))))
    return float(np.median(vals)) if vals else float('nan')
args = sys.argv[1:]
if args[0].endswith('.json'):
    d = json.load(open(args[0]))
    for k in args[1:]: print(f'{k:10} HNR {hnr(pcm_of(base64.b64decode(d[k]))):5.1f} dB')
else:
    for f in args: print(f'{f.split("/")[-1]:24} HNR {hnr(pcm_of(open(f, "rb").read())):5.1f} dB')
