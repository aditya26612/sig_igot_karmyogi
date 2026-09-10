import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { api } from '../../api/client';
import { getCurrentLang } from '../../i18n';
import { AssistantAskResponse, QuickPromptItem, CuratedLessonDTO } from '../../types';

/* ==========================================================================
   AI Learning Copilot — full-page workspace
   One column of conversation, a slim context strip, and a calm input bar.
   ========================================================================== */

interface MessageItem {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  source?: string;
  timestamp?: string;
  citation?: string;
  actions?: string[];
  error?: boolean;
}

let msgCounter = 0;
const nextId = () => `msg-${Date.now()}-${++msgCounter}`;

/* ---------- Minimal ambient types for Web Speech API (Chrome/Edge) ---------- */
interface SpeechRecognitionLike {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  onresult: ((e: any) => void) | null;
  onend: (() => void) | null;
  onerror: ((e: any) => void) | null;
  start: () => void;
  stop: () => void;
  abort: () => void;
}
type SpeechRecognitionCtor = new () => SpeechRecognitionLike;
declare global {
  interface Window {
    SpeechRecognition?: SpeechRecognitionCtor;
    webkitSpeechRecognition?: SpeechRecognitionCtor;
  }
}

/* ---------- Inline rendering: bold / italic / code / timestamps ---------- */
const renderInline = (text: string): React.ReactNode => {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|\[[0-9]{1,2}:[0-9]{2}\]|`[^`]+`)/g);
  return (
    <>
      {parts.map((p, i) => {
        if (p.startsWith('**') && p.endsWith('**')) return <strong key={i} style={{ color: 'var(--color-text-strong)' }}>{p.slice(2, -2)}</strong>;
        if (p.startsWith('`') && p.endsWith('`') && p.length > 2) return <code key={i} className="copilot-code-inline">{p.slice(1, -1)}</code>;
        if (/^\[[0-9]{1,2}:[0-9]{2}\]$/.test(p)) return <span key={i} className="copilot-timestamp-chip">{p}</span>;
        if (p.startsWith('*') && p.endsWith('*') && p.length > 2) return <em key={i}>{p.slice(1, -1)}</em>;
        return <span key={i}>{p}</span>;
      })}
    </>
  );
};

/* ---------- Structured block renderer (full-line fences only) ---------- */
type BlockKind = 'heading' | 'bullet' | 'numbered' | 'code' | 'quote' | 'text';

const renderRichText = (text: string): React.ReactNode => {
  const elements: React.ReactNode[] = [];
  let codeBuffer: string[] = [];
  let inCode = false;

  text.split('\n').forEach((line, i) => {
    // Only a fence that occupies the whole line toggles code mode — stray backticks stay literal.
    if (line.trim().startsWith('```')) {
      if (inCode) {
        elements.push(<pre key={`c-${i}`} className="copilot-code-block">{codeBuffer.join('\n')}</pre>);
        codeBuffer = [];
        inCode = false;
      } else {
        inCode = true;
      }
      return;
    }
    if (inCode) { codeBuffer.push(line); return; }

    const kind: BlockKind =
      line.match(/^#{1,4}\s/) ? 'heading' :
      line.match(/^\s*[-*]\s+/) ? 'bullet' :
      line.match(/^\s*\d+\.\s+/) ? 'numbered' :
      line.match(/^\s*>\s+/) ? 'quote' : 'text';

    if (kind === 'heading') {
      const m = line.match(/^#{1,4}\s+(.*)/)!;
      elements.push(<div key={`h-${i}`} className="copilot-block-heading">{renderInline(m[1])}</div>);
    } else if (kind === 'bullet') {
      const m = line.match(/^\s*[-*]\s+(.*)/)!;
      elements.push(
        <div key={`b-${i}`} className="copilot-block-list-row">
          <span className="copilot-bullet-dot" aria-hidden="true" />
          <span>{renderInline(m[1])}</span>
        </div>
      );
    } else if (kind === 'numbered') {
      const m = line.match(/^\s*(\d+)\.\s+(.*)/)!;
      elements.push(
        <div key={`n-${i}`} className="copilot-block-list-row">
          <span className="copilot-number-dot">{m[1]}.</span>
          <span>{renderInline(m[2])}</span>
        </div>
      );
    } else if (kind === 'quote') {
      const m = line.match(/^\s*>\s+(.*)/)!;
      elements.push(<div key={`q-${i}`} className="copilot-block-quote">{renderInline(m[1])}</div>);
    } else if (line.trim() === '') {
      elements.push(<div key={`s-${i}`} className="copilot-block-spacer" />);
    } else if (line.includes('---') && line.replace(/[\s-]/g, '') === '') {
      // horizontal rules are decoration from an older prompt; drop them
    } else {
      elements.push(<div key={`t-${i}`}>{renderInline(line)}</div>);
    }
  });

  if (inCode && codeBuffer.length) {
    elements.push(<pre key="c-last" className="copilot-code-block">{codeBuffer.join('\n')}</pre>);
  }
  return <>{elements}</>;
};

