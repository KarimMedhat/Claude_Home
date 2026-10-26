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

### Unfold (Personal Startup)

**Status:** UX phase — work in Figma step by step, only when I ask

**Figma file:** https://www.figma.com/design/1rJxwwH7qnUPwOjFvQDXjd/Karim-Draft
- File key: `1rJxwwH7qnUPwOjFvQDXjd`
- UX page: node `2058:632`
- UI page: node `2058:633`
- Wireframes page (`Unfolf_Wireframes`, name has a typo): node `2083:2447`
- Design System presentation page: node `2058:634` (variables system planned later, not started)

**Rule:** All Unfold work is done inside Figma (UX deliverables on the UX page, UI on the UI page). No markdown or code deliverables; local files are only for keeping notes in sync.

See the full Unfold section below and `Unfold_User_Flow.md`.

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

## Unfold — Personal Startup

**Status:** UX phase. User Flow, Competitive Analysis, Proto-Personas, Information Architecture, Wireframes v2 and Usability Test Plan done in Figma. UI and the variables system come after UX.

**User flow:** `Unfold_User_Flow.md` (source of truth for flows and screens)

### Concept
- AI website that turns a designer's raw project material into a polished, portfolio-ready presentation
- Problem: making the presentation (case study, UI shots, redesign) often takes more effort than the UI itself
- Target users: UI/UX designers, product designers, and developers who need to show their work on Behance, Dribbble, and portfolios
- Powered by the Claude API (Opus tier). Users never see which model is used.

### Product Decisions
- **Platform:** Website, English, LTR
- **Handoff:** Design goes to a developer once complete
- **Project types (user chooses):** Case Study, UI Shots, Redesign, Design System, Landing Page / Website, Mobile App Showcase, Concept / Personal Project, Other
- **Output formats (user chooses):** Behance Long-scroll, Slides 16:9, Dribbble Shots, PDF Portfolio
- **Format switching:** Content is written once. Each format is just a different layout, switchable from the Editor ("Create once, publish everywhere")
- **Industry:** Drives mood, color, and visual style
- **Scope:** UI / UX / Both. Decides which sections get generated
- **Pricing:** First presentation free. Then 3 ways to pay: (1) **Pay per presentation** — one-time, 1 generation + 10 section regenerations + all formats/exports, never expires; (2) **Credit pack** (best value, credits never expire); (3) **Pro monthly**. No unlimited subscription. Example prices in wireframes: $6 / $12 for 100 credits / $16 per month — final pricing TBD

### Core Flow (summary)
Project type → Output format → Industry → Scope → Upload (screens / Figma link / docs) → Smart AI questions → 3 visual directions → Generate → Editor → Export

