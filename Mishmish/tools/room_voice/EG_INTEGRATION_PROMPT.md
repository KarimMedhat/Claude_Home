# Egyptian voice for Farha's Room (cats and objects): integration plan for Claude

STATUS: this is a plan to apply in Karim's artifact. Nothing was applied live. The English pack (english_audio_complete.zip) is not touched and is not part of this ZIP.

## What Karim asked (his words, Nov 26, 8:37 AM)
The sounds in Farha's room, the interactions with Mishmish and the other cats, should be in Arabic, in the Egyptian voice too. Musical and instrument sounds stay as they are. The Egyptian clips come in their own ZIP, `audio/eg/EG-001.mp3 ... EG-200.mp3` (199 files; EG-016 is reserved and has no clip) (voice: the same Egyptian "Mishmish" voice used for science and math), matched by `manifest.csv`.

## Design decisions (Instinct's recommendation, not a proven learning claim)
1. Cat speech and room reactions become Egyptian: clip plus Arabic bubble text.
2. The English practice stays English: the command chips ("Jump", "Go to the bed"), the English commands Farha says or types, the "Where is the X?" find game, and the item-name drill. The chips keep showing the Egyptian meaning under each English command (for example Jump / نُطّي). The command parser keeps accepting the same English inputs. The Arabic label is only a support, it does not replace the command.
3. Cats' replies to those commands play the Egyptian clip (EG ids below).
4. Tapping an object says its Egyptian name (`label_*` clips), not the English name. Keep the English name visible on the card if it is already.
5. No child name inside any clip. The bubble text may still show the name visually, but the audio is generic.
6. Do not change the synthesized sounds (meow, tones, music items). Do not touch the English `say()` path.
7. If an Egyptian clip is missing, show the Arabic bubble only. Do not fall back to English or device speech. Log the missing key.

## Code changes
1. Add an `EG` clip map from `manifest.csv` (key to file) and load clips lazily with the same audio loader used for the science Arabic pack.
```js
const EG = { /* key: 'eg/EG-001.mp3' from manifest.csv */ };
const EG_TEXT = { /* key: egyptian_text from manifest.csv, for the bubble */ };
function egSay(key){ if(!S.sound) return; const f = EG[key]; if(!f){ console.warn('no eg clip', key); return; } stopSpeech(); playClip(f); }  // playClip = existing Arabic clip player
function catLine(id, key, ms){ catBubble(id, EG_TEXT[key] || '', ms); setTimeout(() => egSay(key), 300); }
```
2. Replace each English `bubble/say/catBubble/friendBubble` line in the room code with `catLine(id, key)`. Call sites and keys (from `manifest.csv`, `key` column):
- welcome, hungry (also the idle hungry bubbles): keys `hungry`, `welcome`, `hungry2`.
- `friendTap` lines: `tap_love`, `tap_friend`, `tap_play`; wake: `wake`; the intro: `intro_<cat>` (7 cats).
- `IDLE_LINES` (8 lines): `idle1..idle7` use clips. `idle8` (EG-016, the purr) has NO clip: keep the existing purr sound effect from the code and show the purr bubble text without speech.
- `reply(w, en, ar)` inside the command parser: replace with `reply(w, key)` using keys `nobed, tobed, awake, here, nofood, dance, jump, chase, left, right, love2, hello, stay, dontget`. The "did you hear" Arabic line stays. Per-item replies: `love_<id>` (when the cat loves an item), "This is the X" can reuse `label_<id>`.
- Window tap: `win_night, win_moon, win_sunset, win_sunny`.
- Room objects (`ACTIONS`): lamp `lampon/lampoff`, mirror `mirror`, disco `disco`, `dance2`, globe `globe1..4`, stars `stars`, plant `plant_big/plant_water`, aquarium `fish`, easel `paint_has/paint_none`, TV `tv`, race `race`; the default `say(it.en)` becomes `egSay('label_' + it.id.slice(2))` style lookup, with the id in the manifest (`label_r_xxx`).
- Purchase: `bought_<id>`; adoption: `intro_<cat>`.
3. Keep as English: `say(b.dataset.cmd)` for chips, the command parser inputs, `findSt` questions (`Where is the ...?`, `Yes! The ...`), mall and lesson speech.
4. Chips: keep the two-line chip (English command, Egyptian meaning below). Make the Egyptian meaning visible at all times (not only as a title tooltip).

## Test
- Tap each cat, each object, buy an item, give each command in English (typed and tapped): the cat answers with the Egyptian clip and Arabic bubble; the English input still works.
- No call to `say()` with English text from the room except the chips, the find game and item drills.
- Say plainly what was and was not covered. Nobody listened to the clips on the device.

- EG-016 has no audio file. The manifest row has an empty audio_file and status reserved_no_clip_keep_purr_effect. This is not a missing reference: do not log it as one.
- EG-009 and EG-030 contain a spoken meow word. Listen to them first on the device.
