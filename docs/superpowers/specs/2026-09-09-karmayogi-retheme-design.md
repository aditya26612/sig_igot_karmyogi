# Design Spec — "Karmayogi Sunrise" Orange-Led Re-Theme

**Project:** MoSPI AI-Enabled Competency & Learning Platform (SIH26101)
**Scope:** Whole-app re-theme of the existing React + Vite frontend (`frontend/`). Theme-only — no behavior, route, or data-flow changes.
**Status:** Approved by user (2026-09-09). Decisions locked via Q&A; see "Locked Decisions".
**Token source of truth:** root `design.md` §2–§12 (official iGOT Karmayogi extracted tokens) + user's orange-led override.

---

## 1. Locked Decisions (user-approved)

| # | Decision | Choice |
|---|----------|--------|
| D1 | Palette lead | **Orange-led hybrid**: orange `#F3962F` carries CTAs, active states, progress; ink `#1B2133` carries text/footer; royal blue `#1B4CA1` stays quiet (links, info chips). |
| D2 | Scope | **Whole app re-theme + landing page** (amended 2026-09-09: user supplied the landing background image and asked for the landing in this pass). Token rewrite + glass navbar + all 6 views + modals/drawer/player + new `LandingPage.tsx` built around the supplied hero image. |
| D3 | Hero | **Typewriter hero over the supplied background image** (`frontend/src/assets/landing-hero.jpg`, 1600×639, 88% bright, warm cream/peach palette that is theme-native). Clean rotating words: `Learning · Competency · Practising · Verifying · Growing` (orange `#F3962F`, 50ms/char, hold 4s, delete, cycle). Ink text stays legible on the bright cream image; no dark overlay needed — a white gradient wash keeps the left text zone clear. |
| D8 | Landing background | User-supplied image `landing-hero.jpg` — measured dominant colors `#FDF9F4`/`#FBE3C8`/`#EABA8E` (cream/peach, ≈ the theme's `--wash-cream`/`--orange-100`/`--orange-300`). It reinforces rather than fights the orange+white theme. Left-anchored white gradient overlay for text legibility; `object-fit: cover`; `loading="eager"` + `fetchpriority="high"` (it is the LCP element); static poster under `prefers-reduced-motion`. |
| D4 | Navbar form | **Floating glass pill** (inset ~16px, `rgba(255,255,255,.72)`, `backdrop-filter: blur(6px)`, 59px radius, orange active underline, pill auth buttons) + welcome micro-strip above. |
| D5 | Motion level | Signature moments only — typewriter hero, count-up stats, soft scroll reveals, hover lift. No video dependency, demo-safe, `prefers-reduced-motion` respected. |
| D6 | Icons | All emoji-as-icon instances replaced with inline SVGs (single stroke/weight, Material-Symbols-like). |
| D7 | Landing hero vocabulary | User confirmed typewriter words are clean-spelled; hyphens in design.md were rhythm notation only, never rendered. |

---

## 2. Token System (rewrite `frontend/src/index.css` `:root`)

Three layers: primitive tokens (raw scales) → semantic tokens (roles) → component classes. Values from design.md §2/§12 hand-off map:

### Primitives
```css
:root {
  /* Orange scale (brand lead) */
  --orange-50: #FEF5EA; --orange-100: #FBDEBF; --orange-300: #F7B974;
  --orange-500: #F3962F; --orange-600: #DD892B; --orange-700: #AD6B21;
  --orange-bright: #FFA730;

  /* Royal blue scale (quiet support) */
  --blue-50: #E8EDF6; --blue-100: #B8C8E2; --blue-500: #1B4CA1;
  --blue-600: #194593; --blue-700: #133672; --blue-900: #0B2044;

  /* Ink scale (text, footer) */
  --ink-100: #B8BAC0; --ink-300: #666A76; --ink-400: #494D5C; --ink-500: #1B2133;
  --ink-600: #191E2E; --ink-700: #131724; --ink-divider: #2C3448;

  /* Warm neutrals & canvas */
  --canvas: #FFFFFF; --wash-cream: #FEF5EA; --wash-blue: #E8EDF6;
  --wash-ivory: #F8F9FF; --wash-peach: #FCE5CC;
  --body-text: #374957; --label-text: #4A5764; --muted-text: #5F7D95;

  /* Semantic */
  --success: #1D8923; --warning: #E99E38; --error: #D13924; --info: #0A5396;

  /* Type */
  --font-heading: 'Montserrat', sans-serif;   /* 600/700, headings */
  --font-sans: 'Lato', sans-serif;             /* nav, labels, body */
  --font-fallback: 'Inter', sans-serif;        /* body fallback in stack */

  /* Radii & shadows — official iGOT values */
  --radius-btn: 4px; --radius-card: 8px; --radius-pill: 9999px;
  --radius-nav: 59px; --radius-auth-pill: 32px;
  --shadow-card: 0 0 8px rgba(0,0,0,.1);
  --shadow-elevated: 0 4px 16px rgba(27,76,161,.12);
  --shadow-cta: 0 0 .5rem rgba(5,45,172,.25);
}
```

### Semantic + component layer
The existing class names (`gov-card`, `btn`, `btn-primary`, `badge-*`, `nav-tab`, `progress-*`, `modal-*`, `assistant-*`, `grid-*`) are **kept** (no renames) and restyled to the new tokens. This is deliberate: 14 files reference these classes; a value-swap re-themes every screen at once, and no component logic changes.

Additional component classes to add: `.glass-navbar`, `.welcome-strip`, `.brand-sun` (radial gradient mark), `.stat-chip`, `.hero-*`, `.reveal` (scroll animation), `.igot-btn`, `.igot-btn-outline`, `.igot-typewriter-cursor` classes as needed by Navbar/Landing components.

### Color discipline (from design.md §2.7)
- White/ivory canvas dominates; orange is spoken accent (CTAs, one orange element per viewport lead) — target White 60 / Ink-Blue 30 / Orange 10.
- Ink `#1B2133` never appears in the content area — footer only. Content text uses `#374957`/`#4A5764`/`#5F7D95`.
- One filled orange button per viewport; everything else blue-fill/blue-outline/white.
- Light-wash section backgrounds alternate (cream/blue/ivory) for rhythm.
- Orange `#F3962F` on white = 2.2:1 → never carries body text. Text on orange fills must be white (and only at large/bold sizes ≥ 18.66px bold or 24px, checked in verification).

---

## 3. Files & Changes

### 3.1 `frontend/index.html`
- Google Fonts link → Montserrat (400;600;700), Lato (400;700), Noto Sans (Devanagari, for हिंदी toggle later).
- Remove Outfit/Inter request. Keep preconnects.

### 3.1 Font decision: replace, keep Inter as fallback only
`--font-sans` becomes `'Lato','Inter',system` — Inter stays in the CSS fallback chain but is no longer loaded. `index.html` loads only Montserrat (400;600;700) + Lato (400;700) + Noto Sans (Devanagari subset, for the हिंदी toggle later). Outfit is dropped entirely. Both Montserrat and Lato are grotesque sans faces close in metrics to Inter; any layout shift gets caught in the verification screenshot pass.

### 3.2 `frontend/src/index.css` (full rewrite, ~600 lines)
Structure: tokens → base → glass navbar system → component classes → scroll-reveal utility → a11y states → responsive tweaks → `prefers-reduced-motion`. Sections:

1. **Tokens**: primitives → semantic → component tokens (as §2 above).
2. **Base**: reset, body on `--canvas` + `--font-sans` 16px/1.5, selection color (orange 30%), caret-color orange, focus-visible ring (blue 500 2px offset 2px), tabular numerals for stats, scrollbar theming (thin, ink/neutral).
2b. **Browser surfaces**: text selection (cream bg, ink text), custom scrollbar (light track, warm thumb), `::placeholder` styling, underline offset on links, tabular numbers on `.stat-chip`.
2c. **Focus-visible**: 2px ring `#1B4CA1` offset 2px on all interactive elements.
2d. **`prefers-reduced-motion`**: kill typewriter deletion (show static full word), disable reveals/parallax/counter animations, keep opacity fades.
3. **Glass navbar system**: `.glass-navbar` floating pill + welcome micro-strip above (flag SVG + "WELCOME TO iGOT KARMAYOGI — MoSPI" + EN/हिंदी toggle placeholder). Orange 2px active underline; pill auth buttons (outline blue login / filled orange register).
4. **Nav styles**: `.nav-tab` restyle — Lato 700, 12px, letter-spacing .25px (official iGOT spec), orange 2px underline on active state.
   *Fit note:* the app nav runs 6+ tabs (Home, My Learning, Skill Gaps, Career Path, AI Copilot + role links). The 12px official size is kept; if the verification pass shows crowding at 1280px, shorten labels ("My Learning" → "Learning", "Skill Gaps" → "Gaps") rather than bumping font size.

5. **Component classes** (restyled, names kept): cards (4-8px radius, official shadows, hover lift), buttons (btn, btn-primary=orange fill, btn-navy→blue fill, btn-secondary, btn-success), badges (on-wash chips), progress bars (orange gradient fill), modals (radius 16px, elevated shadow), assistant drawer + FAB (orange fill, soft pulse).
6.  **Reveal utility**: `.reveal` — fade-up 24px, 600ms, `cubic-bezier(0.22,1,0.35,1)`, IntersectionObserver in `LearnerHomeView` (or a `useReveal` hook shared across views).
7.  **Responsive**: 1280 container, section rhythm 80-96px desktop / 56-64px mobile, card padding 24-32px.
8.  **Reduced motion**: `.reveal` → opacity-only, counters static, typewriter shows static word.
9.  **Reduc stray old-theme imports**: ensure no leftover `#1a365d`-family hexes anywhere in src.

### 3.3 `Navbar.tsx` (full rebuild, ~230 lines)
- **Welcome micro-strip**: flag SVG + "WELCOME TO iGOT KARMAYOGI — MoSPI" (Lato 700 12px, ink) + EN/हिंदी toggle button (non-functional placeholder, honest label).
- **Glass pill**: `rgba(255,255,255,.72)` + `backdrop-filter: blur(6px)`, 59px radius, inset 16px from viewport top, full-width minus gutters.
- **Left**: brand lockup — sun SVG (radial `#E94E12→#EB6D07→#F4970E→#FCBF06→#F5EC74→#FFFFFF`) + "iGOT Karmayogi" ink wordmark + "MoSPI" orange suffix.
- **Center**: nav tabs (Lato 700 12px) — Home · My Learning · Skill Gaps · Career Path · AI Copilot (SVG icon inline) · role links (Supervisor Queue / Admin Console, SVG icons).
- **Right**: persona switcher chip (32px circle, role-tinted fill) + avatar dropdown (role badges, fresh styling).
  - Access dropdown styling from inline → class-based.
- **Mobile (<768px)**: hamburger inside pill → accordion below.
- Emoji ✨🔍👑 replaced by SVGs.
- Dropdown menu positioning stays JS-state, class-styled.

### 3.3b Sub-decisions — pill layout and role links
- **Persona switcher** lives inside the glass pill, right side; brand | nav links | persona reads left→right. On mobile, links + persona collapse into the hamburger panel.
- **Role links:** Supervisor Queue = blue-outline pill (info role, SVG icon), Admin Console = blue-fill pill (SVG icon). Learner tabs stay text-only with orange active underline. Both role pills sit in the center nav group, shown only when the role matches.

### 3.4 `Footer.tsx` (restyle, ~85 lines)
Two-tier ink footer: upper grid (brand + mission, core pipeline list with SVG checks, architecture notice), hairline divider `#2C3448`, copyright bar in royal blue `#1B4CA1` with white text (MoSPI copyright + terms links). Remove saffron 4px top border. Emoji ✓ → SVG.

### 3.5 Views (de-inline-style → classes; theme + hierarchy polish; no logic changes)
- `LearnerHomeView.tsx` — hero-style officer header (greeting + roles + readiness badge), official competency grid, one-next-action card, priority gaps grid, journey list. Wash rhythm: header area ivory, competency card white, gaps section blue wash. Hero badge chip: orange subtle. Greeting uses Montserrat 700 (greeting data comes from API `dashboard.greeting`, keep). Promotion banner (green semantic) styled on wash. **Add a `useReveal` hook** (IntersectionObserver) shared via `src/hooks/useReveal.ts` for scroll reveals across views.
- `MyLearningView.tsx` (387 lines) — modules list, video player chrome, transcript viewer panel. Video player accents (progress, controls) in orange, transcript highlights in blue-100 wash.
- `SkillGapsView.tsx` — gap cards on alternating wash. Gap cards: level chips, severity badges on washes, CTA button (blue-outline; orange-fill reserved for the primary gap CTA only).
- `AdminDashboardView.tsx` — division analytics on light canvas, chart bars in orange/blue gradient, question-bank table re-skinned (tabular numerals, hover rows, sticky header).
- `ReviewerDashboardView.tsx` — queue cards with status chips (approval states on semantic washes), rubric scoring modal styling (ReviewModal.tsx shared).
- `CareerPathView.tsx` — 5-step journey with orange gradient connector, step nodes blue-fill, orange for the current step. Scroll-drawn connector: `scaleX` 0→1 on reveal, 2px orange gradient line (pure CSS transition triggered by the reveal class).
- Modals: `AssessmentModal`, `QuizModal`, `ReviewModal` — radius 16px, elevated shadow, header wash strip, orange focus ring. `TranscriptViewer` — search input restyle, highlight chip blue wash.
- `AssistantDrawer.tsx` — orange FAB with soft pulse, chat bubbles (user=blue-50 wash, ai=cream wash, input row on white).
- `OneNextActionCard` / `SkillGapCard` — card class + orange CTA, severity chip, progress mini-bar orange fill.

### 3.6 Landing page (`LandingPage.tsx` new, ~450 lines) — "sleek, attractive, professional, theme-matched"

Front door of the app; sections per design.md §5 mount order, adapted to orange-led hybrid. All copy honors craft-floor (no fake stats; demo-registry numbers labeled honestly).

- **3.6.1 Welcome micro-strip** — sits above the glass pill: tiny tricolor flag SVG + "WELCOME TO iGOT KARMAYOGI — MoSPI" (Lato 700 12px ink) + EN/हिंदी toggle (honest placeholder).
- **3.6.2 Glass pill navbar** — shared `Navbar.tsx` in "landing" mode: brand | Home · Learning · Skill Gaps · Career Path | persona. Auth pills: Login (blue outline) · Register (orange fill).
- **3.6.3 Hero (showpiece)** — the supplied image as full-bleed background (`landing-hero.jpg`, 1600×639, `object-fit: cover`, warm cream/peach). Left-anchored white gradient wash (`rgba(255,255,255,.94) → .72 → .25`, 90deg) keeps the text zone legible — no dark overlay; the image is 88% bright and theme-native.
  - Intro line (Montserrat 600 24px): "iGOT Karmayogi for India's Official Statistical System"
  - Typewriter headline (Montserrat 700, 32–40px, clamp): fixed "iGOT " + cycling orange words: **Learning · Competency · Practising · Verifying · Growing** — 50ms/char, hold 4s, delete, cycle. `prefers-reduced-motion` → static "iGOT Learning" (no JS animation).
  - Sub-line 16px `#374957`, CTA row: "Begin Your Learning Journey" (orange fill pill — the viewport's one orange fill) + "Explore the Platform" (blue-outline pill). Trust line 12px `#5F7D95`.
  - Image is the LCP element: `loading="eager"`, `fetchpriority="high"`, ` decoding="async"`, width/height attributes set (1600×639) to avoid CLS.
- **3.6.4 Stats band** — solid royal blue `#1B4CA1` rounded container (orange-led exception: the band is blue per iGOT signature; orange appears in the count-up numerals? **No** — white numerals on blue, orange reserved for the band's top accent line). White line-art SVG icons + count-up numbers (IntersectionObserver, 1200ms ease-out, tabular numerals): **20 Officers Onboarded (demo registry) · 40+ Competency Domains · 200+ Curated Courses · 26 iGOT Integration Tables · 100% Rubric-Verified Promotions**. Reduced motion → static numbers.
- **3.6.5 Orbital hub selector** — signature iGOT component: six 64px white circles on an orbit ring (CSS `--angle` 0/60/120/180/240/300deg), Material-style SVG icons: Learning · Discussion · Network · Competency · Career · Events. Selected hub inverts to blue fill. Detail card beside the orbit: title + 2-line description, cross-fade swap (300ms). Mobile <768px → 2×3 circle grid, ring hidden.
- **3.6.6 Competency journey** — horizontal 5-step timeline (Admin Registers → Profile Created → Gaps Identified → Curated Learning → Verified Promotion), blue number nodes, orange gradient connector that draws `scaleX` 0→1 on scroll. Mobile → vertical timeline, left connector.
- **3.6.7 Featured resources strip** — 3 curated course cards (from real demo data via API where available; honest "sample" label otherwise), card hover lift −4px, image zoom 1.05.
- **3.6.8 Register strip** — angled (clip-path) band on cream `#FEF5EA` wash with angled white card: "Built for India's Official Statistical System" + Register CTA (blue fill here — the hero CTA already owns this viewport-pair's orange fill).
- **3.6.9 Footer** — two-tier ink (§3.4 Footer).
- **Route wiring** — `activeView === 'landing'` (default view before login; after login the default becomes `home`). `Navbar` hides learner tabs when not authenticated; persona chip shows "Sign In" state. No router package added — stays within the existing `activeView` state pattern in `AuthContext`.

**Landing craft-floor discipline:** no gradient text, no nested cards, no icon-plus-heading-plus-text same-size card scaffold as page structure (orbital hubs are an interactive selector, not a card grid — they carry selection state), no eyebrow labels above headings, no emoji icons, heading carries its own weight.

### 3.7 Verification plan (per impeccable: bounded passes, not a loop)
1. `npm install` (if node_modules absent) + `npm run dev`; confirm compile + pages load.
2. Screenshot pass **once, batched** at 1440/768/375 widths: landing (hero + stats band + orbital hub + journey + register strip), navbar, home, learning, gaps, career, reviewer, admin + one modal open + assistant drawer open. Inspect once, fix everything in one batch, confirm with at most one more round.
3. Contrast checks: body ≥4.5:1, large-text ≥3:1 (orange only large/bold on white; never body text). Check with quick script + computed values.
4. Old-theme hexes gone: `grep -riE '#1a365d|#d97706|#0f294a|#ebf8ff|#fef3c7|#1e40af|#92400e' src/` returns 0 hits (covers all legacy navy/saffron tokens).
5. **Browser-surfaces spot-check**: selection/caret/scrollbar/focus ring visually confirmed in the screenshot pass.
6. Residuals: any leftover inline hex pointing at dead tokens is rewritten to a class or `var()` token reference.

### 3.8 Out of scope (explicitly)
Video hero, parallax, dark mode, backend changes, copy changes, route changes, `/impeccable init` PRODUCT.md (offered separately). The landing page — originally deferred — is **now in scope** per the 2026-09-09 amendment (supplied background image, typewriter hero, stats band, orbital hub, competency journey).
