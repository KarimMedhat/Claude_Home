# Fix: read English sentences as one natural sentence (whole game)

Give this file to Claude together with the game artifact.
STATUS: this is a patch plan. Nothing here was applied to the live artifact. Nothing was changed live.

## Karim's decisions (already made)
- Every question or sentence is read as ONE connected utterance. Word-by-word reading is only for deliberate single-word drills (vocabulary and phonics) and stays as it is.
- Voice: Leda (American, young, friendly) for everything that has a recording.
- A sentence with no recording: use the phone's own American English voice as ONE whole utterance, when the phone has one. Karim accepted this (voice note, Nov 25, 9:52 PM).
- If the phone has no English voice: never glue word clips. Show a clear message to the child and parent instead of staying silent.
- No spoken feedback after each answer. Spoken feedback only at the end of a set or exam (already in the ZIP: audio/feedback, audio/encouragement).
- Nothing here claims the whole game is fixed. Only 59 extra sentences are recorded (see Coverage).

## What was found (evidence from the artifact's own code, read-only)
All spoken English goes through `say(text, rate)`:
1. `veFind(text)` looks for a recorded Leda clip: a single word or verb form (`VE.idx.lex`), or a whole reading passage (`VE_PAS`). There were NO sentence clips.
2. A miss goes to `sayOld(text, rate)`.
   - With a device English voice: the whole string is ONE `SpeechSynthesisUtterance` (connected, device voice, rate 0.82).
   - Without one (the code comment says the Claude app on Android has none; `useClips` is true): `sayClips(text)` splits the sentence into words (`/[a-z][a-z']*/g`), loads one old clip per word (`voice/v_<letter>.json`) and plays them one after another with a 0.04 s gap. That is word-by-word reading.
3. `choose()` speaks the completed sentence after a correct answer (`say(full)`). The wrong-answer line `say(tapped + '. Listen again. ' + target, .75)` is glued the same way.
Verified in code: all of the above. INFERRED, not measured: that Karim's phone takes the per-word path (it matches his symptom; a desktop browser with device speech reads the sentence whole).

## Coverage of the recordings in this ZIP
- Recorded sentences (Leda): 59, `audio/sentences/SEN-001..059.mp3` (static question sentences from Unit games, see `sentences_manifest.csv`).
- Not recorded: other static sentences (exam questions, Reading Corner story lines and questions, Read Sentences, passage questions, blank questions) and every sentence the game builds at run time ("This is X. Find Y." etc.). These rely on the device American voice when it exists.
- Not checked by anyone's ears: the 59 clips were checked by speech-to-text (wording only) and a pause check. Listen to them before calling them natural.

## Changes to make

### 1. Add the 59 sentence clips to the ve pack
Put the MP3s in a new chunk (`ve/sen_1`) and in `ve-index.json` add `chunks['sen_1'] = {clipId: [offset, length]}` and a map `sen = { <veNorm key>: clipId }` (keys are in `sentences_index.json`; they use the same `veNorm`). Same packing method as the `lex_*` chunks. Bump `VE_VER`. Load `sen_` chunks in `vePrefetchWords`.

### 2. veFind looks at sentences first
```js
function veFind(text){
  if(!VE.idx || text == null) return null;
  const n = veNorm(text); if(!n) return null;
  return (VE.idx.sen && VE.idx.sen[n]) || VE.idx.lex[n] || VE.idx.lex[n.replace(/'s$/, '')]
      || (VE_PAS && VE_PAS[n]) || null;
}
```

