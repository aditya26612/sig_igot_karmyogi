import React, { useState, useEffect } from 'react';
import { api } from '../../api/client';
import { ReviewQueueItemDTO } from '../../types';
import { ReviewModal } from '../../components/ReviewModal';

export const ReviewerDashboardView: React.FC = () => {
  const [queue, setQueue] = useState<ReviewQueueItemDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedItem, setSelectedItem] = useState<ReviewQueueItemDTO | null>(null);

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
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <span className="badge badge-saffron">Lead Assessor Authority</span>
          <span style={{ fontSize: '13px', color: '#64748b' }}>National Sample Survey Office (NSSO)</span>
        </div>
        <h1 style={{ fontSize: '28px', fontWeight: 800, color: '#1a365d' }}>
          Supervisor Evidence Evaluation Queue
        </h1>
        <p style={{ fontSize: '14px', color: '#64748b', marginTop: '4px' }}>
          Review practical task evidence and authorize official competency level promotions. Max 1 level promotion per approved assessment.
        </p>
      </div>

      {/* Review Queue Summary Banner */}
      <div style={{
        padding: '20px 24px',
        backgroundColor: '#ffffff',
        borderRadius: 'var(--radius-md)',
        border: '1px solid #e2e8f0',
        marginBottom: '28px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <div style={{ display: 'flex', gap: '32px' }}>
          <div>
            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>
              Submissions Awaiting Verification
            </div>
            <div style={{ fontSize: '26px', fontWeight: 800, color: queue.length > 0 ? '#d97706' : '#166534', marginTop: '4px' }}>
              {queue.length} Pending
            </div>
          </div>
          <div>
            <div style={{ fontSize: '12px', color: '#64748b', textTransform: 'uppercase', fontWeight: 700 }}>
              Evaluation Rubric Version
            </div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#1a365d', marginTop: '8px' }}>
              sampling-practical-demo-v1
            </div>
          </div>
        </div>

        <button className="btn btn-secondary" onClick={loadQueue} style={{ fontSize: '13px', minHeight: '36px' }}>
          ↻ Refresh Queue
        </button>
      </div>

      {/* Queue Items */}
      {loading ? (
        <div style={{ padding: '60px', textAlign: 'center' }}>
          <div style={{ fontSize: '16px', color: '#1a365d' }}>Loading evaluation queue...</div>
        </div>
      ) : queue.length === 0 ? (
        <div className="gov-card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <div style={{ fontSize: '40px', marginBottom: '12px' }}>✓</div>
          <h3 style={{ fontSize: '20px', fontWeight: 800, color: '#166534', marginBottom: '6px' }}>
            Assessment Queue is All Caught Up
          </h3>
          <p style={{ color: '#64748b', fontSize: '14px', maxWidth: '520px', margin: '0 auto' }}>
            There are no pending practical submissions waiting for evaluation. When learners submit assessments in the learning portal, they will appear here for review.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {queue.map(item => (
            <div
              key={item.submission_id}
              className="gov-card"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '20px',
                borderLeft: '6px solid #d97706'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                  <span className="badge badge-saffron">PENDING REVIEW</span>
                  <span style={{ fontSize: '12px', color: '#64748b' }}>
                    Submitted: {new Date(item.submitted_at).toLocaleDateString()}
                  </span>
                </div>

                <h3 style={{ fontSize: '18px', fontWeight: 800, color: '#1a365d' }}>
                  {item.learner_name} ({item.user_id})
                </h3>

                <div style={{ fontSize: '14px', color: '#334155', marginTop: '4px' }}>
                  Competency: <strong>{item.competency_label}</strong> ({item.competency_id})
                </div>

                <div style={{ display: 'flex', gap: '20px', fontSize: '13px', color: '#64748b', marginTop: '8px' }}>
                  <span>Current: <strong>Level {item.current_level}</strong></span>
                  <span>Evaluated Target: <strong style={{ color: '#166534' }}>Level {item.proposed_level}</strong></span>
                  <span>Score: <strong style={{ color: '#1e40af' }}>{item.overall_score}%</strong></span>
                  <span>Confidence: <strong>{Math.round(item.confidence * 100)}%</strong></span>
                </div>
              </div>

              <div>
                <button
                  className="btn btn-primary"
                  onClick={() => setSelectedItem(item)}
                  style={{ padding: '12px 24px', fontSize: '14px', fontWeight: 700 }}
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
