import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { CareerReadinessResponse, LearningPathDTO, LearningPathItemDTO } from '../../types';
import { useReveal } from '../../hooks/useReveal';

const ScalesIcon: React.FC = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M12 3v18" />
    <path d="M5 7h14" />
    <path d="M5 7l-3 6a3.5 3.5 0 0 0 6 0L5 7z" />
    <path d="M19 7l-3 6a3.5 3.5 0 0 0 6 0l-3-6z" />
    <path d="M8 21h8" />
  </svg>
);

const ArrowRightIcon: React.FC = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <line x1="3" y1="12" x2="19" y2="12" />
    <polyline points="13 6 19 12 13 18" />
  </svg>
);

export const CareerPathView: React.FC = () => {
  const { currentUser, setActiveView, setSelectedLessonId, setActiveAssessmentId } = useAuth();
  const [readiness, setReadiness] = useState<CareerReadinessResponse | null>(null);
  const [learningPath, setLearningPath] = useState<LearningPathDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const bannerReveal = useReveal<HTMLDivElement>();
  const pathReveal = useReveal<HTMLDivElement>();

  // Draw the journey connector when the timeline scrolls into view (fail-visible)
  const connectorRef = useCallback((node: HTMLDivElement | null) => {
    if (!node || node.dataset.connectorInit === '1') return;
    node.dataset.connectorInit = '1';
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      node.classList.add('is-visible');
      return;
    }
    if (node.getBoundingClientRect().top < window.innerHeight) {
      node.classList.add('is-visible');
      return;
    }
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          node.classList.add('is-visible');
          obs.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    obs.observe(node);
    window.setTimeout(() => node.classList.add('is-visible'), 3000);
  }, []);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [cr, lp] = await Promise.all([
          api.getCareerReadiness(currentUser?.user_id),
          api.getLearningPath(currentUser?.user_id)
        ]);
        setReadiness(cr);
        setLearningPath(lp);
      } catch (err) {
        console.error('Failed to load career readiness data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [currentUser]);

  if (loading) {
    return (
      <div className="gov-container" style={{ padding: '60px', textAlign: 'center' }}>
        <div style={{ fontSize: '18px', color: 'var(--color-text-strong)' }}>Evaluating career learning pathway...</div>
      </div>
    );
  }

  if (!readiness || !learningPath) {
    return (
      <div className="gov-container" style={{ padding: '40px' }}>
        <p>Career readiness profile unavailable.</p>
      </div>
    );
  }

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* Header */}
      <div style={{ marginBottom: '28px' }}>
        <span className="eyebrow-meta">Career Progression & Readiness</span>
        <h1 className="page-title">Cadre Transition Pathway</h1>
        <p className="meta-line">
          Structured competency progression for officers transitioning from field survey roles to supervisory responsibilities.
        </p>
      </div>

      {/* Crucial Invariant Notice */}
      <div className="gov-card static" style={{
        padding: '16px 20px',
        backgroundColor: 'var(--blue-50)',
        border: '1px solid var(--blue-100)',
        marginBottom: '32px',
        display: 'flex',
        alignItems: 'center',
        gap: '14px'
      }}>
        <div style={{ color: 'var(--blue-500)', lineHeight: 1 }}><ScalesIcon /></div>
        <div>
          <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--blue-600)' }}>
            Official Notice on Career & Promotion Governance:
          </div>
          <div style={{ fontSize: '12px', color: 'var(--color-text-primary)', marginTop: '2px', lineHeight: 1.5 }}>
            {readiness.notice}
          </div>
        </div>
      </div>

      {/* Role Transition Visual Banner */}
      <div ref={bannerReveal} className="reveal">
        <div className="gov-card static" style={{ marginBottom: '32px', padding: '32px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '24px' }}>
            {/* Current Position */}
            <div style={{ flex: 1, minWidth: '260px' }}>
              <span className="badge badge-gray" style={{ marginBottom: '8px' }}>Current Substantive Role</span>
              <h3 style={{ fontSize: '20px', marginTop: '4px' }}>
                {readiness.current_position}
              </h3>
              <p className="section-sub" style={{ marginTop: '4px' }}>
                Field Operations Division • NSSO
              </p>
            </div>

            <div style={{ textAlign: 'center', padding: '0 20px' }}>
              <div style={{ color: 'var(--orange-500)', display: 'inline-flex' }}><ArrowRightIcon /></div>
              <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Cadre Advancement</div>
            </div>

            {/* Target Position */}
            <div style={{ flex: 1, minWidth: '260px', backgroundColor: 'var(--wash-cream)', padding: '20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--orange-100)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', flexWrap: 'wrap', gap: '6px' }}>
                <span className="badge badge-saffron">Target Promotional Role</span>
                <span className="badge badge-navy">{readiness.plain_readiness_label.split(':')[1]}</span>
              </div>
              <h3 style={{ fontSize: '20px', marginTop: '4px' }}>
                {readiness.target_position}
              </h3>
              <p className="section-sub" style={{ marginTop: '4px' }}>
                Requires Level 4 Sampling, Supervisory Auditing, and Data Validation.
              </p>
            </div>
          </div>

          {/* Readiness Progress Bar */}
          <div style={{ marginTop: '28px', borderTop: '1px solid var(--color-border)', paddingTop: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '8px', flexWrap: 'wrap', gap: '6px' }}>
              <span style={{ fontWeight: 700, color: 'var(--color-text-strong)' }}>Competency Requirements Fulfilled</span>
              <span style={{ fontWeight: 700, color: 'var(--orange-700)' }}>
                {readiness.met_competencies_count} of {readiness.total_required_competencies} Competencies Verified
              </span>
            </div>
            <div className="progress-track">
              <div
                className="progress-fill"
                style={{ width: `${Math.round((readiness.met_competencies_count / readiness.total_required_competencies) * 100)}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Sequential Learning Path Timeline */}
      <div ref={pathReveal} className="reveal">
        <div style={{ marginBottom: '20px' }}>
          <h2 className="section-heading" style={{ fontSize: '22px' }}>
            Sequential Pathway Progression
          </h2>
          <p className="section-sub">
            Vertical curriculum sequenced to resolve foundational dependencies before practical evaluation.
          </p>
        </div>

        <div className="career-connector-wrap" aria-hidden="true">
          <div className="career-connector" ref={connectorRef} />
        </div>

        <div className="career-steps">
          {learningPath.items.map((item: LearningPathItemDTO, idx: number) => {
            const isFirst = idx === 0;
            return (
              <div
                key={item.path_item_id}
                className={`career-step ${isFirst ? 'current' : ''}`}
              >
                <div className="career-step-node">{item.sequence_no}</div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px', flexWrap: 'wrap' }}>
                  <span className={`badge ${isFirst ? 'badge-green' : 'badge-gray'}`} style={{ fontSize: '11px' }}>
                    Stage: {item.stage}
                  </span>
                  <span style={{ fontSize: '12px', color: 'var(--color-text-muted)' }}>
                    Status: <strong>{item.status.replace(/_/g, ' ')}</strong>
                  </span>
                </div>

                <h3 style={{ fontSize: '16px' }}>
                  {item.action_label}
                </h3>

                <div style={{ fontSize: '13px', color: 'var(--color-text-secondary)', marginTop: '4px' }}>
                  Competency: <strong>{item.competency_label}</strong>
                  {item.course_title && ` • Course: ${item.course_title}`}
                </div>

                <div style={{ marginTop: '14px' }}>
                  <button
                    className={`btn btn-sm ${isFirst ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => {
                      if (item.stage === 'PRACTICAL' || item.stage === 'ASSESSMENT') {
                        setActiveAssessmentId('ASS-DEMO-PRACTICAL-001');
                      } else {
                        setSelectedLessonId('sampling-lesson-3');
                      }
                      setActiveView('learning');
                    }}
                  >
                    {isFirst ? 'Continue Now →' : 'View Module'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
