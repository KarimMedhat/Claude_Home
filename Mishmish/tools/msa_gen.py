"""Record standard-Arabic narration with Piper (ar_JO-kareem-medium, automatic diacritics) and pack into voice_ar/<chapter>.json.
usage: msa_gen.py <narr.json> <outdir> <packdir>"""
import base64, io, json, os, re, subprocess, sys, wave
from piper import PiperVoice, SynthesisConfig
HERE = os.path.dirname(os.path.abspath(__file__))
narr, out, pack = sys.argv[1:4]
os.makedirs(out, exist_ok=True); os.makedirs(pack, exist_ok=True)
v = PiperVoice.load(os.path.join(HERE, 'ar_JO-kareem-medium.onnx'))
cfg = SynthesisConfig(length_scale=1.0, noise_scale=0.6, noise_w_scale=0.7)
items = json.load(open(narr, encoding='utf-8'))
packs = {}
for i, x in enumerate(items):
    mp3 = os.path.join(out, x['id'] + '.mp3')
    txt = re.sub(r'[«»"()]', '', x['say'])
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        v.synthesize_wav(txt, wf, syn_config=cfg)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'pipe:0', '-af', 'apad=pad_dur=0.15', '-ac', '1', '-ar', '22050', '-b:a', '40k', mp3], input=buf.getvalue(), check=True)
    ch = re.match(r'(c\d+|g)', x['id']).group(1)
    packs.setdefault(ch, {})[x['id']] = base64.b64encode(open(mp3, 'rb').read()).decode()
    if i % 50 == 0: print(i, x['id'], flush=True)
for k, d in packs.items():
    p = os.path.join(pack, k + '.json')
    json.dump(d, open(p, 'w'), separators=(',', ':'))
    print(k, len(d), round(os.path.getsize(p) / 1e6, 2), 'MB')
