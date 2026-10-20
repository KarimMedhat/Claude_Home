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

### Mi'yar | مِعيار — Performance & Governance Platform (Portfolio)

**Status:** Active — UX phase (Problem → Personas → MVP → IA → User Flows), then Wireframes → Design System → UI

**Full brief:** `Miyar_Product_Brief.md` (read it before any Mi'yar work)

- **Type:** Enterprise Web Platform · concept project for a Behance Product Design case study — fictional, not tied to any real agency or company; all data is fictional and labelled as such
- **Language:** Arabic, full RTL · **Visual direction (v2):** Electric Violet `#5B4CF5` + coral accent `#FF8A4C` on lavender-white — **no navy, no green** (Karim uses those in other projects); status colors sky / amber / red / gray · **Visual reference only:** rouya360.com
- **Users:** government managers and employees — Ahmed (performance director, primary), Sara (performance analyst, data contributor), Khaled (department head / initiative owner, action owner)
- **Core flow (prototype):** spot a KPI below target → understand the gap → create a corrective action → assign an owner + deadline → track progress
- **Supporting flows:** B — update a KPI and submit it for approval · C — follow up on a delayed initiative
- **Case study rule:** keep assumptions, validated findings, and design decisions clearly separate — personas and the research plan are hypotheses, not real interviews
- **Decided:** KPI status computed automatically from the approved value vs target, with polarity (higher/lower-is-better), on track ≥95% / needs attention 85–95% / off track <85% / no data · corrective action states New → In progress → Pending verification → Closed (+ Cancelled), with "Overdue" as a flag rather than a state · Arabic-Indic numerals (٠–٩) · Gregorian dates · RTL charts (time runs right→left) · font **IBM Plex Sans Arabic** · balanced dashboard (KPIs plus "needs attention" above the fold)
- **Case study:** 11-section Behance structure + visual references in the brief · screen order: Dashboard → KPI detail → create corrective action
- **Figma:** file `1rJxwwH7qnUPwOjFvQDXjd` (Karim Draft, Uniparticle team), page `Mi'yar | مِعيار` `1805:1485` — IA `1808:234` · User Flows `1809:234` · Dashboard Low-Fi `1810:234` · Dashboard Hi-Fi v1 (archived) `1819:268` · Components `1816:234` · **v2: Dashboard `1828:656` · KPI Explorer `1834:921` · KPI Detail `1836:1315` · Action Drawer `1838:1455`**
- **Design system:** variables `Mi'yar · Primitives/Color/Spacing/Radius`, text styles `Mi'yar/*`, shadows `Mi'yar/Shadow/*` — details in the brief
- **Dashboard = the hero of the case study** — it has to look excellent. IBM Plex Sans Arabic isn't available in Figma; v2 uses **Readex Pro** as the stand-in. Karim wants senior-level, creative screens — not basic layouts

### TIEC Dashboard Redesign (tiec.gov.eg/arabic/pages/dashboard.aspx)

**Status:** Active — desktop redesign v1 done in Figma

- **What:** redesign of TIEC's public impact dashboard page (Technology Innovation & Entrepreneurship Center, part of ITIDA). Karim works on it ("our page")
- **Figma:** file `1rJxwwH7qnUPwOjFvQDXjd`, page "Page 9" `1842:2896` — Audit `1845:234` · Desktop page `1847:323` · **Mobile page (390) `1860:364`** · icons `1847:234` · **Interaction states desktop `1866:459` (S1 period 2026 · S2 year menu · S3 chart hover · S4 definition popover · S5 sticky tabs) · mobile `1871:511` (M1–M5) · Before/After `1873:622` (8 audit issues; "before" = crops of the live site)**. **Don't touch the Mi'yar page** when working on TIEC
- **Management deck (v1 done):** section `06 · Presentation — TIEC management (1400px)` `1875:701` on Page 9, below the work (y 8200). 18 slides, **1400×788** (Karim uploads to Behance at 1400px wide), stacked vertically in one column (40px gap) — Karim wants them one under another, not side by side. Footer component `TIEC/Deck/Footer` `1875:696` (Page text prop "NN / 18"). Deck text styles `TIEC/Deck/*`. Order: cover → context → current page → 8 findings → data notes → principles → structure → hero → journey → charts → 3 before/after → period filter → details on demand → mobile → next steps → thanks
- **Deck v2 (card slides, more creative):** second column in the same section at x 1600, each v2 next to its v1 — 02 bento tiles (`1885:1151`) · 04 findings pinned on the live page (`1885:1337`) · 05 evidence cards with mini charts + stamps (`1886:1168`) · 06 outlined giant numbers in quadrants (`1886:1253`) · 09 journey as a winding path ending at jobs (`1890:1180`) · 17 zigzag timeline (`1886:1303`). 02 v2 = bento for the 4 stats + v1 dark challenge banner. Karim felt equal side-by-side cards looked dated
- **Behance cover:** `07 · Behance Cover — TIEC (1400×1094)` `1899:1157` (x 3280, y 8200), built from Karim's reference but mirrored (text on the right): title "لوحة بيانات TIEC" + subtitle "إعادة تصميم صفحة الأثر", MacBook mockup `1901:1157` with the desktop page, iPhone mockup `1901:1591` with the mobile page. Deck cover title is also "لوحة بيانات TIEC" (not "لوحة بيانات الأثر")
- **Behance cover v2 (preferred):** `07 · Behance Cover v2 — TIEC (1400×1094)` `1905:1323`, below v1. Uses the photoreal MacBook + iPhone from Karim's own reference image (mirrored, old text removed) with our screens perspective-warped into them, as one flattened image fill; title/subtitle/description stay editable Figma text on the right. Source screens: `Mockup screen · desktop 1440×900` `1903:1239`, `Mockup screen · mobile 390×844` `1903:1618` — if the design changes, re-render these and rebuild the image
- **Presentation prep (done):** states + QA + before/after. No prototype (Karim's call). QA fixes applied: years no longer comma-formatted on mobile, thousand separators on chart value labels, `text/muted` darkened to `#66666F` (AA), small red text → `brand/red-dark`, "قيد المراجعة" text → new `brand/gold-dark` `#7A5E1C`
- **2026 YTD figures (from the live page):** trainees 33,601 · entrepreneurs 3,058 · incubated startups 46 (37 current / 9 graduated) · jobs 1,053 — compared against 2025 totals (67,212 · 5,746 · — · 1,311)
- **Brand:** TIEC colors — red `#E2202B`, ink/charcoal `#141416`/`#232328`, gold `#B08D3C`, warm canvas `#F6F5F2` (variables `TIEC · Color`) — **not violet**
- **Font:** **Cairo** (text styles `TIEC/*`) · Western digits (matches the live site)
- **Structure:** header/nav → dark hero (period filter: cumulative / 2026 YTD / years, 4 headline numbers) → impact journey (training → ideas → entrepreneurs → startups → companies → jobs) + supporting metrics → sticky section tabs → pillar sections matching the site nav (ابنِ موهبتك · ادعم فكرتك · ابدأ شركتك · طوّر شركتك · مجتمع الإبداع) → past programs (collapsed) → methodology → newsletter → footer
- **Rules applied:** 2026 is shown as partial (to June), not a decline · time axis RTL · selective value labels · special 2025 incubation cohort (130) shown separately · data anomalies (2025 platform entities/users, 3× "2026" consulting bars, mixed categories in the jobs chart) flagged "قيد المراجعة" for the data team
- **Mobile:** hamburger header with official logo · period filter as scroll chips · 2×2 stat grids · journey as vertical timeline · charts as RTL horizontal bars, newest year first, last 8 years + "عرض 2013–2018" · community as mini column charts · methodology/past programs/footer link groups as accordions · mobile text styles `TIEC/Mobile/*`
- **Header & footer = exact replicas of the live site** (Karim's request): `Header — live site` `1854:370`, `Footer — live site` `1854:414`. Logos use Karim's official files (source images on Page 9: `ITIDA-TIEC 1` `1857:3033`, `eubic 1` `1857:3034` — keep them)

### Techtifai Website

**Status:** Active — design in progress in Figma

**Local files:** `E:\Uniparticle\Techtifai Website\Techtifai Website\`

**Figma file:** https://www.figma.com/design/asG6t4nSDCGwWT8jBeMbf8/TECHTIFAI-Website?node-id=106-3
- File key: `asG6t4nSDCGwWT8jBeMbf8`
- Home page hero frame: node `51:120`
- Design System page: `0:1` (children: Colors–Primitives `16:97`, Colors–Semantic `16:171`, Typography `16:285`, Components `16:502`, Navigation & Footer `16:621`)

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
