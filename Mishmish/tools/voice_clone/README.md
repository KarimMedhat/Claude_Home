# Mishmish Egyptian voice — how to make new lines in the same voice

The science narration (Mishmish/va/*.mp3, 3,742 lines) was recorded in one Egyptian female voice.
New lines (math, social studies, edited science) are made in that same voice by zero-shot cloning:

1. Reference: `mishmish_voice_ref.wav` — 12 s cut from `va/c3l1.mp3` (clip c3l1_s1). More references can be cut from
   any `va/<chunk>.mp3` using `va/va-index.json` ({chunk: {clipId: [byteOffset, byteLength]}}).
2. Engine: **NAMAA-Egyptian-TTS** (Chatterbox multilingual fine-tuned on Egyptian dialect; load the base model, then
   `t3.load_state_dict(NAMAA t3_mtl23ls_v2.safetensors)`), `language_id='ar'`, reference `mishmish_voice_ref_long.wav`
   (26 s from c3l1_s1 + c3l1_s3), `cfg_weight=0.3, exaggeration=0.5`. Write the text in Egyptian Arabic.
   `best_of.py` makes 4 takes per line and keeps the one the recognizer hears best (score ≈ 0.97).
   The plain multilingual model keeps the voice but sounds less colloquial — the user preferred the Egyptian model's fluency.
3. Check every new line: `asr_check.py` (faster-whisper small) must hear the sentence; regenerate with another seed if a
   word is lost. Speaker similarity with Chatterbox's voice encoder: real voice vs real voice ≈ 0.94, clone ≈ 0.93,
   a different voice ≈ 0.64 (test run in `clone_test.py`).
4. Pack like the existing chunks (mp3 22050 Hz mono ~48 kbps, appended to a chunk + byte index) and add
   `va-h.json` entries = djb2/base36 hash of the exact on-screen text (see README in `va/`), then bump AR_VER.


## Don't: phrase-by-phrase
`phrase_by_phrase.py` (each phrase made alone, then joined) sounded much worse to the user (sample 6) than whole sentences
(sample 4). Always generate whole sentences with best_of.py. Open issue: some words get formal-Arabic vowels instead of
Egyptian ones (e.g. «نتعلم» should sound نِتْعَلِّم).
