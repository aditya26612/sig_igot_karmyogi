import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { AssessmentDetailDTO } from '../types';
import { api } from '../api/client';

interface AssessmentModalProps {
  assessmentId: string;
  onClose: () => void;
  onSubmitted?: () => void;
}

const ClockIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="9" />
    <polyline points="12 7 12 12 15.5 14" />
  </svg>
);

const ShieldIcon: React.FC = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    <polyline points="9 12 11 14 15 10" />
  </svg>
);

const TaskIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <rect x="8" y="2" width="8" height="4" rx="1" />
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
    <polyline points="9 12 11 14 15 10" />
  </svg>
);

const HourglassIcon: React.FC = () => (
  <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M5 22h14" />
    <path d="M5 2h14" />
    <path d="M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22" />
    <path d="M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2" />
  </svg>
);

export const AssessmentModal: React.FC<AssessmentModalProps> = ({ assessmentId, onClose, onSubmitted }) => {
  const { t } = useTranslation();
  const [detail, setDetail] = useState<AssessmentDetailDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const [stratumA, setStratumA] = useState('');
  const [stratumB, setStratumB] = useState('');
  const [designWeight, setDesignWeight] = useState('');
  const [justification, setJustification] = useState('');
  const [task1Text, setTask1Text] = useState('');
  const [task2Text, setTask2Text] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationMsg, setValidationMsg] = useState<string | null>(null);
  const [currentTask, setCurrentTask] = useState(0);

  useEffect(() => {
    async function loadAssessment() {
      try {
        const data = await api.getAssessmentDetail(assessmentId);
        setDetail(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load assessment blueprint.');
      } finally {
        setLoading(false);
      }
    }
    loadAssessment();
  }, [assessmentId]);

  // Answers start EMPTY — the learner must produce their own practical evidence.
  const tasksComplete = () => {
    if (!detail) return false;
    if (detail.assessment_id === 'ASS-DEMO-PRACTICAL-001') {
      return stratumA.trim() !== '' && stratumB.trim() !== '' && designWeight.trim() !== '' && justification.trim() !== '';
    }
    return task1Text.trim() !== '' && task2Text.trim() !== '';
  };

  const handleSubmit = async () => {
    if (!detail) return;
    if (!tasksComplete()) {
      setValidationMsg(t('assessment.answerRequired'));
      return;
    }
    setValidationMsg(null);
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
  const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '10px 12px',
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
    marginBottom: '6px'
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()} style={{ maxWidth: '860px' }}>
        {loading && (
          <div style={{ textAlign: 'center', padding: '48px' }}>
            <div style={{ fontSize: '18px', fontWeight: 600, color: 'var(--color-text-strong)' }}>{t('assessment.loading')}</div>
          </div>
        )}

        {error && !submitted && (
          <div style={{ textAlign: 'center', padding: '32px' }}>
            <h3 style={{ color: 'var(--color-danger)' }}>{t('assessment.errorTitle')}</h3>
            <p style={{ color: 'var(--color-text-muted)', margin: '12px 0 20px 0' }}>{error}</p>
            <button className="btn btn-secondary" onClick={onClose}>{t('common.close')}</button>
          </div>
        )}

        {detail && !submitted && (
          <div className="assessment-shell">
            {/* ---- Sticky header ---- */}
            <div className="assessment-head">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span className="badge badge-navy">{t('assessment.badge')}</span>
                  <span className="badge badge-saffron">{t('assessment.rubricLabel', { rubric: detail.rubric_version })}</span>
                </div>
                <button className="copilot-icon-btn" onClick={onClose} title={t('common.close')} aria-label={t('common.close')}>✕</button>
              </div>
              <h2 style={{ fontSize: '22px', fontWeight: 800, color: 'var(--color-text-strong)', marginTop: '10px' }}>
                {detail.title}
              </h2>
              <div className="assessment-meta-row">
                <span className="assessment-meta-chip"><TargetGlyph /> {t('assessment.target', { level: detail.target_level })}</span>
                <span className="assessment-meta-chip">{t('assessment.current', { level: detail.current_level })}</span>
                <span className="assessment-meta-chip"><ClockIcon /> {t('assessment.time', { minutes: detail.estimated_time_minutes })}</span>
                <span className="assessment-meta-chip">{t('assessment.auditor')}</span>
              </div>
              <div className="assessment-invariant-note">
                <ShieldIcon />
                <span>{t('assessment.supervisorInvariant', { rubric: detail.rubric_version })}</span>
              </div>
            </div>

            {/* ---- Rules ---- */}
            <div className="assessment-rules">
              <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-strong)', marginBottom: '6px' }}>
                {t('assessment.protocols')}
              </div>
              <ul style={{ paddingLeft: '20px', fontSize: '12.5px', color: 'var(--color-text-secondary)', lineHeight: 1.6, margin: 0 }}>
                {detail.rules.map((rule, idx) => (
                  <li key={idx}>{rule}</li>
                ))}
              </ul>
            </div>

            {/* ---- Task navigation ---- */}
            {detail.tasks.length > 1 && (
              <div className="assessment-task-tabs" role="tablist">
                {detail.tasks.map((task, i) => (
                  <button
                    key={task.task_id}
                    role="tab"
                    aria-selected={currentTask === i}
                    className={`assessment-task-tab ${currentTask === i ? 'active' : ''} ${i < currentTask ? 'done' : ''}`}
                    onClick={() => setCurrentTask(i)}
                  >
                    <TaskIcon /> {t('assessment.taskLabel', { no: i + 1 })}
                  </button>
                ))}
              </div>
            )}

            {/* ---- Task cards (one at a time; both must be completed) ---- */}
            {detail.tasks.map((task, i) => currentTask === i && (
              <div key={task.task_id} className="assessment-task-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px', gap: '8px', flexWrap: 'wrap' }}>
                  <h4 style={{ color: 'var(--color-text-strong)', fontSize: '16px', margin: 0 }}>
                    {task.title}
                  </h4>
                  <span className="badge badge-gray">{task.expected_output_type}</span>
                </div>
                <p style={{ fontSize: '13px', color: 'var(--color-text-primary)', lineHeight: 1.5, marginBottom: '8px' }}>
                  <strong>{t('assessment.scenario')}:</strong> {task.scenario}
                </p>
                <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', lineHeight: 1.45, marginBottom: '16px' }}>
                  <strong>{t('assessment.instructions')}:</strong> {task.instructions}
                </p>

                {isSampling && i === 0 ? (
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
                    <div>
                      <label style={labelStyle} htmlFor="stratum-a">{t('assessment.stratumA')}</label>
                      <input id="stratum-a" type="number" value={stratumA} onChange={e => setStratumA(e.target.value)} style={inputStyle} placeholder="—" />
                    </div>
                    <div>
                      <label style={labelStyle} htmlFor="stratum-b">{t('assessment.stratumB')}</label>
                      <input id="stratum-b" type="number" value={stratumB} onChange={e => setStratumB(e.target.value)} style={inputStyle} placeholder="—" />
                    </div>
                  </div>
                ) : isSampling && i === 1 ? (
                  <>
                    <div style={{ marginBottom: '14px' }}>
                      <label style={labelStyle} htmlFor="design-weight">{t('assessment.designWeight')}</label>
                      <input id="design-weight" type="number" value={designWeight} onChange={e => setDesignWeight(e.target.value)} style={{ ...inputStyle, maxWidth: '160px' }} placeholder="—" />
                    </div>
                    <div>
                      <label style={labelStyle} htmlFor="justification">{t('assessment.justification')}</label>
                      <textarea
                        id="justification"
                        rows={4}
                        value={justification}
                        onChange={e => setJustification(e.target.value)}
                        style={{ ...inputStyle, lineHeight: 1.5, resize: 'vertical' }}
                        placeholder="…"
                      />
                    </div>
                  </>
                ) : (
                  <div>
                    <label style={labelStyle} htmlFor={`task-${i}`}>
                      {i === 0 ? t('assessment.task1Label') : t('assessment.task2Label')}
                    </label>
                    <textarea
                      id={`task-${i}`}
                      rows={7}
                      value={i === 0 ? task1Text : task2Text}
                      onChange={e => i === 0 ? setTask1Text(e.target.value) : setTask2Text(e.target.value)}
                      style={{ ...inputStyle, fontFamily: i === 0 ? 'monospace' : 'var(--font-sans)', lineHeight: 1.5, resize: 'vertical' }}
                      placeholder={i === 0 ? t('assessment.answerHintTask1') : t('assessment.answerHintTask2')}
                    />
                  </div>
                )}
              </div>
            ))}

            {validationMsg && (
              <div style={{ padding: '10px 14px', backgroundColor: 'var(--color-danger-subtle)', color: 'var(--color-danger)', borderRadius: 'var(--radius-sm)', fontSize: '13px', fontWeight: 600 }}>
                {validationMsg}
              </div>
            )}

            {/* ---- Footer actions ---- */}
            <div className="assessment-footer">
              <button className="btn btn-secondary" onClick={onClose}>
                {t('common.cancel')}
              </button>
              <div style={{ display: 'flex', gap: '10px' }}>
                {detail.tasks.length > 1 && currentTask < detail.tasks.length - 1 ? (
                  <button className="btn btn-primary" onClick={() => setCurrentTask(prev => prev + 1)}>
                    {t('quiz.nextQuestion')}
                  </button>
                ) : detail.tasks.length > 1 && currentTask > 0 ? (
                  <button className="btn btn-secondary" onClick={() => setCurrentTask(prev => prev - 1)}>
                    {t('quiz.previous')}
                  </button>
                ) : null}
                <button
                  className="btn btn-primary"
                  disabled={submitting || !tasksComplete()}
                  onClick={handleSubmit}
                  style={{ opacity: tasksComplete() ? 1 : 0.55 }}
                >
                  {submitting ? t('assessment.packaging') : t('assessment.submit')}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Post-submission pending screen */}
        {submitted && detail && (
          <div style={{ textAlign: 'center', padding: '32px 8px' }}>
            <div style={{
              width: '72px',
              height: '72px',
              borderRadius: '50%',
              backgroundColor: 'var(--orange-50)',
              color: 'var(--orange-700)',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '16px'
            }}>
              <HourglassIcon />
            </div>
            <h2 style={{ fontSize: '22px', fontWeight: 800, color: 'var(--color-text-strong)', marginBottom: '10px' }}>
              {t('assessment.submittedTitle')}
            </h2>
            <p style={{ fontSize: '14px', color: 'var(--color-text-secondary)', maxWidth: '600px', margin: '0 auto 24px auto', lineHeight: 1.6 }}>
              {t('assessment.submittedBody')}
            </p>

            <div style={{ padding: '14px 20px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', display: 'inline-block', textAlign: 'left', marginBottom: '24px', fontSize: '13px' }}>
              <div><strong>{t('assessment.statusLabel')}</strong> <span className="badge badge-saffron" style={{ marginLeft: '6px' }}>{t('assessment.statusPending')}</span></div>
              <div style={{ marginTop: '6px' }}><strong>{t('assessment.competencyLabel')}</strong> {detail.competency_id} ({detail.competency_label})</div>
              <div style={{ marginTop: '6px' }}><strong>{t('assessment.proposedUpdate')}</strong> {t('assessment.levelTo', { from: detail.current_level, to: detail.target_level })}</div>
              <div style={{ marginTop: '6px' }}><strong>{t('assessment.rubricLine')}</strong> {detail.rubric_version}</div>
            </div>

            <div>
              <button className="btn btn-navy" onClick={onClose}>
                {t('assessment.returnToPortal')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

const TargetGlyph: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" aria-hidden="true">
    <circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1.4" fill="currentColor" />
  </svg>
);
