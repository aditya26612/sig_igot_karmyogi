import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { LearnerHomeView } from './views/learner/LearnerHomeView';
import { MyLearningView } from './views/learner/MyLearningView';
import { SkillGapsView } from './views/learner/SkillGapsView';
import { CareerPathView } from './views/learner/CareerPathView';
import { ReviewerDashboardView } from './views/reviewer/ReviewerDashboardView';
import { AdminDashboardView } from './views/admin/AdminDashboardView';
import { CopilotView } from './views/copilot/CopilotView';
import { LandingView } from './views/LandingView';

/** Default landing route per role. */
export function defaultRouteForRole(role?: string): string {
  if (role === 'ADMIN') return '/admin';
  if (role === 'REVIEWER') return '/reviewer';
  return '/home';
}

const ROLE_ROUTES: Record<string, string[]> = {
  LEARNER: ['/home', '/learning', '/gaps', '/career', '/copilot'],
  REVIEWER: ['/reviewer', '/copilot'],
  ADMIN: ['/admin', '/copilot'],
};

/** Scrolls to top on every route change (except same-page hash/query navigation). */
const ScrollToTop: React.FC = () => {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'auto' });
  }, [pathname]);
  return null;
};

/** Blocks rendering until the demo auth bootstrap completes (avoids redirect flicker). */
const RouteGuard: React.FC<{ allowed: string[]; children: React.ReactNode }> = ({ allowed, children }) => {
  const { currentUser, isLoading } = useAuth();
  const location = useLocation();
  if (isLoading) {
    return (
      <div className="gov-container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-text-strong)' }}>
          Loading portal…
        </div>
      </div>
    );
  }
  const role = currentUser?.role || 'LEARNER';
  if (!allowed.includes(role)) {
    return <Navigate to={defaultRouteForRole(role)} replace />;
  }
  return <>{children}</>;
};

const MainLayout: React.FC = () => {
  const { currentUser, isLoading } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const isLanding = location.pathname === '/';

  // While auth bootstraps, hold on landing so the user never sees a flash of the wrong shell.
  if (isLoading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-text-strong)' }}>
          Loading iGOT Karmayogi SkillBridge…
        </div>
      </div>
    );
  }

  const role = currentUser?.role || 'LEARNER';

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {!isLanding && <Navbar />}

      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/" element={<LandingView />} />
          <Route path="/home" element={<RouteGuard allowed={['LEARNER']}><LearnerHomeView /></RouteGuard>} />
          <Route path="/learning" element={<RouteGuard allowed={['LEARNER']}><MyLearningView /></RouteGuard>} />
          <Route path="/gaps" element={<RouteGuard allowed={['LEARNER']}><SkillGapsView /></RouteGuard>} />
          <Route path="/career" element={<RouteGuard allowed={['LEARNER']}><CareerPathView /></RouteGuard>} />
          <Route path="/reviewer" element={<RouteGuard allowed={['REVIEWER', 'ADMIN']}><ReviewerDashboardView /></RouteGuard>} />
          <Route path="/admin" element={<RouteGuard allowed={['ADMIN']}><AdminDashboardView /></RouteGuard>} />
          <Route
            path="/copilot"
            element={
              <RouteGuard allowed={['LEARNER', 'REVIEWER', 'ADMIN']}>
                <CopilotView />
              </RouteGuard>
            }
          />
          <Route path="*" element={<Navigate to={defaultRouteForRole(role)} replace />} />
        </Routes>
      </main>

      {!isLanding && <Footer />}
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ScrollToTop />
        <MainLayout />
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
