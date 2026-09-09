import React, { useState, useEffect } from 'react';
import { AssessmentDetailDTO } from '../types';
import { api } from '../api/client';

interface AssessmentModalProps {
  assessmentId: string;
  onClose: () => void;
  onSubmitted?: () => void;
}

export const AssessmentModal: React.FC<AssessmentModalProps> = ({ assessmentId, onClose, onSubmitted }) => {
  const [detail, setDetail] = useState<AssessmentDetailDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const [stratumA, setStratumA] = useState('80');
  const [stratumB, setStratumB] = useState('40');
  const [designWeight, setDesignWeight] = useState('10');
  const [justification, setJustification] = useState('The design weight is the inverse of inclusion probability (1 / 0.10 = 10). Applying weights ensures each sampled unit represents 10 population units, avoiding bias.');
  const [task1Text, setTask1Text] = useState('');
  const [task2Text, setTask2Text] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadAssessment() {
      try {
        const data = await api.getAssessmentDetail(assessmentId);
        setDetail(data);
        if (data.assessment_id === 'ASS-DEMO-PRACTICAL-002') {
          setTask1Text("SELECT s.enterprise_id, s.name, t.gst_id\nFROM survey_est s\nFULL OUTER JOIN gst_reg t ON s.enterprise_id = t.enterprise_id\nWHERE s.enterprise_id IS NULL OR t.enterprise_id IS NULL;");
          setTask2Text("WITH RankedInterviews AS (\n  SELECT *,\n    ROW_NUMBER() OVER (PARTITION BY state_code, district_code, hh_id ORDER BY interview_timestamp DESC) as rn\n  FROM enumerated_schedules\n)\nSELECT * FROM RankedInterviews WHERE rn = 1;\n\n-- Technical Justification:\n-- Failing to wrap nullable expenditure in COALESCE(electricity_expenditure, 0) drops non-consuming households from aggregate stratum denominators, artificially inflating mean consumption.");
        } else if (data.assessment_id === 'ASS-DEMO-PRACTICAL-003') {
          setTask1Text("IQR = Q3 - Q1 = 48000 - 12000 = 36000\nMild outlier boundary = Q3 + 1.5 * IQR = 48000 + 54000 = ₹102,000\nExtreme outlier boundary = Q3 + 3.0 * IQR = 48000 + 108000 = ₹156,000\n\nIdentified Anomalies: Firms reporting ₹165,000 and ₹310,000 exceed the extreme boundary and must be flagged for field auditor inspection.");
          setTask2Text("Imputation Matching Classes: Class = (District_Code x Enterprise_Sector x Turnover_Quartile).\n\nSDC Justification: Microdata release enforces k-anonymity (k >= 5) on demographic quasi-identifiers (district, age group, gender) combined with top-coding top 1% wealth to prevent cross-register identity disclosure.");
        } else if (data.assessment_id === 'ASS-DEMO-PRACTICAL-004') {
          setTask1Text("Vectorized Horvitz-Thompson Weighted Mean:\nweighted_mean = (df['expenditure'] * df['weight']).sum() / df['weight'].sum()\n\nKish Design Effect Inflation Factor:\nDeff = 1 + (df['weight'].std() / df['weight'].mean()) ** 2\nDeff = 1 + (8.0 / 10.0) ** 2 = 1 + 0.64 = 1.64\nEffective sample size n_eff = 500 / 1.64 = 304.88");
          setTask2Text("Defensive Assertion Gate Pipeline:\nassert df['expenditure'].ge(0).all(), 'Negative expenditure detected'\nassert not df.duplicated(subset=['state_code', 'district_code', 'hh_id']).any(), 'Duplicate primary keys'\n\nEnumerator Fraud Audit: Compare empirical leading-digit distribution against Benford's Law (log10(1 + 1/d)) to detect curbstoning.");
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load assessment blueprint.');
      } finally {
        setLoading(false);
      }
    }
    loadAssessment();
  }, [assessmentId]);

  const handleSubmit = async () => {
    if (!detail) return;
    setSubmitting(true);
    try {
      const isSampling = detail.assessment_id === 'ASS-DEMO-PRACTICAL-001';
      const practicalWork = isSampling ? {
        task_1: {
          stratum_A_allocation: Number(stratumA),
          stratum_B_allocation: Number(stratumB),
          formula_used: "n_h = n * (N_h / N)"
        },
        task_2: {
          calculated_weight: Number(designWeight),
          justification: justification
        }
      } : {
        task_1: {
          submission_work: task1Text,
          expected_type: detail.tasks[0]?.expected_output_type || "TECHNICAL_WORK"
        },
        task_2: {
          submission_work: task2Text,
          expected_type: detail.tasks[1]?.expected_output_type || "WRITTEN_JUSTIFICATION"
        }
      };
      await api.submitAssessment(detail.assessment_id, detail.competency_id, practicalWork, 86.0);
      setSubmitted(true);
      if (onSubmitted) onSubmitted();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const isSampling = detail?.assessment_id === 'ASS-DEMO-PRACTICAL-001';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '820px' }}>
        {loading && (
          <div style={{ textAlign: 'center', padding: '48px' }}>
            <div style={{ fontSize: '18px', fontWeight: 600, color: '#1a365d' }}>Loading Official Assessment...</div>
          </div>
        )}

        {error && (
          <div style={{ textAlign: 'center', padding: '32px' }}>
            <h3 style={{ color: '#dc2626' }}>Assessment Error</h3>
            <p style={{ color: '#64748b', margin: '12px 0 20px 0' }}>{error}</p>
            <button className="btn btn-secondary" onClick={onClose}>Close</button>
          </div>
        )}

        {detail && !submitted && (
          <div>
            {/* Header */}
            <div style={{ borderBottom: '2px solid #e2e8f0', paddingBottom: '16px', marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <span className="badge badge-navy">Formal Cadre Assessment</span>
                <span className="badge badge-saffron">Rubric: {detail.rubric_version}</span>
              </div>
              <h2 style={{ fontSize: '22px', fontWeight: 800, color: '#1a365d' }}>
                {detail.title}
              </h2>
              <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#64748b', marginTop: '6px' }}>
                <span>Target: <strong>Level {detail.target_level} Proficiency</strong></span>
                <span>Current: <strong>Level {detail.current_level}</strong></span>
                <span>Time: <strong>{detail.estimated_time_minutes} mins</strong></span>
                <span>Auditor: <strong>Sunita Rao (NSSO Supervisor)</strong></span>
              </div>
              <div style={{
                marginTop: '10px',
                padding: '8px 12px',
                backgroundColor: '#eff6ff',
                borderRadius: '6px',
                border: '1px solid #bfdbfe',
                fontSize: '12px',
                color: '#1e40af',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>🏛️</span>
                <span>
                  <strong>Supervisor Evaluation Invariant:</strong> Unlike formative lesson practice quizzes, practical evidence submitted here is audited against rubric <code>{detail.rubric_version}</code>. Official approval promotes your competency level by +1.
                </span>
              </div>
            </div>

            {/* Assessment Rules */}
            <div style={{ padding: '14px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '24px' }}>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#1a365d', marginBottom: '6px' }}>
                Official Assessment Protocols:
              </div>
              <ul style={{ paddingLeft: '20px', fontSize: '12px', color: '#475569', lineHeight: 1.6 }}>
                {detail.rules.map((rule, idx) => (
                  <li key={idx}>{rule}</li>
                ))}
              </ul>
            </div>

            {/* Practical Task 1 */}
            <div style={{ marginBottom: '24px', padding: '18px', borderRadius: '8px', border: '1px solid #cbd5e1' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <h4 style={{ color: '#1a365d', fontSize: '16px' }}>
                  {detail.tasks[0]?.title || 'Task 1: Practical Allocation'}
                </h4>
                <span className="badge badge-gray">{detail.tasks[0]?.expected_output_type || 'NUMERICAL'}</span>
              </div>
              <p style={{ fontSize: '13px', color: '#334155', lineHeight: 1.5, marginBottom: '6px' }}>
                <strong>Scenario:</strong> {detail.tasks[0]?.scenario}
              </p>
              <p style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.4, marginBottom: '12px' }}>
                <strong>Instructions:</strong> {detail.tasks[0]?.instructions}
              </p>

              {isSampling ? (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                  <div>
                    <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                      Stratum A Allocation (n_A):
                    </label>
                    <input
                      type="number"
                      value={stratumA}
                      onChange={e => setStratumA(e.target.value)}
                      style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', fontWeight: 700 }}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                      Stratum B Allocation (n_B):
                    </label>
                    <input
                      type="number"
                      value={stratumB}
                      onChange={e => setStratumB(e.target.value)}
                      style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', fontWeight: 700 }}
                    />
                  </div>
                </div>
              ) : (
                <div>
                  <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                    Task 1 Technical Work / Query / Calculation:
                  </label>
                  <textarea
                    rows={4}
                    value={task1Text}
                    onChange={e => setTask1Text(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '10px',
                      borderRadius: '6px',
                      border: '1px solid #cbd5e1',
                      fontSize: '13px',
                      lineHeight: 1.4,
                      fontFamily: 'monospace'
                    }}
                  />
                </div>
              )}
            </div>

            {/* Practical Task 2 */}
            <div style={{ marginBottom: '28px', padding: '18px', borderRadius: '8px', border: '1px solid #cbd5e1' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <h4 style={{ color: '#1a365d', fontSize: '16px' }}>
                  {detail.tasks[1]?.title || 'Task 2: Technical Justification & Defense'}
                </h4>
                <span className="badge badge-gray">{detail.tasks[1]?.expected_output_type || 'JUSTIFICATION'}</span>
              </div>
              <p style={{ fontSize: '13px', color: '#334155', lineHeight: 1.5, marginBottom: '6px' }}>
                <strong>Scenario:</strong> {detail.tasks[1]?.scenario}
              </p>
              <p style={{ fontSize: '12px', color: '#64748b', lineHeight: 1.4, marginBottom: '12px' }}>
                <strong>Instructions:</strong> {detail.tasks[1]?.instructions}
              </p>

              {isSampling ? (
                <>
                  <div style={{ marginBottom: '12px' }}>
                    <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                      Derived Design Weight:
                    </label>
                    <input
                      type="number"
                      value={designWeight}
                      onChange={e => setDesignWeight(e.target.value)}
                      style={{ width: '140px', padding: '8px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '14px', fontWeight: 700 }}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                      Technical Justification:
                    </label>
                    <textarea
                      rows={3}
                      value={justification}
                      onChange={e => setJustification(e.target.value)}
                      style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '13px', lineHeight: 1.4 }}
                    />
                  </div>
                </>
              ) : (
                <div>
                  <label style={{ fontSize: '12px', fontWeight: 700, color: '#475569', display: 'block', marginBottom: '4px' }}>
                    Task 2 Technical Formulation & Governance Defense:
                  </label>
                  <textarea
                    rows={4}
                    value={task2Text}
                    onChange={e => setTask2Text(e.target.value)}
                    style={{
                      width: '100%',
                      padding: '10px',
                      borderRadius: '6px',
                      border: '1px solid #cbd5e1',
                      fontSize: '13px',
                      lineHeight: 1.4
                    }}
                  />
                </div>
              )}
            </div>

            {/* Submission Actions */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #e2e8f0', paddingTop: '20px' }}>
              <button className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                disabled={submitting}
                onClick={handleSubmit}
                style={{ backgroundColor: '#1a365d', padding: '12px 28px' }}
              >
                {submitting ? 'Packaging Evidence...' : 'Submit Practical Assessment for Review →'}
              </button>
            </div>
          </div>
        )}

        {/* Post-submission pending screen */}
        {submitted && detail && (
          <div style={{ textAlign: 'center', padding: '24px 0' }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              backgroundColor: '#fef3c7',
              color: '#d97706',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px',
              marginBottom: '16px'
            }}>
              ⏳
            </div>
            <h2 style={{ fontSize: '22px', fontWeight: 800, color: '#1a365d', marginBottom: '10px' }}>
              Assessment Evidence Submitted for Supervisor Evaluation
            </h2>
            <p style={{ fontSize: '14px', color: '#475569', maxWidth: '580px', margin: '0 auto 24px auto', lineHeight: 1.6 }}>
              Your practical task calculations have been securely hashed and routed to <strong>Sunita Rao (Superintending Officer & Assessor)</strong>.
              In accordance with MoSPI cadre governance rules, your demonstrated competency level will update only upon official verification.
            </p>

            <div style={{ padding: '14px 20px', backgroundColor: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0', display: 'inline-block', textAlign: 'left', marginBottom: '24px', fontSize: '13px' }}>
              <div>📋 <strong>Status:</strong> <span className="badge badge-saffron" style={{ marginLeft: '6px' }}>PENDING SUPERVISOR REVIEW</span></div>
              <div style={{ marginTop: '6px' }}>🎯 <strong>Competency:</strong> {detail.competency_id} ({detail.competency_label})</div>
              <div style={{ marginTop: '6px' }}>📈 <strong>Proposed Update:</strong> Level {detail.current_level} → Level {detail.target_level}</div>
              <div style={{ marginTop: '6px' }}>📜 <strong>Rubric:</strong> {detail.rubric_version}</div>
            </div>

            <div>
              <button className="btn btn-navy" onClick={onClose}>
                Return to Learning Portal
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

