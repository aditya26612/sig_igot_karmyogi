# Design Specification — iGOT Karmayogi × MoSPI Competency Platform Landing Page

**Project:** MoSPI AI-Enabled Competency & Learning Platform (SIH26101)
**Scope:** Landing page only — cinematic, sleek, and as close to the real igotkarmayogi.gov.in as possible
**Source of truth:** Design tokens extracted from the official iGOT Karmayogi design-token stylesheet (`design-tokens-F6JRIVZB.css`), homepage bundle, and portal styles — exact hex values, not approximations.
**Output target:** Google Stitch AI generation, desktop-first with full responsive behavior.

---

## 1. Design Philosophy

Three adjectives govern every decision: **Official. Modern-product. Cinematic.**

The real iGOT Karmayogi is NOT a traditional GIGW government portal — it is a modern product-marketing site (Bootstrap + Tailwind hybrid) for a 100% government-owned SPV. Its identity:

- **White/light canvas** with warm washes — not a navy-heavy government portal.
- **Royal blue** carries the brand; **amber-orange** is the single accent; **ink navy** for footer/dark surfaces.
- **Pill-shaped glassmorphism navbar** (59px end radius, frosted white blur) — its most distinctive component.
- **No GoI emblem strip, no tricolor band** — identity is carried by the Karmayogi Bharat brand (tricolor appears only as a tiny flag icon beside the welcome text). We follow this exactly.
- The cinematic layer (your tiger-reserve trick) is added on top: one strong ambient hero video, slow scroll reveals, one scroll-drawn narrative. Everything else stays calm.

> **Important correction from research:** the earlier navy `#1a365d` / saffron `#d97706` palette in the current codebase is NOT the real iGOT palette. The real system is below. Hand-off mapping is in §12.

---

## 2. Color System (EXACT — official iGOT Karmayogi tokens)

### 2.1 Primary — Royal Blue scale

| Token | Hex | Role |
|---|---|---|
| `color-primary-50` | `#E8EDF6` | Light wash backgrounds, chips |
| `color-primary-100` | `#B8C8E2` | Borders on light blue |
| `color-primary-200` | `#96ADD4` | — |
| **`color-primary-500`** | **`#1B4CA1`** | **THE brand blue** — primary buttons, stats band, hub circles, copyright bar |
| `color-primary-600` | `#194593` | Hover / focus state |
| `color-primary-700` | `#133672` | Active / pressed |
| `color-primary-800` | `#0F2A59` | Deep surfaces |
| `color-primary-900` | `#0B2044` | Deepest navy (video overlays) |

Legacy homepage var: `--color-primary:#264092` (deep indigo-blue, used in the big white strip CTA text). Keep both; `#264092` for the angled-strip CTA text, `#1B4CA1` for everything else.

### 2.2 Secondary — Amber/Orange scale

| Token | Hex | Role |
|---|---|---|
| `color-secondary-50` | `#FEF5EA` | Warm cream wash |
| `color-secondary-100` | `#FBDEBF` | Badge fills |
| `color-secondary-300` | `#F7B974` | — |
| **`color-secondary-500`** | **`#F3962F`** | **THE accent** — typewriter hero words, primary CTAs, nav active underline |
| `color-secondary-600` | `#DD892B` | Hover |
| `color-secondary-700` | `#AD6B21` | Pressed |
| Bright variant | `#FFA730` | Highlights, video-player progress, legacy `--yellow` |

### 2.3 Tertiary — Ink/Charcoal scale (dark surfaces & footer)

| Token | Hex | Role |
|---|---|---|
| `color-tertiary-100` | `#B8BAC0` | Muted text on dark |
| `color-tertiary-300` | `#666A76` | — |
| `color-tertiary-400` | `#494D5C` | — |
| **`color-tertiary-500`** | **`#1B2133`** | Footer bg, surface-inverse |
| `color-tertiary-600` | `#191E2E` / `#1A2235` | Footer provider-strip bg |
| `color-tertiary-700` | `#131724` | Deepest ink |
| Divider on dark | `#2C3448` | Footer hairlines |

### 2.4 Text, neutrals & borders

