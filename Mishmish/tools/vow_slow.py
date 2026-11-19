"""Short vowels a e i o u, said slower so they last about half a second."""
import os, sys, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_kok.py')).read()
sys.argv = ['x', '', sys.argv[1]]
exec(src[:src.index('snd, log = {}, []')])
path = os.path.join(sys.argv[2], 'v_snd.json'); d = json.load(open(path))
for k, ipa in {'a': 'æ', 'e': 'ɛ', 'i': 'ɪ', 'o': 'ɑ', 'u': 'ʌ'}.items():
    a, sr = synth(ipa, True, 0.55); d[k] = base64.b64encode(mp3(a, sr)).decode(); print(k, round(len(a) / sr, 2), 's')
json.dump(d, open(path, 'w'), separators=(',', ':'))
