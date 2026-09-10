import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import { setLanguage, getCurrentLang, type Lang } from '../i18n';

/* ---- Inline SVG icon set (Material-Symbols-like, single stroke weight) ---- */

const FlagIcon: React.FC = () => (
  <svg width="18" height="12" viewBox="0 0 18 12" fill="none" aria-hidden="true">
    <rect width="18" height="12" rx="1.5" fill="#FFFFFF" stroke="#CBD2DC" strokeWidth="0.5" />
    <rect x="0.75" y="0.75" width="16.5" height="3.5" rx="1" fill="#FF9933" />
    <rect x="0.75" y="7.75" width="16.5" height="3.5" rx="1" fill="#138808" />
    <circle cx="9" cy="6" r="1.1" fill="none" stroke="#000080" strokeWidth="0.5" />
    <circle cx="9" cy="6" r="0.3" fill="#000080" />
  </svg>
);

const BrandSunIcon: React.FC = () => (
  <svg width="44" height="44" viewBox="0 0 44 44" fill="none" aria-hidden="true">
    <defs>
      <radialGradient id="sunGrad" cx="50%" cy="55%" r="60%">
        <stop offset="0%" stopColor="#FCBF06" />
        <stop offset="45%" stopColor="#F4970E" />
        <stop offset="100%" stopColor="#E94E12" />
      </radialGradient>
    </defs>
    <circle cx="22" cy="22" r="13" fill="url(#sunGrad)" />
    <circle cx="22" cy="22" r="5.5" fill="#FFF7E0" />
    {Array.from({ length: 12 }).map((_, i) => {
      const angle = (i * Math.PI) / 6;
      const x1 = 22 + Math.cos(angle) * 15;
      const y1 = 22 + Math.sin(angle) * 15;
      const x2 = 22 + Math.cos(angle) * 19.5;
      const y2 = 22 + Math.sin(angle) * 19.5;
      return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#F0951E" strokeWidth="2" strokeLinecap="round" />;
    })}
  </svg>
);

const SparkIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 2l2.1 6.9L21 11l-6.9 2.1L12 20l-2.1-6.9L3 11l6.9-2.1L12 2z" />
  </svg>
);

const SearchIcon: React.FC = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden="true">
    <circle cx="10.5" cy="10.5" r="6.5" />
    <line x1="15.5" y1="15.5" x2="21" y2="21" />
  </svg>
);

const AdminIcon: React.FC = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M3 21h18" />
    <path d="M5 21V7l7-4 7 4v14" />
    <path d="M9 21v-4h6v4" />
    <path d="M9 11h.01M15 11h.01" />
  </svg>
);

const MenuIcon: React.FC = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden="true">
    <line x1="4" y1="7" x2="20" y2="7" />
    <line x1="4" y1="12" x2="20" y2="12" />
    <line x1="4" y1="17" x2="20" y2="17" />
  </svg>
);

const ChevronDownIcon: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden="true">
    <polyline points="6 9 12 15 18 9" />
  </svg>
);

/* ---- Accessibility controls (persisted font zoom) ---- */

const FONT_ZOOM_KEY = 'igot_font_zoom';

function applyAccessibility() {
  const zoom = Number(localStorage.getItem(FONT_ZOOM_KEY) || '1');
  document.documentElement.style.zoom = String(zoom);
}

const AccessibilityControls: React.FC = () => {
  const { t } = useTranslation();
  const [zoom, setZoom] = useState<number>(() => Number(localStorage.getItem(FONT_ZOOM_KEY) || '1'));

  const changeZoom = (z: number) => {
    setZoom(z);
    localStorage.setItem(FONT_ZOOM_KEY, String(z));
    applyAccessibility();
  };

  return (
    <div className="a11y-controls" role="group" aria-label={t('accessibility.fontSize')}>
      <span className="a11y-label" aria-hidden="true">A</span>
      <div className="a11y-zoom-group">
        <button
          className="a11y-zoom-btn"
          onClick={() => changeZoom(Math.max(0.85, Number((zoom - 0.1).toFixed(2))))}
          aria-label="Decrease font size"
          title="A−"
        >−</button>
        <span className="a11y-zoom-value" aria-live="polite">{Math.round(zoom * 100)}%</span>
        <button
          className="a11y-zoom-btn"
          onClick={() => changeZoom(Math.min(1.25, Number((zoom + 0.1).toFixed(2))))}
          aria-label="Increase font size"
          title="A+"
        >+</button>
      </div>
    </div>
  );
};

