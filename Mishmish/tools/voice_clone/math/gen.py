"""Math narration in the game's Egyptian voice (approved method: NAMAA-Egyptian + the game voice, whole sentences, light Egyptian vowels, best of 3 by ASR)."""
import os, sys, json, difflib, torch, torchaudio as ta, numpy as np, time
from huggingface_hub import snapshot_download
from safetensors.torch import load_file
from chatterbox import mtl_tts
from faster_whisper import WhisperModel
torch.set_num_threads(4)
D = os.path.dirname(os.path.abspath(__file__)); REF = '/home/user/Claude_Home/Mishmish/tools/voice_clone/mishmish_voice_ref_long.wav'
ck = snapshot_download(repo_id='NAMAA-Space/NAMAA-Egyptian-TTS', repo_type='model')
m = mtl_tts.ChatterboxMultilingualTTS.from_pretrained(device='cpu')
m.t3.load_state_dict(load_file(f'{ck}/t3_mtl23ls_v2.safetensors', device='cpu')); m.t3.to('cpu').eval()
asr = WhisperModel('small', device='cpu', compute_type='int8')
strip = lambda t: ''.join(c for c in t if not ('ً' <= c <= 'ْ'))
norm = lambda t: ''.join(c for c in strip(t).replace('ة', 'ه').replace('ى', 'ي').replace('أ', 'ا').replace('إ', 'ا') if c.isalpha() or c == ' ')
os.makedirs(os.path.join(D, 'out'), exist_ok=True)
for cid, txt in json.load(open(os.path.join(D, 'lines.json'), encoding='utf-8')):
    mp3 = os.path.join(D, 'out', cid + '.mp3')
    if os.path.exists(mp3): continue
    best = None; t0 = time.time()
    for seed in [1, 2, 3]:
        torch.manual_seed(seed)
        w = m.generate(txt, language_id='ar', audio_prompt_path=REF, cfg_weight=0.3, exaggeration=0.5)
        a = ta.functional.resample(w, m.sr, 16000)[0].numpy().astype(np.float32)
        heard = ' '.join(s.text.strip() for s in asr.transcribe(a, language='ar', beam_size=5)[0])
        score = difflib.SequenceMatcher(None, norm(txt), norm(heard)).ratio()
        if not best or score > best[0]: best = (score, w, seed, heard)
        if score >= 0.93: break
    wav = os.path.join(D, 'out', cid + '.wav'); ta.save(wav, best[1], m.sr)
    os.system(f"ffmpeg -loglevel error -y -i {wav} -ar 22050 -ac 1 -b:a 48k {mp3}"); os.remove(wav)
    print(cid, 'seed', best[2], round(best[0], 3), round(time.time() - t0), 's |', best[3], flush=True)
print('ALL DONE')
