"""Phonics sounds (voice/v_snd.json) + any foundation words missing from voice/v_<letter>.json.
Usage: python3 -I gen_fnd.py <fnd.js> <voice_dir>"""
import re, sys, os, json, wave, io, base64, subprocess
from piper import PiperVoice, SynthesisConfig
import numpy as np

js_path, vdir = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
v = PiperVoice.load(os.path.join(HERE, 'en_US-lessac-medium.onnx'))
SR = v.config.sample_rate
AF = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.05'

def to_mp3(wav_bytes):
    return subprocess.run(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-af', AF, '-ac', '1', '-ar', '22050', '-b:a', '32k', '-f', 'mp3', 'pipe:1'],
                          input=wav_bytes, capture_output=True, check=True).stdout

def wav_of(audio):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        a = np.asarray(audio)
        if a.dtype != np.int16: a = (np.clip(a, -1, 1) * 32767).astype(np.int16)
        wf.writeframes(a.tobytes())
    return buf.getvalue()

# --- phonics sounds: IPA fed straight to the voice ---
STOP, CONT, VOW = 1.0, 1.7, 1.5
SND = {
  'b': ('bə', STOP), 'd': ('də', STOP), 'g': ('ɡə', STOP), 'p': ('pə', STOP), 't': ('tə', STOP), 'k': ('kə', STOP),
  'j': ('dʒə', STOP), 'ch': ('tʃə', STOP), 'h': ('hə', STOP), 'w': ('wə', STOP), 'y': ('jə', STOP), 'qu': ('kwə', STOP), 'q': ('kwə', STOP),
  'x': ('ks', CONT), 's': ('sːː', CONT), 'f': ('fːː', CONT), 'm': ('mːː', CONT), 'n': ('nːː', CONT), 'l': ('lːː', CONT), 'r': ('ɹːː', CONT),
  'v': ('vːː', CONT), 'z': ('zːː', CONT), 'sh': ('ʃːː', CONT), 'th': ('θːː', CONT), 'ng': ('ŋːː', CONT),
  'a': ('ˈæː', VOW), 'e': ('ˈɛː', VOW), 'i': ('ˈɪː', VOW), 'o': ('ˈɑː', VOW), 'u': ('ˈʌː', VOW),
  'A': ('ˈeɪ', VOW), 'E': ('ˈiː', VOW), 'I': ('ˈaɪ', VOW), 'O': ('ˈoʊ', VOW), 'U': ('jˈuː', VOW),
  'ee': ('ˈiː', VOW), 'ai': ('ˈeɪ', VOW), 'oa': ('ˈoʊ', VOW), 'oo': ('ˈuː', VOW), 'ow': ('ˈaʊ', VOW),
  'ar': ('ˈɑːɹ', VOW), 'or': ('ˈɔːɹ', VOW), 'er': ('ˈɜː˞', VOW),
}
snd = {}
for k, (ph, ls) in SND.items():
    ids = v.phonemes_to_ids(list(ph))
    audio = v.phoneme_ids_to_audio(ids, SynthesisConfig(length_scale=ls))
    snd[k] = base64.b64encode(to_mp3(wav_of(audio))).decode()
json.dump(snd, open(os.path.join(vdir, 'v_snd.json'), 'w'), separators=(',', ':'))
print('sounds', len(snd), os.path.getsize(os.path.join(vdir, 'v_snd.json')))

# --- words ---
js = open(js_path, encoding='utf-8').read()
words = set()
for lst in re.findall(r'fwList\("([^"]+)"\)', js):
    words |= {x.split('|')[0] for x in lst.split(';')}
words |= set(re.findall(r"\['[a-z]','([a-z-]+)','", js))                       # letter key words
words |= set(re.search(r'F_SIGHT = "([^"]+)"', js).group(1).lower().split())
for blk in ('F_PAIRS_BD', 'F_PAIRS_E', 'F_BD_FILL'):
    body = re.search(blk + r' = (\[.*?\]\]);', js, re.S).group(1)
    words |= set(re.findall(r"'([a-z]+)'", body))
for s in re.findall(r'\["([A-Z][^"]+\.)"', js):
    words |= {w.lower() for w in re.findall(r"[A-Za-z]+", s)}
words |= {'great', 'job', 'super', 'well', 'done', 'amazing', 'you', 'got', 'it', 'excellent', 'cot', 'cut', 'bag', 'big', 'bug'}
added = 0
for letter in sorted({w[0] for w in words}):
    path = os.path.join(vdir, f'v_{letter}.json')
    d = json.load(open(path)) if os.path.exists(path) else {}
    miss = sorted(w for w in words if w[0] == letter and w not in d)
    for w in miss:
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            v.synthesize_wav(w.replace('-', ' ') if w != 'i' else 'I', wf, syn_config=SynthesisConfig(length_scale=1.1))
        d[w] = base64.b64encode(to_mp3(buf.getvalue())).decode(); added += 1
    if miss:
        json.dump(d, open(path, 'w'), separators=(',', ':')); print(letter, miss)
print('words needed', len(words), 'added', added)
