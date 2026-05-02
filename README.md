# Techtifai — Web Development Handoff Package

This package contains everything the design and development team needs to build the Techtifai website. It accompanies the **Website Content Brief** (separate Word document) which provides all approved page copy.

---

## What's in this package

```
techtifai-handoff/
├── README.md                       ← you are here
├── BRAND_QUICK_REFERENCE.md        ← one-page brand cheatsheet
├── logos/                          ← all logo variants + favicons + social
│   ├── wordmark/                   ← full "techtifai" wordmark (8 variants)
│   ├── mark/                       ← "tt" mark only (8 variants)
│   ├── favicons/                   ← favicon set, including .ico and apple-touch
│   └── social/                     ← Open Graph / LinkedIn / Twitter cards
├── tokens/                         ← design tokens for code
│   ├── tokens.css                  ← CSS custom properties (drop into any project)
│   ├── tokens.json                 ← W3C Design Tokens format (for Style Dictionary, Tokens Studio)
│   └── tailwind.preset.js          ← Tailwind preset (drop into tailwind.config.js)
└── wireframes/                     ← 9 page wireframes
    ├── 01-home.svg / .png
    ├── 02-about.svg / .png
    ├── 03-services.svg / .png
    ├── 04-industries.svg / .png
    ├── 05-process.svg / .png
    ├── 06-why-us.svg / .png
    ├── 07-case-studies.svg / .png
    ├── 08-team.svg / .png
    └── 09-contact.svg / .png
```

---

## How to use this package

### Step 1 — Read the Website Content Brief first
The accompanying `Techtifai_Website_Content_Brief.docx` contains:
- Approved copy for every page (use **verbatim**)
- SEO meta titles and descriptions
- CTA button labels and link destinations
- Form field specifications
- Notes and open items to confirm with the client

This handoff package is the **visual and technical companion** to that brief.

### Step 2 — Set up your design tokens
Choose one of these depending on your stack:

**Plain CSS / no framework:**
```html
<link rel="stylesheet" href="tokens/tokens.css">
```
Then use `var(--color-navy)`, `var(--color-red)`, etc. throughout your CSS.

**Tailwind:**
```js
// tailwind.config.js
const techtifai = require('./tokens/tailwind.preset.js');
module.exports = {
  presets: [techtifai],
  content: [...your content paths],
};
```
Then use `bg-navy`, `text-red-accent`, `font-heading`, etc. in your markup.

**Style Dictionary / Tokens Studio for Figma:**
Import `tokens/tokens.json` — it's in the W3C Design Tokens community format.

### Step 3 — Use the wireframes as your layout reference
Each `.png` file shows the full layout for that page including:
- Navigation and footer
- Hero treatment
- Section structure and flow
- Card grids, comparison rows, photo placeholders
- CTA placement

The wireframes are intentionally **low-fidelity** — they specify *structure*, not final visual polish. Match the brand tokens to bring them to life.

### Step 4 — Drop in the logos
Use the **transparent PNG variants** in production code:
- `techtifai-wordmark-navy-transparent.png` — for navigation on light backgrounds
- `techtifai-wordmark-white-transparent.png` — for navigation on dark backgrounds
- `techtifai-mark-navy-transparent.png` — for favicons, social icons, constrained spaces

Favicons are pre-generated in `logos/favicons/`. Drop them straight into your `<head>`:
```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicons/favicon-192x192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicons/apple-touch-icon.png">
```

Use the social card images in OG meta tags:
```html
<meta property="og:image" content="/social/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="/social/twitter-card.png">
```

---

## Recommended tech stack (suggestion only)

The site is a **brochure / marketing site** with one form. Suggested stacks ranked by trade-off:

| Stack | Pro | Con |
|---|---|---|
| **Next.js + Vercel** | Best SEO, fast, scalable, easy to extend later | Slight learning curve if team unfamiliar |
| **Astro + Netlify** | Super-fast static, simple, great DX | Newer ecosystem |
| **Plain HTML + Netlify/Vercel** | Zero framework overhead, dead simple | Harder to maintain at scale |
| **Webflow** | No-code option, client can edit | Subscription cost, less flexible |

For the **contact form**, hook up to:
- **Formspree** (recommended — free tier sufficient, drop-in form action)
- **Netlify Forms** (if hosting on Netlify)
- **Resend / SendGrid** (if you have a backend)

---

## Open items the client needs to provide

These are flagged in the Website Content Brief but listed here for visibility:

1. **Headshot photography** for all 4 leadership team members
2. **Final contact details** — address, phone, email, website domain, LinkedIn URL
3. **Decision on blog/insights section** for v1 (currently not included)
4. **Decision on client logo / trust bar** for the homepage (currently not included)
5. **Privacy policy + cookie consent copy** (need before launch in GCC and EU jurisdictions)
6. **Domain + hosting setup** — which provider, who manages DNS

---

## Brand essentials at a glance

See `BRAND_QUICK_REFERENCE.md` for a one-page printable summary, but in short:

- **Primary**: Navy `#243C65`
- **Accent**: Red `#E33722` (used sparingly — accent lines, hover states, key highlights)
- **Secondary**: Light Blue `#B2DFF5` (backgrounds on dark surfaces, supporting graphics)
- **Supporting**: Mid Blue `#156082` (eyebrows, links, secondary buttons)
- **Type**: Aptos Display (headings) / Aptos (body); fallback to Inter

---

## Aesthetic direction

- **Clean, minimalist white** with generous whitespace on content sections
- **Navy hero/section dividers** with a subtle tech-circuit pattern (interconnected nodes and lines in light blue)
- **Red as a precise accent** — thin underlines, button hover states, key highlights only. Never as a primary fill except the primary CTA button.
- **Thin horizontal accent line** at the bottom of major sections — a signature template element
- **Tech-forward, not corporate** — avoid generic "businesspeople in suits" stock photos. Prefer abstract tech imagery, infrastructure photography, or product photos of real connectivity hardware.

---

## Performance and accessibility targets

- Lighthouse 90+ across Performance, Accessibility, Best Practices, SEO
- WCAG 2.1 AA contrast compliance (verify red `#E33722` only used as text on white when ≥18pt or bold)
- Fully responsive: mobile (320–767), tablet (768–1023), desktop (1024+)
- All images need descriptive alt text; decorative SVGs use `role="presentation"`
- Page weight: target <500KB initial load (excluding images)

---

## Questions or issues

For copy/content questions: refer to the **Website Content Brief** appendix or contact the client.
For brand/visual questions: refer to `BRAND_QUICK_REFERENCE.md`.

---

*This handoff package was prepared as a development-ready spec. Treat the wireframes as structural references, not pixel-perfect mockups — bring them to life with the brand tokens and the visual direction described above.*
