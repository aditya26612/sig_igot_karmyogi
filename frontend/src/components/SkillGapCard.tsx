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
    <div className="gov-card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
          <div>
            <div style={{ fontSize: '11px', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>
              {gap.competency_id}
            </div>
            <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#1a365d', marginTop: '2px' }}>
              {gap.plain_title}
            </h3>
          </div>
          {getStatusBadge(gap.gap_status)}
        </div>

        <p style={{ fontSize: '13px', color: '#475569', lineHeight: 1.5, marginBottom: '16px' }}>
          {gap.plain_explanation}
        </p>

        {/* Level metrics */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px 14px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '16px' }}>
          <div style={{ flex: 1, textAlign: 'center' }}>
            <div style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase' }}>Current Level</div>
            <div style={{ fontSize: '16px', fontWeight: 800, color: gap.current_level ? '#1a365d' : '#94a3b8' }}>
              {gap.current_level ? `Level ${gap.current_level}` : 'Unknown'}
            </div>
          </div>

          <div style={{ color: '#cbd5e1', fontWeight: 700 }}>→</div>

          <div style={{ flex: 1, textAlign: 'center' }}>
            <div style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase' }}>Target Role Need</div>
            <div style={{ fontSize: '16px', fontWeight: 800, color: '#d97706' }}>
              Level {gap.required_level}
            </div>
          </div>

          <div style={{ width: '1px', height: '24px', backgroundColor: '#cbd5e1' }} />

          <div style={{ flex: 1, textAlign: 'center' }}>
            <div style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase' }}>Unmet Gap</div>
            <div style={{ fontSize: '16px', fontWeight: 800, color: (gap.unmet_gap || 0) > 0 ? '#dc2626' : '#166534' }}>
              {(gap.unmet_gap || 0) > 0 ? `${gap.unmet_gap} Level${gap.unmet_gap! > 1 ? 's' : ''}` : 'None'}
            </div>
          </div>
        </div>

        {/* Expandable Why this gap matters? */}
        {expanded && (
          <div style={{ padding: '14px', backgroundColor: '#ebf8ff', borderRadius: '8px', border: '1px solid #bfdbfe', marginBottom: '16px', fontSize: '13px' }}>
            <div style={{ fontWeight: 700, color: '#1e40af', marginBottom: '6px' }}>
              Why this competency matters for {gap.target_role_name}:
            </div>
            <p style={{ color: '#1e3a8a', lineHeight: 1.5, margin: 0 }}>
              Your target role requires independent verification and execution. In NSSO field operations, officers must audit sampling frames and calculate strata weights.
            </p>
            {gap.contributing_activities.length > 0 && (
              <div style={{ marginTop: '10px' }}>
                <strong style={{ color: '#1e40af', fontSize: '11px', textTransform: 'uppercase' }}>Contributing Official Activities:</strong>
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '4px' }}>
                  {gap.contributing_activities.map((act, i) => (
                    <span key={i} style={{ backgroundColor: '#dbeafe', color: '#1e40af', padding: '2px 8px', borderRadius: '4px', fontSize: '11px' }}>
                      {act}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', borderTop: '1px solid #f1f5f9' }}>
        <button
          onClick={() => setExpanded(!expanded)}
          style={{ background: 'none', border: 'none', color: '#1a365d', fontSize: '12px', fontWeight: 600, cursor: 'pointer', padding: 0 }}
        >
          {expanded ? '▲ Hide context' : '▼ Why this skill?'}
        </button>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="btn btn-secondary" onClick={handleLearnClick} style={{ padding: '6px 12px', fontSize: '13px', minHeight: '34px' }}>
            Watch Lessons
          </button>
          <button className="btn btn-primary" onClick={handleAssessClick} style={{ padding: '6px 12px', fontSize: '13px', minHeight: '34px' }}>
            Assessment
          </button>
        </div>
      </div>
    </div>
  );
};
