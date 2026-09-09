# Karmayogi Sunrise Re-Theme — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-theme the MoSPI SIH26101 frontend to the orange-led "Karmayogi Sunrise" system (glass pill navbar, orange #F3962F lead, ink #1B2133 structure, official iGOT tokens) and add a new landing page built around the user-supplied hero image.

**Architecture:** Token-first CSS rewrite of `frontend/src/index.css` (class names preserved so all views re-theme at once), then a rebuilt Navbar/Footer, then de-inline-styling of views module by module, then a new `LandingPage.tsx` wired into the existing `activeView` state pattern. Theme-only — no behavior, route, or data-flow changes except adding the `landing` view state.

**Tech Stack:** React 18 + Vite 5 + TypeScript, plain CSS (no Tailwind, no UI kit), Google Fonts Montserrat/Lato/Noto Sans.

**Spec:** `docs/superpowers/specs/2026-09-09-karmayogi-retheme-design.md` — the plan argues from the spec; executors read both.

## Global Constraints

- Orange `#F3962F` never carries body text (2.2:1 on white); text on orange fills is white, only at large/bold sizes. Body text ≥4.5:1, large text ≥3:1.
- One filled orange button per viewport; everything else blue-fill / blue-outline / white.
- Ink `#1B2133` appears only in footer and wordmark — never in content-area text; content text uses `#374957` / `#4A5764` / `#5F7D95`.
- Nav links: Lato 700, 12px, letter-spacing .25px; orange 2px underline on active. If crowded at 1280px, shorten labels, never bump size.
- All emoji-as-icon instances (✨ 🔍 👑 🏅 ✓) become inline SVGs (single stroke/weight, Material-Symbols-like).
- Class names from the old stylesheet (`gov-card`, `btn`, `badge-*`, `nav-tab`, `modal-*`, `assistant-*`, `grid-*`) are KEPT — restyled, never renamed.
- Every animation has a `prefers-reduced-motion` fallback (typewriter → static word, count-up → static number, reveals → opacity-only).
- Fonts: `index.html` loads Montserrat (400;600;700) + Lato (400;700) + Noto Sans Devanagari subset; Inter stays only in the CSS fallback chain.
- No behavior changes: same routes/views, state, API calls, buttons, and copy (except icon swaps and the new landing view).
- Project is NOT a git repo — each task ends with a verification step instead of a commit step. (If git is initialized during execution, commit per task with the given messages.)

---

## Module A — Token Foundation

### Task A1: Fonts + asset wiring

**Files:**
- Modify: `frontend/index.html`
- Verify: `frontend/src/assets/landing-hero.jpg` exists (already copied, 1600×639, 166KB)

**Interfaces:**
- Consumes: nothing
- Produces: Google Fonts link for Montserrat/Lato/Noto Sans that Tasks A2+ reference via `var(--font-heading)` / `var(--font-sans)`; hero image importable as `@/assets/landing-hero.jpg` (relative import from `src/`).

- [ ] **Step 1: Replace the fonts link in index.html**

Replace the existing `<link href="https://fonts.googleapis.com/css2?family=Inter...>` line with:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Lato:wght@400;700&family=Noto+Sans:wght@400;700&display=swap" rel="stylesheet">
```

- [ ] **Step 2: Verify the hero image is in place**

Run: `ls -la frontend/src/assets/landing-hero.jpg`
Expected: file present, ~166KB. If missing, copy from `C:\Users\Aastha sengar\Downloads\WhatsApp Image 2026-09-09 at 9.22.55 PM.jpeg`.

- [ ] **Step 3: Verify dev server still serves**

Run: `cd frontend && npm run dev` (briefly, Ctrl+C after Vite banner)
Expected: Vite starts with no HTML parse errors.

### Task A2: index.css token system rewrite

**Files:**
- Modify: `frontend/src/index.css` (full rewrite, ~600 lines)

**Interfaces:**
- Consumes: font names from A1.
- Produces: all tokens (`--orange-500: #F3962F` etc.) and component classes every later task uses. Key classes produced: `.gov-container`, `.gov-card`, `.btn`/`.btn-primary`/`.btn-navy`/`.btn-secondary`/`.btn-success`, `.badge-saffron`/`-navy`/`-green`/`-gray`/`-danger`, `.progress-track`/`.progress-fill`, `.nav-tab`, `.modal-overlay`/`.modal-content`, `.assistant-drawer`, `.assistant-trigger-btn`, `.grid-2`/`.grid-3`, plus NEW: `.glass-navbar`, `.welcome-strip`, `.brand-sun`, `.hero-*`, `.stat-chip`, `.reveal`, `.igot-btn-outline`, `.igot-btn-fill`.