### 3. Never read a sentence word by word
```js
// A sentence is anything that is not a single word, whatever its length ("Find the bag.", "This is a cat.", even 2 words).
// Only calls explicitly marked as a word/phonics drill may use isolated tokens.
const isSentence = (t, opts) => !(opts && opts.drill) && veNorm(t).split(' ').filter(Boolean).length >= 2;
const SENTENCE_FALLBACK = 'device';   // Karim's decision: whole-sentence device American voice
const SPEAK_COMPLETED = false;        // no spoken answer after each choice
const MISSING_SENTENCES = new Set();

function englishDeviceVoice(){
  try{ const vs = speechSynthesis.getVoices();
    return vs.find(v => /^en[-_]US/i.test(v.lang)) || vs.find(v => /^en/i.test(v.lang)) || null; }catch(e){ return null; }
}
function say(text, rate=0.82, opts){
  if(!S.sound) return;
  const vid = veFind(text);
  if(vid){ stopSpeech(); vePlay(vid).then(d => { if(d === 0 && isSentence(text, opts)) saySentenceFallback(text); }); return; }
  if(isSentence(text, opts)) return saySentenceFallback(text);
  sayOld(text, rate);              // single words and phonics: unchanged (slow rate stays)
}
function saySentenceFallback(text){
  MISSING_SENTENCES.add(veNorm(text)); console.warn('no sentence clip:', text);
  const v = englishDeviceVoice();
  if(SENTENCE_FALLBACK === 'device' && v){
    const u = new SpeechSynthesisUtterance(text);   // ONE utterance for the whole sentence
    u.lang = v.lang || 'en-US'; u.voice = v; u.rate = 1.0; u.pitch = 1.0;
    try{ speechSynthesis.cancel(); speechSynthesis.speak(u); }catch(e){}
    return;
  }
  noEnglishVoiceNotice();           // never sayClips for a sentence
}
let _nv = 0;
function noEnglishVoiceNotice(){
  if(Date.now() - _nv < 8000) return; _nv = Date.now();
  toast('الجهاز ده مفيهوش صوت إنجليزي للجُمل. ممكن تحمّلي صوت إنجليزي أمريكي من إعدادات الجهاز، أو اقري الجملة المكتوبة 📖');
}
```
In `sayOld`, change `if(useClips) return void sayClips(text);` to `if(useClips){ if(isSentence(text)) return noEnglishVoiceNotice(); return void sayClips(text); }` (sayOld receives only single words, drills and numbers after the check in `say`; any text with 2 or more words is a sentence). Pass `{drill:true}` as the third argument only at deliberate word or phonics drill call sites (vocabulary tile, letter sound, Blend & Read, the two-word verb row "base, past" buttons) that should keep isolated tokens. Single words and numbers keep working through the old clips.
Use the app's existing toast or visible banner (one short Arabic line). It must be visible, not only a console message.
The device voice is not Leda. That is Karim's accepted tradeoff. Do not describe it as Leda.

### 3b. No spoken completed answer
In `choose()`, wrap the call that speaks the completed sentence after a right answer: `if(SPEAK_COMPLETED) say(full)`. Same for any other spoken feedback after a single answer. Feedback only at the end of a set or exam. Blank questions (a sentence with ___ on screen) are read with the blank spoken as the word "blank", never with the answer: `say(q.replace('___', 'blank'))`.

### 4. Wrong-answer line in the word questions
Replace `say(b.dataset.w + '. Listen again. ' + q.w, .75)` with two separate `say` calls: the tapped word, then (after it ends, about 0.5 s) the target word. The Arabic text already says "listen again".

### 5. Keep isolated and slow playback for drills only
Single-word buttons, vocabulary drills, letter sounds and Blend & Read keep rate 0.7 and word clips. Sentences are never slowed word by word.

### 6. Check list (do this and report what you find)
- Wrap `say` temporarily to log every string; open every game, question type and exam; write the sentences that have no `sen` clip to `sentences_missing.txt`. They use the device voice (or show the notice).
- Acceptance: no call reaches `sayClips` with 2 or more words unless it is marked `{drill:true}`. Short sentences such as "Find the bag." or "This is a cat." count as sentences. On a phone with an English voice, a Sound Lab question plays as one utterance. On a phone with no English voice, the visible notice appears and nothing is read word by word.
- Say plainly what was and was not covered. Do not report the game as fully fixed.

---
## ملخص بالعربي لكلود
السبب: دالة `say` ملاقتش تسجيل للجملة، فبترجع لـ `sayClips` اللي بيشغّل كل كلمة لوحدها. المطلوب: (١) ضيف ٥٩ تسجيل جملة بصوت ليدا لحزمة `ve`. (٢) `veFind` يدوّر على الجمل الأول. (٣) أي جملة من كلمتين فأكتر ملهاش تسجيل تتقري كاملة مرة واحدة بصوت الجهاز الإنجليزي الأمريكي لو موجود، وكريم وافق على كده. لو مفيش صوت إنجليزي في الجهاز، تظهر رسالة واضحة، وممنوع تركيب أي جملة (كلمتين فأكتر) كلمة كلمة. (٤) مفيش صوت بعد كل إجابة، والتقييم الصوتي في آخر المجموعة أو الامتحان بس. (٥) تدريبات الكلمات المفردة والأصوات تفضل زي ما هي. ده مخطط تعديل، ماتطبّقش على اللعبة الحيّة من غير ما تراجعه، ومش كل الجمل مسجّلة.
