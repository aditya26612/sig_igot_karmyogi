import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { AdminDashboardMetrics, LearnerAdminListItem } from '../../types';

export const AdminDashboardView: React.FC = () => {
  const [metrics, setMetrics] = useState<AdminDashboardMetrics | null>(null);
  const [learners, setLearners] = useState<LearnerAdminListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'learners' | 'content' | 'sync'>('learners');

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

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '28px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <span className="badge badge-navy">System Administration & Oversight</span>
          <h1 style={{ fontSize: '28px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
            MoSPI Cadre Competency Governance
          </h1>
          <p style={{ fontSize: '14px', color: '#64748b', marginTop: '4px' }}>
            National Statistical System officer profiling, curriculum catalog management, and iGOT integration simulator controls.
          </p>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => setShowRegisterModal(true)}
          style={{ padding: '10px 20px', fontSize: '14px' }}
        >
          + Register New Officer
        </button>
      </div>

      {/* Metrics Row */}
      {metrics && (
        <div className="grid-3" style={{ marginBottom: '32px' }}>
          <div className="gov-card" style={{ borderLeft: '4px solid #1a365d' }}>
            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>Total Registered Officers</div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>{metrics.total_learners}</div>
            <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>Full MoSPI cadre registry imported from dataset.</div>
          </div>

          <div className="gov-card" style={{ borderLeft: '4px solid #d97706' }}>
            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>Priority Gap Backlog</div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: '#d97706', marginTop: '4px' }}>{metrics.learners_with_critical_gaps}</div>
            <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>Officers currently requiring guided development.</div>
          </div>

          <div className="gov-card" style={{ borderLeft: '4px solid #166534' }}>
            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>Curated Playlists & Lessons</div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: '#166534', marginTop: '4px' }}>
              {metrics.content_curated_playlists} ({metrics.total_lessons} Lessons)
            </div>
            <div style={{ fontSize: '12px', color: '#64748b', marginTop: '4px' }}>Mapped to 32 Official Statistical Competencies.</div>
          </div>
        </div>
      )}

      {/* Admin Tabs */}
      <div style={{ borderBottom: '1px solid #e2e8f0', display: 'flex', gap: '16px', marginBottom: '24px' }}>
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
        <div className="gov-card" style={{ overflowX: 'auto', padding: '0' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
            <thead>
              <tr style={{ backgroundColor: '#f8fafc', borderBottom: '2px solid #e2e8f0', color: '#475569' }}>
                <th style={{ padding: '14px 18px', fontWeight: 700 }}>User ID</th>
                <th style={{ padding: '14px 18px', fontWeight: 700 }}>Officer Name</th>
                <th style={{ padding: '14px 18px', fontWeight: 700 }}>Designation</th>
                <th style={{ padding: '14px 18px', fontWeight: 700 }}>Division</th>
                <th style={{ padding: '14px 18px', fontWeight: 700 }}>Readiness Status</th>
                <th style={{ padding: '14px 18px', fontWeight: 700 }}>Target Gaps</th>
              </tr>
            </thead>
            <tbody>
              {learners.map((u, i) => (
                <tr key={u.user_id} style={{ borderBottom: '1px solid #f1f5f9', backgroundColor: i % 2 === 0 ? '#ffffff' : '#fcfcfd' }}>
                  <td style={{ padding: '12px 18px', fontFamily: 'monospace', fontWeight: 700, color: '#1a365d' }}>{u.user_id}</td>
                  <td style={{ padding: '12px 18px', fontWeight: 700, color: '#0f172a' }}>{u.name}</td>
                  <td style={{ padding: '12px 18px', color: '#475569' }}>{u.designation}</td>
                  <td style={{ padding: '12px 18px', color: '#475569' }}>{u.division_name}</td>
                  <td style={{ padding: '12px 18px' }}>
                    <span className={`badge ${u.readiness_status === 'READY' ? 'badge-green' : u.readiness_status === 'NEAR_READY' ? 'badge-navy' : 'badge-saffron'}`} style={{ fontSize: '10px' }}>
                      {u.readiness_status}
                    </span>
                  </td>
                  <td style={{ padding: '12px 18px', fontWeight: 700, color: u.priority_gaps_count > 0 ? '#dc2626' : '#166534' }}>
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
        <div className="gov-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <span className="badge badge-saffron">Provider Abstraction Control</span>
              <h3 style={{ fontSize: '18px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
                iGOT Karmayogi Course & Training Record Synchronization
              </h3>
              <p style={{ fontSize: '13px', color: '#64748b', marginTop: '2px' }}>
                Simulates bidirectional catalog synchronization with the national civil service LMS.
              </p>
            </div>

            <button
              className="btn btn-primary"
              disabled={syncing}
              onClick={handleTriggerSync}
              style={{ backgroundColor: '#1a365d' }}
            >
              {syncing ? 'Synchronizing...' : '↻ Trigger Simulated Catalog Sync'}
            </button>
          </div>

          {syncMsg && (
            <div style={{ padding: '14px', backgroundColor: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '8px', color: '#166534', fontSize: '13px', marginBottom: '20px' }}>
              ✓ {syncMsg}
            </div>
          )}

          <div style={{ padding: '18px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '13px', color: '#334155', lineHeight: 1.6 }}>
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
            <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#1a365d', marginBottom: '16px' }}>
              Register Officer into Cadre System
            </h2>

            {regMsg && (
              <div style={{ padding: '12px', backgroundColor: '#f0fdf4', color: '#166534', borderRadius: '6px', marginBottom: '16px', fontSize: '13px' }}>
                {regMsg}
              </div>
            )}

            <form onSubmit={handleRegister}>
              <div style={{ marginBottom: '14px' }}>
                <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                  Officer Full Name:
                </label>
                <input
                  type="text"
                  required
                  value={regName}
                  onChange={e => setRegName(e.target.value)}
                  placeholder="e.g. Smt. Vandana Sharma"
                  style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px' }}
                />
              </div>

              <div style={{ marginBottom: '14px' }}>
                <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                  Government Email:
                </label>
                <input
                  type="email"
                  required
                  value={regEmail}
                  onChange={e => setRegEmail(e.target.value)}
                  placeholder="e.g. vandana.sharma@mospi.gov.in"
                  style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px' }}
                />
              </div>

              <div style={{ marginBottom: '20px' }}>
                <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                  Designation:
                </label>
                <select
                  value={regDesignation}
                  onChange={e => setRegDesignation(e.target.value)}
                  style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px' }}
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