- [ ] **Step 1: Write the token block**

Full `:root` with primitives → semantic mapping exactly as spec §2 (orange scale, blue scale, ink scale, washes, semantic colors, fonts, official iGOT radii/shadows: `--radius-btn: 4px`, `--radius-card: 8px`, `--radius-nav: 59px`, `--radius-auth-pill: 32px`, `--shadow-card: 0 0 8px rgba(0,0,0,.1)`, `--shadow-elevated: 0 4px 16px rgba(29,76,161,.12)`, `--shadow-cta: 0 0 .5rem rgba(5,45,172,.25)`).

- [ ] **Step 2: Write base layer**

Reset (`* { box-sizing: border-box; margin: 0; padding: 0 }`), body on `--canvas` with `var(--font-sans)` 16px/1.5, headings in `var(--font-heading)`, and browser-surface theming: `::selection { background: #FCE5CC; color: #1B2133 }`, `caret-color: var(--orange-500)`, `:focus-visible { outline: 2px solid #1B4CA1; outline-offset: 2px }`, custom scrollbar (light track, warm thumb), `::placeholder { color: #5F7D95 }`.

- [ [ ] **Step 3: Write component classes**

Keep every old class name, restyled to tokens. This is the bulk of the file (~350 lines). Follow the existing file's section comments as the template (Cards → Buttons → Badges → Progress → Nav tabs → Modals → Assistant → Grids) and add new sections for glass navbar, welcome strip, brand sun mark, hero, stats, reveal utility. Cards: 8px radius, `--shadow-card`, hover lift −4px + `--shadow-elevated`, no border under shadow (craft floor: declare elevation once). Buttons: `--radius-btn: 4px`, min-height 44px, `.btn-primary` orange fill white text, `.btn-navy` blue `#1B4CA1` fill (class name kept, value swapped), `.btn-secondary` white + border. Badges on washes (`--orange-50` fill, `--orange-700` text; blue-50/`#194593`; success `#1D8923` on `#E8F5E9`; gray neutral; danger `#D13924` on `#FBE9E7`). Progress: `--orange-500` → `--orange-600` gradient fill on `--wash-ivory` track. Nav-tab: Lato 700 12px .25px spacing, orange underline active. Modals: radius 16px `--shadow-elevated`. Assistant FAB: orange fill, soft pulse (respects reduced motion). Reveal utility: `.reveal { opacity: 0; transform: translateY(24px); transition: opacity .6s cubic-bezier(.22,1,.35,1), transform .6s cubic-bezier(.22,1,.35,1) }` `.reveal.is-visible { opacity: 1; transform: none }`.

- [ ] **Step 4: Write responsive + reduced-motion blocks**

Media queries at 900px (grid collapse, drawer full-width) mirroring the old file, plus nav pill gutters. `@media (prefers-reduced-motion: reduce) { .reveal { transition: opacity .3s; transform: none } .assistant-trigger-btn, .count-up-num { animation: none } }`.

- [ ] **Step 2 (verify): Compile + visual smoke check**

Run: `cd frontend && npm run dev`
Expected: compiles; app renders with new tokens (background still white/ivory, headings Montserrat).

- [ ] **Step 3 (verify): Old-hex residue audit**

Run: `grep -riE "#1a365d|#d97706|#0f294a|#ebf8ff|#fef3c7|#1e40af|#92400e|#166534|#f0fdf4|#bbf7d0" frontend/src/index.css`
Expected: 0 hits in index.css. (Views still contain them until their tasks run.)

---

## Module B — Chrome (Navbar + Footer)

### Task B1: Navbar rebuild as glass pill

**Files:**
- Modify: `frontend/src/components/Navbar.tsx` (full rebuild, ~230 lines)

**Interfaces:**
- Consumes: `useAuth()` → `{ currentUser, demoAccounts, switchDemoUser, activeView, setActiveView, setIsAssistantOpen }` (all existing); classes from A2: `.glass-navbar`, `.welcome-strip`, `.brand-sun`, `.nav-tab`, `.persona-chip`, `.role-pill-*`.
- Produces: `<Navbar />` with the same exported name and zero props, used by `App.tsx` unchanged.

- [ ] **Step 1: Replace the whole component**

Structure: welcome micro-strip (SVG flag + "WELCOME TO iGOT KARMAYOGI — MoSPI" + EN/हिंदी toggle placeholder) → glass pill row (brand-sun SVG mark + ink wordmark + orange "MoSPI" suffix | nav tabs | persona chip + dropdown). Pill: `rgba(255,255,255,.72)`, `backdrop-filter: blur(6px)`, radius 59px, inset 16px top, full-width minus gutters. Nav tabs Lato 700 12px with orange underline; AI Copilot tab keeps its SVG sparkle icon (replacing ✨), Supervisor Queue blue-outline pill, Admin Console blue-fill pill (replacing 🔍 👑). Persona chip: 32px circle role-tinted (ADMIN→blue-500, REVIEWER→orange-700, LEARNER→success). Mobile <768px: hamburger button inside pill → accordion panel below with all links. Keep dropdown JS state (`dropdownOpen`) and click handlers exactly as before. All styling moves inline-style → className with a small `style` prop only where dynamic (e.g., active tab accent).

```tsx
// Key structural snippet (full JSX in file):
<header className="site-header">
  <div className="welcome-strip">
    <FlagIcon />
    <span>WELCOME TO iGOT KARMAYOGI — MoSPI</span>
    <button className="lang-toggle" type="button">EN | हिंदी</button>
  </div>
  <nav className="glass-navbar" aria-label="Primary">
    <button className="brand-lockup" onClick={() => setActiveView('home')}>
      <BrandSunIcon />
      <span className="brand-word">iGOT Karmayogi <em className="brand-suffix">MoSPI</em></span>
    </button>
    <div className="nav-links">{/* nav-tab buttons, role pills, AI Copilot */}</div>
    <PersonaSwitcher />  {/* existing dropdown logic, class-styled */}
    <button className="hamburger" aria-expanded={menuOpen} aria-controls="mobile-menu" aria-label="Menu" onClick={() => setMenuOpen(!menuOpen)}><MenuIcon /></button>
  </nav>
  {menuOpen && <div className="mobile-menu" id="mobile-menu" role="dialog" aria-label="Menu">{/* same links */}</div>}
</header>
```

- [ ] **Step 2: Verify compile + a11y attributes**

Run: `npm run dev` and open the app; tab through the navbar with keyboard.
Expected: all nav items focusable, focus ring visible (blue), no TS errors.

### Task B2: Footer restyle (two-tier ink)

**Files:**
- Modify: `frontend/src/components/Footer.tsx` (~85 lines)

**Interfaces:**
- Consumes: classes `.footer-ink`, `.footer-grid`, `.footer-divider`, `.footer-copyright` from A2.
- Produces: unchanged export `<Footer />`.

- [ ] ✓ **Step 1: Restyle to two-tier ink + blue copyright bar**

Upper tier: ink `#1B2133` background, grid: brand+mission / core pipeline list (SVG check icons replacing ✓) / architecture notice. Hairline `#2C3448`. Lower tier: royal-blue `#1B4CA1` copyright bar, white text, terms links in white. Remove saffron 4px top border. All inline hexes → classes/tokens.

- [ ] **Step 2: Verify visually**

App renders footer ink tier + blue bar; no old navy/saffron hexes.

---

## Module C — Learner views

### Task C1: LearnerHomeView de-inline-style

**Files:**
- Replace styling in: `frontend/src/views/learner/LearnerHomeView.tsx` (296 lines)

**Interfaces:**
- Consumes: A2 classes (`.gov-card`, `.btn`, `.badge-*`, `.grid-3`, `.reveal`), new hook from this task `useReveal`.
- Produces: `useReveal()` hook exported from `frontend/src/hooks/useReveal.ts` — signature `useReveal<T extends HTMLElement>(): React.RefObject<T>` — auto-applies `.is-visible` via IntersectionObserver at 20% viewport entry; later view tasks import it.

- [ ] **Step 1: Create `hooks/useReveal.ts`**

```ts
import { useEffect, useRef } from 'react';

export function useReveal<T extends HTMLElement>(): React.RefObject<T> {
  const ref = useRef<T>(null);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      el.classList.add('is-visible');
      return;
    }
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { el.classList.add('is-visible'); obs.disconnect(); } },
      { threshold: 0.2 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);
  return ref;
}
```

- [ ] **Step 2: Convert LearnerHomeView inline styles → classes + useReveal**

Replace every inline `style={{...}}` hex with class names from index.css; add a few view-specific classes in index.css (`.officer-header`, `.competency-tile`, `.competency-tile.met`, `.journey-item`, `.journey-item.current`, `.journey-node`). Attach `useReveal` to section containers (competency profile card, gaps grid, journey card) with staggered transition-delay via inline `style={{ transitionDelay: `${i * 80}ms` }}` (dynamic value — legitimate inline style). Keep ALL data logic identical (`api.getDashboard`, `api.getLearnerProfile`, the `met`/`pct` calculations, conditional rendering).

- [ ] **Step 3: Verify data still flows + visuals**

Run: `npm run dev`, open Home (USR-001 Aarav).
Expected: greeting, roles, readiness badge, competency tiles, next-action card, gap cards, journey list all render with new theme; reveal animations fire on scroll; no console errors.

### Task C2: SkillGapsView + SkillGapCard

**Files:**
- Modify: `frontend/src/views/learner/SkillGapsView.tsx` (149 lines)
- Modify: `frontend/src/components/SkillGapCard.tsx` (131 lines)

**Interfaces:**
- Consumes: A2 classes, `useReveal` from C1, `.gap-severity-*` classes from this task.
- Produces: unchanged exports `SkillGapsView`, `SkillGapCard` (same props: `{ gap: CompetencyGapItem }`).

- [ ] **Step 1: Add gap classes to index.css**

`.gap-card` (gov-card derivative), `.gap-severity-HIGH` (orange-50 fill, orange-700 text), `.gap-severity-MEDIUM` (blue-50, blue-700 text), `.gap-severity-NO_GAP` (success wash), `.gap-severity-INSUFFICIENT_EVIDENCE` (neutral wash), `.gap-cta-row`.

- [ ] **Step flow: severity→class map + convert both files**

In `SkillGapCard.tsx`: map `gap.gap_status` → severity class; convert inline styles to classes; orange CTA only on the primary gap (`recommendation_status === 'RECOMMENDED' && priority === 'HIGH'`), otherwise blue-outline. In `SkillGapsView.tsx`: heading row + grid of cards; `useReveal` per section. Keep the same conditional logic for gaps with/without recommended courses.

- [ ] **Step 2 (verify): render gaps view with USR-001**

Expected: HIGH severity cards read orange-tinted, MEDIUM blue-tinted, CTAs correct, no console errors.

### Task C3: MyLearningView + video/transcript components

**Files:**
- Modify: `frontend/src/views/learner/MyLearningView.tsx` (387 lines)
- Modify: `frontend/src/components/VideoPlayer.tsx` (126 lines)
- Modify: `frontend/src/components/TranscriptViewer.tsx (112 lines)`

**Files note:** Add `MyLearningView` needs `.lesson-row`, `.video-shell`, `.transcript-panel`, `.transcript-hit` classes to index.css (A2 already defines the shared base; add these to the shared file, keeping section comments).

**Interfaces:**
- Consumes: A2 classes, `useReveal` from C1, `.lesson-row` etc. from this task.
- Products: unchanged exports `MyLearningView`, `VideoPlayer`, `TranscriptViewer` (same props as today: VideoPlayer takes lesson/video data; TranscriptViewer takes transcript + search state from parent).

- [ ] **Step 1: MyLearningView layout conversion**

Lesson list rows (`.lesson-row` — white card, hover lift, active row orange left accent... **correction, no border-left over 1px (craft floor):** active row gets a 3px orange inline `border-left`? No — craft floor bans colored border-left above 1px. Use a filled orange 4px round dot / chevron marker or background tint `--wash-cream` + orange chevron SVG instead.) Video section: `.video-shell` (16px radius, elevated shadow, deep surface `--blue-900` only if video chrome dark — else white shell). Transcript: `.transcript-panel` with sticky search input, `.transcript-hit` highlight chip on `--blue-50` wash. Keep all state logic (selected lesson, player events, search filtering) identical.

- [ ] **Step 2: Verify video + transcript interplay**

Run: `npm run dev`, open My Learning (lesson `sampling-lesson-3` selected by default).
Expected: lesson rows clickable, video loads, transcript search filters + highlights; themed controls.

### Task C4: CareerPathView (journey timeline)

**Files:**
- Modify: `frontend/src/views/learner/CareerPathView.tsx` (220 lines)

**Interfaces:**
- Consumes: A2 classes, `useReveal` from C1; this task adds `.journey-line`, `.journey-step`, `.journey-step.current`, `.journey-connector`.
- Produces: unchanged export `CareerPathView`.

- [ ] **Step 1: Build the timeline classes**

5-step horizontal timeline (desktop) → vertical (mobile <768px). Blue number nodes `#1B4CA1`, current step orange fill; connector `.journey-connector { transform: scaleX(0); transform-origin: left; transition: transform 1.2s cubic-bezier(.22,1,.35,1) }` `.journey-connector.is-visible { transform: scaleX(1) }` — orange gradient line drawn by the same reveal hook.

- [ ] **Step 2: Convert view + verify**

Convert inline styles → classes; timeline renders 5 steps with scroll-drawn connector; mobile shows vertical.

---

## Module D — Dashboards (Admin + Reviewer)

### Task D1: AdminDashboardView

**Files:**
- Modify: `frontend/src/views/admin/AdminDashboardView.tsx (295 lines)`

**Interfaces:**
- Consumes: A2 classes, `useReveal`; adds `.stat-chip`, `.chart-bar`, `.admin-table`, `.admin-table th` sticky.
- Produces: unchanged export `AdminDashboardView`.

- [ ] **Step 1: Convert stats + chart + table**

Stat chips (`.stat-chip` — tabular numerals, white card, blue icon accent), chart bars (`.chart-bar` — orange/blue gradient fills by series), question-bank table (`.admin-table` — white surface, hover rows `--wash-ivory`, sticky header, tabular numerals). Keep all data calls (`api.getAdminStats` etc. — check actual method names in `api/client.ts` before use; do not invent).

- [ ] task D2: ReviewerDashboardView + ReviewModal

**Files:**
- Modify: `frontend/src/views/reviewer/ReviewerDashboardView.tsx` (162 lines)
- Modify: `frontend/src/components/ReviewModal.tsx` (204 lines)

**Interfaces:**
- Consumes: A2 classes, `useReveal`; adds `.queue-card`, `.rubric-row`, `.rubric-score-picker`.
- Produces: unchanged exports.

- [ ] **Step 1: Convert queue + rubric modal**

Queue cards with status chips on semantic washes (pending → neutral, approved → success, rejected → danger), CTA per card (blue-outline). ReviewModal: 16px radius, elevated shadow, header wash strip, rubric rows with score picker buttons — orange focus ring; disabled state for locked criteria. Keep assessment-fetch and score-submission logic identical.

- [ ] **Step 2: Verify with reviewer persona**

Switch persona to `reviewer-001` (Sunita Rao) via the persona chip.
Expected: queue renders, modal opens, scores submit unchanged.

### Task D3: Modals + drawer polish (QuizModal, AssessmentModal, AssistantDrawer)

**Files:**
- Modify: `frontend/src/components/QuizModal.tsx` (266 lines)
- Module: `frontend/src/components/AssessmentModal.tsx` (335 lines)
- Modify: `frontend/src/components/AssistantDrawer.tsx` (248 lines)

**Interfaces:**
- Consumes: A2 classes only.
- Produces: unchanged exports.

- [ ] **Step 1: Convert all three**

QuizModal: question cards on white, option rows with orange selected-state ring, progress bar (orange gradient fill). AssessmentModal: same modal chrome, instructions header strip, submit row. AssistantDrawer: orange FAB (pulse, reduced-motion-off), chat bubbles user=`--blue-50`/ai=`--wash-cream`, input row white. Replace any remaining emoji (✨ in drawer header) with SVG.

- [ ] **Step 2: Verify modals across learner flow**

Learner → My Learning → open quiz → answer → submit; open assessment; open copilot drawer.
Expected: all three render themed, submit flows unchanged.

---

## Module E — Landing page

### Task E1: LandingPage sections 1 (hero + stats band)

**Files:```
- Create: `frontend/src/views/landing/LandingPage.tsx`
- Create: `frontend/src/views/landing/hero.tsx` — wait, keep it single-file per existing codebase pattern (views are single files). **One file: `LandingPage.tsx`.**
- Modify: `frontend/src/index.css` (add `.hero-*`, `.stats-band`, `.stat-chip` landing variants)

**Interfaces:**
- Consumes: A2 tokens/classes, `useReveal` (C1), hero image `import heroImg from '../assets/landing-hero.jpg'`, `useAuth().setActiveView`.
- Produces: `<LandingPage />` exported for Task E3 wiring; internal sections local to the file (no new shared exports).

- [ ] **Step 1: Hero section**

Full-bleed section, `landing-hero.jpg` as `<img>` with `object-fit: cover`, `loading="eager"`, `fetchpriority="high"` (React: `fetchPriority`), `decoding="async"`, width/height 1600×639 attrs. Left white gradient wash (`linear-gradient(90deg, rgba(255,255,255,.94), rgba(255,255,255,.72) 45%, rgba(255,255,255,.25))`) as absolute overlay div. Content: intro line (Montserrat 600 24px) → typewriter headline (Montserrat 700, clamp 32–40px): fixed "iGOT " + cycling orange words Learning · Competency · Practising · Verifying · Growing. Typewriter via `useEffect` interval at 50ms/char, hold 4000ms, delete phase 30ms/char, cycle. Reduced-motion → static "iGOT Learning". Sub-line 16px `#374957`. CTA row: "Begin Your Learning Journey" orange fill pill (the one orange fill) + "Explore the Platform" blue outline. Trust line 12px `#5F7D95`. Cursor `.typewriter-caret` (thin orange bar, blinking, reduced-motion static).

```tsx
// Typewriter hook (in LandingPage.tsx):
function useTypewriter(words: string[], speedMs = 50, holdMs = 4000) {
  const [text, setText] = useState('');
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { setText(words[0]); return; }
    let word = 0, char = 0, deleting = false, timer: number;
    const tick = () => {
      const current = words[word];
      if (!deleting) { char++; setText(current.slice(0, char));
        if (char === current.length) { deleting = true; timer = window.setTimeout(tick, holdMs); return; }
        timer = window.setTimeout(tick, speedMs);
      } else { char--; setText(current.slice(0, char));
        if (char === 0) { deleting = false; word = (word + 1) % words.length; }
        timer = window.setTimeout(tick, 30);
      }
    };
    timer = window.setTimeout(tick, 400);
    return () => clearTimeout(timer);
  }, []);
  return text;
}
```

- [ ] **Step 2: Stats band (count-up)**

Royal-blue `#1B4CA1` rounded container. Five stats with white SVG line icons: 20 Officers Onboarded (demo registry) · 40+ Competency Domains · 200+ Curated Courses · 26 iGOT Integration Tables · 100% Rubric-Verified Promotions. Count-up: IntersectionObserver → animate 1200ms ease-out; tabular numerals; reduced-motion → static.

```tsx
function useCountUp(target: number, start: boolean, durationMs = 1200) {
  const [n, setN] = useState(0);
  useEffect(() => {
    if (!start) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { setN(target); return; }
    let raf: number; const t0 = performance.now();
    const step = (t: number) => {
      const p = Math.min(1, (t - t0) / durationMs);
      setN(Math.round(target * (1 - Math.pow(1 - p, 2)))); // ease-out
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [start, target, durationMs]);
  return n;
}
```

- [ ] **Step 3: Verify hero + stats**

Dev server; landing renders image hero, typewriter cycles orange words, stats count up on scroll into view.

### Task E2: LandingPage sections 2 (orbital hub + journey + resources + register strip)

**Files:**
- Modify: `frontend/src/views/landing/LandingPage.tsx` (extend)
- Modify: `frontend/src/index.css` (add `.orbital-*`, `.journey-*` landing variant, `.resource-card`, `.register-strip`)

**Interfaces:**
- Consumes: tokens; `useReveal`, `useCountUp` patterns from E1.
- Produces: complete `<LandingPage />` used by E3.

- [ ] **Step 1: Orbital hub selector**

Six 64px white circles on an orbit ring: CSS custom property `--angle` at 0/60/120/180/240/300deg, `transform: rotate(var(--angle)) translateX(orbit-radius) rotate(calc(-1 * var(--angle)))` on each circle wrapper. SVG icons: Learning (book-open), Discussion (chat), Network (share-2), Competency (award), Career (trending-up), Events (calendar). Selected hub inverts to blue fill + white icon; detail card cross-fades 300ms (CSS opacity transition on keyed content). Data: static array of `{ id, icon, title, description }` — content from design.md §5.5 descriptions. Mobile <768px → 2×3 grid, ring hidden.

- [ ] **Step 2: Competency journey**

5-step timeline: Admin Registers → Profile Created → Gaps Identified → Curated Learning → Verified Promotion. Blue number nodes, orange gradient connector `scaleX` 0→1 on reveal (same mechanism as C4). Mobile → vertical with left connector. Descriptions from README pipeline.

- [ ] **Step 3: Featured resources + register strip**

3 resource cards (title, competency tag chip, duration meta, hover lift + image zoom 1.05). Sample-data labeled honestly: a caption "Sample curation — live data wired post-demo" is false — **use real demo data:** call existing API (`api.getDashboard` returns learning path preview with course titles — verify actual method in `api/client.ts` first; if a courses endpoint exists, use it; otherwise render from `dashboard.learning_path_preview`). Angled register strip: cream `#FEF5EA` band, clip-path angled top, white card "Built for India's Official Statistical System" + Register CTA (blue fill). No new auth logic — button calls `setActiveView('home')` (enters demo).

- [ ] ] **Step 4: Verify landing sections 2**

