import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
for f in sys.argv[1:]:
    pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', '16000', '-f', 'f32le', 'pipe:1'], capture_output=True).stdout, np.float32)
    segs, _ = m.transcribe(pcm, language='ar', beam_size=5)
    print(f.split('/')[-1], '→', ' '.join(s.text.strip() for s in segs))
