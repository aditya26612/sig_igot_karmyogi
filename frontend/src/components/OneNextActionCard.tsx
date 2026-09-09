import React from 'react';
import { NextActionItem } from '../types';
import { useAuth } from '../context/AuthContext';

interface OneNextActionCardProps {
  nextAction: NextActionItem;
}

export const OneNextActionCard: React.FC<OneNextActionCardProps> = ({ nextAction }) => {
  const { setActiveView, setSelectedLessonId, setActiveAssessmentId } = useAuth();

  const handleActionClick = () => {
    if (nextAction.action_type === 'START_ASSESSMENT') {
      setActiveAssessmentId('ASS-DEMO-PRACTICAL-001');
      setActiveView('learning');
    } else {
      setSelectedLessonId('sampling-lesson-3');
      setActiveView('learning');
    }
  };

  return (
    <div style={{
      background: 'linear-gradient(135deg, #1a365d 0%, #0f294a 100%)',
      color: '#ffffff',
      borderRadius: 'var(--radius-lg)',
      padding: '32px',
      boxShadow: 'var(--shadow-lg)',
      position: 'relative',
      overflow: 'hidden',
      borderLeft: '6px solid #d97706'
    }}>
      {/* Subtle decorative watermark */}
      <div style={{
        position: 'absolute',
        right: '-20px',
        bottom: '-20px',
        fontSize: '120px',
        fontWeight: 900,
        opacity: 0.04,
        userSelect: 'none',
        pointerEvents: 'none',
        fontFamily: 'var(--font-heading)'
      }}>
        ACTION
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
        <div style={{ maxWidth: '680px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
            <span style={{
              backgroundColor: '#d97706',
              color: '#ffffff',
              padding: '3px 10px',
              borderRadius: '999px',
              fontSize: '11px',
              fontWeight: 800,
              letterSpacing: '0.04em',
              textTransform: 'uppercase'
            }}>
              {nextAction.badge_label || 'RECOMMENDED NEXT STEP'}
            </span>
            <span style={{ color: '#93c5fd', fontSize: '13px', fontWeight: 600 }}>
              Competency: {nextAction.competency_label}
            </span>
          </div>

          <h2 style={{ color: '#ffffff', fontSize: '24px', fontWeight: 800, marginBottom: '8px' }}>
            {nextAction.title}
          </h2>
          <p style={{ color: '#cbd5e1', fontSize: '15px', lineHeight: 1.5, margin: 0 }}>
            {nextAction.subtitle}
          </p>
        </div>

        <div>
          <button
            className="btn btn-primary"
            onClick={handleActionClick}
            style={{
              padding: '14px 28px',
              fontSize: '16px',
              fontWeight: 700,
              boxShadow: '0 4px 14px rgba(217, 119, 6, 0.4)'
            }}
          >
            {nextAction.button_label} →
          </button>
        </div>
      </div>
    </div>
  );
};
