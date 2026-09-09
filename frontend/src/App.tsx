import React from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { AssistantDrawer } from './components/AssistantDrawer';
import { LearnerHomeView } from './views/learner/LearnerHomeView';
import { MyLearningView } from './views/learner/MyLearningView';
import { SkillGapsView } from './views/learner/SkillGapsView';
import { CareerPathView } from './views/learner/CareerPathView';
import { ReviewerDashboardView } from './views/reviewer/ReviewerDashboardView';
import { AdminDashboardView } from './views/admin/AdminDashboardView';

const MainLayout: React.FC = () => {
  const { activeView } = useAuth();

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar />

      <main style={{ flex: 1 }}>
        {activeView === 'home' && <LearnerHomeView />}
        {activeView === 'learning' && <MyLearningView />}
        {activeView === 'gaps' && <SkillGapsView />}
        {activeView === 'career' && <CareerPathView />}
        {activeView === 'reviewer' && <ReviewerDashboardView />}
        {activeView === 'admin' && <AdminDashboardView />}
      </main>

      <Footer />
      <AssistantDrawer />
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <MainLayout />
    </AuthProvider>
  );
};

export default App;