| Role | Hex |
|---|---|
| Body text | `#374957` (slate gray-blue) |
| Labels / secondary | `#4A5764` |
| Muted / captions | `#5F7D95` |
| Light gray text | `#424242` |
| Light muted on dark | `#E5E7EB`, `#C1C9D1` |
| Borders | `#E5E7EB` (standard), `#D7D7EE` (lavender-gray, strip gradients) |
| Canvas | `#FFFFFF` with washes `#F8F9FF`, `#FEF5EA`, `#E8EDF6`, `#FCE5CC` (peach inner-page wash) |

### 2.5 Semantic colors

Success `#1D8923` · Warning `#E99E38` · Error `#D13924` / `#B02925` · Info `#0A5396`.
Chips/category accent palette (for domain tags): blue `#0088FF`, cyan `#00C0E8`, green `#34C759`, indigo `#6155F5`, mint `#00C8B3`, orange `#FF8D28`, pink `#FF2D55`, purple `#CB30E0`, red `#FF383C`, teal `#00C3D0`, yellow `#FFCC00`, brown `#AC7F5E`.

### 2.6 Signature gradients & surfaces

```
Logo sun motif:      radial #E94E12 → #EB6D07 → #F4970E → #FCBF06 → #F5EC74 → #FFFFFF (deep orange-to-gold)
Angled CTA strip bg: #8C9EDC (light periwinkle; 128px tall, angled, sits behind a white card)
Blue stats band:     solid #1B4CA1 (rounded container, white icons/numbers)
Card shadow (soft):  0 0 8px rgba(0,0,0,.1)
Card shadow (blue):   0 4px 16px rgba(27,76,161,.12)  (rgba of #1B4CA1)
Big CTA shadow:      0 0 .5rem rgba(5,45,172,.25)
Glass navbar:        rgba(255,255,255,.72) + backdrop-filter: blur(6px) + 1px border rgba(0,0,0,.24)
Hero video overlay:  linear-gradient(90deg, rgba(255,255,255,.94) 0%, rgba(255,255,255,.72) 45%, rgba(255,255,255,.25) 100%)
                      (light ivory wash keeps the iGOT light canvas while video glows beneath)
```

### 2.7 Color rules (strict)

1. White/ivory canvas dominates; blue is structure (buttons, band, nodes); orange is a **spoken accent only** (typewriter words, one CTA, active underlines). Roughly White 60 / Blue 30 / Orange 10.
2. One filled orange button per viewport; everything else is blue-fill, blue-outline, or white.
3. Ink `#1B2133` appears only in the footer — never in the content area.
4. The light-wash section backgrounds (`#F8F9FF`, `#FEF5EA`, `#E8EDF6`) alternate to create gentle rhythm — no dark-navy sections in the content area (that was the old assumption; the real iGOT stays light all the way down).

### 2.8 Dark mode (from the real "my iGOT" portal tokens — optional bonus)

Surfaces `#1B2133` / `#252D3F` / `#333D4C`; text `rgba(255,255,255,.96/.8/.72)`; canvas `#1B2133`. Wire later via `[data-theme]`; not needed for Stitch v1.

---

## 3. Typography (EXACT — official iGOT stack)

| Role | Font | Weights / notes |
|---|---|---|
| Headings & marketing body | **Montserrat** | 600 / 700; `--font-family-heading` |
| Nav & labels | **Lato** | 700, letter-spacing `.25px`, 12px nav links |
| Devanagari (Hindi toggle) | **Noto Sans** | Google Fonts, unicode-range U+0900–097F |
| Icons | **Material Icons** (24px, ligature) | + FontAwesome chevrons for carousels if needed |

Load Montserrat (400/600/700), Lato (400/700), Noto Sans (Devanagari subset) from Google Fonts with `display=swap`.

### 3.1 Type scale (official token scale)

| Token | Desktop | Tablet | Mobile |
|---|---|---|---|
| Display-1 | 48px | 36px | 30px |
| Display-2 | 40px | 30px | 28px |
| Heading-1 | 32px | 28px | 24px |
| Heading-2 | 28px | 24px | 20px |
| Title-1 | 24px | 20px | 18px |
| Title-2 | 20px | 16px | 16px |
| Sub-heading | 18px / 16px | 16/14px | 16/14px |
| Body | 16px / 14px | — | — |
| Caption / Fine-print | 12px | — | — |

Hero specifically: intro line `text-1` = 600 weight, 24px / 29px line-height; rotating headline `text-2` = 700 weight, 32px / 40px line-height in `#F3962F`.

### 3.2 Typography rules

