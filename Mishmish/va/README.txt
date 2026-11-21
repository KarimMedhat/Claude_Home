شرح دمج الصوت في لعبة «استوديو مشمش» على Claude
==================================================

يا كريم، الملفات دي فيها تسجيلات الصوت المصرية الجاهزة + الكود اللي بيشغّلها + تعليمات الدمج.
الفكرة: ترفع الملفات لكلود في نفس الشات اللي فيه اللعبة وتطلب منه يركّبها في نفس الـartifact الموجود.

⚠️ مهم: فكّ ضغط كل ملف ZIP الأول على جهازك، وارفع لكلود ملفات الـmp3 نفسها (مش ملفات الـZIP).
مش متأكدين إن كلود يقدر يفك ZIP جوه الـartifact، فالأضمن ترفع الملفات مفكوكة.

جوا الحزمة دي إيه؟
------------------
1) سبع ملفات مضغوطة فيها 80 ملف صوت mp3 (دفعات مجمّعة لكل درس/امتحان):
   va-part1-intro-ch1.zip        المقدمة + الفصل الأول
   va-part2-ch2-ch3.zip          الفصل التاني + التالت
   va-part3-ch4-ch5.zip          الفصل الرابع + الخامس
   va-part4-ch6-ch8.zip          الفصول 6-8
   va-part5-exams-final.zip      نماذج آخر الترم
   va-part6-exams-units.zip      امتحانات الوحدات
   va-part7-exams-weekly.zip     التقييمات الأسبوعية
2) va-index.json  → فهرس: كل جملة صوتية مكانها بالظبط (أوفسيت وطول بالبايت) جوه ملف الـmp3 بتاع فصلها.
3) va-h.json      → بصمة (هاش) النص المكتوب اللي اتسجّلت عليه كل جملة، للتأكد إن التسجيل مطابق للنص المعروض.
4) mishmish-audio-module.js → كود التشغيل كامل (جاهز ومتجرّب): تحميل، تقطيع، تشغيل، وفحص المطابقة.

اللي تقوله لكلود (انسخه زي ما هو):
----------------------------------
"دي تسجيلات صوتية جاهزة للّعبة + كود الدمج. ارفع ملفات الـmp3 كملفات مرفوعة للـartifact (أو أي استضافة تسمح بيها
الـartifact)، وعدّل اللعبة بكود mishmish-audio-module.js بحيث أزرار «اسمعي» تشغّل التسجيلات بدل صوت الجهاز.
اقرأ README.txt للمواصفات الكاملة. ممنوع استخدام صوت الجهاز (TTS) لأي محتوى متسجّل."

مواصفات فنية لكلود (English technical spec):
--------------------------------------------
AUDIO FILES
- 80 chunk mp3 files. Naming: g.mp3 (intro/global), c<chapter>l<lesson>.mp3 (lessons), c<n>x.mp3 (boss stems),
  c<n>o.mp3 (boss options), sxr_w<N>.mp3 (weekly exams), sxr_u<N><a|b>.mp3 (unit exams), sxr_f<N>.mp3 (finals).
- Encoding: MP3, 22050 Hz, mono, ~48 kbps. Total ~87 MB. Every clip id belongs to exactly one chunk.
- va-index.json: { chunk: { clipId: [byteOffset, byteLength] } } — slice with ArrayBuffer.slice(offset, offset+length).
- va-h.json: { clipId: ohash } where ohash = djb2 base36 of the EXACT displayed text the clip was recorded for:
  h=5381; for each char h=((h<<5)+h+charCodeAt(0))>>>0; result .toString(36). MUST match generation side exactly.

PLAYBACK RULES (already implemented in mishmish-audio-module.js — reuse as-is)
- sayAr(text, clipId, btn): plays one clip. sayArSeq(parts, btn): stem+options back-to-back.
  sxParts(q) builds exam-hall parts; qParts(q, islandId, displayedOpts) builds boss question parts.
- A clip plays only when va-h.json hash matches ohash(current display text). On mismatch: suppress playback,
  show toast "✏️ السطر ده اتعدّل ومحتاج تسجيل جديد" (edited line needs re-recording). NEVER fall back to device TTS.
- Covered route with missing clip: show toast "🎙️ صوت مشمش للجزء ده لسه بيتسجل". Never device TTS.
- 120 lab feedback clips (ids ending _m<nn>) are hash-EXEMPT: they bind by exact display string at the call site
  (pass text=null and they play; unmapped ones stay silent).
- Clip id patterns: c<ch>l<n>_s<i> slide, _s<i>n slide note, _s<i>w ask-feedback, _q<i> question,
  _t<i>/_td<i> term/definition, _tn<i> term name, _tq<i> term question, _lab<i> lab, _m<nn> lab feedback;
  sxr_*_i<nn>q question, _i<nn>a answer; g_* global (g_ok<k>/g_no<k> praise/oops, g_termq prefix, g.mp3 intro).
- Bump AR_VER when recordings change (cache-busting). Fetch chunks lazily per lesson/exam, not all at once.
- AudioContext needs a user-gesture unlock on first tap (the game already has unlockAudio).

PLAYBACK SAFETY (fail closed)
- A clip plays ONLY when its va-h.json hash matches the exact display text, or it is a lab _m feedback clip
  bound by exact display string (text=null). If the hash file itself fails to load, covered clips stay silent
  and show "⚠️ مش قادرين نتأكد من تسجيل الجزء ده دلوقتي" instead of playing unverified. No silent fallbacks.
- mishmish-audio-module.js status: logic-verified with an automated stub test (5 scenarios: match plays,
  mismatch suppressed + edit notice, hash-load failure suppressed + verification notice in both sayAr and
  sayArSeq, lab exception plays). NOT yet browser-tested inside a Claude artifact - Claude should run the
  game after integrating and we can re-verify.

KNOWN CAVEATS
- 3 clips with plant-name words are still flagged for a final ear-check; not confirmed 100% clean:
  * c1l4_q1     «تمتلك نباتات الصحراء (مثل السَّنْط) أوراقًا صغيرة بهدف ...»  (السنط)
  * c1l4_q9     «استخرج الكلمة المختلفة: اللوف – البرتقال – اللوتس – السَّنْط»  (اللوف والسنط)
  * sxr_u1b_i13a  answer clip mentioning شجرة السنط  (السنط)
  Everything else passed transcription QA on the actual exported files.
- Whether Claude artifacts accept uploaded audio files and let the game code play them is NOT verified from our
  side — Claude needs to confirm the upload route when you give him the files. If direct upload does not work,
  ask Claude what asset hosting the artifact supports; the module only needs a GET-able URL per chunk.
