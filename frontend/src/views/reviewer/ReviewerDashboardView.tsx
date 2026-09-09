import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { ReviewQueueItemDTO } from '../../types';
import { ReviewModal } from '../../components/ReviewModal';
import { useReveal } from '../../hooks/useReveal';

const RefreshIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M21 12a9 9 0 1 1-2.64-6.36" />
    <polyline points="21 3 21 9 15 9" />
  </svg>
);

const BigCheckIcon: React.FC = () => (
  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="10" />
    <polyline points="8 12.5 11 15.5 16 9.5" />
  </svg>
);

export const ReviewerDashboardView: React.FC = () => {
  const [queue, setQueue] = useState<ReviewQueueItemDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState<ReviewQueueItemDTO | null>(null);
  const queueReveal = useReveal<HTMLDivElement>();

  const loadQueue = async () => {
    setLoading(true);
    try {
      const data = await api.getReviewQueue();
      setQueue(data);
    } catch (err) {
      console.error('Failed to load review queue:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadQueue();
  }, []);

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* Header */}
      <div style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px', flexWrap: 'wrap' }}>
          <span className="badge badge-saffron">Lead Assessor Authority</span>
          <span style={{ fontSize: '13px', color: 'var(--color-text-muted)' }}>National Sample Survey Office (NSSO)</span>
        </div>
        <h1 className="page-title">Supervisor Evidence Evaluation Queue</h1>
        <p className="meta-line">
          Review practical task evidence and authorize official competency level promotions. Max 1 level promotion per approved assessment.
        </p>
      </div>

      {/* Review Queue Summary Banner */}
      <div className="gov-card static" style={{
        padding: '20px 24px',
        marginBottom: '28px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        <div style={{ display: 'flex', gap: '32px', flexWrap: 'wrap' }}>
          <div>
            <div className="readiness-label">
              Submissions Awaiting Verification
            </div>
            <div className="stat-chip" style={{ boxShadow: 'none', padding: '4px 0', background: 'transparent' }}>
              <div className="stat-value" style={{ fontSize: '26px', color: queue.length > 0 ? 'var(--orange-700)' : 'var(--color-success)' }}>
                {queue.length} Pending
              </div>
            </div>
          </div>
          <div>
            <div className="readiness-label">
              Evaluation Rubric Version
            </div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--blue-500)', marginTop: '8px' }}>
              sampling-practical-demo-v1
            </div>
          </div>
        </div>

        <button className="btn btn-secondary btn-sm" onClick={loadQueue}>
          <RefreshIcon /> Refresh Queue
        </button>
      </div>

      {/* Queue Items */}
      {loading ? (
        <div style={{ padding: '60px', textAlign: 'center' }}>
          <div style={{ fontSize: '16px', color: 'var(--color-text-strong)' }}>Loading evaluation queue...</div>
        </div>
      ) : queue.length === 0 ? (
        <div className="gov-card static" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <div style={{ color: 'var(--color-success)', marginBottom: '12px', display: 'inline-block' }}><BigCheckIcon /></div>
          <h3 style={{ fontSize: '20px', color: '#146B1A', marginBottom: '6px' }}>
            Assessment Queue is All Caught Up
          </h3>
          <p style={{ color: 'var(--color-text-muted)', fontSize: '14px', maxWidth: '520px', margin: '0 auto' }}>
            There are no pending practical submissions waiting for evaluation. When learners submit assessments in the learning portal, they will appear here for review.
          </p>
        </div>
      ) : (
        <div ref={queueReveal} className="reveal" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {queue.map(item => (
            <div
              key={item.submission_id}
              className="queue-card"
              style={{
                flexDirection: 'row',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '20px'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px', flexWrap: 'wrap' }}>
                  <span className="badge badge-saffron">PENDING REVIEW</span>
                  <span style={{ fontSize: '12px', color: 'var(--color-text-muted)' }}>
                    Submitted: {new Date(item.submitted_at).toLocaleDateString()}
                  </span>
                </div>

                <h3 style={{ fontSize: '18px' }}>
                  {item.learner_name} ({item.user_id})
                </h3>

                <div style={{ fontSize: '14px', color: 'var(--color-text-primary)', marginTop: '4px' }}>
                  Competency: <strong>{item.competency_label}</strong> ({item.competency_id})
                </div>

                <div style={{ display: 'flex', gap: '20px', fontSize: '13px', color: 'var(--color-text-muted)', marginTop: '8px', flexWrap: 'wrap' }}>
                  <span>Current: <strong>Level {item.current_level}</strong></span>
                  <span>Evaluated Target: <strong style={{ color: '#146B1A' }}>Level {item.proposed_level}</strong></span>
                  <span>Score: <strong style={{ color: 'var(--blue-600)' }}>{item.overall_score}%</strong></span>
                  <span>Confidence: <strong>{Math.round(item.confidence * 100)}%</strong></span>
                </div>
              </div>

              <div>
                <button
                  className="btn btn-primary"
                  onClick={() => setSelectedItem(item)}
                >
                  Evaluate Evidence & Rubric →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Review Modal Dialog */}
      {selectedItem && (
        <ReviewModal
          item={selectedItem}
          onClose={() => setSelectedItem(null)}
          onDecisionComplete={() => {
            loadQueue();
            setSelectedItem(null);
          }}
        />
      )}
    </div>
  );
};