/* ---------- Icons (SVG only — no emoji chrome) ---------- */
const SparkIcon: React.FC<{ size?: number }> = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 2l2.1 6.9L21 11l-6.9 2.1L12 20l-2.1-6.9L3 11l6.9-2.1L12 2z" />
  </svg>
);

const MicIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" />
    <path d="M19 10v1a7 7 0 0 1-14 0v-1" />
    <line x1="12" y1="18" x2="12" y2="22" />
  </svg>
);

const MicOffIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" />
    <path d="M19 10v1a7 7 0 0 1-14 0v-1" />
    <line x1="1" y1="1" x2="23" y2="23" />
  </svg>
);

const SendIcon: React.FC = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M3.4 20.4l17.4-7.5a1 1 0 0 0 0-1.8L3.4 3.6a1 1 0 0 0-1.4 1.1L4 11l9 1-9 1-2 6.3a1 1 0 0 0 1.4 1.1z" />
  </svg>
);

const CopyIcon: React.FC = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <rect x="9" y="9" width="12" height="12" rx="2" />
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
  </svg>
);

const CheckIcon: React.FC = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const DocIcon: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
    <polyline points="14 2 14 8 20 8" />
  </svg>
);

const ClockIcon: React.FC = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="9" />
    <polyline points="12 7 12 12 15.5 14" />
  </svg>
);

const RefreshIcon: React.FC = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M21 12a9 9 0 1 1-2.64-6.36" />
    <polyline points="21 3 21 9 15 9" />
  </svg>
);

const ChevronIcon: React.FC<{ open?: boolean }> = ({ open }) => (
  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"
    style={{ transform: open ? 'rotate(90deg)' : 'none', transition: 'transform 0.15s ease' }} aria-hidden="true">
    <polyline points="9 6 15 12 9 18" />
  </svg>
);

