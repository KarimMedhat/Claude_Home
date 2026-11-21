"""Math line made phrase by phrase: best of 5 takes per phrase (recognizer score), joined with short natural pauses."""
import os, re, difflib, torch, torchaudio as ta, numpy as np
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
norm = lambda t: ''.join(c for c in re.sub(r'[ً-ْ]', '', t).replace('ة', 'ه').replace('ى', 'ي').replace('أ', 'ا') if c.isalpha() or c == ' ').replace('ث', 'ت')
phrases = [('يلا نتعلم الجمع!', .45), ('لو معاكي تلات تفاحات،', .25), ('وجبتي اتنين كمان،', .25), ('يبقى معاكي خمس تفاحات.', 0)]
out = []
for txt, gap in phrases:
    best = None
    for seed in range(1, 6):
        torch.manual_seed(seed)
        w = m.generate(txt, language_id='ar', audio_prompt_path=os.path.join(D, 'ref_long.wav'), cfg_weight=0.3, exaggeration=0.55)
        a = ta.functional.resample(w, m.sr, 16000)[0].numpy().astype(np.float32)
        heard = ' '.join(s.text.strip() for s in asr.transcribe(a, language='ar', beam_size=5)[0])
        sc = difflib.SequenceMatcher(None, norm(txt), norm(heard)).ratio()
        if not best or sc > best[0]: best = (sc, w, heard)
    print(round(best[0], 3), txt, '→', best[2], flush=True)
    out += [best[1], torch.zeros(1, int(m.sr * gap))]
w = torch.cat(out, 1); p = os.path.join(D, 'phrase_math.wav'); ta.save(p, w, m.sr)
os.system(f"ffmpeg -loglevel error -y -i {p} -af 'silenceremove=start_periods=1:start_threshold=-45dB' -ac 1 -b:a 64k {p[:-4]}.mp3")
