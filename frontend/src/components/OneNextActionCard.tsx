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
      background: 'linear-gradient(135deg, var(--ink-500) 0%, var(--blue-900) 100%)',
      color: '#FFFFFF',
      borderRadius: 'var(--radius-lg)',
      padding: '32px',
      boxShadow: 'var(--shadow-elevated)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
        <div style={{ maxWidth: '680px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px', flexWrap: 'wrap' }}>
            <span style={{
              backgroundColor: 'var(--orange-500)',
              color: 'var(--color-on-orange)',
              padding: '3px 10px',
              borderRadius: 'var(--radius-full)',
              fontSize: '11px',
              fontWeight: 800,
              letterSpacing: '0.04em',
              textTransform: 'uppercase',
              fontFamily: 'var(--font-sans)'
            }}>
              {nextAction.badge_label || 'RECOMMENDED NEXT STEP'}
            </span>
            <span style={{ color: 'var(--blue-100)', fontSize: '13px', fontWeight: 700 }}>
              Competency: {nextAction.competency_label}
            </span>
          </div>

          <h2 style={{ color: '#FFFFFF', fontSize: '24px', marginBottom: '8px' }}>
            {nextAction.title}
          </h2>
          <p style={{ color: 'var(--ink-100)', fontSize: '15px', lineHeight: 1.5, margin: 0 }}>
            {nextAction.subtitle}
          </p>
        </div>

        <div>
          <button
            className="btn btn-primary"
            onClick={handleActionClick}
            style={{
              padding: '14px 28px',
              fontSize: '16px'
            }}
          >
            {nextAction.button_label} →
          </button>
        </div>
      </div>
    </div>
  );
};
