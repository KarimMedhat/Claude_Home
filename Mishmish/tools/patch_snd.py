"""Re-record only the given sound keys of voice/v_snd.json with the settings in gen_kok.py."""
import os, sys, json, base64, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_kok.py')).read()
head = src[:src.index('snd, log = {}, []')]          # imports, models, helpers and the SND table
sys.argv = ['x', '', sys.argv[1]] + sys.argv[2:]
exec(head)
vdir, keys = sys.argv[2], sys.argv[3:]
path = os.path.join(vdir, 'v_snd.json'); d = json.load(open(path))
for k in keys:
    txt, ph = SND[k][1][0]
    a, sr = synth(txt, ph); d[k] = base64.b64encode(mp3(a, sr)).decode(); print(k, repr(txt), '->', hear(a, sr))
json.dump(d, open(path, 'w'), separators=(',', ':'))
