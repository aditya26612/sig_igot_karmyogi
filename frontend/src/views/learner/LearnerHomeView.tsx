import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { LearnerDashboardResponse } from '../../types';
import { OneNextActionCard } from '../../components/OneNextActionCard';
import { SkillGapCard } from '../../components/SkillGapCard';
import { useReveal } from '../../hooks/useReveal';

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

const AwardIcon: React.FC = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <circle cx="12" cy="9" r="6" />
    <path d="M8.5 14L7 22l5-3 5 3-1.5-8" />
  </svg>
);

export const LearnerHomeView: React.FC = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [dashboard, setDashboard] = useState<LearnerDashboardResponse | null>(null);
  const [profile, setProfile] = useState<LearnerProfile | null>(null);
  const [loading, setLoading] = useState(true);

  const profileReveal = useReveal<HTMLDivElement>();
  const gapsReveal = useReveal<HTMLDivElement>();
  const journeyReveal = useReveal<HTMLDivElement>();

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
        <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--color-text-strong)' }}>{t('home.loadingDashboard')}</div>
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="gov-container" style={{ padding: '40px 0' }}>
        <p>{t('home.noData')}</p>
      </div>
    );
  }

  return (
    <div id="dashboard-top" className="gov-container" style={{ padding: '36px 0' }}>
      {/* Officer Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px', marginBottom: '28px' }}>
        <div>
          <span className="eyebrow-meta">{t('home.journeyBadge')}</span>
          <h1 className="page-title">{dashboard.greeting}</h1>
          <div className="meta-line">
            {t('home.currentRole')}: <strong className="strong-ink">{dashboard.current_role}</strong>
            <span style={{ margin: '0 8px', color: 'var(--color-border-strong)' }}>•</span>
            {t('home.targetRole')}: <strong className="strong-orange">{dashboard.target_role}</strong>
          </div>
        </div>

        {/* Readiness Badge */}
        <div className="readiness-chip">
          <div className="readiness-label">{t('home.readiness')}</div>
          <div className="readiness-value">{dashboard.readiness_status.replace(/_/g, ' ')}</div>
        </div>
      </div>

      {/* 0. OFFICIAL COMPETENCY PROFILE (updates when a supervisor approves an assessment) */}
      {profile && profile.official_competencies && profile.official_competencies.length > 0 && (
        <div style={{ marginBottom: '36px' }}>
          {profile.recent_promotions && profile.recent_promotions.length > 0 && (
            <div className="promotion-banner">
              <span className="promotion-banner-icon"><AwardIcon /></span>
              <div>
                <div className="promotion-title">
                  {t('home.upgraded', { name: profile.recent_promotions[0].label })}
                </div>
                <div className="promotion-sub">
                  {t('home.upgradedDetail', { level: profile.recent_promotions[0].level_label })}
                </div>
              </div>
            </div>
          )}

          <div ref={profileReveal} className="reveal">
            <div className="gov-card static" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '8px' }}>
                <div>
                  <h2 style={{ fontSize: '18px', margin: 0 }}>{t('home.competencyLevels')}</h2>
                  <p className="section-sub">
                    {t('home.competencyLevelsHint')}
                  </p>
                </div>
                <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
                  {t('home.target')}: <strong className="strong-orange">{profile.target_position_name}</strong>
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(210px, 1fr))', gap: '10px' }}>
                {profile.official_competencies.map(c => {
                  const met = c.required_level !== null && c.current_level !== null && c.current_level >= c.required_level;
                  const pct = c.required_level ? Math.min(100, Math.round(((c.current_level || 0) / c.required_level) * 100)) : null;
                  return (
                    <div key={c.competency_id} className={`competency-tile ${met ? 'met' : ''}`}>
                      <div className="competency-tile-label">{c.label}</div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                        <span className="competency-tile-level">{c.level_label}</span>
                        {c.required_level !== null && (
                          <span className="competency-tile-need">{t('home.needsLevel', { level: c.required_level })}</span>
                        )}
                      </div>
                      {pct !== null && (
                        <div className="mini-track">
                          <div className={`mini-fill ${met ? 'met' : ''}`} style={{ width: `${pct}%` }} />
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 1. PRIMARY ONE NEXT ACTION */}
      <div style={{ marginBottom: '36px' }}>
        <OneNextActionCard nextAction={dashboard.next_action} />
      </div>

      {/* 2. PRIORITY SKILL GAPS */}
      <div style={{ marginBottom: '40px' }} ref={gapsReveal} className="reveal">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '8px' }}>
          <div>
            <h2 className="section-heading">{t('home.prioritySkills')}</h2>
            <p className="section-sub">
              {t('home.prioritySkillsHint', { role: dashboard.target_role })}
            </p>
          </div>

          <button
            className="btn btn-secondary btn-sm"
            onClick={() => navigate('/gaps')}
          >
            {t('home.viewGaps', { count: dashboard.total_gaps_count })}
          </button>
        </div>

        <div className="grid-3">
          {dashboard.priority_gaps.map(gap => (
            <SkillGapCard key={gap.gap_id} gap={gap} />
          ))}
        </div>
      </div>

      {/* 3. LEARNING PATHWAY PROGRESSION */}
      <div ref={journeyReveal} className="reveal">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '8px' }}>
          <div>
            <h2 className="section-heading">{t('home.learningJourney')}</h2>
            <p className="section-sub">
              {t('home.learningJourneyHint')}
            </p>
          </div>

          <button
            className="btn btn-secondary btn-sm"
            onClick={() => navigate('/career')}
          >
            {t('home.viewPathway')}
          </button>
        </div>

        <div className="gov-card static">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {dashboard.learning_path_preview.map((item, idx) => (
              <div key={item.path_item_id} className={`journey-item ${idx === 0 ? 'current' : ''}`}>
                <div className="journey-node">{item.sequence_no}</div>

                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                    <span className={`badge ${idx === 0 ? 'badge-green' : 'badge-gray'}`} style={{ fontSize: '10px' }}>
                      {item.stage}
                    </span>
                    <span className="journey-label">{item.action_label}</span>
                  </div>
                  <div className="journey-meta">
                    {t('home.competency')}: {item.competency_label} {item.course_title ? `• ${t('home.course')}: ${item.course_title}` : ''}
                  </div>
                </div>

                <div>
                  <button
                    className={`btn btn-sm ${idx === 0 ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => navigate(`/learning?lesson=${encodeURIComponent('sampling-lesson-3')}`)}
                  >
                    {idx === 0 ? t('home.startNow') : t('home.viewModule')}
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