- Section headings: Montserrat 700, ink `#1B2133` or body `#374957`; UPPERCASE eyebrow labels in `#374957` where iGOT uses them (e.g., "TAKE THE FIRST STEP…").
- Card titles clamp to 1 line (`-webkit-line-clamp:1`) exactly like iGOT cards.
- Nav links: Lato 700, 12px, letter-spacing `.25px`; active state = `border-bottom: 2px solid` orange.
- Buttons ≥ 14px/600. Minimum text 12px anywhere. Numbers in stats band use tabular alignment.

---

## 4. Spacing, Grid, Radius & Shadows

- **Container:** max-width 1280px, 24px side padding (16px mobile). iGOT uses Bootstrap container widths — 1140–1280px works.
- **Vertical rhythm:** sections 80–96px desktop / 56–64px mobile. Section header → content gap 40px.
- **Card padding:** 24–32px (iGOT uses ~1.7rem).
- **Radii (official):** content buttons 4px (`.25rem`) · cards 4–8px · hub circles `50%` · navbar pills 32–59px · portal tokens `--radius-4/8/12/16/999`. **The pill navbar and pill auth buttons are signature — do not square them.**
- **Buttons:** min-height 44px touch target (GIGW floor), content padding `.625rem`, min-width 110px.
- **Shadows:** card `0 0 8px rgba(0,0,0,.1)` · elevated `0 4px 16px rgba(27,76,161,.12)` · big CTA `0 0 .5rem rgba(5,45,172,.25)`.

---

## 5. Landing Page Structure (section-by-section, mirroring the real iGOT homepage)

Real iGOT mount order: welcome strip → glass pill header → hero (typewriter) → banner carousel → blue stats band → orbital hub section → "What is iGOT" how-to carousel → featured courses → newsroom/testimonials → video walkthrough → app download → angled register strip → two-tier footer. We keep that exact order, with the hero upgraded to the cinematic video hero and two MoSPI-specific insertions (§5.7 competency journey, §5.9 AI Copilot).

### 5.0 — Welcome Micro-Strip (replaces any GoI strip)
- Thin top strip on white/ivory: small **tricolor flag icon** (`flag.svg` style) + text **"WELCOME TO iGOT KARMAYOGI — MoSPI"** in Lato 700, 12px, ink.
- Right side: **हिंदी / English** language toggle button (Lato 700 12px).
- No Government-of-India dark bar, no tricolor band — the real site has neither.