### Work Completed
- [x] User Flow v1 built in Figma on `Unfold_UX` — frame `2061:283` (Flows A–D with Goal / Success Metric / Key UX Decision, Edge Cases, Screens Inventory: 27 screens)
- [x] Local components live in the **UX Components** board on `Unfold_UX` — frame `2061:234` (18 components, 22 variants, grouped: Flow · Competitive Analysis · Personas · Board · IA · Usability Testing, each with description). Add every new UX component here, inside its group
- Board order on `Unfold_UX` (left → right, 400px gaps): User Flow → Competitive Analysis → Proto-Personas → Information Architecture → Usability Test Plan → UX Components
- [x] Competitive Analysis v1 on `Unfold_UX` — frame `2065:833` (7 competitors, feature matrix, positioning map, pricing benchmark, 5 insights, positioning statement)
- [x] Added components: Competitor Card (Threat variants), Matrix Cell (Yes/Partial/No), Map Dot, Insight Card
- [x] Proto-Personas v1 on `Unfold_UX` — frame `2068:1347` (Nour Adel = Primary junior designer, Omar Haddad = Secondary senior freelancer, Priya Nair = Tertiary developer; comparison table, 4 design implications, assumptions to validate, research plan)
- [x] Added components: Meter (Level 1–5), Bullet Item, Stat
- [x] Polish pass on all 3 boards: Board Cover (dark gradient hero + 4 stats) on each, upgraded Section Header, Flow Node, Insight Card, Competitor Card (brand mark), Flow Note; flow Goal/Metric/Decision rebuilt as icon cards + dark decision callout
- [x] Added components: Board Cover, Cover Stat (use Board Cover as the header of every new UX board)
- [x] Information Architecture v1 on `Unfold_UX` — frame `2075:1719` (sitemap: 5 areas / 18 pages / 31 views & overlays, navigation model with 4 nav specimens, content model: 7 objects, presentation lifecycle, labeling & URL conventions, 5 IA principles)
- [x] Added component: IA Node (Page · Sub-page · Overlay)
- [x] Wireframes v1 on `Unfolf_Wireframes` — frame `2087:318`: 10 annotated desktop screens (1440×900): Wizard 01–07 (Basics, Format, Industry, Scope, Upload, Smart Questions, Visual Direction), 08 Generating, 09 Editor, 10 Export; each with numbered pins + annotation panel + states to design (51 annotations, 41 states)
- [x] Wireframe Kit on `Unfolf_Wireframes` — frame `2085:234` (13 components, 15 variants: Button, Input, Select Card, Chip, Image, Text Lines, Pin, Annotation, Logo, Stepper, App Bar, Wizard Header, Wizard Footer). Wireframes are grayscale; purple only for AI actions and annotations
- [x] Wireframes v2 added to the same board (now 17 screens, 95 annotations, 66 states): C Home & Account (11 Dashboard, 12 Empty State, 13 Onboarding Role, 14 Brand Kit), D Pricing & Payment (15 Paywall with 3 ways to pay, 16 Checkout), E Marketing (17 Landing Page, full length with pricing + FAQ)
- [x] Usability Test Plan v1 on `Unfold_UX` — frame `2109:2125`: objective, 5 research questions (RQ1–RQ5), scope; moderated remote think-aloud, 8 participants (3 junior · 3 senior/freelance · 2 developers), Figma prototype of Wireframes v2, 45-min agenda; 6 tasks (T1 start case study · T2 upload · T3 smart questions · T4 generate · T5 edit/switch/export · T6 pay for one presentation); metrics (task success ≥80%, T1 <3 min, SEQ ≥5.5, SUS ≥75, pricing clarity 6/8, 0 critical); severity 0–4; session script + moderator rules; screener, synthesis steps, deliverables, decision rules
- [x] Added components: Task Card, Metric Card, Question Card (group F in UX Components)
- [x] Clickable prototype on `Unfolf_Wireframes` — section `2121:2014` "Prototype — Usability Test v1": 18 top-level frames (clean clones of wireframes, no pins) + extra states (05b upload retried, 09r regenerating, 09s Slides view, 10d downloaded toast, T6 start with no credits); 51 click hotspots (transparent "Hotspot → …" rects) + 2 timers (Generating → Editor, Regenerating → Editor); flow starting points: "T1–T5 · Create, edit & export" (Dashboard) and "T6 · Pay for just this one". Selections inside screens (type cards, paywall options) are static
- [ ] Pilot the prototype with 1 designer, then run the 8 sessions
- [x] Brand Exploration v1 on `Unfold_Design_System` — frame `2123:234`: Brand Foundation (name story, mission, positioning, promise, personality Confident/Crafted/Smart/Warm with "not" pairs, voice do/don't); 3 directions each with logo stage, concept, 5-color palette, type specimen and 3 applications (product UI, presentation cover, social card): **A Folded Paper** (Paper #F6F1E8 · Ink #14120F · Vermilion #FF4F1F · Clay #D9C9B4 · Stone #6B645B; Instrument Serif + Inter; folded-u mark), **B Studio Violet** (Night #0C0A1D · Violet #7C5CFF · Lilac #C9B8FF; Geist), **C Blueprint** (Graphite #17181C · Lime #D4FF3A · Concrete #E9EAE6; Space Grotesk + Inter); scorecard A 29/30 · B 20 · C 19; recommendation: Folded Paper
- [x] Added **A2 — Folded Paper Night** (dark-first) section to Brand Exploration — frame `2129:298` (Karim asked for dark mode): Night #12110F · Surface #1C1A17 · Raised #262320 · Paper text #F6F1E8 · Stone #A39B90 · Vermilion #FF5A2C (brighter for dark); paper "u" + vermilion fold; contrast checks (AI buttons = Night text on Vermilion); dark product UI, cover, social card. **Type: Geist only** (Karim asked to replace Instrument Serif + Inter): display SemiBold/Medium at -4% tracking, UI/body Regular/Medium. Cover stat now 4 directions; recommendation: "Folded Paper — dark-first", variables Dark mode first, Light second. Dark = app UI only; exports keep their own visual direction
- [ ] Karim to pick the brand direction → refine logo → color variables → type scale → UI kit
- [x] Updated for pay-per-presentation: User Flow Flow D renamed **Payment** (free first presentation → credits → Paywall with 3 ways to pay → checkout → unlock & resume / payment failed); IA content model now 8 objects in a 3-column grid (new **Purchase** object: kind one-time | pack | pro; Presentation gets "Paid with"; Credit Transaction type generate | regen | grant | refund), 2 new relationships, labeling row "One presentation", Principle 04 adds "a subscription is never required", sitemap Paywall/Checkout/Billing labels

### Key Findings (Competitive Analysis)
- Closest threat: UXfolio (AI case studies, but locked to its own site, no Behance/Dribbble/slides export)
- Gap: no tool exports Behance-ready long-scroll; generic AI deck tools don't understand design process
- Price anchor: $10–16/mo entry plans; credits already familiar (Gamma, Canva, Figma)

### IA Decisions
- Marketing at `/`, app under `/app`; wizard steps `/app/new/:step`; one presentation `/app/p/:id/:view`
- Areas: Marketing (public) · Onboarding (first run) · Core App · Account · Overlays (global)
- App bar: Dashboard, Brand Kit, New Presentation, credits balance (always visible), Help, avatar menu (Settings · Billing · Log out)
- Labels: Presentation (not Project/Deck), Brand Kit, Generate / Regenerate, Export, Credits, Format, Visual Direction
- Lifecycle: Draft → Generating → Ready → Exported, with Failed → Retry (free)
- Payment label: "One presentation" (not "single credit" / "one-off unlock")

### Visual Standard for UX Boards
- Karim wants every deliverable, UX included, to look elite and polished (Senior Product Designer level)
- Personas board is the reference: gradient hero, big quote, icon tiles, stats, dark gradient callouts

### Open Decisions
- Final prices for single presentation, credit pack and Pro
- Brand direction: A2 Folded Paper Night (dark-first, recommended) vs A light vs B Studio Violet vs C Blueprint — see Brand Exploration board
- Showcase examples for the landing page

---

## Installed Plugins

- **designer-skills plugin** at `C:\Users\kmedhat\.claude\plugins\marketplaces\designer-skills\`
  - Sub-plugins: design-ops, design-research, design-systems, designer-toolkit, interaction-design, prototyping-testing, ui-design, ux-strategy
