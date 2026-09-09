import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { LearnerDashboardResponse } from '../../types';
import { OneNextActionCard } from '../../components/OneNextActionCard';
import { SkillGapCard } from '../../components/SkillGapCard';

interface ProfileCompetency {
  competency_id: string;
  label: string;
  current_level: number | null;
  level_label: string;
  required_level: number | null;
  gap_status: string | null;
}

interface LearnerProfile {
  user_id: string;
  name: string;
  designation: string;
  division: string;
  current_position_name: string;
  target_position_name: string;
  official_competencies: ProfileCompetency[];
  recent_promotions: ProfileCompetency[];
}

export const LearnerHomeView: React.FC = () => {
  const { currentUser, setActiveView } = useAuth();
  const [dashboard, setDashboard] = useState<LearnerDashboardResponse | null>(null);
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      setLoading(true);
      try {
        const [data, me] = await Promise.all([
          api.getDashboard(currentUser?.user_id),
          api.getLearnerProfile(currentUser?.user_id)
        ]);
        setDashboard(data);
        setProfile(me);
      } catch (err) {
        console.error('Failed to load dashboard:', err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboard();
  }, [currentUser]);

  if (loading) {
    return (
      <div className="gov-container" style={{ padding: '60px 0', textAlign: 'center' }}>
        <div style={{ fontSize: '18px', fontWeight: 600, color: '#1a365d' }}>Loading your personalized learning plan...</div>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="gov-container" style={{ padding: '40px 0' }}>
        <p>Could not retrieve dashboard data.</p>
      </div>
    );
  }

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* Officer Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px', marginBottom: '28px' }}>
        <div>
          <span style={{ fontSize: '12px', fontWeight: 700, color: '#d97706', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            Officer Competency Journey
          </span>
          <h1 style={{ fontSize: '28px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
            {dashboard.greeting}
          </h1>
          <div style={{ fontSize: '14px', color: '#475569', marginTop: '4px' }}>
            Current Role: <strong style={{ color: '#0f172a' }}>{dashboard.current_role}</strong>
            <span style={{ margin: '0 8px', color: '#cbd5e1' }}>•</span>
            Target Role: <strong style={{ color: '#d97706' }}>{dashboard.target_role}</strong>
          </div>
        </div>

        {/* Readiness Badge */}
        <div style={{
          padding: '12px 18px',
          backgroundColor: '#ffffff',
          borderRadius: 'var(--radius-md)',
          border: '1px solid #e2e8f0',
          boxShadow: 'var(--shadow-sm)',
          textAlign: 'right'
        }}>
          <div style={{ fontSize: '11px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>
            Learning Readiness Status
          </div>
          <div style={{ fontSize: '16px', fontWeight: 800, color: '#1a365d', marginTop: '2px' }}>
            {dashboard.readiness_status.replace(/_/g, ' ')}
          </div>
        </div>
      </div>

      {/* 0. OFFICIAL COMPETENCY PROFILE (updates when a supervisor approves an assessment) */}
      {profile && profile.official_competencies && profile.official_competencies.length > 0 && (
        <div style={{ marginBottom: '36px' }}>
          {profile.recent_promotions && profile.recent_promotions.length > 0 && (
            <div style={{
              display: 'flex', alignItems: 'center', gap: '12px',
              padding: '14px 18px', marginBottom: '16px',
              backgroundColor: '#f0fdf4', border: '1px solid #bbf7d0',
              borderRadius: 'var(--radius-md)'
            }}>
              <span style={{ fontSize: '24px' }}>🏅</span>
              <div>
                <div style={{ fontSize: '14px', fontWeight: 800, color: '#166534' }}>
                  Official Competency Upgraded: {profile.recent_promotions[0].label}
                </div>
                <div style={{ fontSize: '12px', color: '#15803d' }}>
                  Supervisor-verified promotion to <strong>{profile.recent_promotions[0].level_label}</strong> — your official MoSPI registry record has been updated.
                </div>
              </div>
            </div>
          )}

          <div className="gov-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
              <div>
                <h2 style={{ fontSize: '18px', fontWeight: 800, color: '#1a365d', margin: 0 }}>
                  Official Competency Levels
                </h2>
                <p style={{ fontSize: '12px', color: '#64748b', margin: '2px 0 0' }}>
                  Verified levels in the MoSPI registry. Levels change only through supervisor-approved assessments.
                </p>
              </div>
              <span style={{ fontSize: '11px', color: '#64748b' }}>
                Target: <strong style={{ color: '#d97706' }}>{profile.target_position_name}</strong>
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(210px, 1fr))', gap: '10px' }}>
              {profile.official_competencies.map(c => {
                const met = c.required_level !== null && c.current_level !== null && c.current_level >= c.required_level;
                const pct = c.required_level ? Math.min(100, Math.round(((c.current_level || 0) / c.required_level) * 100)) : null;
                return (
                  <div key={c.competency_id} style={{
                    padding: '12px', borderRadius: '8px',
                    backgroundColor: met ? '#f0fdf4' : '#f8fafc',
                    border: met ? '1px solid #bbf7d0' : '1px solid #e2e8f0'
                  }}>
                    <div style={{ fontSize: '12px', fontWeight: 700, color: '#0f172a', marginBottom: '6px', lineHeight: 1.25 }}>
                      {c.label}
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                      <span style={{ fontSize: '15px', fontWeight: 800, color: met ? '#166534' : '#1a365d' }}>
                        {c.level_label}
                      </span>
                      {c.required_level !== null && (
                        <span style={{ fontSize: '11px', color: '#64748b' }}>
                          needs L{c.required_level}
                        </span>
                      )}
                    </div>
                    {pct !== null && (
                      <div style={{ height: '4px', backgroundColor: '#e2e8f0', borderRadius: '2px', marginTop: '8px', overflow: 'hidden' }}>
                        <div style={{
                          height: '100%', width: `${pct}%`,
                          backgroundColor: met ? '#16a34a' : '#d97706',
                          borderRadius: '2px', transition: 'width 0.6s ease'
                        }} />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* 1. PRIMARY ONE NEXT ACTION */}
      <div style={{ marginBottom: '36px' }}>
        <OneNextActionCard nextAction={dashboard.next_action} />
      </div>

      {/* 2. PRIORITY SKILL GAPS */}
      <div style={{ marginBottom: '40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#1a365d' }}>
              Priority Skills to Strengthen
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
              Identified by comparing your current verified evidence against {dashboard.target_role} requirements.
            </p>
          </div>

          <button
            className="btn btn-secondary"
            onClick={() => setActiveView('gaps')}
            style={{ fontSize: '13px', minHeight: '36px', padding: '6px 14px' }}
          >
            View All Gaps ({dashboard.total_gaps_count}) →
          </button>
        </div>

        <div className="grid-3">
          {dashboard.priority_gaps.map(gap => (
            <SkillGapCard key={gap.gap_id} gap={gap} />
          ))}
        </div>
      </div>

      {/* 3. LEARNING PATHWAY PROGRESSION */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <div>
            <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#1a365d' }}>
              Your Structured Learning Journey
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
              Step-by-step career path progression from foundation concepts to verified practical assessments.
            </p>
          </div>

          <button
            className="btn btn-secondary"
            onClick={() => setActiveView('career')}
            style={{ fontSize: '13px', minHeight: '36px', padding: '6px 14px' }}
          >
            View Full Pathway →
          </button>
        </div>

        <div className="gov-card">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {dashboard.learning_path_preview.map((item, idx) => (
              <div
                key={item.path_item_id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '16px',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  backgroundColor: idx === 0 ? '#f0fdf4' : '#f8fafc',
                  border: idx === 0 ? '1px solid #bbf7d0' : '1px solid #e2e8f0'
                }}
              >
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  backgroundColor: idx === 0 ? '#166534' : '#cbd5e1',
                  color: '#ffffff',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '13px'
                }}>
                  {item.sequence_no}
                </div>

                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className={`badge ${idx === 0 ? 'badge-green' : 'badge-gray'}`} style={{ fontSize: '10px' }}>
                      {item.stage}
                    </span>
                    <span style={{ fontSize: '14px', fontWeight: 700, color: '#0f172a' }}>
                      {item.action_label}
                    </span>
                  </div>
                  <div style={{ fontSize: '12px', color: '#64748b', marginTop: '2px' }}>
                    Competency: {item.competency_label} {item.course_title ? `• Course: ${item.course_title}` : ''}
                  </div>
                </div>

                <div>
                  <button
                    className={`btn ${idx === 0 ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setActiveView('learning')}
                    style={{ fontSize: '12px', minHeight: '32px', padding: '6px 14px' }}
                  >
                    {idx === 0 ? 'Start Now →' : 'View Module'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
