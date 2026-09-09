import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { AdminDashboardMetrics, LearnerAdminListItem } from '../../types';
import { useReveal } from '../../hooks/useReveal';

const RefreshIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M21 12a9 9 0 1 1-2.64-6.36" />
    <polyline points="21 3 21 9 15 9" />
  </svg>
);

const PlusIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.8" strokeLinecap="round" aria-hidden="true">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const CheckIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

export const AdminDashboardView: React.FC = () => {
  const [metrics, setMetrics] = useState<AdminDashboardMetrics | null>(null);
  const [learners, setLearners] = useState<LearnerAdminListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'learners' | 'content' | 'sync'>('learners');
  const metricsReveal = useReveal<HTMLDivElement>();

  // New Learner Form
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [regName, setRegName] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regDesignation, setRegDesignation] = useState('Statistical Assistant');
  const [regMsg, setRegMsg] = useState<string | null>(null);

  // Sync state
  const [syncing, setSyncing] = useState(false);
  const [syncMsg, setSyncMsg] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const [m, l] = await Promise.all([
        api.getAdminDashboard(),
        api.getAdminLearners()
      ]);
      setMetrics(m);
      setLearners(l);
    } catch (err) {
      console.error('Failed to load admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.registerLearner({
        name: regName,
        email: regEmail,
        designation: regDesignation,
        division_id: 'DIV-001',
        position_id: 'POS-001',
        target_position_id: 'POS-002',
        experience_years: 2
      });
      setRegMsg(res.message);
      loadData();
      setTimeout(() => {
        setShowRegisterModal(false);
        setRegMsg(null);
        setRegName('');
        setRegEmail('');
      }, 1500);
    } catch (err: any) {
      setRegMsg(err.message || 'Registration failed');
    }
  };

  const handleTriggerSync = async () => {
    setSyncing(true);
    setSyncMsg(null);
    try {
      const res = await api.triggerIgotSync();
      setSyncMsg(res.message);
      loadData();
    } catch (err: any) {
      setSyncMsg(err.message || 'Sync failed');
    } finally {
      setSyncing(false);
    }
  };

  const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '10px',
    borderRadius: 'var(--radius-sm)',
    border: '1px solid var(--color-border)',
    fontSize: '14px',
    fontFamily: 'var(--font-sans)',
    background: 'var(--color-bg-surface)'
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '12px',
    fontWeight: 700,
    color: 'var(--color-text-secondary)',
    display: 'block',
    marginBottom: '4px'
  };

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '28px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <span className="badge badge-navy">System Administration & Oversight</span>
          <h1 className="page-title" style={{ marginTop: '8px' }}>
            MoSPI Cadre Competency Governance
          </h1>
          <p className="meta-line">
            National Statistical System officer profiling, curriculum catalog management, and iGOT integration simulator controls.
          </p>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => setShowRegisterModal(true)}
        >
          <PlusIcon /> Register New Officer
        </button>
      </div>

      {/* Metrics Row */}
      {metrics && (
        <div ref={metricsReveal} className="reveal">
          <div className="grid-3" style={{ marginBottom: '32px' }}>
            <div className="stat-chip">
              <div className="stat-label">Total Registered Officers</div>
              <div className="stat-value">{metrics.total_learners}</div>
              <div className="section-sub" style={{ fontSize: '12px' }}>Full MoSPI cadre registry imported from dataset.</div>
            </div>

            <div className="stat-chip">
              <div className="stat-label" style={{ color: 'var(--orange-700)' }}>Priority Gap Backlog</div>
              <div className="stat-value" style={{ color: 'var(--orange-700)' }}>{metrics.learners_with_critical_gaps}</div>
              <div className="section-sub" style={{ fontSize: '12px' }}>Officers currently requiring guided development.</div>
            </div>

            <div className="stat-chip">
              <div className="stat-label" style={{ color: '#146B1A' }}>Curated Playlists & Lessons</div>
              <div className="stat-value" style={{ color: 'var(--color-success)' }}>
                {metrics.content_curated_playlists} <span style={{ fontSize: '16px' }}>({metrics.total_lessons} Lessons)</span>
              </div>
              <div className="section-sub" style={{ fontSize: '12px' }}>Mapped to 32 Official Statistical Competencies.</div>
            </div>
          </div>
        </div>
      )}

      {/* Admin Tabs */}
      <div style={{ borderBottom: '1px solid var(--color-border)', display: 'flex', gap: '16px', marginBottom: '24px' }}>
        <button
          className={`nav-tab ${activeTab === 'learners' ? 'active' : ''}`}
          onClick={() => setActiveTab('learners')}
        >
          Officer Registry ({learners.length})
        </button>
        <button
          className={`nav-tab ${activeTab === 'sync' ? 'active' : ''}`}
          onClick={() => setActiveTab('sync')}
        >
          iGOT Integration Simulator
        </button>
      </div>

      {/* Tab Content: Officer Registry */}
      {activeTab === 'learners' && (
        <div className="gov-card static" style={{ overflowX: 'auto', padding: '0' }}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>User ID</th>
                <th>Officer Name</th>
                <th>Designation</th>
                <th>Division</th>
                <th>Readiness Status</th>
                <th>Target Gaps</th>
              </tr>
            </thead>
            <tbody>
              {learners.map(u => (
                <tr key={u.user_id}>
                  <td style={{ fontFamily: 'monospace', fontWeight: 700, color: 'var(--blue-600)' }}>{u.user_id}</td>
                  <td style={{ fontWeight: 700, color: 'var(--color-text-strong)' }}>{u.name}</td>
                  <td>{u.designation}</td>
                  <td>{u.division_name}</td>
                  <td>
                    <span className={`badge ${u.readiness_status === 'READY' ? 'badge-green' : u.readiness_status === 'NEAR_READY' ? 'badge-navy' : 'badge-saffron'}`} style={{ fontSize: '10px' }}>
                      {u.readiness_status}
                    </span>
                  </td>
                  <td style={{ fontWeight: 700, color: u.priority_gaps_count > 0 ? 'var(--color-danger)' : 'var(--color-success)' }}>
                    {u.target_gaps_count} Gaps ({u.priority_gaps_count} High)
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab Content: iGOT Integration Simulator */}
      {activeTab === 'sync' && (
        <div className="gov-card static">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '16px' }}>
            <div>
              <span className="badge badge-saffron">Provider Abstraction Control</span>
              <h3 style={{ fontSize: '18px', marginTop: '4px' }}>
                iGOT Karmayogi Course & Training Record Synchronization
              </h3>
              <p className="section-sub">
                Simulates bidirectional catalog synchronization with the national civil service LMS.
              </p>
            </div>

            <button
              className="btn btn-navy"
              disabled={syncing}
              onClick={handleTriggerSync}
            >
              <RefreshIcon /> {syncing ? 'Synchronizing...' : 'Trigger Simulated Catalog Sync'}
            </button>
          </div>

          {syncMsg && (
            <div className="promotion-banner" style={{ marginBottom: '20px' }}>
              <span className="promotion-banner-icon"><CheckIcon /></span>
              <span className="promotion-title">{syncMsg}</span>
            </div>
          )}

          <div style={{ padding: '18px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', fontSize: '13px', color: 'var(--color-text-primary)', lineHeight: 1.6 }}>
            <strong>Architecture Integrity Statement:</strong>
            <p style={{ marginTop: '6px' }}>
              Public iGOT API documentation and live production credentials are currently restricted to authorized ministry nodal officers.
              Our platform implements a clean provider interface (<code>BaseCourseProvider</code>) so that when official credentials become available,
              no frontend or engine logic will need to be rewritten.
            </p>
          </div>
        </div>
      )}

      {/* Registration Modal */}
      {showRegisterModal && (
        <div className="modal-overlay" onClick={() => setShowRegisterModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '540px' }}>
            <h2 style={{ fontSize: '20px', marginBottom: '16px' }}>
              Register Officer into Cadre System
            </h2>

            {regMsg && (
              <div style={{ padding: '12px', backgroundColor: 'var(--color-success-subtle)', color: '#146B1A', borderRadius: 'var(--radius-sm)', marginBottom: '16px', fontSize: '13px' }}>
                {regMsg}
              </div>
            )}

            <form onSubmit={handleRegister}>
              <div style={{ marginBottom: '14px' }}>
                <label style={labelStyle} htmlFor="reg-name">
                  Officer Full Name:
                </label>
                <input
                  id="reg-name"
                  type="text"
                  required
                  value={regName}
                  onChange={e => setRegName(e.target.value)}
                  placeholder="e.g. Smt. Vandana Sharma"
                  style={inputStyle}
                />
              </div>

              <div style={{ marginBottom: '14px' }}>
                <label style={labelStyle} htmlFor="reg-email">
                  Government Email:
                </label>
                <input
                  id="reg-email"
                  type="email"
                  required
                  value={regEmail}
                  onChange={e => setRegEmail(e.target.value)}
                  placeholder="e.g. vandana.sharma@mospi.gov.in"
                  style={inputStyle}
                />
              </div>

              <div style={{ marginBottom: '20px' }}>
                <label style={labelStyle} htmlFor="reg-designation">
                  Designation:
                </label>
                <select
                  id="reg-designation"
                  value={regDesignation}
                  onChange={e => setRegDesignation(e.target.value)}
                  style={inputStyle}
                >
                  <option value="Junior Statistical Officer">Junior Statistical Officer</option>
                  <option value="Statistical Assistant">Statistical Assistant</option>
                  <option value="Data Processing Assistant">Data Processing Assistant</option>
                  <option value="Field Investigator">Field Investigator</option>
                </select>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowRegisterModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Establish Officer Profile →
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
