import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { CareerReadinessResponse, LearningPathDTO, LearningPathItemDTO } from '../../types';

export const CareerPathView: React.FC = () => {
  const { currentUser, setActiveView, setSelectedLessonId, setActiveAssessmentId } = useAuth();
  const [readiness, setReadiness] = useState<CareerReadinessResponse | null>(null);
  const [learningPath, setLearningPath] = useState<LearningPathDTO | null>(null);
  const [loading, setLoading] = useState(true);

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
        <div style={{ fontSize: '18px', color: '#1a365d' }}>Evaluating career learning pathway...</div>
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
        <span style={{ fontSize: '12px', fontWeight: 700, color: '#d97706', textTransform: 'uppercase' }}>
          Career Progression & Readiness
        </span>
        <h1 style={{ fontSize: '28px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
          Cadre Transition Pathway
        </h1>
        <p style={{ fontSize: '14px', color: '#64748b', marginTop: '4px' }}>
          Structured competency progression for officers transitioning from field survey roles to supervisory responsibilities.
        </p>
      </div>

      {/* Crucial Invariant Notice */}
      <div style={{
        padding: '16px 20px',
        backgroundColor: '#ebf8ff',
        borderRadius: '10px',
        borderLeft: '5px solid #2b6cb0',
        marginBottom: '32px',
        display: 'flex',
        alignItems: 'center',
        gap: '14px'
      }}>
        <div style={{ fontSize: '24px' }}>⚖️</div>
        <div>
          <div style={{ fontSize: '13px', fontWeight: 700, color: '#1e40af' }}>
            Official Notice on Career & Promotion Governance:
          </div>
          <div style={{ fontSize: '12px', color: '#1e3a8a', marginTop: '2px', lineHeight: 1.5 }}>
            {readiness.notice}
          </div>
        </div>
      </div>

      {/* Role Transition Visual Banner */}
      <div className="gov-card" style={{ marginBottom: '32px', padding: '32px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '24px' }}>
          {/* Current Position */}
          <div style={{ flex: 1, minWidth: '260px' }}>
            <span className="badge badge-gray" style={{ marginBottom: '8px' }}>Current Substantive Role</span>
            <h3 style={{ fontSize: '20px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
              {readiness.current_position}
            </h3>
            <p style={{ fontSize: '13px', color: '#64748b', marginTop: '4px' }}>
              Field Operations Division • NSSO
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '0 20px' }}>
            <div style={{ fontSize: '28px', color: '#d97706', fontWeight: 900 }}>➔</div>
            <div style={{ fontSize: '11px', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>Cadre Advancement</div>
          </div>

          {/* Target Position */}
          <div style={{ flex: 1, minWidth: '260px', backgroundColor: '#f8fafc', padding: '20px', borderRadius: '10px', border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span className="badge badge-saffron">Target Promotional Role</span>
              <span className="badge badge-navy">{readiness.plain_readiness_label.split(':')[1]}</span>
            </div>
            <h3 style={{ fontSize: '20px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
              {readiness.target_position}
            </h3>
            <p style={{ fontSize: '13px', color: '#64748b', marginTop: '4px' }}>
              Requires Level 4 Sampling, Supervisory Auditing, and Data Validation.
            </p>
          </div>
        </div>

        {/* Readiness Progress Bar */}
        <div style={{ marginTop: '28px', borderTop: '1px solid #f1f5f9', paddingTop: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '8px' }}>
            <span style={{ fontWeight: 700, color: '#1a365d' }}>Competency Requirements Fulfilled</span>
            <span style={{ fontWeight: 700, color: '#d97706' }}>
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

      {/* Sequential Learning Path Timeline */}
      <div>
        <div style={{ marginBottom: '20px' }}>
          <h2 style={{ fontSize: '22px', fontWeight: 800, color: '#1a365d' }}>
            Sequential Pathway Progression
          </h2>
          <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
            Vertical curriculum sequenced to resolve foundational dependencies before practical evaluation.
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {learningPath.items.map((item: LearningPathItemDTO, idx: number) => {
            const isFirst = idx === 0;
            return (
              <div
                key={item.path_item_id}
                className="gov-card"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '20px',
                  padding: '20px',
                  borderLeft: isFirst ? '6px solid #166534' : '6px solid #cbd5e1',
                  backgroundColor: isFirst ? '#ffffff' : '#fcfcfd'
                }}
              >
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '50%',
                  backgroundColor: isFirst ? '#166534' : '#e2e8f0',
                  color: isFirst ? '#ffffff' : '#64748b',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '15px',
                  fontWeight: 800
                }}>
                  {item.sequence_no}
                </div>

                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                    <span className={`badge ${isFirst ? 'badge-green' : 'badge-gray'}`} style={{ fontSize: '11px' }}>
                      Stage: {item.stage}
                    </span>
                    <span style={{ fontSize: '12px', color: '#64748b' }}>
                      Status: <strong>{item.status.replace(/_/g, ' ')}</strong>
                    </span>
                  </div>

                  <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#0f172a' }}>
                    {item.action_label}
                  </h3>

                  <div style={{ fontSize: '13px', color: '#475569', marginTop: '4px' }}>
                    Competency: <strong>{item.competency_label}</strong>
                    {item.course_title && ` • Course Reference: ${item.course_title}`}
                  </div>
                </div>

                <div>
                  <button
                    className={`btn ${isFirst ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => {
                      if (item.stage === 'PRACTICAL' || item.stage === 'ASSESSMENT') {
                        setActiveAssessmentId('ASS-DEMO-PRACTICAL-001');
                      } else {
                        setSelectedLessonId('sampling-lesson-3');
                      }
                      setActiveView('learning');
                    }}
                    style={{ fontSize: '13px', minHeight: '36px', padding: '8px 18px' }}
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