Orbital selector clicks swap detail card; journey connector draws on scroll; register CTA navigates to home.

### Task E3: Wire landing into app + view routing

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/context/AuthContext.tsx` (only if needed for initial view state)

**Interfaces:**
- Consumes: `<LandingPage />` from E1/E2.
- Produces: `activeView === 'landing'` renders Landing; initial state landing-first.

- [ ] **Step 1: App.tsx wiring**

```tsx
{activeView === 'landing' && <LandingPage />}
```
added to the view switch. Import from `./views/landing/LandingPage`.

- [ ] **Step 2: AuthContext initial view**

`useState<string>('landing')` (was `'home'`). `switchDemoUser` routes by role as today (landing → role view). Navbar: when `activeView === 'landing'`, learner tabs + persona chip show "Sign In" state — wait, there's no login flow (demo persona auto-login USR-001). **Resolution:** keep persona chip always visible (demo mode — persona switching IS the auth), Navbar "landing mode" hides learner tabs; Register/Login pills in navbar call `switchDemoUser('USR-001')` (honest demo entry).

- [ ] **Step 2 (verify): Route transitions**

Load app → landing shows; Begin Your Learning Journey → home (USR-001); persona switch → reviewer/admin views render.

---

## Module F — Final verification

### Task F1: Full batched verification pass

**Files:**
- No file changes planned; fix-batch only if issues found.

**Interfaces:**
- Consumes: everything.
- Produces: verified, demo-ready frontend.

- [ ] **Step 1: Clean install + build**

Run: `cd frontend && npm install && npm run build`
Expected: TS + Vite build passes with 0 errors.

- [ ] **Step 2: Batched screenshot pass (one round)**

Run: `npm run dev`, then at 1440 / 768 / 375 widths capture: landing (all sections), home, learning, gaps, career, reviewer, admin, one modal, assistant drawer. Inspect once, list every defect, fix in one batch.

- [ ] **Step 3: Contrast + residue checks**

Run: `grep -riE "#1a365d|#d97706|#0f294a|#ebf8ff|#fef3c7|#1e40af|#92400e" frontend/src/` → expect 0 hits.
Contrast: verify body text `#374957` on white (7.5:1), muted `#5F7D95` on white (4.6:1), white on orange `#F3962F` (2.2:1 — orange large/bold only), white on blue `#1B4CA1` (8:1) — compute with a quick script if in doubt.

