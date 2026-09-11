import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { CompetencyGapItem } from '../../types';
import { SkillGapCard } from '../../components/SkillGapCard';
import { useReveal } from '../../hooks/useReveal';

export const SkillGapsView: React.FC = () => {
  const { currentUser } = useAuth();
  const { t } = useTranslation();
  const [gaps, setGaps] = useState<CompetencyGapItem[]>([]);
  const [scope, setScope] = useState<'TARGET' | 'CURRENT'>('TARGET');
  const [filterStatus, setFilterStatus] = useState<string>('ALL');
  const [loading, setLoading] = useState(true);
  const summaryReveal = useReveal<HTMLDivElement>();
  const gridReveal = useReveal<HTMLDivElement>();

  useEffect(() => {
    async function loadGaps() {
      setLoading(true);
      try {
        const data = await api.getGaps(scope, currentUser?.user_id);
        setGaps(data);
      } catch (err) {
        console.error('Failed to load gaps:', err);
      } finally {
        setLoading(false);
      }
    }
    loadGaps();
  }, [scope, currentUser]);

  const filteredGaps = gaps.filter(g => {
    if (filterStatus === 'ALL') return true;
    if (filterStatus === 'HIGH') return g.gap_status === 'HIGH';
    if (filterStatus === 'MEDIUM') return g.gap_status === 'MEDIUM';
    if (filterStatus === 'NO_GAP') return g.gap_status === 'NO_GAP';
    return true;
  });

  const highCount = gaps.filter(g => g.gap_status === 'HIGH').length;
  const mediumCount = gaps.filter(g => g.gap_status === 'MEDIUM').length;
  const metCount = gaps.filter(g => g.gap_status === 'NO_GAP').length;

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* Header */}
      <div style={{ marginBottom: '28px' }}>
        <span className="eyebrow-meta">{t('gaps.eyebrow')}</span>
        <h1 className="page-title">{t('gaps.title')}</h1>
        <p className="meta-line">
          {t('gaps.hint')}
        </p>
      </div>

      {/* Summary Cards */}
      <div ref={summaryReveal} className="reveal">
        <div className="grid-3" style={{ marginBottom: '32px' }}>
          <div className="stat-chip" style={{ borderTop: 'none' }}>
            <div className="stat-label" style={{ color: 'var(--color-danger)' }}>{t('gaps.highCardLabel')}</div>
            <div className="stat-value" style={{ color: 'var(--color-danger)' }}>{highCount}</div>
            <div className="section-sub" style={{ fontSize: '12px' }}>{t('gaps.highCardHint')}</div>
          </div>

          <div className="stat-chip">
            <div className="stat-label" style={{ color: 'var(--orange-700)' }}>{t('gaps.mediumCardLabel')}</div>
            <div className="stat-value" style={{ color: 'var(--orange-700)' }}>{mediumCount}</div>
            <div className="section-sub" style={{ fontSize: '12px' }}>{t('gaps.mediumCardHint')}</div>
          </div>

          <div className="stat-chip">
            <div className="stat-label" style={{ color: '#146B1A' }}>{t('gaps.metCardLabel')}</div>
            <div className="stat-value" style={{ color: 'var(--color-success)' }}>{metCount}</div>
            <div className="section-sub" style={{ fontSize: '12px' }}>{t('gaps.metCardHint')}</div>
          </div>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 20px',
        backgroundColor: 'var(--color-bg-surface)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--color-border)',
        marginBottom: '28px',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-secondary)' }}>{t('gaps.evaluationScope')}</span>
          <button
            className={`btn btn-sm ${scope === 'TARGET' ? 'btn-navy' : 'btn-secondary'}`}
            onClick={() => setScope('TARGET')}
          >
            {t('gaps.targetRoleReq')}
          </button>
          <button
            className={`btn btn-sm ${scope === 'CURRENT' ? 'btn-navy' : 'btn-secondary'}`}
            onClick={() => setScope('CURRENT')}
          >
            {t('gaps.currentRoleReq')}
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-secondary)' }}>{t('gaps.filterLabel')}</span>
          {['ALL', 'HIGH', 'MEDIUM', 'NO_GAP'].map(status => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              style={{
                padding: '6px 12px',
                borderRadius: 'var(--radius-sm)',
                border: filterStatus === status ? '1px solid var(--blue-500)' : '1px solid var(--color-border)',
                backgroundColor: filterStatus === status ? 'var(--blue-50)' : 'var(--color-bg-surface)',
                color: filterStatus === status ? 'var(--blue-600)' : 'var(--color-text-secondary)',
                fontSize: '12px',
                fontWeight: filterStatus === status ? 700 : 500,
                fontFamily: 'var(--font-sans)',
                cursor: 'pointer'
              }}
            >
              {status === 'ALL' ? t('gaps.allSkills') : status.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Gaps Grid */}
      {loading ? (
        <div style={{ padding: '60px', textAlign: 'center' }}>
          <div style={{ fontSize: '16px', color: 'var(--color-text-strong)' }}>{t('gaps.loadingMatrix')}</div>
        </div>
      ) : filteredGaps.length === 0 ? (
        <div className="gov-card" style={{ padding: '60px', textAlign: 'center' }}>
          <p className="section-sub">{t('gaps.noMatch')}</p>
        </div>
      ) : (
        <div ref={gridReveal} className="reveal grid-3">
          {filteredGaps.map(g => (
            <SkillGapCard key={g.gap_id} gap={g} />
          ))}
        </div>
      )}
    </div>
  );
};
