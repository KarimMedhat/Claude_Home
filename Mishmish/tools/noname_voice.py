"""Re-record the two praise clips that say the child's name, without it, and write a g.json for the nameless copy.
usage: noname_voice.py <tts dir with ar_JO-kareem-medium.onnx> <src g.json> <out g.json>"""
import base64, io, json, subprocess, sys, wave
from piper import PiperVoice, SynthesisConfig
tts, src, out = sys.argv[1:4]
v = PiperVoice.load(tts + '/ar_JO-kareem-medium.onnx')
cfg = SynthesisConfig(length_scale=1.0, noise_scale=0.6, noise_w_scale=0.7)
g = json.load(open(src))
for cid, text in {'g_ok1': 'رائع جدًا!', 'g_done': 'أحسنتِ! أنتِ ذكية جدًا.'}.items():
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf: v.synthesize_wav(text, wf, syn_config=cfg)
    mp3 = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-af', 'apad=pad_dur=0.15', '-ac', '1', '-ar', '16000', '-b:a', '24k', '-f', 'mp3', 'pipe:1'],
                         input=buf.getvalue(), capture_output=True, check=True).stdout
    g[cid] = base64.b64encode(mp3).decode()
json.dump(g, open(out, 'w'), separators=(',', ':'))
print('ok', len(g))
