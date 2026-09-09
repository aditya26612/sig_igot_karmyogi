import React from 'react';

/* Shared inline SVG icon set — Material-Symbols-like, single 1.8px stroke, round caps, 24px box.
   Usage: <Icon.Check /> — color & size flow from currentColor / CSS. */

type IconProps = { size?: number; className?: string; style?: React.CSSProperties; title?: string };

const Svg: React.FC<React.PropsWithChildren<IconProps>> = ({ size, className, style, children, title }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    style={style}
    aria-hidden={title ? undefined : true}
    role={title ? 'img' : undefined}
  >
    {title && <title>{title}</title>}
    {children}
  </svg>
);

export const Icon = {
  /* Brand / chrome */
  Sparkle: (p: IconProps) => (
    <Svg {...p}>
      <path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z" />
      <path d="M18.5 15.5l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8.8-2.2z" />
    </Svg>
  ),
  Sun: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="12" cy="12" r="4.2" />
      <path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5 5l1.6 1.6M17.4 17.4L19 19M19 5l-1.6 1.6M6.6 17.4L5 19" />
    </Svg>
  ),
  Flag: (p: IconProps) => (
    <Svg {...p}>
      <path d="M5 3v18" />
      <path d="M5 4h11l-1.5 3.5L16 11H5z" />
    </Svg>
  ),
  Home: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4 11l8-7 8 7" />
      <path d="M6 10v10h12V10" />
      <path d="M10 20v-5h4v5" />
    </Svg>
  ),
  Menu: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4 7h16M4 12h16M4 17h16" />
    </Svg>
  ),
  Close: (p: IconProps) => (
    <Svg {...p}>
      <path d="M6 6l12 12M18 6L6 18" />
    </Svg>
  ),
  ChevronDown: (p: IconProps) => (
    <Svg {...p}>
      <path d="M6 9.5l6 6 6-6" />
    </Svg>
  ),
  ArrowRight: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4 12h15" />
      <path d="M13 6l6 6-6 6" />
    </Svg>
  ),
  ArrowUpRight: (p: IconProps) => (
    <Svg {...p}>
      <path d="M7 17L17 7" />
      <path d="M8 7h9v9" />
    </Svg>
  ),
  Refresh: (p: IconProps) => (
    <Svg {...p}>
      <path d="M20 12a8 8 0 1 1-2.34-5.66" />
      <path d="M20 4v4h-4" />
    </Svg>
  ),
  Copy: (p: IconProps) => (
    <Svg {...p}>
      <rect x="9" y="9" width="11" height="11" rx="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </Svg>
  ),
  Maximize: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4 9V4h5M20 15v5h-5M15 4h5v5M9 20H4v-5" />
    </Svg>
  ),
  Restore: (p: IconProps) => (
    <Svg {...p}>
      <path d="M9 4v5H4M15 20v-5h5M20 9h-5V4M4 15h5v5" />
    </Svg>
  ),

  /* Domain: learning / competency */
  Book: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z" />
      <path d="M4 5.5V20.5" />
      <path d="M8 7h8M8 11h6" />
    </Svg>
  ),
  Target: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="12" cy="12" r="8.5" />
      <circle cx="12" cy="12" r="4.5" />
      <circle cx="12" cy="12" r="0.5" fill="currentColor" />
    </Svg>
  ),
  ChartGaps: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4 20h16" />
      <path d="M7 20v-6M12 20V8M17 20v-9" />
    </Svg>
  ),
  Route: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="6" cy="18" r="2.5" />
      <circle cx="18" cy="6" r="2.5" />
      <path d="M8.5 18h5a4 4 0 0 0 4-4V8.5" />
      <path d="M15.5 10.5L18 8l2.5 2.5" transform="translate(-2 0)" opacity="0" />
    </Svg>
  ),
  Search: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="11" cy="11" r="7" />
      <path d="M21 21l-4.3-4.3" />
    </Svg>
  ),
  ShieldAdmin: (p: IconProps) => (
    <Svg {...p}>
      <path d="M12 3l7 3v5c0 4.5-3 8.5-7 10-4-1.5-7-5.5-7-10V6z" />
      <path d="M9 12l2 2 4-4" />
    </Svg>
  ),
  Scale: (p: IconProps) => (
    <Svg {...p}>
      <path d="M12 3v18M8 21h8" />
      <path d="M5 7h14M5 7l-2.5 6h5L5 7zM19 7l-2.5 6h5L19 7z" />
      <path d="M7 5h10" />
    </Svg>
  ),
  Medal: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="12" cy="14.5" r="5" />
      <path d="M12 12.2l.8 1.7 1.9.2-1.4 1.3.4 1.9-1.7-1-1.7 1 .4-1.9-1.4-1.3 1.9-.2z" fill="currentColor" stroke="none" />
      <path d="M8.5 3h7l-2.5 6h-2z" />
    </Svg>
  ),
  Clock: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="12" cy="12" r="8.5" />
      <path d="M12 7v5l3.5 2" />
    </Svg>
  ),
  Tag: (p: IconProps) => (
    <Svg {...p}>
      <path d="M3 11.5V4a1 1 0 0 1 1-1h7.5L21 12.5 12.5 21z" />
      <circle cx="7.5" cy="7.5" r="1.3" fill="currentColor" stroke="none" />
    </Svg>
  ),
  Transcript: (p: IconProps) => (
    <Svg {...p}>
      <path d="M6 3h9l5 5v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z" />
      <path d="M15 3v5h5" />
      <path d="M9 12h7M9 16h5" />
    </Svg>
  ),
  Play: (p: IconProps) => (
    <Svg {...p}>
      <path d="M8 5.5v13l10.5-6.5z" fill="currentColor" />
    </Svg>
  ),
  Lightbulb: (p: IconProps) => (
    <Svg {...p}>
      <path d="M9 17h6M10 21h4" />
      <path d="M12 3a6 6 0 0 1 3.5 10.9c-.6.5-.9 1.1-.9 1.6H9.4c0-.5-.3-1.1-.9-1.6A6 6 0 0 1 12 3z" />
    </Svg>
  ),
  Bank: (p: IconProps) => (
    <Svg {...p}>
      <path d="M3 9.5L12 4l9 5.5" />
      <path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8" />
      <path d="M3 20h18" />
    </Svg>
  ),
  Clipboard: (p: IconProps) => (
    <Svg {...p}>
      <rect x="5" y="4" width="14" height="18" rx="2" />
      <path d="M9 4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1H9z" />
      <path d="M9 11h6M9 15h4" />
    </Svg>
  ),
  TrendUp: (p: IconProps) => (
    <Svg {...p}>
      <path d="M3 17l6-6 4 4 8-8" />
      <path d="M15 7h6v6" />
    </Svg>
  ),
  Paperclip: (p: IconProps) => (
    <Svg {...p}>
      <path d="M8 12.5l6-6a3.2 3.2 0 0 1 4.5 4.5l-8 8a5 5 0 0 1-7-7l7.5-7.5" />
    </Svg>
  ),
  Plus: (p: IconProps) => (
    <Svg {...p}>
      <path d="M12 5v14M5 12h14" />
    </Svg>
  ),
  Check: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4.5 12.5l5 5 10-11" />
    </Svg>
  ),
  CheckCircle: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="12" cy="12" r="9" />
      <path d="M8 12.5l2.5 2.5 5.5-6" />
    </Svg>
  ),
  Mic: (p: IconProps) => (
    <Svg {...p}>
      <rect x="9" y="3" width="6" height="11" rx="3" />
      <path d="M5 11a7 7 0 0 0 14 0" />
      <path d="M12 18v3" />
    </Svg>
  ),
  Send: (p: IconProps) => (
    <Svg {...p}>
      <path d="M21 3L10.5 13.5" />
      <path d="M21 3l-7 18-3.5-7.5L3 10z" />
    </Svg>
  ),
  Hourglass: (p: IconProps) => (
    <Svg {...p}>
      <path d="M7 3h10M7 21h10" />
      <path d="M8 3v3.5c0 2 1.5 3.5 4 5.5 2.5-2 4-3.5 4-5.5V3" />
      <path d="M8 21v-3.5c0-2 1.5-3.5 4-5.5 2.5 2 4 3.5 4 5.5V21" />
    </Svg>
  ),
  Users: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="9" cy="8" r="3.5" />
      <path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" />
      <path d="M15.5 5a3.5 3.5 0 0 1 0 7M17.5 14.5c2.1.8 3.5 2.9 3.5 5.5" />
    </Svg>
  ),
  Database: (p: IconProps) => (
    <Svg {...p}>
      <ellipse cx="12" cy="5.5" rx="8" ry="2.5" />
      <path d="M4 5.5v13c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5v-13" />
      <path d="M4 12c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5" />
    </Svg>
  ),
  Sync: (p: IconProps) => (
    <Svg {...p}>
      <path d="M4 12a8 8 0 0 1 13.66-5.66L20 8" />
      <path d="M20 4v4h-4" />
      <path d="M20 12a8 8 0 0 1-13.66 5.66L4 16" />
      <path d="M4 20v-4h4" />
    </Svg>
  ),
  Video: (p: IconProps) => (
    <Svg {...p}>
      <rect x="3" y="6" width="13" height="12" rx="2" />
      <path d="M16 10.5l5-3v9l-5-3z" />
    </Svg>
  ),
  Info: (p: IconProps) => (
    <Svg {...p}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 11v5" />
      <circle cx="12" cy="8" r="0.6" fill="currentColor" stroke="none" />
    </Svg>
  ),
};
