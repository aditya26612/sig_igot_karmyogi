import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import { AssistantAskResponse, QuickPromptItem } from '../types';

interface MessageItem {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  source?: string;
  timestamp?: string;
  citation?: string;
  actions?: string[];
  justAnswered?: boolean;
}

let msgCounter = 0;
const nextId = () => `msg-${++msgCounter}`;

/* ---------- Markdown-lite renderer (bold, lists, headings, code, math-safe) ---------- */
const renderRichText = (text: string): React.ReactNode => {
  const blocks = text.split(/\n(?=#{1,4}\s|[-*]\s|\d+\.\s|```)/g);
  const elements: React.ReactNode[] = [];

  let codeBuffer: string[] = [];
  let inCode = false;
  text.split('\n').forEach((line, i) => {
    if (line.trim().startsWith('```')) {
      if (inCode) {
        elements.push(
          <pre key={`c-${i}`} style={{
            backgroundColor: '#0f172a', color: '#e2e8f0', borderRadius: '8px',
            padding: '10px 12px', fontSize: '11px', fontFamily: 'monospace',
            overflowX: 'auto', margin: '6px 0'
          }}>{codeBuffer.join('\n')}</pre>
        );
        codeBuffer = []; inCode = false;
      } else {
        inCode = true;
      }
      return;
    }
    if (inCode) { codeBuffer.push(line); return; }

    const headingMatch = line.match(/^(#{1,4})\s+(.*)/);
    if (headingMatch) {
      elements.push(<div key={`h-${i}`} style={{ fontWeight: 800, fontSize: '13px', color: '#1a365d', margin: '8px 0 4px' }}>{renderInline(headingMatch[2])}</div>);
      return;
    }
    const bulletMatch = line.match(/^\s*[-*]\s+(.*)/);
    if (bulletMatch) {
      elements.push(
        <div key={`b-${i}`} style={{ display: 'flex', gap: '8px', margin: '3px 0' }}>
          <span style={{ color: '#d97706', fontWeight: 800 }}>•</span>
          <span>{renderInline(bulletMatch[1])}</span>
        </div>
      );
      return;
    }
    const numMatch = line.match(/^\s*(\d+)\.\s+(.*)/);
    if (numMatch) {
      elements.push(
        <div key={`n-${i}`} style={{ display: 'flex', gap: '8px', margin: '3px 0' }}>
          <span style={{ color: '#d97706', fontWeight: 800, minWidth: '16px' }}>{numMatch[1]}.</span>
          <span>{renderInline(numMatch[2])}</span>
        </div>
      );
      return;
    }
    if (line.trim() === '') {
      elements.push(<div key={`s-${i}`} style={{ height: '6px' }} />);
      return;
    }
    elements.push(<div key={`t-${i}`}>{renderInline(line)}</div>);
  });
  if (inCode && codeBuffer.length) {
    elements.push(<pre key="c-last" style={{ backgroundColor: '#0f172a', color: '#e2e8f0', borderRadius: '8px', padding: '10px', fontSize: '11px', fontFamily: 'monospace', overflowX: 'auto' }}>{codeBuffer.join('\n')}</pre>);
  }
  return <>{elements}</>;
};

const renderInline = (text: string): React.ReactNode => {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[[0-9]{1,2}:[0-9]{2}\]|`[^`]+`)/g);
  return (
    <>
      {parts.map((p, i) => {
        if (p.startsWith('**') && p.endsWith('**')) return <strong key={i} style={{ color: '#0f172a' }}>{p.slice(2, -2)}</strong>;
        if (p.startsWith('`') && p.endsWith('`')) return <code key={i} style={{ backgroundColor: '#f1f5f9', padding: '1px 5px', borderRadius: '4px', fontFamily: 'monospace', fontSize: '12px' }}>{p.slice(1, -1)}</code>;
        if (p.match(/^\[[0-9]{1,2}:[0-9]{2}\]$/)) return (
          <span key={i} style={{ backgroundColor: '#fef3c7', color: '#92400e', fontWeight: 700, padding: '1px 6px', borderRadius: '4px', fontFamily: 'monospace', fontSize: '11px' }}>{p}</span>
        );
        if (p.startsWith('*') && p.endsWith('*') && p.length > 2) return <em key={i}>{p.slice(1, -1)}</em>;
        return <span key={i}>{p}</span>;
      })}
    </>
  );
};

const WELCOME = "Namaste! 🙏 I am your **AI Learning Copilot** for India's Official Statistical System.\n\nI help you master:\n- Survey sampling & design\n- SQL, Python & R for statistics\n- Data quality & official methodology\n\nEvery answer is **grounded in your curriculum** with exact timestamp citations. What shall we explore?";

export const AssistantDrawer: React.FC = () => {
  const { isAssistantOpen, setIsAssistantOpen, selectedLessonId } = useAuth();
  const [messages, setMessages] = useState<MessageItem[]>([
    { id: nextId(), sender: 'assistant', text: WELCOME }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [thinkingStage, setThinkingStage] = useState(0);
  const [prompts, setPrompts] = useState<QuickPromptItem[]>([]);
  const [maximized, setMaximized] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [listening, setListening] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    async function loadPrompts() {
      try {
        const data = await api.getQuickPrompts();
        setPrompts(data);
      } catch (err) {
        console.error(err);
      }
    }
    loadPrompts();
  }, []);

  // Smooth auto-scroll as the conversation grows
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [messages, loading, thinkingStage]);

  // Staged thinking indicator while the copilot composes its answer
  useEffect(() => {
    if (!loading) { setThinkingStage(0); return; }
    setThinkingStage(1);
    const t2 = setTimeout(() => setThinkingStage(2), 1200);
    const t3 = setTimeout(() => setThinkingStage(3), 2400);
    return () => { clearTimeout(t2); clearTimeout(t3); };
  }, [loading]);

  const handleSend = useCallback(async (questionText?: string) => {
    const q = (questionText || inputValue).trim();
    if (!q || loading) return;

    const userMsg: MessageItem = { id: nextId(), sender: 'user', text: q };
    const base = messages.length <= 1 ? messages : messages;
    setMessages([...base, userMsg]);
    setInputValue('');
    setLoading(true);

    try {
      const res: AssistantAskResponse = await api.askAssistant(
        q,
        'LESSON',
        selectedLessonId || 'sampling-lesson-3',
        'COMP-SAMPLING'
      );
      setMessages(prev => [...prev, {
        id: nextId(),
        sender: 'assistant',
        text: res.answer,
        source: res.source_lesson_title,
        timestamp: res.timestamp_label,
        citation: res.citation_snippet,
        actions: res.suggested_actions,
        justAnswered: true
      }]);
    } catch (err: any) {
      setMessages(prev => [...prev, {
        id: nextId(),
        sender: 'assistant',
        text: "I encountered an issue connecting to the AI service. The copilot works offline too — please retry, or reopen this lesson and ask again.",
      }]);
    } finally {
      setLoading(false);
    }
  }, [inputValue, loading, messages, selectedLessonId]);

  const handleCopy = async (m: MessageItem) => {
    try {
      await navigator.clipboard.writeText(m.text);
      setCopiedId(m.id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch { /* clipboard unavailable */ }
  };

  const handleClearChat = () => {
    setMessages([{ id: nextId(), sender: 'assistant', text: WELCOME }]);
  };

  // Voice input via Web Speech API (Chrome/Edge)
  const toggleVoice = () => {
    const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SR) { alert('Voice input is supported in Chrome/Edge.'); return; }
    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }
    const rec = new SR();
    rec.lang = 'en-IN';
    rec.interimResults = false;
    rec.onresult = (e: any) => {
      const transcript = e.results[0][0].transcript;
      setInputValue(prev => (prev ? prev + ' ' : '') + transcript);
    };
    rec.onend = () => setListening(false);
    rec.onerror = () => setListening(false);
    recognitionRef.current = rec;
    setListening(true);
    rec.start();
  };

  const drawerStyle: React.CSSProperties = maximized
    ? { position: 'fixed', top: '24px', left: '24px', right: '24px', bottom: '24px', width: 'auto', maxHeight: 'calc(100vh - 48px)', height: 'calc(100vh - 48px)' }
    : {};

  if (!isAssistantOpen) {
    return (
      <>
        <button
          className="assistant-trigger-btn"
          onClick={() => { setIsAssistantOpen(true); setTimeout(() => inputRef.current?.focus(), 300); }}
          title="Open AI Learning Copilot"
        >
          <span style={{ fontSize: '24px' }}>✨</span>
        </button>
        <div className="assistant-trigger-label" onClick={() => { setIsAssistantOpen(true); }}>
          Ask Karmayogi Copilot
        </div>
      </>
    );
  }

  const STAGES = ['Reading your question…', 'Searching curriculum transcripts…', 'Verifying with lesson timestamps…', 'Composing grounded answer…'];

  return (
    <div className="assistant-drawer" style={drawerStyle}>
      {/* Header */}
      <div className="copilot-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div className="copilot-avatar">✨</div>
          <div>
            <div style={{ fontSize: '14px', fontWeight: 800, fontFamily: 'var(--font-heading)' }}>
              AI Learning Copilot
            </div>
            <div style={{ fontSize: '10px', color: '#93c5fd', display: 'flex', alignItems: 'center', gap: '5px' }}>
              <span className="online-dot" /> Online • Grounded in MoSPI curriculum
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '4px', alignItems: 'center' }}>
          <button className="copilot-icon-btn" onClick={handleClearChat} title="New conversation">⟳</button>
          <button className="copilot-icon-btn" onClick={() => setMaximized(m => !m)} title={maximized ? 'Restore' : 'Maximize'}>
            {maximized ? '⤡' : '⤢'}
          </button>
          <button className="copilot-icon-btn" onClick={() => setIsAssistantOpen(false)} title="Close">✕</button>
        </div>
      </div>

      {/* Messages */}
      <div className="copilot-messages">
        {messages.map(m => (
          <div key={m.id} className={m.sender === 'user' ? 'copilot-row-user' : 'copilot-row-bot'}>
            {m.sender === 'assistant' && <div className="copilot-avatar copilot-avatar-sm">✨</div>}
            <div
              className={m.sender === 'user' ? 'copilot-bubble-user' : 'copilot-bubble-bot'}
              style={m.justAnswered ? { animation: 'copilotFadeIn 0.4s ease' } : undefined}
            >
              <div className="copilot-bubble-text">{renderRichText(m.text)}</div>

              {m.citation && (
                <div className="copilot-citation-card">
                  <div style={{ fontWeight: 700, fontSize: '10px', color: '#92400e', textTransform: 'uppercase', letterSpacing: '0.03em' }}>
                    📎 Grounded Citation
                  </div>
                  <div style={{ fontSize: '11px', color: '#64748b', marginTop: '3px', lineHeight: 1.45, fontStyle: 'italic' }}>
                    "{m.citation}"
                  </div>
                </div>
              )}

              {m.source && (
                <div className="copilot-source-row">
                  <span style={{ color: '#d97706', fontWeight: 700 }}>Source:</span> {m.source}
                  {m.timestamp && <span className="copilot-timestamp-chip">▶ {m.timestamp}</span>}
                </div>
              )}

              {m.sender === 'assistant' && !loading && m.id !== messages[0].id && (
                <div className="copilot-msg-actions">
                  <button className="copilot-mini-btn" onClick={() => handleCopy(m)}>
                    {copiedId === m.id ? '✓ Copied' : '⧉ Copy'}
                  </button>
                </div>
              )}

              {m.actions && m.actions.length > 0 && !loading && (
                <div style={{ marginTop: '10px', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {m.actions.slice(0, 3).map((act, i) => (
                    <button key={i} className="copilot-suggested-btn" onClick={() => handleSend(act)}>
                      ↳ {act}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="copilot-row-bot">
            <div className="copilot-avatar copilot-avatar-sm">✨</div>
            <div className="copilot-bubble-bot copilot-thinking">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div className="typing-dots"><span /><span /><span /></div>
                <span style={{ fontSize: '11.5px', color: '#64748b', fontWeight: 600 }}>
                  {STAGES[Math.min(thinkingStage, STAGES.length - 1)]}
                </span>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Quick prompts (hidden once conversation starts) */}
      {messages.length <= 1 && (
        <div className="copilot-prompts-row">
          {prompts.slice(0, 4).map((p, idx) => (
            <button key={idx} className="copilot-prompt-chip" onClick={() => handleSend(p.prompt)}>
              {p.label}
            </button>
          ))}
        </div>
      )}

      {/* Input bar */}
      <div className="copilot-input-bar">
        <input
          ref={inputRef}
          type="text"
          placeholder="Ask about sampling, SQL, weights, formulas…"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          disabled={loading}
        />
        {listening && <span className="copilot-rec-pulse" title="Listening…">🎙</span>}
        <button className="copilot-mic-btn" onClick={toggleVoice} title="Voice input (English)">🎤</button>
        <button
          className="copilot-send-btn"
          disabled={loading || !inputValue.trim()}
          onClick={() => handleSend()}
          title="Send"
        >
          ➤
        </button>
      </div>
      <div className="copilot-disclaimer">
        Answers are grounded only in approved curriculum transcripts. Copilot never changes competency levels or reveals quiz answers.
      </div>
    </div>
  );
};