### 5.1 — Floating Glass Pill Navbar (signature component)
- `border-radius: 59px`, `height: ~70px`, `background: rgba(255,255,255,.72)`, `backdrop-filter: blur(6px)`, `border: 1px solid rgba(0,0,0,.24)`. Floats inset ~16px from page top, full-width minus gutters (like the real site's floating header).
- **Left:** platform logo lockup — sun/flame motif (radial orange-gold gradient) + wordmark in ink `#1B2133`, royal blue `#1F3C85`, orange `#F0951E` (the real logo's three ink colors). For Stitch, describe: "radiant sun gradient mark + 'iGOT Karmayogi MoSPI' wordmark".
- **Center nav links** (Lato 700 12px): Home · My Learning · Skill Gaps · Career Path · Newsroom · Help Center — active link gets `border-bottom: 2px solid #F3962F`.
- **Right:** **Login** = outline pill (`color:#1B4CA1; border:1px solid #1B4CA1; border-radius:32px`) · **Register** = filled orange pill (`#F3962F`, radius 32px). Persona switcher avatar chip beside them (32px circle, blue fill).
- Mobile: hamburger inside the pill; accordion menu below.

### 5.2 — Cinematic Hero (the showpiece — tiger-project formula, iGOT skin)
- **Full-viewport (90–100vh) muted looping background video**: Indian government officers in training, census field operations, data-visualization close-ups, New Delhi institutional architecture. Slow pans, no fast cuts, 12–20s loop.
- **Overlay:** light ivory wash `linear-gradient(90deg, rgba(255,255,255,.94) → .72 → .25)` — text sits on the LEFT on an almost-white field while the video glows through on the right. This keeps the iGOT light-canvas identity AND makes video the hero (the inverse of the old dark-navy assumption).
- **Content (left-aligned, max-width 620px):**
  - Small intro line (Montserrat 600, 24px): "iGOT Karmayogi for India's Official Statistical System"
  - **Rotating typewriter headline** (Montserrat 700, 32–40px): fixed prefix "iGOT " + cycling orange `#F3962F` words: **Learn-ing · Compete-ncy · Practic-ing · Verify-ing · Grow-ing** — typed at 50ms/char, cycling every 4s. (This is the real site's exact hero mechanic.)
  - Sub-line (16px, `#374957`): "AI-curated learning paths, searchable transcripts, and supervisor-verified competency growth for MoSPI officers."
  - CTA row: **filled blue pill** "Begin Your Learning Journey" (`#1B4CA1`, white text) + **outline blue pill** "Explore the Platform".
  - Trust line (12px, `#5F7D95`): "Aligned to Karmayogi Bharat competency principles · 100% rubric-verified promotions".
- **Right side:** floating white glass cards (parallax ±10px) previewing the learner dashboard — competency progress ring (blue), next-action card, AI Copilot bubble. Shadows `0 4px 16px rgba(27,76,161,.12)`.
- Scroll chevron, thin, bottom center. Social-links strip ("Follow us" + X/LinkedIn/YouTube/Instagram, 32px squares) sits at hero bottom like the real site.
- Video tech: `<video autoplay muted loop playsinline preload="metadata">` + poster fallback; below 768px → static poster only.

### 5.3 — Campaign Banner Carousel
- Full-width image carousel, 4 posters (rounded corners, `banner-radius`), dot indicators + chevron arrows (FontAwesome angle-left/right style). Posters = MoSPI campaign art (competency drive, census data quality, AI copilot launch), 1600×500.
- This mirrors iGOT's banner-inner owl-carousel exactly.

### 5.4 — Blue Stats Band (signature)
- Solid `#1B4CA1` rounded container, `padding: 24px 16px` per item, items `min-width 180px / max-width 250px`.
- White line-art icons (Network / Program / people / badge style, 24px) + white numbers + white labels:
  **20 Officers Onboarded (demo registry) · 40+ Competency Domains · 200+ Curated Courses · 26 iGOT Integration Tables · 100% Rubric-Verified Promotions**
- Count-up on scroll. Live-site reference numbers for tone: "30+ Lakhs Karmayogis · 868 courses".

### 5.5 — Orbital Hub Selector ("Solutioning space for all of Government") — the signature component
- Section heading (Montserrat 700, `#374957`): "One platform for the entire competency pipeline".
- **Six 64px white circles arranged on an orbit ring** (CSS `--angle` at 0/60/120/180/240/300deg), each `background:#fff; box-shadow:0 4px 16px #1b4ca11f`, Material icon inside: **Learning · Discussion · Network · Competency · Career · Events**.
- **Selected hub inverts:** solid `#1B4CA1` fill, white icon (`filter: brightness(0) invert(1)`).
- Beside/below the orbit, a detail card (`background:#fff; box-shadow:0 0 8px rgba(0,0,0,.1); height:180px; padding:1.7rem`) with the hub's title (h4, `#374957`) + 2-line description, e.g. Competency: "Identify your competency requirements and gaps, and bridge them with curated learning."
- Interaction: clicking a circle rotates selection (gentle 300ms ease) and swaps the detail card with a soft cross-fade. This is the single most recognizable iGOT component — build it faithfully.

### 5.6 — "What is iGOT / How-to" Carousel
- Horizontal card carousel: **"How to Register?"** · **"How to Login?"** · **"Platform Walkthrough"** — each a thumbnail card (`video1.png`-style art), dot indicators.
- 2–3 cards visible desktop; 1 on mobile; prev/next chevrons.

### 5.7 — The Competency Journey (MoSPI insert, iGOT-styled)
- Eyebrow (UPPERCASE, `#374957`): "THE COMPETENCY JOURNEY" · Heading: "From Skill Gap to Verified Promotion".
- Light canvas `#F8F9FF`. Horizontal 5-step timeline, blue `#1B4CA1` number nodes joined by an **orange gradient connector that draws in on scroll**:
  1. **Profile** — Admin creates your competency profile
  2. **Identify** — Gaps mapped to cadre requirements
  3. **Learn** — Curated videos, searchable transcripts, AI copilot
  4. **Practice** — Formative quizzes (never promote)
  5. **Verify & Promote** — Supervisor rubric review → max +1 level
- Caption strip under the timeline (12px, `#5F7D95`, verified-check icon): "Practice never promotes. Only supervisor-verified evidence moves your official competency level."

### 5.8 — Featured Courses Carousel
- Heading: "Featured Curated Learning" + "Show all" link button.
- **Horizontal carousel of course cards** (iGOT card pattern): image top (16:9, MoSPI lecture stills), 1-line clamped title (Montserrat 600, ink), provider chip (Karmayogi Bharat / MoSPI / NSSO), domain tag (accent-palette chip), duration + level meta.
- White cards, `0 4px 16px rgba(27,76,161,.12)` shadow, hover: translateY(-4px) + shadow deepen + image zoom 1.05.
- 8 cards, chevron arrows + dots. No filter grid — iGOT uses a carousel, not a filterable grid, on the homepage.

### 5.9 — AI Learning Copilot Showcase (MoSPI insert, iGOT-styled)
- Split layout on white: left — eyebrow "AI LEARNING COPILOT" + heading "Ask. Cite. Learn." + body copy ("Answers grounded strictly in MoSPI lecture transcripts with exact timestamp citations and out-of-domain guardrails.") + filled blue CTA "Try the Copilot".
- Right — mock chat UI in a white card: blue `#1B4CA1` header bar "Karmayogi Assistant", chat bubbles (user ink-on-cream, copilot white with blue border), `[02:15]` timestamp chips in orange, "Jump to transcript" outline-blue button, typing dots, suggested-question chips below.

### 5.10 — Newsroom + Karmayogi's Corner
- Two-column: **Newsroom** card list (4 items: "AI Learning Copilot launched for MoSPI cadres", "Aspirational Districts Data Quality Module now live", "Competency Framework v2 published", newsletter PDF links) + **testimonial slider** (officer portrait webp, quote, name/designation — e.g. "The transcript search transformed how I prepare for field assignments." — Junior Statistical Officer, NSSO Field Operations).
- White cards, dot slider, 24px padding.

### 5.11 — Video Walkthrough
- Full-width section: "A quick walkthrough of the MoSPI Competency Platform" + embedded `KarmayogiBharatWalkthroughNew.mp4`-style video in a rounded frame (orange `#FFA730` progress bar, video.js/Plyr player styling).
- Cinematic: screen-record your actual dashboard flow (login → gap → learn → quiz → promote) — authentic b-roll beats stock.

### 5.12 — App Download Section
- Phone mockup (`mobile-latest.png` style) + "Download the app" + Google Play badge + App Store badge + two QR codes (Android/iOS).
- For the hackathon: keep this section with QR codes pointing at the demo URL — it reads as production-real.

### 5.13 — Angled Register CTA Strip (signature)
- Light periwinkle `#8C9EDC` angled strip, 128px tall, positioned behind a **white overlapping card**.
- Card content: UPPERCASE h2 (`#374957`): "Take the **first step** towards learning" + **big white CTA button**: `background:#fff; color:#264092; text-transform:uppercase; font-weight:700; font-size:1.2rem; width:310px; height:72px; border-radius:8px; box-shadow:0 0 .5rem rgba(5,45,172,.25)` → label **"REGISTER NOW"**.
- Above the CTA inside the card: 3 pill role chips — **Learner · Supervisor · Administrator** (selected = blue fill white text) so the MoSPI persona switcher is preserved in iGOT's own visual language.

### 5.14 — Two-Tier Ink Footer (signature)
- **Tier 1 — main footer:** bg `#1B2133`, `padding: 40px 0`, 4-column link groups (links `#E5E7EB`, 14px, hover white):
  - Col 1: Help Center · Contact Us · RTI
  - Col 2: Nodal Office / MDO list · Karmayogi's Corner · Register
  - Col 3 "Related": Mission Karmayogi · DoPT · CBC · Privacy Policy
  - Col 4 (MoSPI): About MoSPI · NSSO · National Statistical Commission · Cadre Competency Matrix
  - Social icons row (X, LinkedIn, YouTube, Instagram, 32px). Mobile: accordion groups.
- **Tier 2 — provider strip:** bg `#1A2235`, `padding: 32px 0`, centered nowrap logo row (max 138px each): **MoSPI · NSSO · National Statistical Commission · Karmayogi Bharat · DoPT · CBC · Digital India · MyGov · data.gov.in · india.gov.in**.
- **Tier 3 — copyright bar:** bg `#1B4CA1`, 90px, rounded bottom corners 12px: "Copyright © Website managed by Karmayogi Bharat (SPV) — MoSPI edition. Smart India Hackathon Prototype."

### Global Floating Elements
- **AI Copilot FAB:** bottom-right, 58px circle, blue `#1B4CA1` fill (not a gradient — iGOT is flat), white sparkle Material icon, soft pulse.
- **Accessibility widget** (UserWay-style) bottom-left: screen-reader/contrast controls — the real site uses exactly this; a pill launcher works for Stitch.
- **Back-to-top** ghost circle near the FAB after scroll.

---

## 6. Cinematic Motion & Micro-interactions

*(The tiger-project formula, formalized — layered onto iGOT's calm product style)*

| Element | Motion |
|---|---|
| Hero video | Muted autoplay loop, 12–20s, slow pans only. |
| Typewriter headline | Types at 50ms/char, holds 4s, deletes, cycles next word — infinite. |
| Scroll reveal | Sections/cards fade-up 24px + fade, 600ms, stagger 80ms per card, `cubic-bezier(0.22,1,0.35,1)`, trigger at 20% viewport entry. |
| Cards hover | translateY(-4px), shadow soft→blue, image zoom 1.05. |
| Journey connector | Orange gradient line draws left→right, scroll-linked. |
| Stats counters | Count-up 1200ms ease-out, tabular numerals. |
| Orbital hubs | Selection swap cross-fades 300ms; orbit ring slowly rotates ±3deg on scroll (very subtle). |
| Hero glass cards | Parallax drift ±10px on scroll. |
| Carousels | Owl-style auto-advance 6s, pause on hover, dot indicators. |
| Navbar | Stays floating glass always (it already is); border darkens slightly after hero. |
| FAB | 2.4s soft pulse. |
| Prefers-reduced-motion | Disable video autoplay, typewriter (show full word), parallax, carousels auto-advance; keep opacity fades. |

**Cinematic formula (same as the tiger project):** one strong ambient hero loop + the typewriter + slow reveals + one scroll-drawn narrative (journey line). Everything else calm. Do not exceed this list.

---

## 7. Responsive Behavior

| Breakpoint | Behavior |
|---|---|
| ≥1280px | Full layout, 1280px container, 4-stat row, 3 how-to cards visible. |
| 1024–1279px | Container 1140px; featured courses 3 visible; hero H2 → 32px. |
| 768–1023px | Glass pill navbar keeps shape but links collapse to hamburger; hero type-2 → 28px; journey becomes 2-row grid; stats wrap 3+2. |
| <768px | Hero video → static poster; typewriter headline → 24px; all carousels 1 card; journey → vertical timeline with left connector; orbital hubs → 2×3 grid of circles (orbit ring hidden); angled strip → stacked card; footer → accordion; FAB inset 16px. |
| <480px | Hero CTAs full-width stacked; register CTA → full-width 56px; provider strip → horizontal scroll. |

Type sizes follow the official token scale (§3.1) per breakpoint — use those exact numbers.

---

## 8. Accessibility (GIGW-informed, as the real site does it)

- The real iGOT carries accessibility via the UserWay widget + bilingual toggle rather than classic GIGW chrome — mirror that: accessibility launcher (contrast, screen-reader, text-size), हिन्दी/English toggle.
- Contrast: white on `#1B4CA1` = 7.5:1 ✓ · ink `#1B2133` on white = 15:1 ✓ · `#374957` on white = 8.4:1 ✓ · white on orange `#F3962F` ≈ 2.4:1 — **use orange fills only for large/bold text (≥20px/700) or with ink text; body-size orange text is forbidden.**
- Focus visible: 2px `#1B4CA1` outline, 2px offset. Touch targets ≥44px. Skip-to-content link. Alt text everywhere. Captions notice for hero video. Full keyboard operability. `prefers-reduced-motion` honored.

---

## 9. Stitch Prompting Guide (section-by-section, with exact hex codes)

Stitch works best focused — generate one screen per prompt, then iterate. Keep hex codes in prompts; Stitch respects explicit colors.

1. **Hero (do this first):** "Landing page hero for a Government of India learning platform. Full-viewport muted background video of Indian government officers training, with a soft white gradient overlay from left (rgba(255,255,255,0.94)) to right (0.25) so the left side is nearly white. Left-aligned text: small intro 'iGOT Karmayogi for India's Official Statistical System' in Montserrat 600 24px dark ink #1B2133, then a large Montserrat 700 40px headline with the word 'Learn-ing' in orange #F3962F, sub-line in #374957, a filled royal blue #1B4CA1 pill button 'Begin Your Learning Journey' and an outlined blue pill button 'Explore the Platform'. On the right, floating white glass cards previewing a learner dashboard with a blue progress ring. Above the hero: a thin welcome strip with a tiny tricolor flag icon and 'WELCOME TO iGOT KARMAYOGI — MoSPI' plus a Hindi/English toggle, and a floating pill-shaped glassmorphism navbar (59px rounded ends, rgba(255,255,255,0.72), blur) with a sun-gradient logo, center nav links, an outlined blue Login pill and a filled orange #F3962F Register pill."
2. **Stats band:** "Full-width solid royal blue #1B4CA1 rounded statistics band with five items — white line icons, large white numbers, small white labels: 20 Officers, 40+ Competency Domains, 200+ Curated Courses, 26 Integration Tables, 100% Verified Promotions. Montserrat font."
3. **Orbital hubs:** "Section with six 64px white circular icon badges arranged on an invisible orbit ring around a center, each with soft blue shadow 0 4px 16px rgba(27,76,161,0.12) and a Material icon: Learning, Discussion, Network, Competency, Career, Events. The selected circle is filled solid royal blue #1B4CA1 with a white inverted icon. Beside it a white detail card with heading in #374957 and two-line description, shadow 0 0 8px rgba(0,0,0,0.1). Light background #F8F9FF."
4. **Journey:** "Horizontal five-step timeline on light background #F8F9FF: blue #1B4CA1 numbered circles joined by an orange #F3962F connector line, steps Profile, Identify, Learn, Practice, Verify & Promote, Montserrat headings in dark ink #1B2133, captions in #5F7D95."
5. **Featured courses:** "Horizontal carousel of white course cards with soft blue shadows: thumbnail top, one-line clamped title in dark ink, provider chip, orange domain tag, duration meta. Rounded 8px corners, Montserrat font."
6. **AI Copilot:** "Split section: left text with royal blue pill CTA, right a white chat mockup card with a royal blue #1B4CA1 header bar titled 'Karmayogi Assistant', chat bubbles, orange #F3962F timestamp chips [02:15], an outlined blue 'Jump to transcript' button, suggested question chips below."
7. **Angled CTA strip:** "Light periwinkle #8C9EDC angled diagonal band behind an overlapping white card. Card has an uppercase Montserrat 700 heading in #374957 'TAKE THE FIRST STEP TOWARDS LEARNING', three pill role chips Learner Supervisor Administrator (selected one filled royal blue), and a very large white button with dark blue #264092 uppercase text 'REGISTER NOW', radius 8px, blue-tinted shadow."
8. **Footer:** "Dark ink navy #1B2133 footer with four columns of light gray #E5E7EB links (Help Center, RTI, Mission Karmayogi, MoSPI links), social icons row; below it a slightly darker #1A2235 strip with a centered row of government partner logos; below that a royal blue #1B4CA1 copyright bar with rounded bottom corners."

**Iteration tips:** regenerate single sections rather than whole pages; export → hand-code into React with the token mapping in §12; feed the typewriter/orbit behaviors as code, not as image content.

---

## 10. Asset Checklist

| Asset | Spec |
|---|---|
| Hero video (12–20s loop) | Officers training / census fieldwork / data-viz b-roll; 1920×1080, <8MB, muted. Pexels/Pixabay: "government office India", "data visualization", "New Delhi architecture". |
| Hero poster | First-frame JPEG <300KB (mobile fallback). |
| Campaign banner posters ×4 | 1600×500 MoSPI campaign art, webp. |
| Course thumbnails ×8 | Real lecture stills/chart close-ups, 16:9, <100KB, webp. |
| How-to thumbnails ×3 | Register / Login / Walkthrough art. |
| Walkthrough video | Screen-record the actual dashboard flow, 60–90s. |
| Sun/flame logo mark | SVG, radial gradient #E94E12→#FCBF06→#FFFFFF, beside ink/blue/orange wordmark. |
| White line icons | Stats band + orbital hubs (Material Icons exports, white 24px). |
| Officer portraits | Testimonial webp avatars. |
| QR codes ×2 | Demo URL (Android/iOS). |
| Partner logos | MoSPI, NSSO, NSC, Karmayogi Bharat, DoPT, CBC, Digital India, MyGov, data.gov.in, india.gov.in — transparent PNG, max-height 138px in footer strip (grayscale-able). |

---

## 11. Copy Deck (ready-to-paste)

- **Welcome strip:** WELCOME TO iGOT KARMAYOGI — MoSPI · हिन्दी / English
- **Hero intro:** iGOT Karmayogi for India's Official Statistical System
- **Typewriter words:** Learn-ing · Compete-ncy · Practic-ing · Verify-ing · Grow-ing (prefix "iGOT ")
- **Hero sub:** AI-curated learning paths, searchable transcripts, and supervisor-verified competency growth for MoSPI officers.
- **CTAs:** Begin Your Learning Journey / Explore the Platform / REGISTER NOW
- **Stats:** 20 Officers Onboarded · 40+ Competency Domains · 200+ Curated Courses · 26 iGOT Integration Tables · 100% Rubric-Verified Promotions
- **Hub descriptions:** Learning — "Learn anytime, anywhere and bridge your competency gaps." · Discussion — "Discuss and learn with peers, colleagues and experts." · Network — "Connect with officers across the National Statistical System." · Competency — "Identify your competency requirements and gaps, and bridge them." · Career — "Explore career opportunities across the cadre." · Events — "Participate in drives, marathons and expert sessions."
- **Journey:** Profile → Identify → Learn → Practice → Verify & Promote · "Practice never promotes. Only supervisor-verified evidence moves your official competency level."
- **Testimonials:** "The transcript search transformed how I prepare for field assignments." — Junior Statistical Officer, NSSO Field Operations · "Competency reviews are finally transparent and evidence-based." — Director, NSSO Evaluation Division
- **Angled strip:** TAKE THE FIRST STEP TOWARDS LEARNING
- **Footer copyright:** Copyright © Website managed by Karmayogi Bharat (SPV) — MoSPI edition. Smart India Hackathon Prototype.

---

## 12. Handoff Notes (React integration & token migration)

Map your existing `frontend/src/index.css` values to the real iGOT tokens (rename nothing, swap values):

| Current token (old value) | New value |
|---|---|
| `--color-primary` `#1a365d` | `#1B4CA1` |
| `--color-primary-dark` `#0f294a` | `#133672` |
| `--color-primary-light` `#2b6cb0` | `#4970B4` |
| `--color-primary-subtle` `#ebf8ff` | `#E8EDF6` |
| `--color-accent` `#d97706` | `#F3962F` |
| `--color-accent-hover` `#b45309` | `#AD6B21` |
| `--color-accent-subtle` `#fef3c7` | `#FEF5EA` |
| `--color-success` `#2e7d32` | `#1D8923` |
| Footer bg `#0f294a` | `#1B2133` (provider strip `#1A2235`, copyright bar `#1B4CA1`) |
| `--color-text-primary` `#0f172a` | `#1B2133` |
| `--color-text-secondary` `#475569` | `#374957` |
| `--color-text-muted` `#64748b` | `#5F7D95` |
| `--color-border` `#e2e8f0` | `#E5E7EB` |
| Fonts: Outfit/Inter | Montserrat (headings, 600/700) + Lato (nav/labels, 700) + Noto Sans (Devanagari) |
| Navbar: white rectangular | Floating glass pill (59px radius, rgba(255,255,255,.72), blur 6px) |
| GoI strip + tricolor band | Remove — replace with welcome micro-strip + flag icon |
| Footer top border saffron 4px | Remove — two-tier ink footer + blue copyright bar instead |

Component notes:
- Landing lives in one `LandingPage.tsx`; keep the existing dashboard views untouched (they'll inherit the new token values automatically).
- Typewriter: simple `setInterval` char-slicer at 50ms/char, 4s hold — no library needed.
- Orbital hubs: absolute-positioned 64px circles with CSS `--angle` transform; swap detail card content from a static map.
- `<video>`: `autoplay muted loop playsinline preload="metadata"` + poster attr as fallback; JS swaps in `src` after `DOMContentLoaded`.
- Lazy-load below-fold sections via `IntersectionObserver`; `loading="lazy"` on all imagery; carousels: Keen-Slider or plain scroll-snap (scroll-snap is lighter and GIGW-friendly).
- Keep the in-app GIGW controls (A−/A/A+, contrast) inside the accessibility launcher — the real site does this via UserWay.

---

All sections above constitute the complete landing page. Read §2 before any color decision, §9 before prompting Stitch, §10–11 before asset hunting and copy-fitting, §12 before touching `index.css`.