export const Navbar: React.FC = () => {
  const { currentUser, demoAccounts, switchDemoUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [lang, setLang] = useState<Lang>(getCurrentLang());
  const role = currentUser?.role || 'LEARNER';

  // One map-driven nav: route + label per role — rendered identically on desktop and mobile.
  const navItems =
    role === 'REVIEWER'
      ? [{ path: '/reviewer', label: t('nav.evidenceQueue'), icon: <SearchIcon /> }]
      : role === 'ADMIN'
        ? [{ path: '/admin', label: t('nav.governance'), icon: <AdminIcon /> }]
        : [
            { path: '/home', label: t('nav.home'), icon: null as React.ReactNode },
            { path: '/learning', label: t('nav.myLearning'), icon: null as React.ReactNode },
            { path: '/gaps', label: t('nav.skillGaps'), icon: null as React.ReactNode },
            { path: '/career', label: t('nav.careerPath'), icon: null as React.ReactNode },
          ];

  const copilotItem = { path: '/copilot', label: t('nav.aiCopilot'), icon: <SparkIcon /> };
  const allItems = [...navItems, copilotItem];

  const toggleLanguage = () => {
    const next: Lang = lang === 'en' ? 'hi' : 'en';
    setLanguage(next);
    setLang(next);
  };

  const go = (path: string) => {
    navigate(path);
    setMenuOpen(false);
  };

  const tagline =
    role === 'REVIEWER' ? 'NSSO Supervisory Evaluation Workspace'
    : role === 'ADMIN' ? 'Cadre Governance & Platform Administration'
    : 'Official Statistical System Competency Platform';

  return (
    <header className="site-header">
      {/* Floating glass pill navbar (signature component) */}
      <div className="gov-container">
        <nav className="glass-navbar" aria-label="Primary">
          {/* Brand lockup */}
          <button className="brand-lockup" onClick={() => go('/')} aria-label="iGOT Karmayogi SkillBridge home">
            <BrandSunIcon />
            <span className="brand-word">
              iGOT Karmayogi <em className="brand-suffix">SkillBridge</em>
              <span className="brand-tagline">{tagline}</span>
            </span>
          </button>

          {/* Center nav links — map-driven, shared by desktop + mobile */}
          <div className="nav-links">
            {allItems.map(item => (
              <button
                key={item.path}
                className={`nav-tab ${location.pathname === item.path ? 'active' : ''}`}
                onClick={() => go(item.path)}
                aria-current={location.pathname === item.path ? 'page' : undefined}
              >
                {item.icon}
                {item.label}
              </button>
            ))}
          </div>

          {/* Accessibility controls (font size + high contrast) */}
          <div className="nav-a11y">
            <AccessibilityControls />
          </div>

          {/* Flag + language toggle (functional EN/HI switch) */}
          <div className="nav-identity">
            <FlagIcon />
            <button
              className="lang-toggle"
              type="button"
              onClick={toggleLanguage}
              aria-label={lang === 'en' ? 'हिंदी में देखें' : 'View in English'}
              title={lang === 'en' ? 'हिंदी में देखें' : 'View in English'}
            >
              {lang === 'en' ? 'EN | हिंदी' : 'हिंदी | EN'}
            </button>
          </div>

          {/* Demo persona switcher */}
          <div style={{ position: 'relative', flex: 'none' }}>
            <button
              className="persona-chip"
              onClick={() => setDropdownOpen(!dropdownOpen)}
              aria-expanded={dropdownOpen}
              aria-haspopup="menu"
            >
              <div className={`persona-avatar role-${currentUser?.role || 'LEARNER'}`}>
                {currentUser?.full_name?.charAt(0) || 'U'}
              </div>
              <span>
                <span className="persona-chip-name">{currentUser?.full_name || 'Switch Demo Persona'}</span>
                <br />
                <span className="persona-chip-meta">
                  Role: <strong>{currentUser?.role}</strong> (Demo)
                </span>
              </span>
              <ChevronDownIcon />
            </button>

            {dropdownOpen && (
              <div className="persona-dropdown" role="menu" aria-label="Quick-switch demo persona">
                <div className="persona-dropdown-title">Quick-Switch Demo Persona</div>
                {demoAccounts.map(acc => (
                  <button
                    key={acc.user_id}
                    className={`persona-option ${currentUser?.user_id === acc.user_id ? 'selected' : ''}`}
                    onClick={() => {
                      switchDemoUser(acc.user_id);
                      setDropdownOpen(false);
                    }}
                  >
                    <span className="persona-option-name-row">
                      <span>{acc.full_name}</span>
                      <span className={`badge ${acc.role === 'ADMIN' ? 'badge-navy' : acc.role === 'REVIEWER' ? 'badge-saffron' : 'badge-green'}`} style={{ fontSize: '10px' }}>
                        {acc.role}
                      </span>
                    </span>
                    <span className="persona-option-desc">{acc.description}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Hamburger (mobile) */}
          <button
            className="hamburger"
            aria-expanded={menuOpen}
            aria-controls="mobile-menu"
            aria-label={t('nav.menu')}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <MenuIcon />
          </button>
        </nav>

        {menuOpen && (
          <div className="mobile-menu" id="mobile-menu" role="dialog" aria-label="Menu">
            {allItems.map(item => (
              <button
                key={item.path}
                className={`nav-tab ${location.pathname === item.path ? 'active' : ''}`}
                style={{ width: '100%', justifyContent: 'flex-start' }}
                onClick={() => go(item.path)}
              >
                {item.icon}
                {item.label}
              </button>
            ))}
            {/* Language toggle also reachable on mobile */}
            <div className="mobile-a11y-row">
              <AccessibilityControls />
              <button className="lang-toggle" type="button" onClick={toggleLanguage}>
                {lang === 'en' ? 'EN | हिंदी' : 'हिंदी | EN'}
              </button>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};
