import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { CompetencyGapItem } from '../../types';
import { SkillGapCard } from '../../components/SkillGapCard';

export const SkillGapsView: React.FC = () => {
  const { currentUser } = useAuth();
  const [gaps, setGaps] = useState<CompetencyGapItem[]>([]);
  const [scope, setScope] = useState<'TARGET' | 'CURRENT'>('TARGET');
  const [filterStatus, setFilterStatus] = useState<string>('ALL');
  const [loading, setLoading] = useState(true);

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
        <span style={{ fontSize: '12px', fontWeight: 700, color: '#d97706', textTransform: 'uppercase' }}>
          Diagnostic & Cadre Evaluation
        </span>
        <h1 style={{ fontSize: '28px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
          Official Competency Gap Analysis
        </h1>
        <p style={{ fontSize: '14px', color: '#64748b', marginTop: '4px' }}>
          Gaps are derived deterministically by calculating unmet proficiency levels: <code>max(required_level - supported_level, 0)</code>.
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid-3" style={{ marginBottom: '32px' }}>
        <div className="gov-card" style={{ borderLeft: '4px solid #dc2626' }}>
          <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>Priority Gaps (High)</div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#dc2626', marginTop: '6px' }}>{highCount}</div>
          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>Unmet gap ≥ 2 levels. Structured training required.</div>
        </div>

        <div className="gov-card" style={{ borderLeft: '4px solid #d97706' }}>
          <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>Moderate Gaps (Medium)</div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#d97706', marginTop: '6px' }}>{mediumCount}</div>
          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>Unmet gap = 1 level. Practice and assessment recommended.</div>
        </div>

        <div className="gov-card" style={{ borderLeft: '4px solid #166534' }}>
          <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>Requirements Satisfied</div>
          <div style={{ fontSize: '28px', fontWeight: 800, color: '#166534', marginTop: '6px' }}>{metCount}</div>
          <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>Demonstrated evidence meets or exceeds target level.</div>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 20px',
        backgroundColor: '#ffffff',
        borderRadius: 'var(--radius-md)',
        border: '1px solid #e2e8f0',
        marginBottom: '28px',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '13px', fontWeight: 700, color: '#475569' }}>Evaluation Scope:</span>
          <button
            className={`btn ${scope === 'TARGET' ? 'btn-navy' : 'btn-secondary'}`}
            onClick={() => setScope('TARGET')}
            style={{ fontSize: '12px', minHeight: '34px', padding: '6px 14px' }}
          >
            Target Role Requirements (Supervisory)
          </button>
          <button
            className={`btn ${scope === 'CURRENT' ? 'btn-navy' : 'btn-secondary'}`}
            onClick={() => setScope('CURRENT')}
            style={{ fontSize: '12px', minHeight: '34px', padding: '6px 14px' }}
          >
            Current Role Requirements
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '13px', fontWeight: 700, color: '#475569' }}>Filter:</span>
          {['ALL', 'HIGH', 'MEDIUM', 'NO_GAP'].map(status => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              style={{
                padding: '6px 12px',
                borderRadius: '6px',
                border: filterStatus === status ? '1px solid #1a365d' : '1px solid #cbd5e1',
                backgroundColor: filterStatus === status ? '#ebf8ff' : '#ffffff',
                color: filterStatus === status ? '#1a365d' : '#475569',
                fontSize: '12px',
                fontWeight: filterStatus === status ? 700 : 500,
                cursor: 'pointer'
              }}
            >
              {status === 'ALL' ? 'All Skills' : status.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Gaps Grid */}
      {loading ? (
        <div style={{ padding: '60px', textAlign: 'center' }}>
          <div style={{ fontSize: '16px', color: '#1a365d' }}>Loading competency gap matrix...</div>
        </div>
      ) : filteredGaps.length === 0 ? (
        <div style={{ padding: '60px', textAlign: 'center', backgroundColor: '#ffffff', borderRadius: '12px' }}>
          <p style={{ color: '#64748b' }}>No competency gaps match the selected filter.</p>
        </div>
      ) : (
        <div className="grid-3">
          {filteredGaps.map(g => (
            <SkillGapCard key={g.gap_id} gap={g} />
          ))}
        </div>
      )}
    </div>
  );
};