- [ ] ratios: `npm run build` re-run after fixes; confirm 0 errors.

- [ ] **Step 4: Reduced-motion + keyboard pass**

Enable `prefers-reduced-motion` in devtools; verify typewriter static, count-up static, reveals opacity-only, connector undrawn. Keyboard-tab through navbar, a modal, and the orbital selector; all focus rings visible.

- [ ] **Step 1 (final): Demo walkthrough**

USR-001: landing → begin → home → gaps → learning (quiz) → career. Switch reviewer: queue → rubric modal. Switch admin: analytics. Confirm no console errors in any flow.

## Self-Review (completed during plan writing)

- Spec coverage: token rewrite (A2), navbar (B1), footer (B2), all views (C1-C4, D1-D2), modals/drawer (D3), landing (E1-E3), verification (F1) — all spec §3 sections have tasks. Typewriter/hero (spec D3/D8), orbital hub, journey, register strip covered in E1/E2.
- Placeholder scan: no TBD/TODO steps; every code step has actual code or exact class/section references; no "similar to Task N" without the code.
- Type consistency: `useReveal<T>(): React.RefObject<T>` used consistently in C1-C4, D1-D2, E1-E2; `useTypewriter`/`useCountUp` signatures defined in E1 and reused in E2; `CompetencyGapItem` prop for SkillGapCard matches types/index.ts; api method names flagged for verification before use (no invented endpoints).
- Known corrections folded in: no `border-left` accent over 1px (craft floor), no fake stats (real demo numbers + honest labels), landing routing kept inside existing state pattern.
