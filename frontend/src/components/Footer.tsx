import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer style={{ backgroundColor: '#0f294a', color: '#94a3b8', padding: '48px 0 24px 0', marginTop: '64px', borderTop: '4px solid #d97706' }}>
      <div className="gov-container">
        <div className="grid-3" style={{ marginBottom: '36px' }}>
          <div>
            <div style={{ color: '#ffffff', fontSize: '16px', fontWeight: 800, marginBottom: '12px', fontFamily: 'var(--font-heading)' }}>
              iGOT Karmayogi | MoSPI
            </div>
            <p style={{ fontSize: '13px', lineHeight: 1.6, color: '#cbd5e1' }}>
              Competency-based capacity building and adaptive learning architecture for officials in India's Official Statistical System.
            </p>
            <div style={{ marginTop: '14px', fontSize: '12px', color: '#94a3b8' }}>
              Ministry of Statistics and Programme Implementation<br />
              Sardar Patel Bhawan, Sansad Marg, New Delhi
            </div>
          </div>

          <div>
            <div style={{ color: '#ffffff', fontSize: '14px', fontWeight: 700, marginBottom: '12px' }}>
              Core Pipeline & Governance
            </div>
            <ul style={{ listStyle: 'none', padding: 0, fontSize: '13px', lineHeight: 2 }}>
              <li>✓ Competency Profiling & Gap Identification</li>
              <li>✓ Curated Video Lessons & Searchable Transcripts</li>
              <li>✓ Groq Llama-3.3 Practice Quiz Generation</li>
              <li>✓ Formal Proficiency Assessments with Rubrics</li>
              <li>✓ Supervisor-Verified Evidence Ingestion</li>
              <li>✓ Automatic Learning Path Recomputation</li>
            </ul>
          </div>

          <div>
            <div style={{ color: '#ffffff', fontSize: '14px', fontWeight: 700, marginBottom: '12px' }}>
              Architecture & Transparency Notice
            </div>
            <p style={{ fontSize: '12px', lineHeight: 1.6, color: '#cbd5e1' }}>
              This platform demonstrates deterministic competency evaluation and an iGOT provider abstraction. Curated YouTube playlists are labeled as external learning resources and are not claimed to be native iGOT LMS courses.
            </p>
            <div style={{ marginTop: '12px', padding: '8px 12px', backgroundColor: 'rgba(255,255,255,0.06)', borderRadius: '6px', fontSize: '11px', color: '#fde68a' }}>
              <strong>Zero Invariant Violation:</strong> Practice quizzes never alter competency levels. Only supervisor-reviewed evidence updates proficiency.
            </div>
          </div>
        </div>

        <div style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            © 2026 Ministry of Statistics & Programme Implementation (MoSPI). Smart India Hackathon Prototype.
          </div>
          <div style={{ display: 'flex', gap: '20px' }}>
            <span>Terms of Service</span>
            <span>Data Privacy Framework</span>
            <span>Accessibility Guidelines</span>
            <span>Cadre Competency Matrix</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
