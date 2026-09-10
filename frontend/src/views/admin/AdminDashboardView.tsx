import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { api } from '../../api/client';
import { AdminDashboardMetrics, LearnerAdminListItem, ReviewQueueItemDTO, CuratedPlaylistDTO } from '../../types';
import { ReviewModal } from '../../components/ReviewModal';
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

const XIcon: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.8" strokeLinecap="round" aria-hidden="true">
    <line x1="5" y1="5" x2="19" y2="19" />
    <line x1="19" y1="5" x2="5" y2="19" />
  </svg>
);

type AdminTab = 'learners' | 'analytics' | 'backlog' | 'questions' | 'content' | 'sync' | 'audit';

interface QuestionReviewItem {
  question_id: string;
  lesson_id?: string;
  question_text: string;
  difficulty: string;
  is_approved: number | boolean;
  review_status: string;
}

interface AuditLogItem {
  log_id: string;
  actor_id: string;
  action: string;
  entity_type: string;
  entity_id: string;
  details: string;
  timestamp: string;
}

export const AdminDashboardView: React.FC = () => {
  const { t } = useTranslation();
  const [metrics, setMetrics] = useState<AdminDashboardMetrics | null>(null);
  const [learners, setLearners] = useState<LearnerAdminListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<AdminTab>('learners');
  const metricsReveal = useReveal<HTMLDivElement>();

  // New Learner Form
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [regName, setRegName] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regDesignation, setRegDesignation] = useState('Statistical Assistant');
  const [regMsg, setRegMsg] = useState<string | null>(null);

  // Backlog (reuses reviewer queue)
  const [backlog, setBacklog] = useState<ReviewQueueItemDTO[]>([]);
  const [backlogLoading, setBacklogLoading] = useState(false);
  const [backlogItem, setBacklogItem] = useState<ReviewQueueItemDTO | null>(null);

  // Question review
  const [questions, setQuestions] = useState<QuestionReviewItem[]>([]);
  const [questionFilter, setQuestionFilter] = useState<'ALL' | 'APPROVED' | 'PENDING' | 'REJECTED'>('ALL');
  const [questionSearch, setQuestionSearch] = useState('');
  const [questionsLoading, setQuestionsLoading] = useState(false);

  // Content management
  const [playlists, setPlaylists] = useState<CuratedPlaylistDTO[]>([]);
  const [playlistsLoading, setPlaylistsLoading] = useState(false);
  const [upLessonId, setUpLessonId] = useState('');
  const [upTopic, setUpTopic] = useState('');
  const [upTimestamp, setUpTimestamp] = useState('00:00');
  const [upStart, setUpStart] = useState('0');
  const [upEnd, setUpEnd] = useState('300');
  const [upText, setUpText] = useState('');
  const [uploadMsg, setUploadMsg] = useState<string | null>(null);

  // Audit logs
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  const [auditLoading, setAuditLoading] = useState(false);

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

  const loadBacklog = async () => {
    setBacklogLoading(true);
    try {
      const q = await api.getReviewQueue();
      setBacklog(q);
    } catch (err) {
      console.error('Failed to load backlog:', err);
    } finally {
      setBacklogLoading(false);
    }
  };

  const loadQuestions = async () => {
    setQuestionsLoading(true);
    try {
      const q = await api.getQuestionsForReview();
      setQuestions(q);
    } catch (err) {
      console.error('Failed to load questions:', err);
    } finally {
      setQuestionsLoading(false);
    }
  };

  const loadContent = async () => {
    setPlaylistsLoading(true);
    try {
      const p = await api.getPlaylistsAdmin();
      setPlaylists(p);
    } catch (err) {
      console.error('Failed to load playlists:', err);
    } finally {
      setPlaylistsLoading(false);
    }
  };

  const loadAuditLogs = async () => {
    setAuditLoading(true);
    try {
      const logs = await api.getAuditLogs(50);
      setAuditLogs(logs);
    } catch (err) {
      console.error('Failed to load audit logs:', err);
    } finally {
      setAuditLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Lazy-load tab data on first visit of each tab
  useEffect(() => {
    if (activeTab === 'backlog' && backlog.length === 0 && !backlogLoading) loadBacklog();
    if (activeTab === 'questions' && questions.length === 0 && !questionsLoading) loadQuestions();
    if (activeTab === 'content' && playlists.length === 0 && !playlistsLoading) loadContent();
    if (activeTab === 'audit' && auditLogs.length === 0 && !auditLoading) loadAuditLogs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab]);

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
      loadAuditLogs();
    } catch (err: any) {
      setSyncMsg(err.message || 'Sync failed');
    } finally {
      setSyncing(false);
    }
  };

  const handleQuestionDecision = async (questionId: string, approved: boolean) => {
    const status = approved ? 'APPROVED' : 'REJECTED';
    try {
      await api.reviewQuestion(questionId, approved, status);
      setQuestions(prev => prev.map(q =>
        q.question_id === questionId ? { ...q, is_approved: approved, review_status: status } : q
      ));
    } catch (err) {
      console.error('Failed to review question:', err);
    }
  };

  const handleUploadTranscript = async (e: React.FormEvent) => {
    e.preventDefault();
    setUploadMsg(null);
    try {
      await api.uploadTranscript({
        lesson_id: upLessonId,
        topic: upTopic,
        text_content: upText,
        timestamp_label: upTimestamp,
        start_seconds: Number(upStart) || 0,
        end_seconds: Number(upEnd) || 300
      });
      setUploadMsg(t('admin.uploaded'));
      setUpLessonId(''); setUpTopic(''); setUpText('');
      loadAuditLogs();
    } catch (err: any) {
      setUploadMsg(err.message || 'Upload failed');
    }
  };

  const filteredQuestions = questions.filter(q => {
    const statusOk =
      questionFilter === 'ALL' ? true :
      questionFilter === 'APPROVED' ? q.review_status === 'APPROVED' :
      questionFilter === 'REJECTED' ? q.review_status === 'REJECTED' :
      q.review_status === 'PENDING' || !q.review_status;
    const searchOk = !questionSearch ||
      q.question_text.toLowerCase().includes(questionSearch.toLowerCase()) ||
      q.question_id.toLowerCase().includes(questionSearch.toLowerCase());
    return statusOk && searchOk;
  });

  const divisionData = metrics?.division_gap_breakdown || {};
  const maxDivGaps = Math.max(1, ...Object.values(divisionData));

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

  const TABS: { id: AdminTab; label: string }[] = [
    { id: 'learners', label: `${t('admin.registry')} (${learners.length})` },
    { id: 'analytics', label: t('admin.analytics') },
    { id: 'backlog', label: `${t('admin.backlog')} (${metrics?.assessment_backlog ?? 0})` },
    { id: 'questions', label: t('admin.questions') },
    { id: 'content', label: t('admin.content') },
    { id: 'sync', label: t('admin.integration') },
    { id: 'audit', label: t('admin.audit') },
  ];

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '28px', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <span className="badge badge-navy">{t('admin.badge')}</span>
          <h1 className="page-title" style={{ marginTop: '8px' }}>
            {t('admin.pageTitle')}
          </h1>
          <p className="meta-line">
            {t('admin.pageHint')}
          </p>
        </div>

        <button
          className="btn btn-primary"
          onClick={() => setShowRegisterModal(true)}
        >
          <PlusIcon /> {t('admin.registerNew')}
        </button>
      </div>

      {/* Metrics Row */}
      {metrics && (
        <div ref={metricsReveal} className="reveal">
          <div className="grid-3" style={{ marginBottom: '32px' }}>
            <div className="stat-chip">
              <div className="stat-label">{t('admin.totalOfficers')}</div>
              <div className="stat-value">{metrics.total_learners}</div>
              <div className="section-sub" style={{ fontSize: '12px' }}>{t('admin.totalOfficersHint')}</div>
            </div>

            <div className="stat-chip">
              <div className="stat-label" style={{ color: 'var(--orange-700)' }}>{t('admin.criticalGaps')}</div>
              <div className="stat-value" style={{ color: 'var(--orange-700)' }}>{metrics.learners_with_critical_gaps}</div>
              <div className="section-sub" style={{ fontSize: '12px' }}>{t('admin.backlogHintMetric')}</div>
            </div>

            <div className="stat-chip">
              <div className="stat-label" style={{ color: '#146B1A' }}>{t('admin.playlists')}</div>
              <div className="stat-value" style={{ color: 'var(--color-success)' }}>
                {metrics.content_curated_playlists} <span style={{ fontSize: '16px' }}>({metrics.total_lessons} {t('admin.lessons')})</span>
              </div>
              <div className="section-sub" style={{ fontSize: '12px' }}>{t('admin.curatedHint')}</div>
            </div>
          </div>
        </div>
      )}

      {/* Admin Tabs */}
      <div style={{ borderBottom: '1px solid var(--color-border)', display: 'flex', gap: '16px', marginBottom: '24px', overflowX: 'auto' }}>
        {TABS.map(tab => (
          <button
            key={tab.id}
            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
            style={{ whiteSpace: 'nowrap' }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab: Officer Registry */}
      {activeTab === 'learners' && (
        <div className="gov-card static" style={{ overflowX: 'auto', padding: '0' }}>
          <table className="admin-table">
            <thead>
              <tr>
                <th>User ID</th>
                <th>{t('admin.officer')}</th>
                <th>{t('admin.designation')}</th>
                <th>{t('admin.division')}</th>
                <th>{t('admin.readiness')}</th>
                <th>{t('admin.gaps')}</th>
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
                    {t('admin.gapsCount', { count: u.target_gaps_count, high: u.priority_gaps_count })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab: Division Analytics (CSS bar charts from existing metrics) */}
      {activeTab === 'analytics' && (
        <div className="gov-card static">
          <span className="badge badge-navy">{t('admin.analytics')}</span>
          <h3 style={{ fontSize: '18px', marginTop: '6px' }}>{t('admin.divisionGapBreakdown')}</h3>
          <p className="section-sub">{t('admin.backlogHintMetric')}</p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '20px' }}>
            {Object.entries(divisionData).length === 0 ? (
              <p className="section-sub">—</p>
            ) : Object.entries(divisionData).sort((a, b) => b[1] - a[1]).map(([div, count]) => (
              <div key={div}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: 700, marginBottom: '4px' }}>
                  <span>{div}</span>
                  <span style={{ color: count / maxDivGaps > 0.66 ? 'var(--color-danger)' : 'var(--orange-700)' }}>{count}</span>
                </div>
                <div style={{ height: '10px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-full)', overflow: 'hidden' }}>
                  <div style={{
                    height: '100%',
                    width: `${Math.max(4, (count / maxDivGaps) * 100)}%`,
                    borderRadius: 'var(--radius-full)',
                    background: count / maxDivGaps > 0.66
                      ? 'linear-gradient(90deg, var(--color-danger), #E4593F)'
                      : 'linear-gradient(90deg, var(--orange-500), var(--orange-600))',
                    transition: 'width 0.4s ease'
                  }} />
                </div>
              </div>
            ))}
          </div>

          <div style={{ marginTop: '24px', padding: '14px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', display: 'flex', gap: '12px', alignItems: 'center', fontSize: '13px' }}>
            <strong style={{ color: 'var(--orange-700)', fontSize: '22px' }}>{metrics?.assessment_backlog ?? 0}</strong>
            <span style={{ color: 'var(--color-text-secondary)' }}>{t('admin.backlogCount')}</span>
          </div>
        </div>
      )}

      {/* Tab: Assessment Backlog (governance — reuses reviewer endpoints) */}
      {activeTab === 'backlog' && (
        <div className="gov-card static">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
            <div>
              <span className="badge badge-saffron">{t('admin.backlog')}</span>
              <h3 style={{ fontSize: '18px', marginTop: '6px' }}>{t('admin.backlogHint')}</h3>
            </div>
            <button className="btn btn-secondary btn-sm" onClick={loadBacklog}>
              <RefreshIcon /> {t('review.refresh')}
            </button>
          </div>

          {backlogLoading ? (
            <p className="section-sub">{t('common.loading')}</p>
          ) : backlog.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <div style={{ color: 'var(--color-success)', display: 'inline-block', marginBottom: '8px' }}><CheckIcon /></div>
              <p className="section-sub">{t('admin.backlogEmpty')}</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {backlog.map(item => (
                <div key={item.submission_id} className="admin-backlog-row">
                  <div style={{ flex: 1, minWidth: '220px' }}>
                    <strong style={{ color: 'var(--color-text-strong)' }}>{item.learner_name}</strong>
                    <span style={{ fontFamily: 'monospace', fontSize: '12px', color: 'var(--blue-600)', marginLeft: '6px' }}>{item.user_id}</span>
                    <div style={{ fontSize: '12px', color: 'var(--color-text-muted)', marginTop: '2px' }}>
                      {item.competency_label} • {t('assessment.levelTo', { from: item.current_level, to: item.proposed_level })} • {item.overall_score}%
                    </div>
                  </div>
                  <button className="btn btn-primary btn-sm" onClick={() => setBacklogItem(item)}>
                    {t('review.evaluate')}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Tab: Question Review Console */}
      {activeTab === 'questions' && (
        <div className="gov-card static">
          <span className="badge badge-navy">{t('admin.questionBank')}</span>
          <h3 style={{ fontSize: '18px', marginTop: '6px' }}>{t('admin.questionBankHint')}</h3>

          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap', margin: '14px 0' }}>
            <input
              type="text"
              placeholder={t('admin.searchQuestions')}
              value={questionSearch}
              onChange={e => setQuestionSearch(e.target.value)}
              style={{ ...inputStyle, maxWidth: '280px' }}
              aria-label={t('admin.searchQuestions')}
            />
            {(['ALL', 'APPROVED', 'PENDING', 'REJECTED'] as const).map(f => (
              <button
                key={f}
                onClick={() => setQuestionFilter(f)}
                style={{
                  padding: '6px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border: questionFilter === f ? '1px solid var(--blue-500)' : '1px solid var(--color-border)',
                  backgroundColor: questionFilter === f ? 'var(--blue-50)' : 'var(--color-bg-surface)',
                  color: questionFilter === f ? 'var(--blue-600)' : 'var(--color-text-secondary)',
                  fontSize: '12px',
                  fontWeight: questionFilter === f ? 700 : 500,
                  cursor: 'pointer'
                }}
              >
                {f === 'ALL' ? t('admin.all') : f === 'APPROVED' ? t('admin.approved') : f === 'PENDING' ? t('admin.pending') : t('admin.rejected')}
              </button>
            ))}
          </div>

          {questionsLoading ? (
            <p className="section-sub">{t('common.loading')}</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '480px', overflowY: 'auto', paddingRight: '4px' }}>
              {filteredQuestions.map(q => (
                <div key={q.question_id} className="admin-question-row">
                  <div style={{ flex: 1, minWidth: '240px' }}>
                    <div style={{ display: 'flex', gap: '6px', alignItems: 'center', flexWrap: 'wrap', marginBottom: '4px' }}>
                      <span style={{ fontFamily: 'monospace', fontSize: '11px', color: 'var(--blue-600)', fontWeight: 700 }}>{q.question_id}</span>
                      <span className={`badge ${q.difficulty === 'HARD' ? 'badge-danger' : q.difficulty === 'MEDIUM' ? 'badge-saffron' : 'badge-green'}`} style={{ fontSize: '9px' }}>
                        {q.difficulty}
                      </span>
                      <span className={`badge ${q.review_status === 'APPROVED' ? 'badge-green' : q.review_status === 'REJECTED' ? 'badge-danger' : 'badge-gray'}`} style={{ fontSize: '9px' }}>
                        {q.review_status || 'PENDING'}
                      </span>
                    </div>
                    <div style={{ fontSize: '13px', color: 'var(--color-text-primary)', lineHeight: 1.45 }}>
                      {q.question_text}
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '6px', flex: 'none' }}>
                    <button
                      className={`btn btn-sm ${q.review_status === 'APPROVED' ? 'btn-success' : 'btn-secondary'}`}
                      onClick={() => handleQuestionDecision(q.question_id, true)}
                      disabled={q.review_status === 'APPROVED'}
                      title={t('admin.approve')}
                    >
                      <CheckIcon /> {t('admin.approve')}
                    </button>
                    <button
                      className="btn btn-sm btn-secondary"
                      onClick={() => handleQuestionDecision(q.question_id, false)}
                      disabled={q.review_status === 'REJECTED'}
                      title={t('admin.reject')}
                      style={{ color: q.review_status === 'REJECTED' ? 'var(--color-danger)' : undefined }}
                    >
                      <XIcon /> {t('admin.reject')}
                    </button>
                  </div>
                </div>
              ))}
              {filteredQuestions.length === 0 && (
                <p className="section-sub">—</p>
              )}
            </div>
          )}
        </div>
      )}

      {/* Tab: Content Management */}
      {activeTab === 'content' && (
        <div className="gov-card static">
          <span className="badge badge-navy">{t('admin.content')}</span>
          <h3 style={{ fontSize: '18px', marginTop: '6px' }}>{t('admin.contentRegistry')}</h3>
          <p className="section-sub">{t('admin.contentHint')} — {t('admin.playlistsCount', { count: playlists.length, lessons: metrics?.total_lessons ?? 0 })}</p>

          {playlistsLoading ? (
            <p className="section-sub">{t('common.loading')}</p>
          ) : (
            <div style={{ overflowX: 'auto', marginTop: '14px' }}>
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>{t('admin.playlistCol')}</th>
                    <th>{t('admin.lessonsCol')}</th>
                    <th>{t('admin.competencyCol')}</th>
                    <th>{t('admin.providerCol')}</th>
                  </tr>
                </thead>
                <tbody>
                  {playlists.map(p => (
                    <tr key={p.playlist_id}>
                      <td style={{ fontWeight: 700, color: 'var(--color-text-strong)' }}>{p.title.split('&')[0].trim()}</td>
                      <td>{p.total_lessons}</td>
                      <td style={{ fontFamily: 'monospace', fontSize: '12px' }}>{p.competency_id}</td>
                      <td>{p.provider_badge || 'YouTube'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Transcript upload */}
          <div style={{ marginTop: '24px', padding: '18px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)' }}>
            <div style={{ fontSize: '15px', fontWeight: 700, color: 'var(--color-text-strong)', marginBottom: '12px' }}>
              {t('admin.uploadTranscript')}
            </div>
            {uploadMsg && (
              <div style={{ padding: '10px 12px', backgroundColor: 'var(--color-success-subtle)', color: '#146B1A', borderRadius: 'var(--radius-sm)', marginBottom: '12px', fontSize: '13px' }}>
                {uploadMsg}
              </div>
            )}
            <form onSubmit={handleUploadTranscript}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', marginBottom: '12px' }}>
                <div>
                  <label style={labelStyle} htmlFor="up-lesson">{t('admin.lessonId')}</label>
                  <input id="up-lesson" type="text" required value={upLessonId} onChange={e => setUpLessonId(e.target.value)} style={inputStyle} placeholder="sampling-lesson-3" />
                </div>
                <div>
                  <label style={labelStyle} htmlFor="up-topic">{t('admin.topic')}</label>
                  <input id="up-topic" type="text" required value={upTopic} onChange={e => setUpTopic(e.target.value)} style={inputStyle} placeholder="…" />
                </div>
                <div>
                  <label style={labelStyle} htmlFor="up-ts">{t('admin.timestamp')}</label>
                  <input id="up-ts" type="text" value={upTimestamp} onChange={e => setUpTimestamp(e.target.value)} style={inputStyle} placeholder="MM:SS" />
                </div>
                <div>
                  <label style={labelStyle} htmlFor="up-start">{t('admin.startSeconds')}</label>
                  <input id="up-start" type="number" value={upStart} onChange={e => setUpStart(e.target.value)} style={inputStyle} />
                </div>
                <div>
                  <label style={labelStyle} htmlFor="up-end">{t('admin.endSeconds')}</label>
                  <input id="up-end" type="number" value={upEnd} onChange={e => setUpEnd(e.target.value)} style={inputStyle} />
                </div>
              </div>
              <div style={{ marginBottom: '14px' }}>
                <label style={labelStyle} htmlFor="up-text">{t('admin.textContent')}</label>
                <textarea id="up-text" required rows={3} value={upText} onChange={e => setUpText(e.target.value)} style={{ ...inputStyle, resize: 'vertical', lineHeight: 1.5 }} />
              </div>
              <button type="submit" className="btn btn-primary">
                {t('admin.upload')}
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Tab: iGOT Integration Simulator */}
      {activeTab === 'sync' && (
        <div className="gov-card static">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '16px' }}>
            <div>
              <span className="badge badge-saffron">{t('admin.syncBadge')}</span>
              <h3 style={{ fontSize: '18px', marginTop: '4px' }}>
                {t('admin.syncTitle')}
              </h3>
              <p className="section-sub">
                {t('admin.syncHint')}
              </p>
            </div>

            <button
              className="btn btn-navy"
              disabled={syncing}
              onClick={handleTriggerSync}
            >
              <RefreshIcon /> {syncing ? t('admin.syncing') : t('admin.triggerSyncBtn')}
            </button>
          </div>

          {syncMsg && (
            <div className="promotion-banner" style={{ marginBottom: '20px' }}>
              <span className="promotion-banner-icon"><CheckIcon /></span>
              <span className="promotion-title">{syncMsg}</span>
            </div>
          )}

          <div style={{ padding: '18px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', fontSize: '13px', color: 'var(--color-text-primary)', lineHeight: 1.6 }}>
            <strong>{t('admin.architectureNote')}</strong>
            <p style={{ marginTop: '6px' }}>
              {t('admin.architectureBody')}
            </p>
          </div>
        </div>
      )}

      {/* Tab: Audit Log Viewer */}
      {activeTab === 'audit' && (
        <div className="gov-card static">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
            <div>
              <span className="badge badge-navy">{t('admin.auditLogBadge')}</span>
              <h3 style={{ fontSize: '18px', marginTop: '6px' }}>{t('admin.auditHint')}</h3>
            </div>
            <button className="btn btn-secondary btn-sm" onClick={loadAuditLogs}>
              <RefreshIcon /> {t('review.refresh')}
            </button>
          </div>

          {auditLoading ? (
            <p className="section-sub">{t('common.loading')}</p>
          ) : auditLogs.length === 0 ? (
            <p className="section-sub">{t('admin.auditEmpty')}</p>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>{t('admin.time')}</th>
                    <th>{t('admin.actor')}</th>
                    <th>{t('admin.action')}</th>
                    <th>{t('admin.entityCol')}</th>
                    <th>{t('admin.details')}</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.map(log => (
                    <tr key={log.log_id}>
                      <td style={{ fontFamily: 'monospace', fontSize: '12px', whiteSpace: 'nowrap' }}>
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td style={{ fontFamily: 'monospace', fontSize: '12px', color: 'var(--blue-600)' }}>{log.actor_id}</td>
                      <td>
                        <span className={`badge ${log.action.includes('APPROVED') ? 'badge-green' : log.action.includes('REJECT') ? 'badge-danger' : 'badge-gray'}`} style={{ fontSize: '9px' }}>
                          {log.action}
                        </span>
                      </td>
                      <td style={{ fontFamily: 'monospace', fontSize: '11px' }}>{log.entity_type}</td>
                      <td style={{ fontSize: '12.5px', maxWidth: '340px' }}>{log.details}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Registration Modal */}
      {showRegisterModal && (
        <div className="modal-overlay" onClick={() => setShowRegisterModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '540px' }}>
            <h2 style={{ fontSize: '20px', marginBottom: '16px' }}>
              {t('admin.registerTitle')}
            </h2>

            {regMsg && (
              <div style={{ padding: '12px', backgroundColor: 'var(--color-success-subtle)', color: '#146B1A', borderRadius: 'var(--radius-sm)', marginBottom: '16px', fontSize: '13px' }}>
                {regMsg}
              </div>
            )}

            <form onSubmit={handleRegister}>
              <div style={{ marginBottom: '14px' }}>
                <label style={labelStyle} htmlFor="reg-name">
                  {t('admin.nameLabel')}
                </label>
                <input
                  id="reg-name"
                  type="text"
                  required
                  value={regName}
                  onChange={e => setRegName(e.target.value)}
                  placeholder="…"
                  style={inputStyle}
                />
              </div>

              <div style={{ marginBottom: '14px' }}>
                <label style={labelStyle} htmlFor="reg-email">
                  {t('admin.emailLabel')}
                </label>
                <input
                  id="reg-email"
                  type="email"
                  required
                  value={regEmail}
                  onChange={e => setRegEmail(e.target.value)}
                  placeholder="…"
                  style={inputStyle}
                />
              </div>

              <div style={{ marginBottom: '20px' }}>
                <label style={labelStyle} htmlFor="reg-designation">
                  {t('admin.designationLabel')}
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
                  {t('common.cancel')}
                </button>
                <button type="submit" className="btn btn-primary">
                  {t('admin.establishProfile')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Backlog review modal (reuses reviewer ReviewModal) */}
      {backlogItem && (
        <ReviewModal
          item={backlogItem}
          onClose={() => setBacklogItem(null)}
          onDecisionComplete={() => {
            loadBacklog();
            loadData();
            setBacklogItem(null);
          }}
        />
      )}
    </div>
  );
};
