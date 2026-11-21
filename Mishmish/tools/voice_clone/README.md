# Mishmish Egyptian voice — how to make new lines in the same voice

The science narration (Mishmish/va/*.mp3, 3,742 lines) was recorded in one Egyptian female voice.
New lines (math, social studies, edited science) are made in that same voice by zero-shot cloning:

1. Reference: `mishmish_voice_ref.wav` — 12 s cut from `va/c3l1.mp3` (clip c3l1_s1). More references can be cut from
   any `va/<chunk>.mp3` using `va/va-index.json` ({chunk: {clipId: [byteOffset, byteLength]}}).
2. Engine: Chatterbox multilingual (`pip install chatterbox-tts`), `language_id='ar'`, `audio_prompt_path=` the reference,
   `cfg_weight=0.5, exaggeration=0.5`. Write the text in Egyptian Arabic, like the existing narration.
3. Check every new line: `asr_check.py` (faster-whisper small) must hear the sentence; regenerate with another seed if a
   word is lost. Speaker similarity with Chatterbox's voice encoder: real voice vs real voice ≈ 0.94, clone ≈ 0.93,
   a different voice ≈ 0.64 (test run in `clone_test.py`).
4. Pack like the existing chunks (mp3 22050 Hz mono ~48 kbps, appended to a chunk + byte index) and add
   `va-h.json` entries = djb2/base36 hash of the exact on-screen text (see README in `va/`), then bump AR_VER.
