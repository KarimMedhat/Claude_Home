# Unfold — User Flow (v1)

> AI-powered presentation generator for designers. Turns raw project material into a portfolio-ready presentation (Behance, Slides, Dribbble, PDF).
> Website · English · LTR · Status: planning (no Figma work yet)

---

## Flow A — First-Time Visitor

```
Landing Page
  └─ CTA "Start Free"
       └─ Sign Up (Google / Email)
            └─ Quick Onboarding
                 ├─ Role: UI/UX Designer · Product Designer · Developer · Other
                 └─ Brand Kit (optional, skippable): logo, colors, font
                      └─ Dashboard (empty state → "Create your first presentation")
                           └─ Flow B
```

---

## Flow B — Create a Presentation (Core Flow)

### Step 1 — Project Basics
- Project name
- Project type:
  - Case Study
  - UI Shots
  - Redesign
  - Design System
  - Landing Page / Website
  - Mobile App Showcase
  - Concept / Personal Project
  - Other (free text, AI decides the structure)

### Step 2 — Output Format
- Behance Long-scroll
- Slides 16:9
- Dribbble Shots
- PDF Portfolio
- Note: switchable later from the Editor (same content, different layout)

### Step 3 — Industry
- Fintech · Health · E-commerce · SaaS · Education · Real Estate · Travel · Food · Other
- Drives mood, color, and visual style suggestions

### Step 4 — Scope
- UI only → Mockups, Style Guide, Components
- UX only → Research, Personas, User Flows, Wireframes
- Both → full set

### Step 5 — Upload Content
- Screens (drag & drop images)
- Figma link (import frames directly)
- Docs: research, notes, PDFs
- Product logo & colors (optional)

### Step 6 — Smart Questions
- AI asks 5–8 short questions based on type + scope (problem, users, goals, process, results)
- Answers pre-filled from uploaded docs when possible
- Every question can be skipped

### Step 7 — Visual Direction
- AI shows 3 style directions (thumbnail previews)
- Pick one, or regenerate

### Step 8 — Generating
- Progress screen with visible steps: Writing story → Building layout → Styling → Done
- Auto-save; user can leave and come back

### Step 9 — Editor
- **Left panel:** sections list (reorder, add, delete)
- **Canvas:** live presentation preview
- **Right panel:** edit text, adjust style, regenerate a section with a prompt
- **Top bar:** format switcher (Behance ↔ Slides ↔ Dribbble ↔ PDF), Export button

### Step 10 — Export
| Format | Output |
|---|---|
| Behance | Long images, 1400px width, sliced into modules |
| Slides | PDF / PPTX |
| Dribbble | 1600×1200 shots |
| PDF | Portfolio-ready PDF |
| Figma | Editable Figma file |

---

## Flow C — Returning User

```
Login → Dashboard
  ├─ Open project → Editor
  ├─ Duplicate project
  ├─ Delete project
  └─ New project → Flow B
```

---

## Flow D — Payment

```
User clicks Generate
  ├─ Free presentation left? → Yes → Generation runs (first one is free)
  └─ No → Enough credits?
       ├─ Yes → Generation runs (credits deducted on success only)
       └─ No → Paywall: choose how to pay
            ├─ One presentation → Checkout ($6 one-time, example price)
            ├─ Credit pack      → Checkout ($12 / 100 credits)
            └─ Pro              → Checkout ($16 / month)

From any checkout → Payment successful?
  ├─ Yes → Unlock & resume (one-time: presentation unlocked · pack/pro: credits added) → Generation runs
  └─ No  → Payment failed → back to Paywall (nothing lost)
```

**One presentation (one-time) includes:** 1 generation, 10 section regenerations, all formats & exports, never expires.

**Credit usage (draft):**
- Full generation = high cost
- Regenerate one section = low cost
- Switch format = low cost

---

## Edge Cases

- Upload fails → retry + clear error message
- Weak input (few screens, no context) → AI asks extra questions before generating
- Generation fails → retry, credits not charged
- User leaves the wizard midway → auto-saved as draft in Dashboard
- Figma link without access → instructions to share the file / make it viewable

---

## Screens List (v1)

**Marketing:** Home · How it Works · Showcase · Pricing · Login · Sign Up

**App:** Onboarding · Dashboard · Wizard (Steps 1–7) · Generating · Editor · Export · Brand Kit · Settings · Billing · Paywall modal
