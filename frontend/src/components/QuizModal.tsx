import React, { useState, useEffect } from 'react';
import { PracticeQuizDTO, PracticeSubmissionResponse } from '../types';
import { api } from '../api/client';

interface QuizModalProps {
  lessonId: string;
  onClose: () => void;
}

export const QuizModal: React.FC<QuizModalProps> = ({ lessonId, onClose }) => {
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
        setError(err.message || 'No practice quiz ready for this lesson yet.');
      } finally {
        setLoading(false);
      }
    }
    loadQuiz();
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

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {loading && (
          <div style={{ textAlign: 'center', padding: '48px' }}>
            <div style={{ fontSize: '18px', fontWeight: 600, color: '#1a365d' }}>Loading Practice Quiz...</div>
          </div>
        )}

        {error && (
          <div style={{ textAlign: 'center', padding: '32px' }}>
            <h3 style={{ color: '#dc2626', marginBottom: '8px' }}>Practice Quiz Notice</h3>
            <p style={{ color: '#64748b', marginBottom: '20px' }}>{error}</p>
            <button className="btn btn-secondary" onClick={onClose}>Close</button>
          </div>
        )}

        {quiz && !result && (
          <div>
            {/* Header */}
            <div style={{ borderBottom: '1px solid #e2e8f0', paddingBottom: '16px', marginBottom: '20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <span className="badge badge-saffron" style={{ fontWeight: 800 }}>
                    🎯 Formative Practice Quiz
                  </span>
                  <span style={{ fontSize: '12px', color: '#166534', backgroundColor: '#dcfce7', padding: '3px 8px', borderRadius: '4px', fontWeight: 700 }}>
                    Lesson-Level Check
                  </span>
                </div>
                <span style={{ fontSize: '13px', fontWeight: 700, color: '#64748b' }}>
                  Question {currentIndex + 1} of {quiz.total_questions}
                </span>
              </div>
              <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#1a365d', marginTop: '4px' }}>
                {quiz.title}
              </h2>
              <div style={{
                marginTop: '10px',
                padding: '8px 12px',
                backgroundColor: '#f8fafc',
                borderRadius: '6px',
                border: '1px solid #e2e8f0',
                fontSize: '12px',
                color: '#475569',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span>💡</span>
                <span>
                  <strong>Formative Invariant:</strong> Instant answers & transcript citations provided upon completion. Practice results never modify your official MoSPI competency level.
                </span>
              </div>
            </div>

            {/* Current Question */}
            {quiz.questions[currentIndex] && (
              <div>
                <div style={{ fontSize: '16px', fontWeight: 700, color: '#0f172a', marginBottom: '20px', lineHeight: 1.5 }}>
                  {quiz.questions[currentIndex].question_text}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '28px' }}>
                  {quiz.questions[currentIndex].options.map(opt => {
                    const qId = quiz.questions[currentIndex].question_id;
                    const isSelected = selectedAnswers[qId] === opt.option_id;
                    return (
                      <div
                        key={opt.option_id}
                        onClick={() => handleSelectOption(qId, opt.option_id)}
                        style={{
                          padding: '14px 18px',
                          borderRadius: '8px',
                          border: isSelected ? '2px solid #d97706' : '1px solid #cbd5e1',
                          backgroundColor: isSelected ? '#fef3c7' : '#ffffff',
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '12px',
                          transition: 'all 0.15s ease'
                        }}
                      >
                        <span style={{
                          width: '28px',
                          height: '28px',
                          borderRadius: '50%',
                          backgroundColor: isSelected ? '#d97706' : '#f1f5f9',
                          color: isSelected ? '#ffffff' : '#475569',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '13px',
                          fontWeight: 700
                        }}>
                          {opt.option_id}
                        </span>
                        <span style={{ fontSize: '14px', color: '#1e293b', fontWeight: isSelected ? 600 : 400 }}>
                          {opt.text}
                        </span>
                      </div>
                    );
                  })}
                </div>

                {/* Navigation Buttons */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <button
                    className="btn btn-secondary"
                    disabled={currentIndex === 0}
                    onClick={() => setCurrentIndex(prev => prev - 1)}
                    style={{ opacity: currentIndex === 0 ? 0.4 : 1 }}
                  >
                    ← Previous
                  </button>

                  {currentIndex < quiz.total_questions - 1 ? (
                    <button
                      className="btn btn-primary"
                      onClick={() => setCurrentIndex(prev => prev + 1)}
                    >
                      Next Question →
                    </button>
                  ) : (
                    <button
                      className="btn btn-primary"
                      disabled={submitting}
                      onClick={handleSubmit}
                      style={{ backgroundColor: '#166534' }}
                    >
                      {submitting ? 'Evaluating...' : 'Submit Practice Quiz'}
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
            <div style={{ textAlign: 'center', paddingBottom: '20px', borderBottom: '1px solid #e2e8f0', marginBottom: '20px' }}>
              <span className="badge badge-green" style={{ marginBottom: '8px' }}>Practice Complete</span>
              <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#1a365d' }}>
                Your Score: {result.score} / {result.total_questions} ({result.percentage}%)
              </h2>
              <div style={{
                marginTop: '12px',
                padding: '10px 14px',
                backgroundColor: '#fef3c7',
                borderRadius: '8px',
                border: '1px solid #fde68a',
                color: '#92400e',
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
                  style={{
                    padding: '14px',
                    borderRadius: '8px',
                    border: `1px solid ${res.is_correct ? '#bbf7d0' : '#fecaca'}`,
                    backgroundColor: res.is_correct ? '#f0fdf4' : '#fef2f2'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <span style={{ fontSize: '13px', fontWeight: 700, color: '#0f172a' }}>
                      Question #{i + 1}
                    </span>
                    <span className={`badge ${res.is_correct ? 'badge-green' : 'badge-danger'}`}>
                      {res.is_correct ? 'Correct' : 'Incorrect'}
                    </span>
                  </div>

                  <p style={{ fontSize: '14px', color: '#1e293b', marginBottom: '8px' }}>
                    {res.question_text}
                  </p>

                  <div style={{ fontSize: '13px', color: '#475569', marginBottom: '6px' }}>
                    Your Answer: <strong>Option {res.selected_option}</strong> | Correct: <strong style={{ color: '#166534' }}>Option {res.correct_option}</strong>
                  </div>

                  <div style={{ fontSize: '12px', color: '#334155', backgroundColor: 'rgba(255,255,255,0.7)', padding: '8px 10px', borderRadius: '6px' }}>
                    <strong>Explanation:</strong> {res.explanation}
                    {res.timestamp_label && (
                      <span style={{ color: '#d97706', fontWeight: 700, marginLeft: '8px' }}>
                        [Transcript: {res.timestamp_label}]
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <button className="btn btn-navy" onClick={onClose}>
                Done Reviewing
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
