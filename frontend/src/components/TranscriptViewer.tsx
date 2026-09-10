import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { TranscriptChunkDTO } from '../types';

interface TranscriptViewerProps {
  chunks: TranscriptChunkDTO[];
}

const SparkIcon: React.FC = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 2l2.1 6.9L21 11l-6.9 2.1L12 20l-2.1-6.9L3 11l6.9-2.1L12 2z" />
  </svg>
);

export const TranscriptViewer: React.FC<TranscriptViewerProps> = ({ chunks }) => {
  const [filterQuery, setFilterQuery] = useState('');
  const navigate = useNavigate();
  const { t } = useTranslation();

  const filteredChunks = chunks.filter(c =>
    c.text_content.toLowerCase().includes(filterQuery.toLowerCase()) ||
    c.topic.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <div className="transcript-panel">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h3 style={{ fontSize: '18px' }}>
            {t('learning.interactiveTranscript')}
          </h3>
          <p className="section-sub">
            {t('learning.transcriptHint')}
          </p>
        </div>

        <div style={{ width: '280px', maxWidth: '100%' }}>
          <input
            type="text"
            className="transcript-search"
            placeholder={t('learning.searchTranscript')}
            value={filterQuery}
            onChange={e => setFilterQuery(e.target.value)}
            aria-label={t('learning.searchTranscript')}
          />
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '420px', overflowY: 'auto', paddingRight: '6px' }}>
        {filteredChunks.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '32px', color: 'var(--color-text-muted)', fontSize: '14px' }}>
            {t('learning.noTranscriptMatch', { query: filterQuery })}
          </div>
        ) : (
          filteredChunks.map(chunk => (
            <div
              key={chunk.chunk_id}
              style={{
                padding: '14px 16px',
                borderRadius: 'var(--radius-md)',
                backgroundColor: 'var(--wash-ivory)',
                border: '1px solid var(--color-border)',
                transition: 'border-color 0.15s, background-color 0.15s'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', flexWrap: 'wrap', gap: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                  <span style={{
                    backgroundColor: 'var(--blue-500)',
                    color: 'var(--color-on-blue)',
                    padding: '2px 8px',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '11px',
                    fontWeight: 700,
                    fontFamily: 'monospace'
                  }}>
                    {chunk.timestamp_label}
                  </span>
                  <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--orange-700)' }}>
                    {chunk.topic}
                  </span>
                </div>

                <button
                  onClick={() => navigate('/copilot')}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--blue-500)',
                    fontSize: '12px',
                    fontWeight: 700,
                    fontFamily: 'var(--font-sans)',
                    cursor: 'pointer',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '5px'
                  }}
                >
                  <SparkIcon /> {t('learning.askCopilot')}
                </button>
              </div>

              <p style={{ fontSize: '14px', color: 'var(--color-text-primary)', lineHeight: 1.6, margin: 0 }}>
                {chunk.text_content}
              </p>

              {chunk.summary && (
                <div style={{ marginTop: '8px', fontSize: '12px', color: 'var(--color-text-muted)', fontStyle: 'italic' }}>
                  Summary: {chunk.summary}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
