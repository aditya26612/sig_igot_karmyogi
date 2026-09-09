import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export const Navbar: React.FC = () => {
  const { currentUser, demoAccounts, switchDemoUser, activeView, setActiveView, setIsAssistantOpen } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <header style={{ position: 'sticky', top: 0, zIndex: 100, backgroundColor: '#ffffff', boxShadow: '0 2px 8px rgba(0,0,0,0.06)' }}>
      {/* Top Official Gov Header */}
      <div style={{ backgroundColor: '#0f294a', color: '#ffffff', padding: '6px 0', fontSize: '12px' }}>
        <div className="gov-container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontWeight: 600, letterSpacing: '0.04em' }}>GOVERNMENT OF INDIA</span>
            <span style={{ opacity: 0.4 }}>|</span>
            <span>Ministry of Statistics and Programme Implementation (MoSPI)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <span>National Statistical System Cadre Training</span>
            <span style={{ opacity: 0.4 }}>|</span>
            <span style={{ color: '#fde68a', fontWeight: 600 }}>iGOT Karmayogi Architecture</span>
          </div>
        </div>
      </div>

      {/* Tricolor Accent */}
      <div className="tricolor-strip" />

      {/* Main Navbar */}
      <div style={{ borderBottom: '1px solid #e2e8f0', backgroundColor: '#ffffff' }}>
        <div className="gov-container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '70px' }}>
          {/* Brand */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px', cursor: 'pointer' }} onClick={() => setActiveView('home')}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '8px',
              background: 'linear-gradient(135deg, #1a365d 0%, #d97706 100%)',
              color: '#ffffff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 800,
              fontSize: '18px',
              letterSpacing: '-0.02em',
              boxShadow: '0 2px 5px rgba(0,0,0,0.15)'
            }}>
              iGOT
            </div>
            <div>
              <div style={{ fontSize: '18px', fontWeight: 800, color: '#1a365d', fontFamily: 'var(--font-heading)', lineHeight: 1.1 }}>
                iGOT Karmayogi <span style={{ color: '#d97706', fontSize: '14px', fontWeight: 600 }}>MoSPI</span>
              </div>
              <div style={{ fontSize: '12px', color: '#64748b', fontWeight: 500 }}>
                Official Statistical System Competency Platform
              </div>
            </div>
          </div>

          {/* 5 Core Learner Navigation Tabs */}
          <nav style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <button
              className={`nav-tab ${activeView === 'home' ? 'active' : ''}`}
              onClick={() => setActiveView('home')}
            >
              Home
            </button>
            <button
              className={`nav-tab ${activeView === 'learning' ? 'active' : ''}`}
              onClick={() => setActiveView('learning')}
            >
              My Learning
            </button>
            <button
              className={`nav-tab ${activeView === 'gaps' ? 'active' : ''}`}
              onClick={() => setActiveView('gaps')}
            >
              Skill Gaps
            </button>
            <button
              className={`nav-tab ${activeView === 'career' ? 'active' : ''}`}
              onClick={() => setActiveView('career')}
            >
              Career Path
            </button>
            <button
              className="nav-tab"
              onClick={() => setIsAssistantOpen(true)}
              style={{ color: '#d97706', fontWeight: 700 }}
            >
              ✨ AI Copilot
            </button>

            {/* Role-Specific Portal Links */}
            {currentUser?.role === 'REVIEWER' && (
              <button
                className={`nav-tab ${activeView === 'reviewer' ? 'active' : ''}`}
                onClick={() => setActiveView('reviewer')}
                style={{ backgroundColor: '#fef3c7', borderRadius: '6px', color: '#92400e', fontWeight: 700, marginLeft: '8px' }}
              >
                🔍 Supervisor Queue
              </button>
            )}

            {currentUser?.role === 'ADMIN' && (
              <button
                className={`nav-tab ${activeView === 'admin' ? 'active' : ''}`}
                onClick={() => setActiveView('admin')}
                style={{ backgroundColor: '#ebf8ff', borderRadius: '6px', color: '#1e40af', fontWeight: 700, marginLeft: '8px' }}
              >
                👑 Admin Console
              </button>
            )}
          </nav>

          {/* Demo Persona Switcher */}
          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                padding: '8px 14px',
                borderRadius: '8px',
                border: '1px solid #cbd5e1',
                backgroundColor: '#f8fafc',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                backgroundColor: currentUser?.role === 'ADMIN' ? '#1e40af' : currentUser?.role === 'REVIEWER' ? '#92400e' : '#166534',
                color: '#ffffff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '13px',
                fontWeight: 700
              }}>
                {currentUser?.full_name?.charAt(0) || 'U'}
              </div>
              <div style={{ textAlign: 'left' }}>
                <div style={{ fontSize: '13px', fontWeight: 700, color: '#0f172a' }}>
                  {currentUser?.full_name || 'Switch Demo Persona'}
                </div>
                <div style={{ fontSize: '11px', color: '#64748b' }}>
                  Role: <strong style={{ color: '#d97706' }}>{currentUser?.role}</strong> (Demo Mode)
                </div>
              </div>
              <span style={{ fontSize: '12px', color: '#94a3b8' }}>▼</span>
            </button>

            {dropdownOpen && (
              <div style={{
                position: 'absolute',
                top: '110%',
                right: 0,
                width: '340px',
                backgroundColor: '#ffffff',
                borderRadius: '10px',
                boxShadow: '0 10px 25px rgba(0,0,0,0.15)',
                border: '1px solid #e2e8f0',
                padding: '10px',
                zIndex: 200
              }}>
                <div style={{ padding: '8px 10px', fontSize: '12px', fontWeight: 700, color: '#64748b', borderBottom: '1px solid #f1f5f9', textTransform: 'uppercase' }}>
                  Quick-Switch Demo Persona
                </div>
                {demoAccounts.map(acc => (
                  <div
                    key={acc.user_id}
                    onClick={() => {
                      switchDemoUser(acc.user_id);
                      setDropdownOpen(false);
                    }}
                    style={{
                      padding: '10px',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      backgroundColor: currentUser?.user_id === acc.user_id ? '#ebf8ff' : 'transparent',
                      borderLeft: currentUser?.user_id === acc.user_id ? '3px solid #1a365d' : '3px solid transparent',
                      marginTop: '4px',
                      transition: 'background-color 0.15s'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontSize: '13px', fontWeight: 700, color: '#0f172a' }}>{acc.full_name}</span>
                      <span className={`badge ${acc.role === 'ADMIN' ? 'badge-navy' : acc.role === 'REVIEWER' ? 'badge-saffron' : 'badge-green'}`} style={{ fontSize: '10px' }}>
                        {acc.role}
                      </span>
                    </div>
                    <div style={{ fontSize: '11px', color: '#64748b', marginTop: '3px' }}>
                      {acc.description}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
