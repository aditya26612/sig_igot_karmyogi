import React from 'react';
import { useTranslation } from 'react-i18next';

export const Footer: React.FC = () => {
  const { t } = useTranslation();

  return (
    <footer style={{ marginTop: '64px' }}>
      {/* Upper tier — ink */}
      <div style={{ backgroundColor: 'var(--ink-500)', color: 'var(--ink-100)', padding: '44px 0 30px' }}>
        <div className="gov-container">
          <div className="grid-3" style={{ marginBottom: '30px', gridTemplateColumns: '1.2fr 1fr' }}>
            <div>
              <div style={{ color: '#FFFFFF', fontFamily: 'var(--font-heading)', fontSize: '16px', fontWeight: 700, marginBottom: '10px' }}>
                {t('footer.brand')}
              </div>
              <p style={{ fontSize: '13px', lineHeight: 1.6, color: '#C1C9D1', margin: 0 }}>
                {t('footer.about')}
              </p>
              <div style={{ marginTop: '12px', fontSize: '12px', color: 'var(--ink-100)' }}>
                {t('footer.address').split(',').map((part, i, arr) => (
                  <React.Fragment key={i}>
                    {part.trim()}{i < arr.length - 1 ? <br /> : ''}
                  </React.Fragment>
                ))}
              </div>
            </div>

            <div>
              <div style={{ color: '#FFFFFF', fontSize: '14px', fontWeight: 700, marginBottom: '10px' }}>
                {t('footer.transparencyTitle')}
              </div>
              <p style={{ fontSize: '12px', lineHeight: 1.6, color: '#C1C9D1', margin: '0 0 12px' }}>
                {t('footer.transparencyBody')}
              </p>
              <div style={{ padding: '8px 12px', backgroundColor: 'var(--ink-600)', border: '1px solid var(--ink-divider)', borderRadius: 'var(--radius-sm)', fontSize: '11px', color: 'var(--orange-bright)' }}>
                <strong>{t('footer.zeroInvariant')}</strong>
              </div>
            </div>
          </div>

          <div style={{ borderTop: '1px solid var(--ink-divider)', paddingTop: '18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', flexWrap: 'wrap', gap: '12px', color: 'var(--ink-100)' }}>
            <div>
              {t('footer.copyright')}
            </div>
            <div style={{ fontSize: '11px', color: '#9AA3AF' }}>
              {t('footer.builtFor')}
            </div>
          </div>
        </div>
      </div>

      {/* Lower tier — royal blue copyright bar */}
      <div style={{ backgroundColor: 'var(--blue-500)', color: '#FFFFFF', padding: '10px 0' }}>
        <div className="gov-container" style={{ display: 'flex', justifyContent: 'center' }}>
          <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '0.04em' }}>
            {t('footer.copyrightBar')}
          </span>
        </div>
      </div>
    </footer>
  );
};
