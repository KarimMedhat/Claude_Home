"""Make several takes of each line with NAMAA-Egyptian + the game voice, keep the one the recognizer hears closest to the text."""
import os, sys, subprocess, difflib, torch, torchaudio as ta, numpy as np
from huggingface_hub import snapshot_download
from safetensors.torch import load_file
from chatterbox import mtl_tts
from faster_whisper import WhisperModel
torch.set_num_threads(4)
D = os.path.dirname(os.path.abspath(__file__))
ck = snapshot_download(repo_id='NAMAA-Space/NAMAA-Egyptian-TTS', repo_type='model')
m = mtl_tts.ChatterboxMultilingualTTS.from_pretrained(device='cpu')
m.t3.load_state_dict(load_file(f'{ck}/t3_mtl23ls_v2.safetensors', device='cpu')); m.t3.to('cpu').eval()
asr = WhisperModel('small', device='cpu', compute_type='int8')
norm = lambda t: ''.join(c for c in t.replace('ة', 'ه').replace('ى', 'ي').replace('أ', 'ا').replace('إ', 'ا') if c.isalpha() or c == ' ')
lines = [('math', 'يلا نتعلم الجمع. لو معاكي تلات تفاحات، وجبتي اتنين كمان، يبقى معاكي خمس تفاحات.'),
         ('social', 'مصر فيها نهر النيل، وهو أطول نهر في العالم، والناس من زمان بيزرعوا جنبه.')]
for name, txt in lines:
    best = None
    for seed in [1, 2, 3, 4]:
        torch.manual_seed(seed)
        w = m.generate(txt, language_id='ar', audio_prompt_path=os.path.join(D, 'ref_long.wav'), cfg_weight=0.3, exaggeration=0.5)
        a = ta.functional.resample(w, m.sr, 16000)[0].numpy().astype(np.float32)
        heard = ' '.join(s.text.strip() for s in asr.transcribe(a, language='ar', beam_size=5)[0])
        score = difflib.SequenceMatcher(None, norm(txt), norm(heard)).ratio()
        print(name, seed, round(score, 3), heard, flush=True)
        if not best or score > best[0]: best = (score, w, seed)
    p = os.path.join(D, f'best_{name}.wav'); ta.save(p, best[1], m.sr)
    os.system(f"ffmpeg -loglevel error -y -i {p} -ac 1 -b:a 64k {p[:-4]}.mp3"); print('kept', name, 'seed', best[2], round(best[0], 3))
