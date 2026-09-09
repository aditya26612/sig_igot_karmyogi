import React, { useState } from 'react';
import { CompetencyGapItem } from '../types';
import { useAuth } from '../context/AuthContext';

interface SkillGapCardProps {
  gap: CompetencyGapItem;
}

export const SkillGapCard: React.FC<SkillGapCardProps> = ({ gap }) => {
  const [expanded, setExpanded] = useState(false);
  const { setActiveView, setSelectedLessonId, setActiveAssessmentId } = useAuth();

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'HIGH':
        return <span className="badge badge-danger">Priority Skill to Improve</span>;
      case 'MEDIUM':
        return <span className="badge badge-saffron">Moderate Gap</span>;
      case 'NO_GAP':
        return <span className="badge badge-green">Requirements Met</span>;
      case 'INSUFFICIENT_EVIDENCE':
        return <span className="badge badge-gray">Diagnostic Required</span>;
      default:
        return <span className="badge badge-navy">{status}</span>;
    }
  };

  const handleLearnClick = () => {
    if (gap.competency_id === 'COMP-SAMPLING') {
      setSelectedLessonId('sampling-lesson-3');
    }
    setActiveView('learning');
  };

  const handleAssessClick = () => {
    setActiveAssessmentId('ASS-DEMO-PRACTICAL-001');
    setActiveView('learning');
  };

  return (
    <div className="gov-card gap-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px', gap: '8px' }}>
          <div>
            <div className="eyebrow-meta" style={{ color: 'var(--color-text-muted)' }}>
              {gap.competency_id}
            </div>
            <h3 className="gap-title" style={{ fontSize: '18px', marginTop: '2px' }}>
              {gap.plain_title}
            </h3>
          </div>
          {getStatusBadge(gap.gap_status)}
        </div>

        <p className="gap-plain" style={{ marginBottom: '16px' }}>
          {gap.plain_explanation}
        </p>

        {/* Level metrics */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 14px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', marginBottom: '16px' }}>
          <div style={{ flex: 1, textAlign: 'center' }}>
            <div className="gap-level-label">Current Level</div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: gap.current_level ? 'var(--blue-500)' : 'var(--color-text-muted)' }}>
              {gap.current_level ? `Level ${gap.current_level}` : 'Unknown'}
            </div>
          </div>

          <div style={{ color: 'var(--color-border-strong)', fontWeight: 700 }}>→</div>

          <div style={{ flex: 1, textAlign: 'center' }}>
            <div className="gap-level-label">Target Role Need</div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--orange-700)' }}>
              Level {gap.required_level}
            </div>
          </div>

          <div style={{ width: '1px', height: '24px', backgroundColor: 'var(--color-border-strong)' }} />

          <div style={{ flex: 1, textAlign: 'center' }}>
            <div className="gap-level-label">Unmet Gap</div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: (gap.unmet_gap || 0) > 0 ? 'var(--color-danger)' : 'var(--color-success)' }}>
              {(gap.unmet_gap || 0) > 0 ? `${gap.unmet_gap} Level${gap.unmet_gap! > 1 ? 's' : ''}` : 'None'}
            </div>
          </div>
        </div>

        {/* Expandable Why this gap matters? */}
        {expanded && (
          <div style={{ padding: '14px', backgroundColor: 'var(--blue-50)', borderRadius: 'var(--radius-md)', border: '1px solid var(--blue-100)', marginBottom: '16px', fontSize: '13px' }}>
            <div style={{ fontWeight: 700, color: 'var(--blue-600)', marginBottom: '6px' }}>
              Why this competency matters for {gap.target_role_name}:
            </div>
            <p style={{ color: 'var(--color-text-primary)', lineHeight: 1.5, margin: 0 }}>
              Your target role requires independent verification and execution. In NSSO field operations, officers must audit sampling frames and calculate strata weights.
            </p>
            {gap.contributing_activities.length > 0 && (
              <div style={{ marginTop: '10px' }}>
                <strong style={{ color: 'var(--blue-600)', fontSize: '11px', textTransform: 'uppercase' }}>Contributing Official Activities:</strong>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '4px' }}>
                  {gap.contributing_activities.map((act, i) => (
                    <span key={i} style={{ backgroundColor: 'var(--blue-50)', color: 'var(--blue-600)', padding: '2px 8px', borderRadius: 'var(--radius-sm)', fontSize: '11px', border: '1px solid var(--blue-100)' }}>
                      {act}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', borderTop: '1px solid var(--color-border)', gap: '8px', flexWrap: 'wrap' }}>
        <button
          onClick={() => setExpanded(!expanded)}
          style={{ background: 'none', border: 'none', color: 'var(--blue-500)', fontSize: '12px', fontWeight: 700, cursor: 'pointer', padding: 0 }}
        >
          {expanded ? '▲ Hide context' : '▼ Why this skill?'}
        </button>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="btn btn-secondary btn-sm" onClick={handleLearnClick}>
            Watch Lessons
          </button>
          <button className="btn btn-primary btn-sm" onClick={handleAssessClick}>
            Assessment
          </button>
        </div>
      </div>
    </div>
  );
};
