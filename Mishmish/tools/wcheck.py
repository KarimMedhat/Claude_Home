"""Transcribe short clips with Whisper to check that each sound is heard as the right consonant.
usage: wcheck.py <file or dir>..."""
import os, sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
files = []
for a in sys.argv[1:]:
    files += sorted(os.path.join(a, f) for f in os.listdir(a)) if os.path.isdir(a) else [a]
for f in files:
    pcm = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-af','apad=pad_dur=0.6','-ac','1','-ar','16000','-f','f32le','pipe:1'],capture_output=True,check=True).stdout, np.float32)
    segs, _ = m.transcribe(pcm, language='en', beam_size=5, initial_prompt='Phonics sounds: buh, duh, tuh, guh, puh, kuh, mmm, sss, ah.')
    print(os.path.basename(f), '→', ' '.join(s.text.strip() for s in segs) or '(nothing)', flush=True)
