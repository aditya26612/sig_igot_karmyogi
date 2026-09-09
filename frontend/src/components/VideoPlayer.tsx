import React, { useState } from 'react';
import { CuratedLessonDTO, CuratedPlaylistDTO } from '../types';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

interface VideoPlayerProps {
  lesson: CuratedLessonDTO;
  playlist: CuratedPlaylistDTO;
  onLaunchQuiz: () => void;
}

const TargetIcon: React.FC = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
    <circle cx="12" cy="12" r="9" />
    <circle cx="12" cy="12" r="5" />
    <circle cx="12" cy="12" r="1.4" fill="currentColor" />
  </svg>
);

const SparkIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 2l2.1 6.9L21 11l-6.9 2.1L12 20l-2.1-6.9L3 11l6.9-2.1L12 2z" />
  </svg>
);

const CheckIcon: React.FC = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const PlayIcon: React.FC = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M6 4l14 8-14 8V4z" />
  </svg>
);

const ClockIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
    <circle cx="12" cy="12" r="9" />
    <polyline points="12 7 12 12 15.5 14" />
  </svg>
);

const TagIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M20.6 13.4L12 22 2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z" />
    <circle cx="7" cy="7" r="1.5" />
  </svg>
);

const DocIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z" />
    <polyline points="14 2 14 8 20 8" />
    <line x1="8" y1="13" x2="16" y2="13" />
    <line x1="8" y1="17" x2="16" y2="17" />
  </svg>
);

export const VideoPlayer: React.FC<VideoPlayerProps> = ({ lesson, playlist, onLaunchQuiz }) => {
  const [completed, setCompleted] = useState<boolean>(lesson.is_completed || false);
  const { setIsAssistantOpen } = useAuth();

  // Keep the button in sync when switching between lessons (e.g. next/prev navigation)
  React.useEffect(() => {
    setCompleted(lesson.is_completed || false);
  }, [lesson.lesson_id, lesson.is_completed]);

  const handleMarkProgress = async () => {
    try {
      await api.recordLessonProgress(lesson.lesson_id, true);
      setCompleted(true);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="video-shell">
      {/* Video Container (16:9 Aspect Ratio) */}
      <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0, backgroundColor: 'var(--blue-900)' }}>
        <iframe
          style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 'none' }}
          src={`https://www.youtube.com/embed/${lesson.youtube_video_id}?rel=0&modestbranding=1`}
          title={lesson.title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerPolicy="strict-origin-when-cross-origin"
          allowFullScreen
        />
      </div>

      {/* Video Metadata & Controls */}
      <div style={{ padding: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '14px', marginBottom: '14px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px', flexWrap: 'wrap' }}>
              <span className="badge badge-saffron">
                {playlist.provider_badge || 'Curated YouTube Resource'}
              </span>
              <span style={{ fontSize: '13px', color: 'var(--color-text-muted)' }}>
                Playlist: {playlist.title} (Lesson #{lesson.sequence_no})
              </span>
            </div>
            <h2 style={{ fontSize: '20px' }}>
              {lesson.title}
            </h2>
          </div>

          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
            <a
              href={`https://www.youtube.com/watch?v=${lesson.youtube_video_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-secondary btn-sm"
              style={{ textDecoration: 'none' }}
              title="Open video on YouTube"
            >
              <PlayIcon /> Watch on YouTube ↗
            </a>
            <button
              className={`btn btn-sm ${completed ? 'btn-success' : 'btn-secondary'}`}
              onClick={handleMarkProgress}
            >
              {completed ? <><CheckIcon /> Watched</> : 'Mark as Watched'}
            </button>
            <button
              className="btn btn-primary btn-sm"
              onClick={onLaunchQuiz}
              title="Formative Lesson Practice Quiz • Instant Feedback • Does not alter official competency level"
            >
              <TargetIcon />
              Lesson Practice Quiz
              <span style={{
                fontSize: '10px',
                padding: '2px 6px',
                backgroundColor: 'rgba(255,255,255,0.25)',
                borderRadius: 'var(--radius-sm)',
                textTransform: 'uppercase',
                fontWeight: 800
              }}>
                Formative
              </span>
            </button>
            <button
              className="btn btn-navy btn-sm"
              onClick={() => setIsAssistantOpen(true)}
            >
              <SparkIcon /> Ask Copilot
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px', fontSize: '13px', color: 'var(--color-text-muted)', borderTop: '1px solid var(--color-border)', paddingTop: '12px', flexWrap: 'wrap' }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}><ClockIcon /> Duration: <strong>{lesson.duration_minutes} mins</strong></span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}><TagIcon /> Competency: <strong>{lesson.competency_id}</strong></span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}><DocIcon /> Interactive Transcript: <strong>Available Below</strong></span>
        </div>
      </div>
    </div>
  );
};
