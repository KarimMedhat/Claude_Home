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

**Status:** UX phase — don't touch Figma until I say so

**Figma file:** https://www.figma.com/design/1rJxwwH7qnUPwOjFvQDXjd/Karim-Draft
- File key: `1rJxwwH7qnUPwOjFvQDXjd`
- UX page: node `2058:632`
- UI page: node `2058:633`
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

**Status:** UX phase. User flow drafted. Figma file created (see Active Projects), nothing designed yet. UI and the variables system come after UX.

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
- **Pricing direction:** Credit-based, not unlimited subscription

### Core Flow (summary)
Project type → Output format → Industry → Scope → Upload (screens / Figma link / docs) → Smart AI questions → 3 visual directions → Generate → Editor → Export

### Work Completed
- [x] User Flow v1 built in Figma on `Unfold_UX` — frame `2061:283` (Flows A–D with Goal / Success Metric / Key UX Decision, Edge Cases, Screens Inventory: 27 screens)
- [x] Local flow components on `Unfold_UX` — frame `2061:234`: Flow Node (Screen · AI · Decision · Modal · Edge Case · Terminal), Flow Arrow, Flow Note, Screen Chip, Section Header
- [ ] Competitive Analysis
- [ ] Personas
- [ ] Information Architecture
- [ ] Wireframes (Wizard + Editor first)

### Open Decisions
- Final pricing and credit amounts
- Brand identity for Unfold (logo, colors, typography)
- Showcase examples for the landing page

---

## Installed Plugins

- **designer-skills plugin** at `C:\Users\kmedhat\.claude\plugins\marketplaces\designer-skills\`
  - Sub-plugins: design-ops, design-research, design-systems, designer-toolkit, interaction-design, prototyping-testing, ui-design, ux-strategy
