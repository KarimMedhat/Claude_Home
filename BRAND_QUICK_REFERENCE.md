# Techtifai Brand Quick Reference

A one-page cheatsheet. Print or pin this in your design tool.

---

## Colors

| Role | Hex | RGB | Usage |
|---|---|---|---|
| **Primary — Navy** | `#243C65` | `36, 60, 101` | Headings, primary buttons, dark sections, body text |
| **Accent — Red** | `#E33722` | `227, 55, 34` | Accent lines, button highlights, hover states. **Use sparingly.** |
| **Secondary — Light Blue** | `#B2DFF5` | `178, 223, 245` | Backgrounds on dark surfaces, supporting graphics, on-dark text accents |
| **Supporting — Mid Blue** | `#156082` | `21, 96, 130` | Eyebrows, links, secondary buttons |
| **Background — White** | `#FFFFFF` | `255, 255, 255` | Page background, card fills |
| **Background Alt — Off-White** | `#F4F6F8` | `244, 246, 248` | Alternating section backgrounds, input fields |
| **Border** | `#DDE2EA` | `221, 226, 234` | Card borders, dividers |
| **Muted Text** | `#6B7280` | `107, 114, 128` | Captions, footer text, secondary labels |

### Color usage rule
The brand should feel **navy-dominant**, with **red as a precise accent only**. As a rough guideline:
- 60% navy (text, headings, dark surfaces)
- 30% white/off-white (backgrounds)
- 8% light blue (secondary surfaces, supporting graphics)
- 2% red (accents, primary CTAs only)

---

## Typography

| Style | Font | Size | Weight | Tracking |
|---|---|---|---|---|
| **H1 (Hero)** | Aptos Display | 60–72px | Bold (700) | Tight (-0.02em) |
| **H2 (Section)** | Aptos Display | 36–48px | Bold (700) | Tight (-0.02em) |
| **H3 (Subsection)** | Aptos Display | 24–30px | Bold (700) | Normal |
| **Eyebrow** | Aptos | 11–12px | Bold (700) | Widest (0.2em), UPPERCASE |
| **Body Large** | Aptos | 18–20px | Regular | Normal |
| **Body** | Aptos | 16px | Regular | Normal |
| **Body Small** | Aptos | 14px | Regular | Normal |
| **Caption** | Aptos | 12px | Regular | Wide (0.05em) |

### Font fallback stack
`"Aptos Display", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`

If Aptos isn't licensed for web use, **Inter** is the recommended substitute — it's free, has the same modern feel, and is widely available via Google Fonts.

---

## Logo usage

### Wordmark variants (use the full "techtifai" wordmark in most contexts)
| File | When to use |
|---|---|
| `techtifai-wordmark-navy-transparent.png` | Default — navigation, headers on white/light backgrounds |
| `techtifai-wordmark-white-transparent.png` | Dark navy backgrounds (hero, section dividers, footer) |
| `techtifai-wordmark-lightblue-transparent.png` | Special accent contexts only — confirm before use |
| `techtifai-wordmark-red-transparent.png` | Special accent contexts only — confirm before use |

### Mark variants (the "tt" symbol — for constrained spaces)
- Favicons, social profile icons, app icons
- Loading spinners, watermarks
- Tab indicators, breadcrumbs

### Logo rules
- **Minimum size**: 80px wide for the wordmark, 32px for the mark
- **Clear space**: keep at least 1× the height of the logo as padding around it
- **Don't**: stretch, recolor outside approved variants, add drop shadows, place over busy imagery without sufficient contrast

---

## Spacing scale

4px base unit. Use multiples for all layout decisions.

```
4px   8px   12px   16px   24px   32px   48px   64px   96px   128px
```

### Section spacing
- **Compact section**: 48–80px vertical padding
- **Standard section**: 80–128px vertical padding
- **Large hero / impact section**: 128–160px vertical padding

### Container
- Max width: **1280px**
- Horizontal gutter: **24px** desktop, **16px** mobile

---

## Components

### Buttons
| Style | Background | Text | Border | Hover |
|---|---|---|---|---|
| **Primary CTA** | Red `#E33722` | White | None | Darken to `#B92C1B` |
| **Secondary** | White | Navy | 1.5px navy | Navy bg + white text |
| **Tertiary / Ghost** | Transparent | Navy | None | Underline navy |
| **On-dark Primary** | Red `#E33722` | White | None | Darken |
| **On-dark Secondary** | Transparent | White | 1.5px white | White bg + navy text |

Button padding: `12px 24px` (small), `16px 32px` (default), `20px 40px` (large)
Border radius: `4px` (squared, on-brand) — avoid pill buttons.

### Cards
- Default: white background, 1px `#DDE2EA` border, no shadow
- Optional: 4px **red top accent bar** for emphasis
- Optional: subtle shadow on hover (`shadow-md` from tokens)

### Section eyebrows
Always uppercase, red, 11–12px, bold, 0.2em letter-spacing. Always followed by a 50–60px red accent line under the section headline.

### Bottom accent line (signature template element)
A thin (1.5px) horizontal navy line near the bottom of every page section, spanning the container width. This is a signature element from the master brand template — keep it consistent throughout.

---

## Aesthetic direction

- **Clean, minimalist white** with generous whitespace
- **Navy hero/section dividers** with subtle tech-circuit patterns (interconnected nodes + thin lines in light blue, ~25% opacity)
- **Red strictly as an accent** — never as a primary fill except the CTA button
- **Tech-forward** — abstract tech imagery, infrastructure photos, product shots of real hardware. **Avoid** generic "businesspeople in suits" stock photos.

---

## Don'ts

- ❌ Don't use red as a primary background color
- ❌ Don't use the wordmark below 80px wide
- ❌ Don't use script, serif, or condensed fonts anywhere — Aptos / Inter only
- ❌ Don't use rounded pill buttons or super-rounded card corners (we're tech-forward, not friendly-startup)
- ❌ Don't use generic stock photos of corporate handshakes or smiling office workers
- ❌ Don't omit the bottom accent line on major sections — it's a signature element
- ❌ Don't use unapproved colors (purple, green, yellow) — stick to the navy/red/light-blue/mid-blue palette

---

## Do's

- ✅ Use lots of whitespace
- ✅ Lead with the navy + a touch of red — the look should feel confident and precise
- ✅ Use the eyebrow → headline → accent line → body pattern for section openings
- ✅ Mix dark navy hero/CTA bands with white content sections for rhythm
- ✅ Use abstract or infrastructure imagery for visual interest
- ✅ Keep buttons squared (4px radius) for the tech-forward feel
