"""Foundation voice (Kokoro af_heart, clear female US English).
- phonics sounds  -> voice/v_snd.json   (each consonant checked with Whisper; first candidate heard right wins)
- words/sentences -> voice/k_<letter>.json  (keys: lowercase text without . ! ?)
usage: gen_kok.py <index.html> <voice_dir>"""
import os, sys, re, io, json, base64, subprocess, numpy as np
from kokoro_onnx import Kokoro
from faster_whisper import WhisperModel
HERE = os.path.dirname(os.path.abspath(__file__))
src, vdir = sys.argv[1], sys.argv[2]
K = Kokoro(os.path.join(HERE, 'kok/kokoro-v1.0.onnx'), os.path.join(HERE, 'kok/voices-v1.0.bin'))
VOICE = 'af_heart'
WM = WhisperModel('small', device='cpu', compute_type='int8')
AF = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.05'

def synth(txt, ph=False, speed=0.85):
    a, sr = K.create(txt, voice=VOICE, speed=speed, lang='en-us', is_phonemes=ph)
    return np.asarray(a, np.float32), sr
def mp3(a, sr):
    return subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', 'pipe:0', '-af', AF, '-ac', '1', '-ar', '22050', '-b:a', '40k', '-f', 'mp3', 'pipe:1'],
                          input=a.tobytes(), capture_output=True, check=True).stdout
def hear(a, sr):
    pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(sr), '-ac', '1', '-i', 'pipe:0', '-af', 'apad=pad_dur=0.6', '-ar', '16000', '-f', 'f32le', 'pipe:1'],
                                       input=a.tobytes(), capture_output=True, check=True).stdout, np.float32)
    segs, _ = WM.transcribe(pcm, language='en', beam_size=5, initial_prompt='Phonics sounds: buh, duh, tuh, guh, puh, kuh, juh, chuh, mmm, sss, fff.')
    return ' '.join(s.text.strip() for s in segs).strip()

# sound key -> (letters Whisper may start with, candidates [(text, is_phoneme)])
C = lambda ipa, txt: [(ipa, True), (txt, False), (ipa.replace('ʌ', 'ə'), True)]
SND = {
  'b': ('b', C('bʌ', 'buh')), 'd': ('d', C('dʌ', 'duh')), 't': ('t', C('tʌ', 'tuh')), 'g': ('g', C('ɡʌ', 'guh')),
  'p': ('p', C('pʌ', 'puh')), 'k': ('ckq', C('kʌ', 'kuh')), 'j': ('jg', C('ʤʌ', 'juh')), 'ch': ('cj', [('ʧʌ', True)]),
  'h': ('h', C('hʌ', 'huh')), 'w': ('w', C('wʌ', 'wuh')), 'y': ('y', C('jʌ', 'yuh')), 'qu': ('qk', C('kwʌ', 'kwuh')), 'q': ('qk', C('kwʌ', 'kwuh')),
  's': ('sz', [('sːː', True)]), 'f': ('ft', [('fːː', True)]), 'm': ('m', [('mːː', True)]), 'n': ('n', [('nːː', True)]),
  'l': ('l', [('lːː', True)]), 'r': ('r', [('ɹːː', True)]), 'v': ('v', [('vːː', True)]), 'z': ('z', [('zːː', True)]),
  'sh': ('s', [('ʃːː', True)]), 'th': ('t', [('θːː', True)]),
  'ng': ('nu', [('ʌŋ', True)]), 'x': ('ex', [('ks', True), ('ks', False)]),
}
VOW = {'a': ('æ', True), 'e': ('ɛ', True), 'i': ('ɪ', True), 'o': ('ɑ', True), 'u': ('ʌ', True),
       'A': ('ay', False), 'E': ('ee', False), 'I': ('eye', False), 'O': ('oh', False), 'U': ('you', False),
       'ee': ('ee', False), 'ai': ('ay', False), 'oa': ('oh', False), 'oo': ('oo', False), 'ow': ('ow', False),
       'ar': ('ar', False), 'or': ('or', False), 'er': ('er', False)}
snd, log = {}, []
for key, (ok, cands) in SND.items():
    best = None
    for txt, ph in cands:
        a, sr = synth(txt, ph); h = hear(a, sr); good = bool(h) and h.lstrip('"\'').lower()[:1] in ok
        log.append(f'{key}: {txt!r} -> {h!r} {"OK" if good else ""}')
        if best is None: best = (a, sr)
        if good: best = (a, sr); break
    snd[key] = base64.b64encode(mp3(*best)).decode()
for key, (txt, ph) in VOW.items():
    a, sr = synth(txt, ph, 0.8); snd[key] = base64.b64encode(mp3(a, sr)).decode()
json.dump(snd, open(os.path.join(vdir, 'v_snd.json'), 'w'), separators=(',', ':'))
print('\n'.join(log))

# --- words and sentences used by the foundation section ---
js = open(src, encoding='utf-8').read()
i = js.index('/* ============ FOUNDATION'); js = js[i:js.index('/* ============ WORD GYM', i)]
texts = set()
for lst in re.findall(r'fwList\("([^"]+)"\)', js): texts |= {x.split('|')[0] for x in lst.split(';')}
texts |= set(re.findall(r"\['[a-z]','([a-z-]+)','", js))
texts |= set(re.search(r'F_SIGHT = "([^"]+)"', js).group(1).split())
for blk in ('F_PAIRS_BD', 'F_PAIRS_E', 'F_BD_FILL'):
    texts |= set(re.findall(r"'([a-z]+)'", re.search(blk + r' = (\[.*?\]\]);', js, re.S).group(1)))
texts |= set(re.findall(r'\["([A-Z][^"]+\.)"', js))
texts |= set(re.findall(r"w:([a-z]+)", js)) | {'panda', 'queen', 'great job', 'super', 'well done', 'amazing', 'you got it', 'excellent', 'was', 'saw', 'on', 'no', 'bag', 'big', 'bug', 'cot', 'cut'}
key = lambda t: re.sub(r'[.!?]', '', t).strip().lower()
packs = {}
for t in sorted(texts, key=key):
    k = key(t)
    if not k: continue
    a, sr = synth(t.replace('-', ' ') if k != 'i' else 'I', False, 0.85 if ' ' not in k else 0.9)
    packs.setdefault(k[0], {})[k] = base64.b64encode(mp3(a, sr)).decode()
for l, d in packs.items():
    json.dump(d, open(os.path.join(vdir, f'k_{l}.json'), 'w'), separators=(',', ':'))
print('words', sum(len(d) for d in packs.values()), 'packs', sorted(packs))
