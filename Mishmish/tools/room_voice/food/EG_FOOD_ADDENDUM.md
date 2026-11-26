# Addendum: cat food reactions (EG-201 to EG-217)

STATUS: plan only. Nothing applied live. The earlier Egyptian pack and the 568 English pack are untouched.

What Karim asked (Nov 26, 9:51 AM): when the cat eats something, she should react with a line like "Yummy! I love fish!", varying with the food Farha feeds, for every food in the mall.

Where: the `feed(tid, id)` function. Today it builds an English line with the child's name and speaks it with `say(t)`:
- normal: `Yum! I love ${it.en}! Thank you, ${kidName()}!`
- favorite: `Yum! ${it.en} is my favorite food! Thank you, ${kidName()}!`

Foods in the mall (room "Mishmish's Food", kind `treat`, 8 items): t_food, t_milk, t_fish, t_chicken, t_cheese, t_icecream, t_cake, t_shrimp.

Clips (audio/eg/EG-201.mp3 ... EG-217.mp3, listed in manifest.csv):
- EG-201..208: `feed_<tid>` normal line, one per food.
- EG-209..216: `feedfav_<tid>` line when it is that cat's favorite food (`catProf(id).fav === tid`).
- EG-217: `feed_any`, generic fallback if a food is added later without its own line.

Code change (same helpers as the room pack: `EG`, `EG_TEXT`, `catLine`/`egSay`):
```js
const key = (fav ? 'feedfav_' : 'feed_') + tid;
const k = EG_TEXT[key] ? key : 'feed_any';
catBubble(id, EG_TEXT[k], 3200); egSay(k);   // replaces: catBubble(id, t, 3200); say(t);
```
Keep the rest of `feed()` as is: walk to the bowl, eating animation, floating emoji, joy, and the `meow()` sound after 2.6 s (that is a synthesized sound, unchanged).
- No child name in the audio or the Arabic bubble. If the name should show, add it in the bubble only.
- Clip lengths are 3.2 to 6.6 s (normal lines 3.8 to 4.9 s, favorite lines 5.4 to 6.6 s, see manifest duration_s). The current bubble lasts 3.2 s and the eating animation 2.6 s, shorter than the clips. Keep the bubble up and the cat in the eating pose until the clip ends (use the clip length or the audio `ended` event). Delay the synthesized meow until the clip ends too, so it does not cut the speech.
- The existing Arabic toast "الأكل خلص" (food is finished) stays as text. Its English `say('food bowl')` fallback in the quick-feed button should become silent or use EG-217 style, never English, per the pack rule.
- Missing clip: show the Arabic bubble only, log the key, no English or device fallback.

Test: buy each of the 8 foods, feed each to Mishmish and to an adopted cat, including a cat whose favorite is that food. Check that each line matches its food and the bubble shows the same Arabic text.
