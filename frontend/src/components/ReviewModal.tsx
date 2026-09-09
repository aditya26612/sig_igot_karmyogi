import React, { useState } from 'react';
import { ReviewQueueItemDTO, ReviewDecisionResponse } from '../types';
import { api } from '../api/client';

interface ReviewModalProps {
  item: ReviewQueueItemDTO;
  onClose: () => void;
  onDecisionComplete: () => void;
}

export const ReviewModal: React.FC<ReviewModalProps> = ({ item, onClose, onDecisionComplete }) => {
  const [comments, setComments] = useState(
    "Verified practical sampling calculations against standard NSSO rubric. Frame allocation and design weights are completely accurate."
  );
  const [submitting, setSubmitting] = useState(false);
  const [decisionResult, setDecisionResult] = useState<ReviewDecisionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDecision = async (approved: boolean) => {
    setSubmitting(true);
    setError(null);
    try {
      const res = await api.submitReviewDecision(item.submission_id, approved, comments);
      setDecisionResult(res);
      onDecisionComplete();
    } catch (err: any) {
      setError(err.message || 'Failed to submit review decision.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '760px' }}>
        {!decisionResult ? (
          <div>
            <div style={{ borderBottom: '2px solid var(--color-border)', paddingBottom: '16px', marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="badge badge-saffron">Supervisor Evaluation Queue</span>
                <span style={{ fontSize: '12px', color: 'var(--color-text-muted)' }}>Rubric: {item.rubric_version}</span>
              </div>
              <h2 style={{ fontSize: '20px', fontWeight: 800, color: 'var(--blue-500)', marginTop: '6px' }}>
                Practical Evidence Review: {item.learner_name}
              </h2>
              <div style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                Officer ID: <strong>{item.user_id}</strong> | Competency: <strong>{item.competency_label}</strong> ({item.competency_id})
              </div>
            </div>

            {error && (
              <div style={{ padding: '12px', backgroundColor: 'var(--color-danger-subtle)', color: '#A82B1B', borderRadius: '6px', marginBottom: '16px', fontSize: '13px' }}>
                {error}
              </div>
            )}

            {/* Level Comparison Banner */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-around',
              padding: '16px',
              backgroundColor: 'var(--wash-ivory)',
              borderRadius: '8px',
              border: '1px solid var(--color-border)',
              marginBottom: '20px'
            }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>Current Level</div>
                <div style={{ fontSize: '20px', fontWeight: 800, color: 'var(--blue-500)' }}>Level {item.current_level}</div>
              </div>
              <div style={{ fontSize: '24px', color: 'var(--orange-500)', fontWeight: 700 }}>→</div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>Evaluated Target</div>
                <div style={{ fontSize: '20px', fontWeight: 800, color: '#146B1A' }}>Level {item.proposed_level}</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>Evidence Score</div>
                <div style={{ fontSize: '20px', fontWeight: 800, color: 'var(--blue-600)' }}>{item.overall_score}%</div>
              </div>
            </div>

            {/* Evidence Checklist */}
            <div style={{ padding: '16px', backgroundColor: 'var(--color-success-subtle)', borderRadius: '8px', border: '1px solid #BEE7C1', marginBottom: '20px' }}>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#146B1A', marginBottom: '8px' }}>
                Automated Rubric Pre-Check ({item.rubric_version}):
              </div>
              <div style={{ fontSize: '13px', color: '#1E7A24', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {item.rubric_version === 'sampling-practical-demo-v1' && (
                  <>
                    <div>✓ Task 1 Allocation: Proportional share matches population ratio (80 & 40 units).</div>
                    <div>✓ Task 2 Weighting: Correctly calculated reciprocal design weight (1 / 0.10 = 10).</div>
                  </>
                )}
                {item.rubric_version === 'sql-practical-demo-v1' && (
                  <>
                    <div>✓ Task 1 Join Semantics: FULL OUTER JOIN discrepancy filtering with NULL conditions verified.</div>
                    <div>✓ Task 2 Deduplication: ROW_NUMBER() PARTITION BY composite primary key properly isolated latest records.</div>
                  </>
                )}
                {item.rubric_version === 'quality-practical-demo-v1' && (
                  <>
                    <div>✓ Task 1 Outlier Screening: Accurate Tukey IQR fences (Q3 + 3.0*IQR = ₹156,000) isolating extreme anomaly.</div>
                    <div>✓ Task 2 Imputation & SDC: Well-specified donor classes and k-anonymity (k ≥ 5) disclosure defense verified.</div>
                  </>
                )}
                {item.rubric_version === 'python-practical-demo-v1' && (
                  <>
                    <div>✓ Task 1 Weighted Calculations: Vectorized Horvitz-Thompson weighted mean and Kish design effect formula verified.</div>
                    <div>✓ Task 2 Pipeline Auditing: Multi-stage assertion gates and Benford's first-digit validation rules formulated.</div>
                  </>
                )}
                <div>✓ Item Coverage: {Math.round(item.coverage * 100)}% | Confidence: {Math.round(item.confidence * 100)}%</div>
                <div>✓ Freshness Rule: Newer than previous evidence records.</div>
                <div>✓ Invariant: Maximum 1 level promotion upon approval (Level {item.current_level} → Level {item.proposed_level}).</div>
              </div>
            </div>

            {/* Supervisor Comments */}
            <div style={{ marginBottom: '24px' }}>
              <label style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-primary)', display: 'block', marginBottom: '6px' }}>
                Official Supervisor / Assessor Feedback:
              </label>
              <textarea
                rows={3}
                value={comments}
                onChange={e => setComments(e.target.value)}
                style={{ width: '100%', padding: '12px', borderRadius: '6px', border: '1px solid var(--color-border)', fontSize: '13px', lineHeight: 1.5 }}
              />
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--color-border)', paddingTop: '20px' }}>
              <button
                className="btn btn-secondary"
                disabled={submitting}
                onClick={onClose}
              >
                Cancel
              </button>

              <div style={{ display: 'flex', gap: '12px' }}>
                <button
                  className="btn"
                  disabled={submitting}
                  onClick={() => handleDecision(false)}
                  style={{ backgroundColor: 'var(--color-danger)', color: '#ffffff' }}
                >
                  Reject / Needs Practice
                </button>
                <button
                  className="btn btn-success"
                  disabled={submitting}
                  onClick={() => handleDecision(true)}
                  style={{ padding: '10px 24px' }}
                >
                  {submitting ? 'Promoting Level...' : '✓ Approve Level Promotion'}
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* Decision Success Screen */
          <div style={{ textAlign: 'center', padding: '24px 0' }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              backgroundColor: decisionResult.status === 'APPROVED' ? 'var(--color-success-subtle)' : 'var(--color-danger-subtle)',
              color: decisionResult.status === 'APPROVED' ? '#146B1A' : '#A82B1B',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px',
              marginBottom: '16px'
            }}>
              {decisionResult.status === 'APPROVED' ? '✓' : '✗'}
            </div>
            <h2 style={{ fontSize: '22px', fontWeight: 800, color: 'var(--blue-500)', marginBottom: '10px' }}>
              {decisionResult.status === 'APPROVED' ? 'Competency Level Successfully Promoted' : 'Assessment Marked as Needs Improvement'}
            </h2>
            <p style={{ fontSize: '14px', color: 'var(--color-text-secondary)', maxWidth: '580px', margin: '0 auto 20px auto', lineHeight: 1.6 }}>
              {decisionResult.message}
            </p>

            {decisionResult.level_promoted && (
              <div style={{ padding: '12px 20px', backgroundColor: 'var(--color-success-subtle)', borderRadius: '8px', border: '1px solid #BEE7C1', display: 'inline-block', marginBottom: '24px', fontSize: '14px', color: '#146B1A' }}>
                Official State Update: <strong>Level {decisionResult.before_level} → Level {decisionResult.after_level}</strong>
                <br />
                <span style={{ fontSize: '12px', color: '#1E7A24' }}>Target learning path and priority gaps recalculated automatically in real-time.</span>
              </div>
            )}

            <div>
              <button className="btn btn-navy" onClick={onClose}>
                Return to Review Queue
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
