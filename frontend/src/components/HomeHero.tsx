import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import heroImg from '../assets/landing-hero.jpg';

/* ==========================================================================
   Hooks (typewriter + in-view counter)
   ========================================================================== */

function useTypewriter(words: string[], speedMs = 50, holdMs = 4000) {
  const [text, setText] = useState('');
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setText(words[0]);
      return;
    }
    let word = 0, char = 0, deleting = false, timer: number;
    const tick = () => {
      const current = words[word];
      if (!deleting) {
        char++;
        setText(current.slice(0, char));
        if (char === current.length) {
          deleting = true;
          timer = window.setTimeout(tick, holdMs);
          return;
        }
        timer = window.setTimeout(tick, speedMs);
      } else {
        char--;
        setText(current.slice(0, char));
        if (char === 0) {
          deleting = false;
          word = (word + 1) % words.length;
        }
        timer = window.setTimeout(tick, 30);
      }
    };
    timer = window.setTimeout(tick, 400);
    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return text;
}

function useInView<T extends HTMLElement>(threshold = 0.3) {
  const ref = useRef<T>(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setInView(true);
      return;
    }
    if (el.getBoundingClientRect().top < window.innerHeight) {
      setInView(true);
      return;
    }
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          obs.disconnect();
        }
      },
      { threshold }
    );
    obs.observe(el);
    const fallback = window.setTimeout(() => setInView(true), 4000);
    return () => {
      obs.disconnect();
      window.clearTimeout(fallback);
    };
  }, []);
  return { ref, inView };
}

function useCountUp(target: number, start: boolean, durationMs = 1200) {
  const [n, setN] = useState(0);
  useEffect(() => {
    if (!start) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setN(target);
      return;
    }
    let raf: number;
    const t0 = performance.now();
    const step = (t: number) => {
      const p = Math.min(1, (t - t0) / durationMs);
      setN(Math.round(target * (1 - Math.pow(1 - p, 2))));
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [start, target, durationMs]);
  return n;
}

/* ==========================================================================
   Static content
   ========================================================================== */

/* (stats content moved into HomeStatsBand for i18n) */

const StatIcon: React.FC<{ idx: number }> = ({ idx }) => {
  const p = { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, 'aria-hidden': true };
  switch (idx) {
    case 0: return <svg {...p}><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" /></svg>;
    case 1: return <svg {...p}><polygon points="12 2 2 7 12 12 22 7 12 2" /><polyline points="2 17 12 22 22 17" /><polyline points="2 12 12 17 22 12" /></svg>;
    case 2: return <svg {...p}><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" /></svg>;
    case 3: return <svg {...p}><ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" /><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" /></svg>;
    default: return <svg {...p}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></svg>;
  }
};

const ArrowIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />
  </svg>
);

/* ==========================================================================
   Landing hero — the landing page: hero image + typewriter + stats band.
   Primary CTA enters the demo as the default learner persona.
   ========================================================================== */

export const HomeHero: React.FC = () => {
  const { t } = useTranslation();
  const typedWords = t('landing.typedWords').split(',');
  const typed = useTypewriter(typedWords);
  const navigate = useNavigate();
  const { switchDemoUser } = useAuth();

  return (
    <div className="gov-container" style={{ paddingTop: '24px' }}>
      <section className="hero" aria-label="Welcome">
        <img
          className="hero-media"
          src={heroImg}
          alt="MoSPI officers in training — India's Official Statistical System"
          width={1600}
          height={639}
          loading="eager"
          fetchPriority="high"
          decoding="async"
        />
        <div className="hero-wash" aria-hidden="true" />
        <div className="hero-content">
          <div className="hero-intro">{t('landing.heroIntro')}</div>
          <h1 className="hero-headline">
            iGOT <span className="typed-word">{typed}</span>
            <span className="typewriter-caret" aria-hidden="true" />
          </h1>
          <p className="hero-sub">
            {t('landing.heroSub')}
          </p>
          <div className="hero-cta-row">
            <button className="btn btn-pill-fill" onClick={() => switchDemoUser('USR-001')}>
              {t('landing.beginJourney')} <ArrowIcon />
            </button>
            <button className="btn btn-pill-outline" onClick={() => switchDemoUser('USR-001').then(() => navigate('/gaps'))}>
              {t('landing.explore')}
            </button>
          </div>
          <div className="hero-trust">
            {t('landing.trust')}
          </div>
        </div>
      </section>

      <HomeStatsBand />
    </div>
  );
};

const HomeStatsBand: React.FC = () => {
  const { ref, inView } = useInView<HTMLDivElement>(0.4);
  const { t } = useTranslation();
  const STATS = [
    { n: 20, suffix: '', label: t('landing.stat1') },
    { n: 40, suffix: '+', label: t('landing.stat2') },
    { n: 200, suffix: '+', label: t('landing.stat3') },
    { n: 26, suffix: '', label: t('landing.stat4') },
    { n: 100, suffix: '%', label: t('landing.stat5') },
  ];
  return (
    <div style={{ marginTop: '24px' }}>
      <div ref={ref} className="stats-band" role="list" aria-label="Platform statistics">
        {STATS.map((s, i) => (
          <HomeStatItem key={s.label} {...s} idx={i} start={inView} />
        ))}
      </div>
      <div className="stats-band-caption">{t('landing.statsCaption')}</div>
    </div>
  );
};

const HomeStatItem: React.FC<{ n: number; suffix: string; label: string; idx: number; start: boolean }> = ({ n, suffix, label, idx, start }) => {
  const count = useCountUp(n, start);
  return (
    <div role="listitem" style={{ display: 'flex', flexDirection: 'column' }}>
      <span className="stat-icon"><StatIcon idx={idx} /></span>
      <span className="stat-num">{count}{suffix}</span>
      <span className="stat-text">{label}</span>
    </div>
  );
};
