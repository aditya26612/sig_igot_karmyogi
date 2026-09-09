import React, { useState } from 'react';
import { TranscriptChunkDTO } from '../types';
import { useAuth } from '../context/AuthContext';

interface TranscriptViewerProps {
  chunks: TranscriptChunkDTO[];
}

export const TranscriptViewer: React.FC<TranscriptViewerProps> = ({ chunks }) => {
  const [filterQuery, setFilterQuery] = useState('');
  const { setIsAssistantOpen } = useAuth();

  const filteredChunks = chunks.filter(c => 
    c.text_content.toLowerCase().includes(filterQuery.toLowerCase()) ||
    c.topic.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <div style={{ backgroundColor: '#ffffff', borderRadius: 'var(--radius-lg)', border: '1px solid #e2e8f0', padding: '24px', boxShadow: 'var(--shadow-sm)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#1a365d' }}>
            Interactive Transcript & Topic Markers
          </h3>
          <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
            Grounding material for practice quizzes and the AI Copilot. Click any timestamp to reference.
          </p>
        </div>

        <div style={{ width: '280px' }}>
          <input
            type="text"
            placeholder="Search transcript text..."
            value={filterQuery}
            onChange={e => setFilterQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '8px 12px',
              borderRadius: '6px',
              border: '1px solid #cbd5e1',
              fontSize: '13px'
            }}
          />
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '420px', overflowY: 'auto', paddingRight: '6px' }}>
        {filteredChunks.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '32px', color: '#94a3b8', fontSize: '14px' }}>
            No transcript segments match "{filterQuery}".
          </div>
        ) : (
          filteredChunks.map(chunk => (
            <div
              key={chunk.chunk_id}
              style={{
                padding: '14px 16px',
                borderRadius: '8px',
                backgroundColor: '#f8fafc',
                border: '1px solid #e2e8f0',
                transition: 'border-color 0.15s, background-color 0.15s'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{
                    backgroundColor: '#1a365d',
                    color: '#ffffff',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '11px',
                    fontWeight: 700,
                    fontFamily: 'monospace'
                  }}>
                    {chunk.timestamp_label}
                  </span>
                  <span style={{ fontSize: '12px', fontWeight: 700, color: '#d97706' }}>
                    {chunk.topic}
                  </span>
                </div>

                <button
                  onClick={() => setIsAssistantOpen(true)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#2563eb',
                    fontSize: '12px',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  ✨ Ask Copilot
                </button>
              </div>

              <p style={{ fontSize: '14px', color: '#334155', lineHeight: 1.6, margin: 0 }}>
                {chunk.text_content}
              </p>

              {chunk.summary && (
                <div style={{ marginTop: '8px', fontSize: '12px', color: '#64748b', fontStyle: 'italic' }}>
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
