import React from 'react';

const CheckIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const footerPipeline = [
  'Competency Profiling & Gap Identification',
  'Curated Video Lessons & Searchable Transcripts',
  'Groq Llama-3.3 Practice Quiz Generation',
  'Formal Proficiency Assessments with Rubrics',
  'Supervisor-Verified Evidence Ingestion',
  'Automatic Learning Path Recomputation',
];

const footerTerms = ['Terms of Service', 'Data Privacy Framework', 'Accessibility Guidelines', 'Cadre Competency Matrix'];

export const Footer: React.FC = () => {
  return (
    <footer style={{ marginTop: '64px' }}>
      {/* Upper tier — ink */}
      <div style={{ backgroundColor: 'var(--ink-500)', color: 'var(--ink-100)', padding: '48px 0 32px' }}>
        <div className="gov-container">
          <div className="grid-3" style={{ marginBottom: '36px' }}>
            <div>
              <div style={{ color: '#FFFFFF', fontFamily: 'var(--font-heading)', fontSize: '16px', fontWeight: 700, marginBottom: '12px' }}>
                iGOT Karmayogi | SkillBridge
              </div>
              <p style={{ fontSize: '13px', lineHeight: 1.6, color: '#C1C9D1' }}>
                Competency-based capacity building and adaptive learning architecture for officials in India's Official Statistical System.
              </p>
              <div style={{ marginTop: '14px', fontSize: '12px', color: 'var(--ink-100)' }}>
                Ministry of Statistics and Programme Implementation<br />
                Sardar Patel Bhawan, Sansad Marg, New Delhi
              </div>
            </div>

            <div>
              <div style={{ color: '#FFFFFF', fontSize: '14px', fontWeight: 700, marginBottom: '12px' }}>
                Core Pipeline & Governance
              </div>
              <ul style={{ listStyle: 'none', padding: 0, fontSize: '13px', lineHeight: 2 }}>
                {footerPipeline.map(item => (
                  <li key={item} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                    <span style={{ color: 'var(--orange-bright)', flex: 'none', marginTop: '9px' }}><CheckIcon /></span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <div style={{ color: '#FFFFFF', fontSize: '14px', fontWeight: 700, marginBottom: '12px' }}>
                Architecture & Transparency Notice
              </div>
              <p style={{ fontSize: '12px', lineHeight: 1.6, color: '#C1C9D1' }}>
                This platform demonstrates deterministic competency evaluation and an iGOT provider abstraction. Curated YouTube playlists are labeled as external learning resources and are not claimed to be native iGOT LMS courses.
              </p>
              <div style={{ marginTop: '12px', padding: '8px 12px', backgroundColor: 'var(--ink-600)', border: '1px solid var(--ink-divider)', borderRadius: 'var(--radius-sm)', fontSize: '11px', color: 'var(--orange-bright)' }}>
                <strong>Zero Invariant Violation:</strong> Practice quizzes never alter competency levels. Only supervisor-reviewed evidence updates proficiency.
              </div>
            </div>
          </div>

          <div style={{ borderTop: '1px solid var(--ink-divider)', paddingTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', flexWrap: 'wrap', gap: '12px', color: 'var(--ink-100)' }}>
            <div>
              © 2026 Ministry of Statistics & Programme Implementation (MoSPI). Smart India Hackathon Prototype.
            </div>
            <div style={{ display: 'flex', gap: '20px' }}>
              {footerTerms.map(term => (
                <span key={term}>{term}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Lower tier — royal blue copyright bar */}
      <div style={{ backgroundColor: 'var(--blue-500)', color: '#FFFFFF', padding: '10px 0' }}>
        <div className="gov-container" style={{ display: 'flex', justifyContent: 'center' }}>
          <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '0.04em' }}>
            Karmayogi Bharat — National Programme for Civil Services Capacity Building
          </span>
        </div>
      </div>
    </footer>
  );
};
