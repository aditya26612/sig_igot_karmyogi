import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api/client';
import { CuratedPlaylistDTO, CuratedLessonDTO, LessonDetailResponse } from '../../types';
import { VideoPlayer } from '../../components/VideoPlayer';
import { TranscriptViewer } from '../../components/TranscriptViewer';
import { QuizModal } from '../../components/QuizModal';
import { AssessmentModal } from '../../components/AssessmentModal';

const TargetIcon: React.FC = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
    <circle cx="12" cy="12" r="9" /><circle cx="12" cy="12" r="5" /><circle cx="12" cy="12" r="1.4" fill="currentColor" />
  </svg>
);

const InstitutionIcon: React.FC = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M3 21h18" /><path d="M5 21V10l7-5 7 5v11" /><path d="M9 21v-5h6v5" /><path d="M10 12h.01M14 12h.01" />
  </svg>
);

const CheckSmallIcon: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const ChevronRightIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="9 6 15 12 9 18" />
  </svg>
);

const PlayCircleIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="10" /><polygon points="10 8 16 12 10 16 10 8" fill="currentColor" stroke="none" />
  </svg>
);

const LightbulbIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M9 18h6" /><path d="M10 22h4" /><path d="M12 2a7 7 0 0 0-4 12.7V18h8v-3.3A7 7 0 0 0 12 2z" />
  </svg>
);

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

  return (
    <div className="gov-container" style={{ padding: '36px 0' }}>
      {/* View Header — plain language, what this page is for */}
      <div style={{ marginBottom: '20px' }}>
        <h1 className="page-title">My Learning</h1>
        <p className="meta-line">
          Watch your course videos, read along with the transcript, and check your understanding with a practice quiz.
        </p>
      </div>

      {/* How it works — 3 simple steps, one row */}
      <div className="gov-card static" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '0',
        padding: '18px 8px',
        marginBottom: '28px'
      }}>
        {[
          { icon: <PlayCircleIcon />, step: '1. Watch', text: 'Play the lesson video. Read the transcript below it any time.' },
          { icon: <TargetIcon />, step: '2. Practice', text: 'Take the practice quiz. It is just for you — it never changes your official level.' },
          { icon: <InstitutionIcon />, step: '3. Get verified', text: 'When you are confident, submit the practical task. Your supervisor reviews and approves the promotion.' },
        ].map((s, i) => (
          <div key={s.step} style={{
            display: 'flex',
            gap: '12px',
            alignItems: 'flex-start',
            padding: '0 16px',
            borderLeft: i > 0 ? '1px solid var(--color-border)' : 'none'
          }}>
            <div style={{ color: 'var(--orange-600)', lineHeight: 1, flex: 'none', marginTop: '2px' }}>{s.icon}</div>
            <div>
              <strong style={{ display: 'block', fontSize: '14px', color: 'var(--color-text-strong)', marginBottom: '3px' }}>{s.step}</strong>
              <span style={{ fontSize: '12.5px', color: 'var(--color-text-secondary)', lineHeight: 1.45 }}>{s.text}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Course selector — tabs with subject names, not codes */}
      <div style={{ marginBottom: '8px' }}>
        <div className="eyebrow-meta" style={{ color: 'var(--color-text-muted)' }}>Choose a course</div>
      </div>
      <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '14px', marginBottom: '20px' }}>
        {playlists.map(p => {
          const isActive = p.playlist_id === activePlaylistId;
          const cleanName = p.title.split('&')[0].trim();
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
                borderRadius: 'var(--radius-sm)',
                border: isActive ? '2px solid var(--blue-500)' : '1px solid var(--color-border)',
                backgroundColor: isActive ? 'var(--blue-500)' : 'var(--color-bg-surface)',
                color: isActive ? 'var(--color-on-blue)' : 'var(--color-text-secondary)',
                fontSize: '13px',
                fontWeight: 700,
                fontFamily: 'var(--font-sans)',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                boxShadow: isActive ? '0 2px 4px rgba(27,76,161,0.2)' : 'none',
                transition: 'all 0.15s ease'
              }}
            >
              {cleanName}
            </button>
          );
        })}
      </div>

      {/* Main layout: video + transcript (left), syllabus (right) */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: '28px', alignItems: 'flex-start' }}>
        {/* Left: what you're watching now */}
        <div>
          {loading ? (
            <div className="gov-card" style={{ padding: '80px', textAlign: 'center' }}>
              <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--color-text-strong)' }}>Loading your lesson...</div>
            </div>
          ) : lessonDetail ? (
            <div>
              <div style={{ marginBottom: '6px' }}>
                <div className="eyebrow-meta" style={{ color: 'var(--color-text-muted)' }}>Now playing</div>
              </div>
              <VideoPlayer
                lesson={lessonDetail.lesson}
                playlist={lessonDetail.playlist}
                onLaunchQuiz={() => setShowQuizModal(true)}
              />

              {/* Practical task callout — shown only when this course has one */}
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
                    <div className="gov-card static" style={{
                      padding: '18px 22px',
                      backgroundColor: 'var(--wash-cream)',
                      border: '1px solid var(--orange-300)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '24px',
                      flexWrap: 'wrap',
                      gap: '14px'
                    }}>
                      <div style={{ flex: 1, minWidth: '260px' }}>
                        <strong style={{ display: 'block', fontSize: '15px', color: 'var(--color-text-strong)' }}>
                          Ready for the official practical task?
                        </strong>
                        <span style={{ fontSize: '13px', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
                          Submit your work on <strong>{currentAss.title}</strong>. Your supervisor (Sunita Rao) reviews it — approval raises your official level by one step.
                        </span>
                      </div>

                      <button
                        className="btn btn-primary btn-sm"
                        onClick={() => setActiveAssessmentId(currentAss.id)}
                        style={{ whiteSpace: 'nowrap' }}
                      >
                        Start the Practical Task →
                      </button>
                    </div>
                  );
                }

                return null;
              })()}

              {/* Transcript */}
              <TranscriptViewer chunks={lessonDetail.transcript_chunks} />
            </div>
          ) : (
            <p>Lesson detail unavailable.</p>
          )}
        </div>

        {/* Right: course lessons list */}
        <div className="gov-card static" style={{ padding: '20px' }}>
          <div style={{ borderBottom: '1px solid var(--color-border)', paddingBottom: '12px', marginBottom: '14px' }}>
            <div className="eyebrow-meta" style={{ color: 'var(--color-text-muted)' }}>Course syllabus</div>
            <h3 style={{ fontSize: '15px', marginTop: '4px' }}>
              {lessonDetail?.playlist.title.split('&')[0] || 'Course Lessons'}
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {(currentPlaylistLessons.length > 0 ? currentPlaylistLessons : (lessonDetail?.playlist?.lessons || [])).map(item => {
              const isSelected = item.lesson_id === selectedLessonId;
              return (
                <button
                  key={item.lesson_id}
                  className={`lesson-row ${isSelected ? 'active' : ''}`}
                  onClick={() => setSelectedLessonId(item.lesson_id)}
                >
                  <span className="lesson-chevron">
                    {item.is_completed
                      ? <span style={{ color: 'var(--color-success)', display: 'inline-flex' }}><CheckSmallIcon /></span>
                      : <ChevronRightIcon />}
                  </span>
                  <span style={{ flex: 1, minWidth: 0 }}>
                    <span className="lesson-row-title" style={{ display: 'block' }}>
                      {item.title}
                    </span>
                    <span className="lesson-row-meta">
                      Lesson {item.sequence_no} {item.is_completed ? '• Watched' : `• ${item.duration_minutes} min`}
                    </span>
                  </span>
                </button>
              );
            })}
          </div>

          <div style={{ marginTop: '18px', padding: '12px', backgroundColor: 'var(--wash-ivory)', borderRadius: 'var(--radius-sm)', fontSize: '11.5px', color: 'var(--color-text-muted)', lineHeight: 1.5, display: 'flex', gap: '8px', alignItems: 'flex-start' }}>
            <span style={{ color: 'var(--orange-600)', flex: 'none', marginTop: '1px' }}><LightbulbIcon /></span>
            <span>Videos come from verified open educational sources. Transcripts and practice questions are processed locally on the platform.</span>
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
