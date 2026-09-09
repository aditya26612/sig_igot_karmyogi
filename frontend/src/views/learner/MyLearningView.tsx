import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { CuratedPlaylistDTO, CuratedLessonDTO, LessonDetailResponse } from '../../types';
import { VideoPlayer } from '../../components/VideoPlayer';
import { TranscriptViewer } from '../../components/TranscriptViewer';
import { QuizModal } from '../../components/QuizModal';
import { AssessmentModal } from '../../components/AssessmentModal';

export const MyLearningView: React.FC = () => {
  const { selectedLessonId, setSelectedLessonId, activeAssessmentId, setActiveAssessmentId } = useAuth();
  const [playlists, setPlaylists] = useState<CuratedPlaylistDTO[]>([]);
  const [activePlaylistId, setActivePlaylistId] = useState<string>('PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J');
  const [lessonDetail, setLessonDetail] = useState<LessonDetailResponse | null>(null);
  const [currentPlaylistLessons, setCurrentPlaylistLessons] = useState<CuratedLessonDTO[]>([]);
  const [loading, setLoading] = useState(true);
  const [showQuizModal, setShowQuizModal] = useState(false);

  // Load playlists
  useEffect(() => {
    async function loadPlaylists() {
      try {
        const data = await api.getPlaylists();
        setPlaylists(data);
      } catch (err) {
        console.error('Failed to load playlists:', err);
      }
    }
    loadPlaylists();
  }, []);

  // Load playlist lessons dynamically when active playlist changes
  useEffect(() => {
    async function loadPlaylistLessons() {
      if (!activePlaylistId) return;
      try {
        const detail = await api.getPlaylistDetail(activePlaylistId);
        if (detail && detail.lessons) {
          setCurrentPlaylistLessons(detail.lessons);
        }
      } catch (err) {
        console.error('Failed to load playlist lessons:', err);
      }
    }
    loadPlaylistLessons();
  }, [activePlaylistId]);

  // Load lesson detail
  useEffect(() => {
    async function loadLesson() {
      if (!selectedLessonId) return;
      setLoading(true);
      try {
        const data = await api.getLessonDetail(selectedLessonId);
        setLessonDetail(data);
        setActivePlaylistId(data.playlist.playlist_id);
      } catch (err) {
        console.error('Failed to load lesson detail:', err);
      } finally {
        setLoading(false);
      }
    }
    loadLesson();
  }, [selectedLessonId]);

  const isSamplingPlaylist = 
    lessonDetail?.playlist.competency_id === 'COMP-SAMPLING' ||
    activePlaylistId === 'PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J';

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* View Header */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
          <span className="badge badge-saffron">Curated Learning Modules</span>
          <span style={{ fontSize: '13px', color: '#64748b' }}>External Videos with Local AI Transcripts & Quizzes</span>
        </div>
        <h1 style={{ fontSize: '28px', fontWeight: 800, color: '#1a365d' }}>
          My Learning & Video Curriculum
        </h1>
      </div>

      {/* Assessment Mechanisms Differentiation Guide */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        gap: '16px',
        backgroundColor: '#ffffff',
        borderRadius: '10px',
        border: '1px solid #e2e8f0',
        padding: '16px 20px',
        marginBottom: '24px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
      }}>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
          <div style={{ fontSize: '24px', lineHeight: 1 }}>🎯</div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <strong style={{ fontSize: '14px', color: '#1a365d' }}>1. Lesson Practice Quiz</strong>
              <span className="badge badge-saffron" style={{ fontSize: '10px', padding: '1px 6px' }}>Formative</span>
            </div>
            <p style={{ fontSize: '12px', color: '#475569', margin: '4px 0 0 0', lineHeight: 1.4 }}>
              Self-paced quiz available for every video. Provides instant feedback and transcript citations. <em>Does not alter your official competency level.</em>
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', borderLeft: '1px solid #f1f5f9', paddingLeft: '16px' }}>
          <div style={{ fontSize: '24px', lineHeight: 1 }}>🏛️</div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <strong style={{ fontSize: '14px', color: '#1a365d' }}>2. Cadre Practical Assessment</strong>
              <span className="badge badge-navy" style={{ fontSize: '10px', padding: '1px 6px' }}>Summative</span>
            </div>
            <p style={{ fontSize: '12px', color: '#475569', margin: '4px 0 0 0', lineHeight: 1.4 }}>
              Formal module-level examination evaluated by NSSO Supervisor (<strong>Sunita Rao</strong>). <em>Official approval promotes your cadre level (+1 Level).</em>
            </p>
          </div>
        </div>
      </div>

      {/* Playlist Selector Chips */}
      <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '16px', marginBottom: '24px' }}>
        {playlists.map(p => {
          const isActive = p.playlist_id === activePlaylistId;
          return (
            <button
              key={p.playlist_id}
              onClick={async () => {
                setActivePlaylistId(p.playlist_id);
                try {
                  const detail = await api.getPlaylistDetail(p.playlist_id);
                  if (detail && detail.lessons && detail.lessons.length > 0) {
                    setCurrentPlaylistLessons(detail.lessons);
                    setSelectedLessonId(detail.lessons[0].lesson_id);
                  }
                } catch (err) {
                  console.error(err);
                }
              }}
              style={{
                padding: '10px 16px',
                borderRadius: '8px',
                border: isActive ? '2px solid #1a365d' : '1px solid #cbd5e1',
                backgroundColor: isActive ? '#1a365d' : '#ffffff',
                color: isActive ? '#ffffff' : '#334155',
                fontSize: '13px',
                fontWeight: 700,
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                boxShadow: isActive ? '0 2px 4px rgba(26,54,93,0.2)' : 'none',
                transition: 'all 0.15s ease'
              }}
            >
              {p.title.split('&')[0]} ({p.competency_id})
            </button>
          );
        })}
      </div>

      {/* Main Learning Grid: Video Player + Playlist Sidebar */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '28px', alignItems: 'flex-start' }}>
        {/* Left Column: Video Player & Transcripts */}
        <div>
          {loading ? (
            <div style={{ padding: '80px', textAlign: 'center', backgroundColor: '#ffffff', borderRadius: '12px' }}>
              <div style={{ fontSize: '18px', fontWeight: 600, color: '#1a365d' }}>Loading Video & Transcript...</div>
            </div>
          ) : lessonDetail ? (
            <div>
              <div style={{ marginBottom: '28px' }}>
                <VideoPlayer
                  lesson={lessonDetail.lesson}
                  playlist={lessonDetail.playlist}
                  onLaunchQuiz={() => setShowQuizModal(true)}
                />
              </div>

              {/* Conditional Assessment Callout Banner */}
              {(() => {
                const ASSESSMENT_MAP: Record<string, { id: string; rubric: string; title: string }> = {
                  'COMP-SAMPLING': {
                    id: 'ASS-DEMO-PRACTICAL-001',
                    rubric: 'sampling-practical-demo-v1',
                    title: 'Sampling Design & Frame Verification'
                  },
                  'COMP-027': {
                    id: 'ASS-DEMO-PRACTICAL-002',
                    rubric: 'sql-practical-demo-v1',
                    title: 'SQL Multi-Table Reconciliation & Registry Audits'
                  },
                  'COMP-018': {
                    id: 'ASS-DEMO-PRACTICAL-003',
                    rubric: 'quality-practical-demo-v1',
                    title: 'Data Quality Auditing, Outlier Detection & Anonymization'
                  },
                  'COMP-025': {
                    id: 'ASS-DEMO-PRACTICAL-004',
                    rubric: 'python-practical-demo-v1',
                    title: 'Python Microdata Cleaning & Automated QA Pipelines'
                  }
                };

                const currentAss = ASSESSMENT_MAP[lessonDetail.playlist.competency_id];

                if (currentAss) {
                  return (
                    <div style={{
                      padding: '20px 24px',
                      backgroundColor: '#fef3c7',
                      borderRadius: '10px',
                      border: '1.5px solid #f59e0b',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '28px',
                      flexWrap: 'wrap',
                      gap: '16px',
                      boxShadow: '0 2px 6px rgba(245, 158, 11, 0.12)'
                    }}>
                      <div style={{ flex: 1, minWidth: '280px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                          <span className="badge badge-saffron" style={{ fontWeight: 800 }}>
                            FORMAL CADRE ASSESSMENT
                          </span>
                          <span style={{ fontSize: '12px', color: '#78350f', fontWeight: 700 }}>
                            Rubric: {currentAss.rubric}
                          </span>
                        </div>
                        <div style={{ fontWeight: 800, color: '#92400e', fontSize: '16px' }}>
                          Ready for Formal Cadre Evaluation? ({currentAss.title})
                        </div>
                        <div style={{ fontSize: '13px', color: '#78350f', marginTop: '4px', lineHeight: 1.5 }}>
                          Unlike formative self-paced practice quizzes, submitting this practical evidence packages your work for NSSO Supervisor evaluation (<strong>Sunita Rao</strong>). Upon approval, your official MoSPI competency level is promoted (Level 2 → Level 3).
                        </div>
                      </div>

                      <button
                        className="btn btn-primary"
                        onClick={() => setActiveAssessmentId(currentAss.id)}
                        style={{
                          backgroundColor: '#92400e',
                          border: '1px solid #78350f',
                          minHeight: '42px',
                          fontSize: '13px',
                          fontWeight: 800,
                          padding: '10px 20px',
                          whiteSpace: 'nowrap'
                        }}
                      >
                        Start Practical Cadre Assessment →
                      </button>
                    </div>
                  );
                }

                return (
                  <div style={{
                    padding: '20px 24px',
                    backgroundColor: '#f0f9ff',
                    borderRadius: '10px',
                    border: '1.5px solid #93c5fd',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '28px',
                    flexWrap: 'wrap',
                    gap: '16px',
                    boxShadow: '0 2px 6px rgba(147, 197, 253, 0.15)'
                  }}>
                    <div style={{ flex: 1, minWidth: '280px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                        <span className="badge badge-navy" style={{ fontWeight: 800 }}>
                          CADRE ASSESSMENT NOTICE
                        </span>
                        <span style={{ fontSize: '12px', color: '#1e40af', fontWeight: 700 }}>
                          Competency: {lessonDetail.playlist.competency_id}
                        </span>
                      </div>
                      <div style={{ fontWeight: 800, color: '#1e3a8a', fontSize: '16px' }}>
                        Course Examination Notice • {lessonDetail.playlist.title}
                      </div>
                      <div style={{ fontSize: '13px', color: '#334155', marginTop: '4px', lineHeight: 1.5 }}>
                        Formal cadre examinations for this competency are scheduled through the MoSPI Departmental Review Board. In this sandbox, active supervisor review queues are available for <strong>Sampling</strong>, <strong>SQL</strong>, <strong>Data Quality</strong>, and <strong>Python</strong>.
                        Use the <strong>🎯 Lesson Practice Quiz</strong> button above to test your understanding of each lecture!
                      </div>
                    </div>

                    <button
                      className="btn btn-secondary"
                      onClick={() => {
                        setActivePlaylistId('PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J');
                        setSelectedLessonId('sampling-lesson-3');
                        setActiveAssessmentId('ASS-DEMO-PRACTICAL-001');
                      }}
                      style={{
                        backgroundColor: '#ffffff',
                        border: '1px solid #1a365d',
                        color: '#1a365d',
                        minHeight: '42px',
                        fontSize: '13px',
                        fontWeight: 700,
                        padding: '10px 18px',
                        whiteSpace: 'nowrap'
                      }}
                    >
                      Go to Active Practical Exams →
                    </button>
                  </div>
                );
              })()}

              {/* Interactive Transcript */}
              <TranscriptViewer chunks={lessonDetail.transcript_chunks} />
            </div>
          ) : (
            <p>Lesson detail unavailable.</p>
          )}
        </div>

        {/* Right Column: Playlist Lesson List */}
        <div className="gov-card" style={{ padding: '20px' }}>
          <div style={{ borderBottom: '1px solid #e2e8f0', paddingBottom: '12px', marginBottom: '14px' }}>
            <span style={{ fontSize: '11px', color: '#64748b', fontWeight: 700, textTransform: 'uppercase' }}>
              Module Syllabus
            </span>
            <h3 style={{ fontSize: '16px', fontWeight: 800, color: '#1a365d', marginTop: '2px' }}>
              {lessonDetail?.playlist.title || 'Course Lessons'}
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {(currentPlaylistLessons.length > 0 ? currentPlaylistLessons : (lessonDetail?.playlist?.lessons || [])).map(item => {
              const isSelected = item.lesson_id === selectedLessonId;
              return (
                <div
                  key={item.lesson_id}
                  onClick={() => setSelectedLessonId(item.lesson_id)}
                  style={{
                    padding: '12px 14px',
                    borderRadius: '8px',
                    backgroundColor: isSelected ? '#ebf8ff' : '#f8fafc',
                    borderLeft: item.is_completed ? '4px solid #2e7d32' : isSelected ? '4px solid #1a365d' : '4px solid transparent',
                    cursor: 'pointer',
                    transition: 'all 0.15s'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: isSelected ? '#1e40af' : '#64748b' }}>
                      Lesson #{item.sequence_no}
                    </span>
                    <span style={{ fontSize: '11px', color: item.is_completed ? '#2e7d32' : '#94a3b8', fontWeight: item.is_completed ? 700 : 400 }}>
                      {item.is_completed ? '✓ Watched' : `${item.duration_minutes} min`}
                    </span>
                  </div>
                  <div style={{ fontSize: '13px', fontWeight: isSelected ? 700 : 500, color: isSelected ? '#1a365d' : '#334155', lineHeight: 1.3 }}>
                    {item.title}
                  </div>
                </div>
              );
            })}
          </div>

          <div style={{ marginTop: '20px', padding: '12px', backgroundColor: '#f1f5f9', borderRadius: '6px', fontSize: '11px', color: '#64748b', lineHeight: 1.5 }}>
            💡 <strong>Notice:</strong> Video playback is sourced directly from verified open educational playlists. Questions and transcripts are processed locally.
          </div>
        </div>
      </div>

      {/* Practice Quiz Modal */}
      {showQuizModal && selectedLessonId && (
        <QuizModal
          lessonId={selectedLessonId}
          onClose={() => setShowQuizModal(false)}
        />
      )}

      {/* Practical Assessment Modal */}
      {activeAssessmentId && (
        <AssessmentModal
          assessmentId={activeAssessmentId}
          onClose={() => setActiveAssessmentId(null)}
        />
      )}
    </div>
  );
};
