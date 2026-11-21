"""Can we speak NEW lines in the recorded Mishmish voice? Zero-shot cloning with Chatterbox (multilingual) from a 12 s reference,
then a speaker-similarity check with Chatterbox's own voice encoder: original-vs-original, clone-vs-original, other-voice-vs-original."""
import os, sys, time, torch, torchaudio as ta, numpy as np, librosa
from chatterbox import mtl_tts
from chatterbox.models.voice_encoder import VoiceEncoder
torch.set_num_threads(4)
D = os.path.dirname(os.path.abspath(__file__))
m = mtl_tts.ChatterboxMultilingualTTS.from_pretrained(device='cpu')
lines = [('math', 'يلا نتعلم الجمع. لو معاكي تلات تفاحات، وجبتي اتنين كمان، يبقى معاكي خمس تفاحات.'),
         ('social', 'مصر فيها نهر النيل، وهو أطول نهر في العالم، والناس من زمان بيزرعوا جنبه.')]
for name, txt in lines:
    for cfg, ex in [(0.5, 0.5)]:
        t0 = time.time(); torch.manual_seed(11)
        w = m.generate(txt, language_id='ar', audio_prompt_path=os.path.join(D, 'ref.wav'), cfg_weight=cfg, exaggeration=ex)
        p = os.path.join(D, f'clone_{name}.wav'); ta.save(p, w, m.sr)
        os.system(f"ffmpeg -loglevel error -y -i {p} -ac 1 -b:a 64k {p[:-4]}.mp3")
        print(name, round(w.shape[1] / m.sr, 1), 's in', round(time.time() - t0), 's', flush=True)
ve = m.ve
def emb(path):
    a, sr = librosa.load(path, sr=16000, mono=True)
    return ve.embeds_from_wavs([a], sample_rate=16000)[0]
ref = emb(os.path.join(D, 'ref.wav'))
cos = lambda a, b: float(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b))
for label, f in [('original (another lesson clip)', 'c3l1_s3.mp3'), ('clone: math', 'clone_math.wav'), ('clone: social', 'clone_social.wav')]:
    print(f'{label:34} similarity to the real voice: {cos(ref, emb(os.path.join(D, f))):.3f}')
other = os.path.join(D, '..', 'tts', 'test.wav')
if os.path.exists(other): print(f'{"a different voice (old Piper male)":34} similarity: {cos(ref, emb(other)):.3f}')
