import React, { useState } from 'react';
import { CuratedLessonDTO, CuratedPlaylistDTO } from '../types';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

interface VideoPlayerProps {
  lesson: CuratedLessonDTO;
  playlist: CuratedPlaylistDTO;
  onLaunchQuiz: () => void;
}

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
    <div style={{ backgroundColor: '#ffffff', borderRadius: 'var(--radius-lg)', border: '1px solid #e2e8f0', overflow: 'hidden', boxShadow: 'var(--shadow-sm)' }}>
      {/* Video Container (16:9 Aspect Ratio) */}
      <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0, backgroundColor: '#0f172a' }}>
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
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
              <span className="badge badge-saffron">
                {playlist.provider_badge || 'Curated YouTube Resource'}
              </span>
              <span style={{ fontSize: '13px', color: '#64748b' }}>
                Playlist: {playlist.title} (Lesson #{lesson.sequence_no})
              </span>
            </div>
            <h2 style={{ fontSize: '20px', fontWeight: 800, color: '#1a365d' }}>
              {lesson.title}
            </h2>
          </div>

          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
            <a
              href={`https://www.youtube.com/watch?v=${lesson.youtube_video_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-secondary"
              style={{ fontSize: '13px', minHeight: '38px', padding: '8px 14px', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
              title="Open video on YouTube"
            >
              ▶ Watch on YouTube ↗
            </a>
            <button
              className={`btn ${completed ? 'btn-success' : 'btn-secondary'}`}
              onClick={handleMarkProgress}
              style={{ fontSize: '13px', minHeight: '38px', padding: '8px 16px' }}
            >
              {completed ? '✓ Watched' : 'Mark as Watched'}
            </button>
            <button
              className="btn btn-primary"
              onClick={onLaunchQuiz}
              style={{
                fontSize: '13px',
                minHeight: '38px',
                padding: '8px 18px',
                backgroundColor: '#d97706',
                border: '1px solid #b45309',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                fontWeight: 700
              }}
              title="Formative Lesson Practice Quiz • Instant Feedback • Does not alter official competency level"
            >
              <span>🎯</span>
              <span>Lesson Practice Quiz</span>
              <span style={{
                fontSize: '10px',
                padding: '2px 6px',
                backgroundColor: 'rgba(255,255,255,0.25)',
                borderRadius: '4px',
                textTransform: 'uppercase',
                fontWeight: 800
              }}>
                Formative
              </span>
            </button>
            <button
              className="btn btn-navy"
              onClick={() => setIsAssistantOpen(true)}
              style={{ fontSize: '13px', minHeight: '38px', padding: '8px 16px' }}
            >
              ✨ Ask Copilot
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px', fontSize: '13px', color: '#64748b', borderTop: '1px solid #f1f5f9', paddingTop: '12px' }}>
          <span>⏱ Duration: <strong>{lesson.duration_minutes} mins</strong></span>
          <span>🏷 Competency: <strong>{lesson.competency_id}</strong></span>
          <span>📜 Interactive Transcript: <strong>Available Below</strong></span>
        </div>
      </div>
    </div>
  );
};
