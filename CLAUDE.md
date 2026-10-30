# Claude Code — Karim Medhat Personal Workspace

This file is read automatically by Claude Code on every session. It contains full context about who I am, my active projects, and how I like to work. Keep it updated as projects evolve.

---

## About Me

- **Name:** Karim Medhat
- **Email:** karimmedhat405@gmail.com
- **Role:** UI/UX Designer — not a developer
- **Preference:** Recommend Figma-based design tools and workflows, not code or npm packages unless explicitly asked
- **Platform:** Windows 11, Claude Code Desktop App

---

## How I Like to Work

- Keep responses short and direct — no long explanations unless I ask
- When working in Figma, always use the `figma-use` skill before calling any Figma tool
- Use the Figma MCP tools to make changes directly in Figma, not by writing code files
- When I share a new reference file (PDF, image, doc), read it fully before doing anything else
- Always compare new brand files against what's already in the design system before updating

---

## Active Projects

### Techtifai Website

**Status:** Active — design in progress in Figma

**Local files:** `E:\Uniparticle\Techtifai Website\Techtifai Website\`

**Figma file:** https://www.figma.com/design/asG6t4nSDCGwWT8jBeMbf8/TECHTIFAI-Website?node-id=106-3
- File key: `asG6t4nSDCGwWT8jBeMbf8`
- Home page hero frame: node `51:120`
- Design System page: `0:1` (children: Colors–Primitives `16:97`, Colors–Semantic `16:171`, Typography `16:285`, Components `16:502`, Navigation & Footer `16:621`)

### Praxis — Products League (K7–K12 STEM challenge)

**Status:** Active — running the UX process step by step, from the beginning

**Figma file:** https://www.figma.com/design/mGhiIvRvnid6fzkkU3Qnuk/Praxis
- File key: `mGhiIvRvnid6fzkkU3Qnuk`
- Work happens on page `🛑 UX Process` (`1:2`); ignore the older boards there unless asked
- **Figma only** — don't use Miro for this project
- **Jira:** project `KAN` at karimsworkspace-32859686.atlassian.net — epic `KAN-1` "Praxis · UX Process", one task per step (`KAN-2` 01 User Problem … `KAN-8` 07 UI + Prototype + Pitch). Move a step's task to Done when it's finished in Figma. Also `KAN-9` Branding and `KAN-10` Development
- **Team:** UI/UX: Karim, Menna Elmagdoub, Nada Yasser · Research: Ahmed Gamal (a.gamal.mu), Ahmed Shelbaya · Branding: Qurany · Development: Qurany, Abdullah Youssef. Jira allows one assignee, so the first person is the assignee and the full team is listed in the description
- Timeline: build days 29–30 Oct 2026, final 31 Oct 2026
- Step 01 — User Problem board: node `93:198`
- Step 02 — Competitive Analysis board: node `259:2` (placed between 01 and 03; boards 03–06 shifted right by 2120). Competitors chosen by Karim: **Nagwa (نجوى), Science Street (شارع العلوم, Abdullah Enan), Alef (ألف)**. Sections: A who we looked at (3 cards: good at / missing), B feature table (9 features, Praxis vs the 3), C positioning map (watch ↔ hands-on × book-first ↔ real life), D 4 opportunities + curriculum watch-out. Desk research 29 Oct 2026, to validate by the Research team
- Step 03 — Insights + Personas board: node `142:2` (assumption-based; personas Omar · See it, Salma · Relate it, Mariam · Check it)
- Step 04 — Journey + How Might We board: node `153:2` (6-stage journey, 9 HMWs, core question; top picks: see it move · start from what they know · know right away they got it)
- Step 05 — Concept board: node `167:2` (15 ideas, impact vs effort, concept "Relate it. See it. Check it.", core loop Hook → Predict → Play → Check, MVP (5) = real-life hook, interactive simulation, AR mode, quick check + confidence, mastery map; demo lesson Forces & motion F = m × a)
- Step 06 — Flows + Wireframes board: node `176:2` (site map, lesson flow, 8 lo-fi wireframes incl. AR on phone)
- Step 07 — Hi-fi UI on page `UI Design` (`170:10389`): 8 screens built only from DS instances, text styles, effect styles and Praxis variables (Dark mode set explicitly). Desktop 1440: 01 Home `186:59`, 02 Explore `186:218`, 03 Hook `187:272`, 04 Predict `187:340`, 05 Play 12 t `188:354` (+ variants 05a 6 t `199:705`, 05c 24 t `199:824`, linked from the preset chips with Smart Animate; shared scale 0–50 m / 0–8 s), 07 Check `191:512`, 08 Lesson complete `191:602`; mobile 390: 06 AR `191:448`; desktop 06 AR view `195:635` (phone mockup holding the AR screen). AR flow section `203:867`: A1 Continue on your phone (desktop overlay with QR, `203:868`), A2 camera permission `203:1156`, A3 scanning `203:1210` (auto → A4 after 2 s), A4 tap to place `203:1291`, A5 placed `191:448` (primary = Brake!), A6 brake & compare `205:926`, A7 quick check in AR `205:1001`, A8 AR not available → 3D view `205:1065`. Desktop "View in AR" opens A1 as an overlay; flow "AR on phone" starts at A2. Local components (frame `185:2`): `UI/Sidebar` `185:3`, `UI/Lesson Header` `185:65`. Prototype: 28 click links; flows "Praxis · Full demo" (starts at Home) and "Lesson loop · Newton’s second law" (starts at Hook); Smart Animate between lesson steps, Move In for AR. Demo-lesson hook corrected to Newton's 2nd law: "Why does a full bus take longer to stop than an empty one?" (12 t, 48 kN → a = 4 m/s², 24 m vs 12 m empty); "jolt forward when the bus brakes" is the 1st-law card
- Step 07 — Arabic RTL version in section `196:11216` (English lives in section `196:11215`). RTL parts frame `212:1009`: `UI/Sidebar · RTL` `212:1010`, `UI/Lesson Header · RTL` `212:1025` (Progress Steps use `Direction=RTL`). Screens: Home `213:1059`, Explore `213:1252`, Hook `213:1438`, Predict `213:1528`, Play 12 t `215:1335` (6 t `215:1568`, 24 t `215:1791`), Check `215:2023`, Complete `215:2123`, desktop AR `215:2313`; AR flow · Arabic section `216:1805`: A1 `216:1806`, A2 `216:2068`, A3 `216:2095`, A4 `216:2156`, A5 `216:2178`, A6 `216:2206`, A7 `216:2250`, A8 `216:2273`. All prototype links point to Arabic frames; flows "Praxis · عربي · العرض الكامل", "حلقة الدرس · قانون نيوتن الثاني", "الواقع المعزز على الهاتف". Formulas, the scene and the graph stay LTR; Western digits with Arabic units. All DS instances in the Arabic screens use `Direction=RTL`
- Step 07 — Hand AR with the laptop webcam (no phone; hand tracking in the browser: open palm = hold the bus, pinch & drag = change mass, fist = brake). "View in AR" on the Play screens now opens H1 (chooser: laptop camera vs phone → A1). English section `241:2082`: H1 chooser overlay `241:2083`, H2 camera permission `242:2028`, H3 show your hand / calibrate `245:2087` (auto → H4 after 2 s), H4 bus on your palm `245:2209` (click camera → H5), H5 fist = brake + compare `245:2369`, H6 can't see your hand `245:2506`. Arabic section `248:2298`: H1 `248:2299`, H2 `248:2362`, H3 `248:2503`, H4 `248:2632`, H5 `248:2810`, H6 `248:2944` (camera picture not mirrored; panel, labels and buttons RTL). Flows "Hand AR · laptop camera" / "الواقع المعزز بيدك · كاميرا اللابتوب". Section layout (both `English` `196:11215` and `Arabic` `196:11216`, stacked top to bottom): 00 Parts · 01 Lesson flow (Home → Complete) · 02 Play states & AR entry (05a, 05c, 06 AR desktop) · 03 AR flow · Phone · 04 Hand AR flow · Laptop camera. New icons: camera `241:2011`, camera-off `241:2020`, hand `241:2031`, hand-grab `241:2042`, move-vertical `241:2054`, sun `241:2064`. Webcam photos are Figma AI images

- ⚠️ **UI change rule (30 Oct):** never edit the existing UI screens. Any change Karim asks for on the UI is built as **new extra screens placed beside them** (a new sub-section), and the originals stay as they are
- Step 07 — **Explain first · v2** (30 Oct, Arabic, section `351:2586` inside `196:11216`): Karim's feedback was that the student comes to understand, so the lesson shouldn't open with a question. New flow: Hook v2 `351:2587` (primary "اشرح لي الفكرة") → 04a Explain · the idea `351:2610` (3 key ideas + empty vs full bus comparison 12 m / 24 m) → 04b Explain · the law `351:2633` (a = F ÷ m, symbols, worked example, "هل الشرح واضح؟" → Play 12 t `215:1335`, or back to 04a). Predict is dropped from this flow. "واضح، جرّبه في المحاكاة" now opens **05 Play · v2** `354:2780` — rebuilt 30 Oct to follow Karim's reference image (node `349:3005`, "Frame 1" on UI Design): left controls panel (تحكم في التجربة: mass + brake-force sliders, presets 6/12/24 t · إعدادات المحاكاة with 2 Switches · reset · "محتاج تلميح؟" hint at the bottom), main sim card (instruction "جرّب وتوقّع!" + "قبل التجربة" prompt, scene without distance/markers, primary "ابدأ التجربة" with play icon), and an "after the run" card (رؤية النتيجة → عرض الرسم البياني → فهم القانون). "ابدأ التجربة" temporarily links to 05b `355:2830` (old layout, graph open) until a result screen is designed. Flow "الشرح أولًا · v2". **Dev notes:** every v2 screen has a dashed "DEV NOTES" card under it (English; why / what changed / removed / interactions / data; Arabic labels at line end) — `357:2886`, `357:2900`, `357:2917`, `357:2931`, `357:2948` — and the same text as a Dev Mode annotation on the screen frame. Note cards sit on the canvas, so they need Dark mode set explicitly. Keep adding a dev-notes card for every new screen. **v3 · Guide character (30 Oct):** 04a Explain with "نور" `361:2922` (6th screen in `351:2586`; dev notes `361:3056`; flow "الشرح مع نور · v3") — 3D AI-image guide (young Egyptian woman, lavender hijab, plum hoodie) on the right, chat bubbles (dimmed greeting + current step, badge "1 من 3"), same comparison visual on the left; buttons "فهمت، التالي" / "وضّحيها أكثر" (no links yet). Steps 2–3 not designed yet. **05 Play · v3 · Calm** `362:2953` (7th screen in `351:2586`, dev notes `362:3173`): Play v2 decluttered — left panel = mass slider + presets + fixed brake-force caption + small "محتاج تلميح؟" ghost; sim card = one prompt "ماذا سيحدث لمسافة التوقف إذا زادت الكتلة؟" + 3 Glass icon buttons (settings, reset, AR) + scene + "ابدأ التجربة"; removed brake slider, settings card, reset button, hint card, instruction bubble, after-run card. "اشرحها بطريقة أخرى" has no target screen yet

**Direction (decided 29 Oct):** the product is a **website** (desktop + mobile browsers). **AR is a core MVP feature**: it opens in the phone's browser from the Play step, no app to install. An **interactive website** for students in general who struggle to *visualize* what they learn in science and math. Three equally important pillars: **interactive visualization**, **real-world connection**, and **confidence to move on** ("Check it": students can't tell if they understood the current part, so they keep rereading and stall; small steps with a quick check + instant feedback). Ignore the "Praxis PoC Brief (Ahmed)" (AI tutor, Thanaweya STEM/IG niche, teacher mode). Jira is no longer used: work in Figma only.

**Problem:** Grades 7–12 students struggle with complex, abstract math & science concepts (textbooks, static illustrations, one-size-fits-all explanations) → hard to visualize, connect to real life, learn at own pace → lower engagement, learning gaps, lower confidence, weak STEM foundations. Missing: personalized guidance, interactive visualization, immediate feedback.

**Product design system (page "🎨 Design System · Overview" + "Logos", v1 Oct 2026):** this is the product's own look, separate from the UX process boards.
- **Fonts: DM Sans (Latin) + Noto Kufi Arabic (Arabic)** — text styles `Praxis/Latin/*` and `Praxis/Arabic/*`. ⚠️ The 7 `Praxis/Arabic/*` styles currently use **Readex Pro** (temporary: Noto Kufi Arabic wasn't available to Claude). Switch the family back to Noto Kufi Arabic in each style and every Arabic screen updates
- Palette: lavender / plum / coral on dark glass. Collections: Praxis Primitives, Praxis Color (Dark + Light), Praxis Spacing, Praxis Radius, Praxis Effects
- 29 component sets + 22 components (Learning page: Quiz Option, Concept Card with real-world Hook, Parameter Slider, Formula Chip, Progress Steps), 58 icons, 12 3D illustrations, logos
- The name is **Praxis** (it was misspelled "Parxis"; fixed everywhere, including the vector wordmark)
- Page "🎨 Design System · Overview" (`0:1`) is now the home of every main component (34 sets / 209 variants, 17 patterns, 64 icons, 12 3D illustrations) plus the cover and foundation docs: 00 Cover · 01 Foundations · 02 Components (one board per category) · 03 Assets. Logos live on page "Logos" (`133:498`). The old per-category pages (Cover, Foundations, Buttons … Loaders, Icons, Illustrations, separators) were deleted on 29 Oct after their components were moved here; all instances stayed linked
- Card radius rule (29 Oct): every card on the UI screens uses `radius/xl` (28). Stat, Parameter Slider and Alert components were moved to `radius/xl` too. Not cards (kept): phone mockups, bottom sheets, browser prompt, QR code, toasts/pills
- DS extension (29 Oct): `Slider` (`133:2037`) got a `Value` property (0/25/50/75/100); Parameter Slider picks it via its nested Slider instance
- DS extension (29 Oct): `Direction` variant property (LTR default / RTL: mirrored order + padding, right-aligned text, arrows/chevrons swapped, sliders fill from the right) on Button, Badge, Alert, Toast, Slider, Checkbox, Accordion Item, Lesson Row, Concept Card, Quiz Option, Progress Steps, Nav Item; single components turned into sets for it: Segmented Control `225:66`, Stat `225:1607`, Parameter Slider `225:1845`, Breadcrumb `225:2099`, Loading Bar `225:2490`. ⚠️ When cloning variants via the API, copy `componentPropertyReferences` from the LTR twin — clones lose them

**UX process board style rules** (boards on the UX Process page only):
- **Font: DM Sans** for UX process boards too (same as the product; Noto Kufi Arabic for Arabic). Geist is no longer used
- Visual language of "UI/UX Sprint Board — v2" (`58:4313`): dark `#121218` cover + panels, warm `#fbf7f0` background, accents orange `#f2603f`, purple `#6c5ce7`, teal `#0f9478`, pink `#f0577a`, gold `#b07a00`, yellow `#ffc83d`; big section numerals, lettered sub-headers (A, B, C…), tinted cards with radius 32–48
- **No coloured circle motifs** — use photos of students in the 12–18 age range instead (Figma AI images, faded into the dark background)

---

## Techtifai — Brand System

> Source of truth: new Branding Guidelines PDF at `E:\Uniparticle\Techtifai Website\Techtifai Website\new reference\Techtifai_Branding Guidelines.pdf`
> This supersedes the old `BRAND_QUICK_REFERENCE.md`

### Official Brand Colors (3 only)

| Role | Hex | Pantone |
|---|---|---|
| Dark Navy (primary) | `#2F476D` | 7694 C |
| Light Blue (secondary) | `#8FB9CC` | 550 C |
| Orange-Red (accent — use sparingly) | `#F0340F` | 172 C |

### Typography

- **Font:** Montserrat-Arabic → in Figma use **Montserrat**
- **Weights:** Light, Regular, Semibold, Bold
- **Hierarchy:** Title = Bold, Subtitle = Medium, Body = Light, Captions = Regular
- **Tracking:** -20 across all styles

### Logo

- Custom geometric rounded wordmark "techtifai"
- Brandmark: stylised "t" bracket shape
- Minimum digital size: 40px wordmark, 40px brandmark
- Do not distort, recolor outside palette, rotate, or add effects

### Graphical Elements

- Overlapping circle/arc motifs as backgrounds and framing devices
- Used subtly — framing devices, background compositions, layered details
- Should never overpower the content

### Imagery Style

- **Portrait:** confident, composed people in clean environments
- **Lifestyle:** technology in action, real business workflows — NOT stock "businesspeople in suits"

---

## Techtifai — Figma Design System State

Last updated: May 2026

### Variable Collections

**Primitives** — all variables updated to new brand palette:
- `navy/500` = `#2F476D` (brand dark navy — primary)
- `navy/200` = `#8FB9CC` (brand light blue — primary; lives in navy scale, no separate blue group)
- `red/500` = `#F0340F` (brand secondary / accent)
- Full scales: navy/50–900, red/50–700, neutral/0–900
- ⚠️ No separate `blue/*` group — light blue anchors at `navy/200`

**Color (Semantic tokens)** — all variables aliasing primitives (auto-cascade):
- `color/bg/navy` → navy/500 = `#2F476D`
- `color/bg/navy-dark` → navy/700 = `#1A2A43`
- `color/bg/brand-secondary` → red/500 = `#F0340F` (secondary brand color per PDF)
- `color/bg/brand-secondary-hover` → red/600 = `#BC290D`
- `color/bg/brand-secondary-subtle` → red/50
- `color/bg/blue-light` → navy/200 = `#8FB9CC`
- `color/text/on-dark` → neutral/0 = `#FFFFFF`
- `color/text/primary` → navy/500
- `color/text/brand-secondary` → red/500
- `color/border/brand-secondary` → red/500
- `color/icon/brand-secondary` → red/500
- `color/border/navy` → navy/500
- `color/text/secondary` → neutral/700 (grey body text — different from brand-secondary)

**Spacing** — 4px base unit, spacing/1–40 (4px–160px), radius/none–full

### Text Styles (14 total) — all using Montserrat
Optimized for 1920×1050 target screen. Line heights in parentheses.

| Style | Size | Line Height | Weight |
|---|---|---|---|
| Display/Hero | 96px | 104px | Bold |
| Heading/H1 | 72px | 80px | Bold |
| Heading/H2 | 52px | 62px | Bold |
| Heading/H3 | 36px | 44px | Bold |
| Heading/H4 | 24px | 32px | SemiBold |
| Label/Eyebrow | 13px | 18px | Bold, UPPERCASE, 2.2px tracking |
| Body/Large | 20px | 30px | Regular |
| Body/Default | 18px | 28px | Regular |
| Body/Small | 15px | 24px | Regular |
| Body/Caption | 12px | 18px | Regular |
| Button/Large | 16px | 24px | SemiBold |
| Button/Default | 14px | 20px | SemiBold |
| Button/Small | 12px | 18px | SemiBold |
| Nav/Link | 16px | 24px | Medium |

---

## Techtifai — 10-Page Site Map

Pages (from content brief):
1. **Home** — "One Partner for Total Transformation"
2. **About** — "Built in 2025, Positioned for Regional Transformation"
3. **Services** — "Everything Needed to Modernize — Under One Roof"
4. **Capabilities** — 5 capability areas (AI CX, GenAI, Smart Connectivity, Enterprise Platforms, Hardware)
5. **Industries** — Real Estate, Retail, Banking, Telecom, Education, Hospitality, Government
6. **Process** — 7-stage delivery process
7. **Why Us** — 6 reasons, competitor comparison table
8. **Case Studies** — 2 cases (Banking AI, Retail Connectivity)
9. **Team** — 4 leaders: Mohamed Hashem (CEO), Dr. Maged Ghoneima, Mohamed Abu-Elnaga "Nagaty", Raiyan Sindi
10. **Contact** — "Let's Build the Future" + contact form

Primary CTA: "Start Your Transformation" → /contact (orange-red button)
Secondary CTA: "See How We Work" → /process
Tagline: "One Partner for Total Transformation"

---

## Techtifai — Open Items (client still needs to provide)

1. Final contact details (address, phone, email, domain, LinkedIn)
2. Headshot photos for 4 leadership team members
3. Decision on blog/insights section in v1
4. Decision on client logo/trust bar on homepage
5. Confirmation of industry sub-copy accuracy
6. Confirmation of which case studies are direct Techtifai deliveries

---

## Techtifai — Work Completed So Far

- [x] Read and understood all local files (README, brand quick ref, content brief, all 9 wireframes)
- [x] Read all 34 pages of new Branding Guidelines PDF
- [x] Audited home page hero frame — found all colors hardcoded, no text styles applied
- [x] Updated Figma design system: all 32 primitive color variables to new brand palette
- [x] Updated Figma design system: all 14 text styles from Inter → Montserrat
- [x] Semantic color tokens verified cascading correctly
- [x] Applied variable bindings to all nodes in home page hero frame
- [x] Applied text styles to all text nodes in home page hero frame
- [x] Renamed all "accent" semantic variables → "brand-secondary" to match PDF terminology
- [x] Removed redundant `blue/*` primitive group — light blue now lives at `navy/200`
- [x] Updated all 14 text styles to 1920×1050 optimized sizes
- [ ] Replace old logo with new logo in navbar
- [ ] Apply design system bindings to remaining page frames
- [ ] Design remaining 9 pages in Figma

---

## Installed Plugins

- **designer-skills plugin** at `C:\Users\kmedhat\.claude\plugins\marketplaces\designer-skills\`
  - Sub-plugins: design-ops, design-research, design-systems, designer-toolkit, interaction-design, prototyping-testing, ui-design, ux-strategy