export const CopilotView: React.FC = () => {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const lessonParam = searchParams.get('lesson');

  const [messages, setMessages] = useState<MessageItem[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [thinkingStage, setThinkingStage] = useState(0);
  const [prompts, setPrompts] = useState<QuickPromptItem[]>([]);
  const [lessons, setLessons] = useState<CuratedLessonDTO[]>([]);
  const [selectedLessonId, setSelectedLessonId] = useState<string | null>(lessonParam);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [sourcesOpenId, setSourcesOpenId] = useState<string | null>(null);
  const [listening, setListening] = useState(false);
  const [voiceError, setVoiceError] = useState<string | null>(null);
  const [lastQuestion, setLastQuestion] = useState<string | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);
  const speechSupported = typeof window !== 'undefined'
    && !!(window.SpeechRecognition || window.webkitSpeechRecognition);

  // Welcome message on first render (re-renders on language change via t())
  const welcomeMsg: MessageItem = {
    id: 'welcome',
    sender: 'assistant',
    text: t('copilot.welcome'),
  };
  const activeMessages = messages.length > 0 ? messages : [welcomeMsg];

  /* Load curriculum lessons (for grounding context picker) */
  useEffect(() => {
    async function load() {
      try {
        const pls = await api.getPlaylists();
        const allLessons: CuratedLessonDTO[] = [];
        for (const pl of pls.slice(0, 8)) {
          try {
            const d = await api.getPlaylistDetail(pl.playlist_id);
            if (d?.lessons) allLessons.push(...d.lessons);
          } catch { /* playlist detail optional */ }
        }
        setLessons(allLessons);
      } catch (err) {
        console.error('Failed to load copilot context:', err);
      }
    }
    load();
  }, []);

  /* Refresh starter prompts when the pinned lesson or language changes */
  useEffect(() => {
    let cancelled = false;
    api.getQuickPrompts(selectedLessonId)
      .then(p => { if (!cancelled) setPrompts(p); })
      .catch(() => { if (!cancelled) setPrompts([]); });
    return () => { cancelled = true; };
  }, [selectedLessonId, getCurrentLang()]);

  // Keep lesson selection synced with ?lesson= deep-links (e.g. from video page "Ask Copilot")
  useEffect(() => {
    const lp = searchParams.get('lesson');
    if (lp) setSelectedLessonId(lp);
  }, [searchParams]);

  // Auto-scroll as the conversation grows
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [activeMessages.length, loading, thinkingStage]);

  // Staged thinking indicator
  useEffect(() => {
    if (!loading) { setThinkingStage(0); return; }
    setThinkingStage(1);
    const t2 = setTimeout(() => setThinkingStage(2), 1200);
    const t3 = setTimeout(() => setThinkingStage(3), 2400);
    return () => { clearTimeout(t2); clearTimeout(t3); };
  }, [loading]);

  // Cleanup speech recognition on unmount
  useEffect(() => () => {
    recognitionRef.current?.abort();
    recognitionRef.current = null;
  }, []);

  const sendQuestion = useCallback(async (questionText: string) => {
    const q = questionText.trim();
    if (!q || loading) return;

    setMessages(prev => [...prev, { id: nextId(), sender: 'user', text: q }]);
    setInputValue('');
    setLastQuestion(q);
    setLoading(true);
    setVoiceError(null);

    try {
      // Ground honestly: only pass a lesson when the learner picked one.
      const res: AssistantAskResponse = await api.askAssistant(
        q,
        selectedLessonId ? 'LESSON' : 'GENERAL',
        selectedLessonId,
        selectedLessonId ? lessons.find(l => l.lesson_id === selectedLessonId)?.competency_id : undefined
      );
      setMessages(prev => [...prev, {
        id: nextId(),
        sender: 'assistant',
        text: res.answer,
        source: res.source_lesson_title,
        timestamp: res.timestamp_label,
        citation: res.citation_snippet,
        actions: res.suggested_actions,
      }]);
    } catch {
      setMessages(prev => [...prev, {
        id: nextId(),
        sender: 'assistant',
        text: t('copilot.errorWithRetry'),
        error: true,
      }]);
    } finally {
      setLoading(false);
    }
  }, [loading, selectedLessonId, lessons, t]);

  const handleSend = useCallback(() => {
    sendQuestion(inputValue);
  }, [inputValue, sendQuestion]);

  const handleCopy = async (m: MessageItem) => {
    try {
      await navigator.clipboard.writeText(m.text);
      setCopiedId(m.id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch { /* clipboard unavailable */ }
  };

  const handleNewChat = () => {
    if (loading) return; // guard: clearing mid-request would orphan the reply
    setMessages([]);
    setSourcesOpenId(null);
    setLastQuestion(null);
  };

  /* ---- Voice input (Web Speech API; SVG mic, cleanup on stop/unmount) ---- */
  const showVoiceError = (key: string) => {
    setVoiceError(t(key));
    setTimeout(() => setVoiceError(null), 5000);
  };

  const stopListening = () => {
    try { recognitionRef.current?.stop(); } catch { /* already stopped */ }
    recognitionRef.current = null;
    setListening(false);
  };

  const toggleVoice = () => {
    if (listening) {
      stopListening();
      return;
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      showVoiceError('copilot.voiceUnsupported');
      return;
    }
    const rec = new SR();
    rec.lang = getCurrentLang() === 'hi' ? 'hi-IN' : 'en-IN';
    rec.interimResults = false;
    rec.continuous = false;
    rec.onresult = (e: any) => {
      const transcript = e.results[0][0].transcript;
      setInputValue(prev => (prev ? prev + ' ' : '') + transcript);
    };
    rec.onend = () => setListening(false);
    rec.onerror = (e: any) => {
      const code = e?.error;
      setListening(false);
      // 'aborted'/'no-speech' are user actions or silence, not failures — stay quiet.
      if (code === 'aborted' || code === 'no-speech') return;
      if (code === 'not-allowed' || code === 'service-not-allowed') {
        showVoiceError('copilot.voiceErrorPermission');
      } else if (code === 'audio-capture') {
        showVoiceError('copilot.voiceErrorNoMic');
      } else if (code === 'network') {
        showVoiceError('copilot.voiceErrorNetwork');
      } else {
        showVoiceError('copilot.voiceError');
      }
    };
    recognitionRef.current = rec;
    try {
      rec.start();
      setListening(true);
    } catch {
      recognitionRef.current = null;
      showVoiceError('copilot.voiceErrorBusy');
    }
  };

  const selectedLesson = lessons.find(l => l.lesson_id === selectedLessonId);
  const STAGES = [t('copilot.thinking1'), t('copilot.thinking2'), t('copilot.thinking3'), t('copilot.thinking4')];
  const showPrompts = activeMessages.length <= 1;

  return (
    <div className="copilot-page">
      <div className="gov-container copilot-container">
        {/* ============ Sidebar: grounding context ============ */}
        <aside className="copilot-side" aria-label={t('copilot.contextTitle')}>
          <div className="copilot-side-head">
            <div className="copilot-avatar-lg"><SparkIcon size={20} /></div>
            <div>
              <div className="copilot-side-title">{t('copilot.name')}</div>
              <div className="copilot-side-sub">
                <span className="online-dot" /> {t('copilot.groundedBadge')}
              </div>
            </div>
          </div>

          <div className="copilot-side-section">
            <label className="copilot-side-label" htmlFor="copilot-context">{t('copilot.contextTitle')}</label>
            <select
              id="copilot-context"
              className="copilot-context-select"
              value={selectedLessonId || ''}
              onChange={e => {
                const v = e.target.value || null;
                setSelectedLessonId(v);
                if (v) setSearchParams({ lesson: v }, { replace: true });
                else setSearchParams({}, { replace: true });
              }}
              aria-label={t('copilot.contextTitle')}
            >
              <option value="">{t('copilot.contextAll')}</option>
              {lessons.map(l => (
                <option key={l.lesson_id} value={l.lesson_id}>
                  {l.title}
                </option>
              ))}
            </select>
            <div className="copilot-context-note">
              {selectedLesson
                ? t('copilot.contextPinned', { title: selectedLesson.title })
                : t('copilot.contextNone')}
            </div>
          </div>

          <div className="copilot-side-disclaimer">
            {t('copilot.disclaimer')}
          </div>
        </aside>

        {/* ============ Chat column ============ */}
        <section className="copilot-main" aria-label={t('copilot.name')}>
          {/* Header */}
          <div className="copilot-main-head">
            <div className="copilot-main-title-row">
              <div className="copilot-avatar"><SparkIcon size={18} /></div>
              <div>
                <div className="copilot-main-title">{t('copilot.name')}</div>
                <div className="copilot-main-sub">
                  <span className="online-dot" /> {t('copilot.subtitle')}
                </div>
              </div>
            </div>
            <div className="copilot-head-actions">
              <button className="copilot-icon-btn" onClick={handleNewChat} disabled={loading || messages.length === 0} title={t('copilot.newChat')}>
                <RefreshIcon />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="copilot-msgs">
            {activeMessages.map(m => (
              <div key={m.id} className={m.sender === 'user' ? 'copilot-row-user' : 'copilot-row-bot'}>
                {m.sender === 'assistant' && (
                  <div className="copilot-avatar copilot-avatar-sm"><SparkIcon size={14} /></div>
                )}

                {m.sender === 'user' ? (
                  <div className="copilot-bubble-user">
                    <div className="copilot-bubble-text">{m.text}</div>
                  </div>
                ) : (
                  <div className={`copilot-card-bot ${m.error ? 'copilot-card-error' : ''}`}>
                    <div className="copilot-bubble-text">{renderRichText(m.text)}</div>

                    {/* Grounded citation (only when the backend actually found one) */}
                    {m.citation && (
                      <div className="copilot-citation-card">
                        <div className="copilot-citation-title">
                          <DocIcon /> {t('copilot.citation')}
                        </div>
                        <div className="copilot-citation-text">"{m.citation}"</div>
                      </div>
                    )}

                    {/* Copy / Sources toolbar */}
                    {m.id !== 'welcome' && !loading && (
                      <div className="copilot-msg-actions">
                        <button className="copilot-mini-btn" onClick={() => handleCopy(m)}>
                          {copiedId === m.id ? <><CheckIcon /> {t('copilot.copied')}</> : <><CopyIcon /> {t('copilot.copy')}</>}
                        </button>
                        {(m.source || m.timestamp) && (
                          <button
                            className="copilot-mini-btn"
                            onClick={() => setSourcesOpenId(sourcesOpenId === m.id ? null : m.id)}
                          >
                            <DocIcon /> {t('copilot.source')} {sourcesOpenId === m.id ? <ChevronIcon open /> : <ChevronIcon />}
                          </button>
                        )}
                        {m.error && lastQuestion && (
                          <button className="copilot-mini-btn copilot-retry-btn" onClick={() => { setMessages(prev => prev.filter(x => x.id !== m.id)); sendQuestion(lastQuestion); }}>
                            <RefreshIcon /> {t('common.retry')}
                          </button>
                        )}
                      </div>
                    )}

                    {/* Sources drawer */}
                    {sourcesOpenId === m.id && (m.source || m.timestamp) && (
                      <div className="copilot-sources-drawer">
                        {m.source && (
                          <div className="copilot-source-row">
                            <DocIcon /> <strong>{m.source}</strong>
                            {m.timestamp && <span className="copilot-timestamp-chip"><ClockIcon /> {m.timestamp}</span>}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Suggested follow-ups: compact, persistent after first answer */}
                    {m.actions && m.actions.length > 0 && !loading && (
                      <div className="copilot-suggestions">
                        {m.actions.slice(0, 3).map((act, i) => (
                          <button key={i} className="copilot-suggested-btn" onClick={() => sendQuestion(act)}>
                            {act}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}

            {/* Staged thinking indicator with progressive checkmarks */}
            {loading && (
              <div className="copilot-row-bot">
                <div className="copilot-avatar copilot-avatar-sm"><SparkIcon size={14} /></div>
                <div className="copilot-card-bot copilot-thinking">
                  {STAGES.slice(0, Math.max(thinkingStage, 1)).map((s, i) => {
                    const isCurrent = i === Math.min(thinkingStage, STAGES.length - 1);
                    const done = i < thinkingStage;
                    return (
                      <div key={i} className={`copilot-stage ${isCurrent ? 'current' : done ? 'done' : ''}`}>
                        {done
                          ? <span className="copilot-stage-check"><CheckIcon /></span>
                          : <span className="copilot-stage-dot" />}
                        <span>{s}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Quick prompts (welcome state) */}
          {showPrompts && prompts.length > 0 && (
            <div className="copilot-prompt-grid">
              {prompts.slice(0, 4).map((p, idx) => (
                <button key={idx} className="copilot-prompt-chip" onClick={() => sendQuestion(p.prompt)}>
                  <span className="copilot-prompt-cat">{p.category}</span>
                  <span>{p.label}</span>
                </button>
              ))}
            </div>
          )}

          {/* Input bar — pill with mic/send swap */}
          <div className="copilot-input-wrap">
            {voiceError && <div className="copilot-voice-error" role="alert">{voiceError}</div>}
            <div className="copilot-input-bar">
              <input
                ref={inputRef}
                type="text"
                placeholder={t('copilot.placeholder')}
                value={inputValue}
                onChange={e => setInputValue(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
                disabled={loading}
                aria-label={t('copilot.placeholder')}
              />
              <div className="copilot-input-actions">
                {speechSupported && (
                  <button
                    className={`copilot-mic-btn ${listening ? 'listening' : ''}`}
                    onClick={toggleVoice}
                    disabled={loading}
                    title={listening ? t('copilot.stopVoice') : t('copilot.startVoice')}
                    aria-pressed={listening}
                    aria-label={listening ? t('copilot.stopVoice') : t('copilot.startVoice')}
                  >
                    {listening ? <MicOffIcon /> : <MicIcon />}
                  </button>
                )}
                <button
                  className="copilot-send-btn"
                  disabled={loading || !inputValue.trim()}
                  onClick={handleSend}
                  title={t('copilot.send')}
                  aria-label={t('copilot.send')}
                >
                  <SendIcon />
                </button>
              </div>
            </div>
            {listening && (
              <div className="copilot-listening-note">
                <span className="copilot-rec-pulse" /> {t('copilot.listening')}
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};
