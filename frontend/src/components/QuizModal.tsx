import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { PracticeQuizDTO, PracticeSubmissionResponse } from '../types';
import { api } from '../api/client';

interface QuizModalProps {
  lessonId: string;
  onClose: () => void;
}

export const QuizModal: React.FC<QuizModalProps> = ({ lessonId, onClose }) => {
  const { t } = useTranslation();
  const [quiz, setQuiz] = useState<PracticeQuizDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<PracticeSubmissionResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function loadQuiz() {
      try {
        const data = await api.getPracticeQuiz(lessonId);
        setQuiz(data);
      } catch (err: any) {
        setError(err.message || t('quiz.noQuiz'));
      } finally {
        setLoading(false);
      }
    }
    loadQuiz();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lessonId]);

  const handleSelectOption = (questionId: string, optionId: string) => {
    setSelectedAnswers(prev => ({ ...prev, [questionId]: optionId }));
  };

  const handleSubmit = async () => {
    if (!quiz) return;
    setSubmitting(true);
    try {
      const answersArray = quiz.questions.map(q => ({
        question_id: q.question_id,
        selected_option: selectedAnswers[q.question_id] || 'A'
      }));
      const res = await api.submitPracticeQuiz(quiz.quiz_id, answersArray);
      setResult(res);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const answeredCount = quiz ? quiz.questions.filter(q => selectedAnswers[q.question_id]).length : 0;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {loading && (
          <div style={{ textAlign: 'center', padding: '48px' }}>
            <div style={{ fontSize: '18px', fontWeight: 600, color: 'var(--color-text-strong)' }}>{t('quiz.loadingQuiz')}</div>
          </div>
        )}

        {error && !result && (
          <div style={{ textAlign: 'center', padding: '32px' }}>
            <h3 style={{ color: 'var(--color-danger)', marginBottom: '8px' }}>{t('quiz.notice')}</h3>
            <p style={{ color: 'var(--color-text-muted)', marginBottom: '20px' }}>{error}</p>
            <button className="btn btn-secondary" onClick={onClose}>{t('common.close')}</button>
          </div>
        )}

        {quiz && !result && (
          <div>
            {/* Header */}
            <div style={{ borderBottom: '1px solid var(--color-border)', paddingBottom: '16px', marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span className="badge badge-saffron" style={{ fontWeight: 800 }}>
                    {t('quiz.formativeBadge')}
                  </span>
                  <span style={{ fontSize: '12px', color: '#146B1A', backgroundColor: 'var(--color-success-subtle)', padding: '3px 8px', borderRadius: '4px', fontWeight: 700 }}>
                    {t('quiz.lessonCheck')}
                  </span>
                </div>
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-muted)' }}>
                  {t('quiz.question', { current: currentIndex + 1, total: quiz.total_questions })}
                </span>
              </div>
              <h2 style={{ fontSize: '20px', fontWeight: 800, color: 'var(--color-text-strong)', marginTop: '4px' }}>
                {quiz.title}
              </h2>
              {/* Progress track */}
              <div style={{ display: 'flex', gap: '5px', marginTop: '12px' }}>
                {quiz.questions.map((q, i) => (
                  <button
                    key={q.question_id}
                    onClick={() => setCurrentIndex(i)}
                    aria-label={t('quiz.question', { current: i + 1, total: quiz.total_questions })}
                    style={{
                      flex: 1,
                      height: '5px',
                      borderRadius: '3px',
                      border: 'none',
                      cursor: 'pointer',
                      backgroundColor:
                        i === currentIndex ? 'var(--orange-500)'
                        : selectedAnswers[q.question_id] ? 'var(--blue-500)'
                        : 'var(--color-border)',
                      transition: 'background-color 0.15s ease'
                    }}
                  />
                ))}
              </div>
              <div style={{
                marginTop: '10px',
                padding: '8px 12px',
                backgroundColor: 'var(--wash-ivory)',
                borderRadius: '6px',
                border: '1px solid var(--color-border)',
                fontSize: '12px',
                color: 'var(--color-text-secondary)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span style={{ color: 'var(--orange-700)', display: 'inline-flex', flex: 'none' }}>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V18h8v-3.3A7 7 0 0 0 12 2z"/></svg>
                </span>
                <span>
                  {t('quiz.invariantNotice')}
                </span>
              </div>
            </div>

            {/* Current Question */}
            {quiz.questions[currentIndex] && (
              <div>
                <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-text-strong)', marginBottom: '20px', lineHeight: 1.5 }}>
                  {quiz.questions[currentIndex].question_text}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '28px' }}>
                  {quiz.questions[currentIndex].options.map(opt => {
                    const qId = quiz.questions[currentIndex].question_id;
                    const isSelected = selectedAnswers[qId] === opt.option_id;
                    return (
                      <button
                        key={opt.option_id}
                        onClick={() => handleSelectOption(qId, opt.option_id)}
                        className={`quiz-option ${isSelected ? 'selected' : ''}`}
                        aria-pressed={isSelected}
                      >
                        <span className="quiz-option-dot">{opt.option_id}</span>
                        <span style={{ fontSize: '14px', color: 'var(--color-text-primary)', fontWeight: isSelected ? 700 : 400, textAlign: 'left' }}>
                          {opt.text}
                        </span>
                      </button>
                    );
                  })}
                </div>

                {/* Navigation Buttons */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '10px' }}>
                  <button
                    className="btn btn-secondary"
                    disabled={currentIndex === 0}
                    onClick={() => setCurrentIndex(prev => prev - 1)}
                    style={{ opacity: currentIndex === 0 ? 0.4 : 1 }}
                  >
                    {t('quiz.previous')}
                  </button>

                  {currentIndex < quiz.total_questions - 1 ? (
                    <button
                      className="btn btn-primary"
                      onClick={() => setCurrentIndex(prev => prev + 1)}
                    >
                      {t('quiz.nextQuestion')}
                    </button>
                  ) : (
                    <button
                      className="btn btn-primary"
                      disabled={submitting || answeredCount < quiz.total_questions}
                      onClick={handleSubmit}
                      style={{ opacity: answeredCount < quiz.total_questions ? 0.55 : 1 }}
                    >
                      {submitting ? t('quiz.evaluating') : `${t('quiz.submitQuiz')} (${answeredCount}/${quiz.total_questions})`}
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Results Screen */}
        {result && (
          <div>
            <div style={{ textAlign: 'center', paddingBottom: '20px', borderBottom: '1px solid var(--color-border)', marginBottom: '20px' }}>
              <span className="badge badge-green" style={{ marginBottom: '8px' }}>{t('quiz.practiceComplete')}</span>
              <h2 style={{ fontSize: '24px', fontWeight: 800, color: 'var(--color-text-strong)' }}>
                {t('quiz.yourScore', { score: result.score, total: result.total_questions, pct: result.percentage })}
              </h2>
              <div style={{
                marginTop: '12px',
                padding: '10px 14px',
                backgroundColor: 'var(--orange-50)',
                borderRadius: '8px',
                border: '1px solid var(--orange-100)',
                color: 'var(--orange-700)',
                fontSize: '13px',
                fontWeight: 600
              }}>
                {result.notice}
              </div>
            </div>

            {/* Questions breakdown */}
            <div style={{ maxHeight: '350px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '20px', paddingRight: '4px' }}>
              {result.results.map((res, i) => (
                <div
                  key={res.question_id}
                  className={`quiz-result-card ${res.is_correct ? 'correct' : 'incorrect'}`}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-strong)' }}>
                      #{i + 1}
                    </span>
                    <span className={`badge ${res.is_correct ? 'badge-green' : 'badge-danger'}`}>
                      {res.is_correct ? t('quiz.correct') : t('quiz.incorrect')}
                    </span>
                  </div>

                  <p style={{ fontSize: '14px', color: 'var(--color-text-primary)', marginBottom: '8px' }}>
                    {res.question_text}
                  </p>

                  <div style={{ fontSize: '13px', color: 'var(--color-text-secondary)', marginBottom: '6px' }}>
                    {t('quiz.yourAnswer')}: <strong>{res.selected_option}</strong> | {t('quiz.correctAnswer')}: <strong style={{ color: '#146B1A' }}>{res.correct_option}</strong>
                  </div>

                  <div style={{ fontSize: '12px', color: 'var(--color-text-primary)', backgroundColor: 'rgba(255,255,255,0.7)', padding: '8px 10px', borderRadius: '6px' }}>
                    <strong>{t('quiz.explanation')}:</strong> {res.explanation}
                    {res.timestamp_label && (
                      <span style={{ color: 'var(--orange-700)', fontWeight: 700, marginLeft: '8px' }}>
                        [{t('quiz.transcript')}: {res.timestamp_label}]
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <button className="btn btn-navy" onClick={onClose}>
                {t('quiz.doneReviewing')}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
