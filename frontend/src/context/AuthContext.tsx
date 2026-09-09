import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile, DemoAccountInfo } from '../types';
import { api, setAuthToken, clearAuthToken } from '../api/client';

interface AuthContextType {
  currentUser: UserProfile | null;
  demoAccounts: DemoAccountInfo[];
  isLoading: boolean;
  switchDemoUser: (userId: string) => Promise<void>;
  logout: () => void;
  activeView: string;
  setActiveView: (view: string) => void;
  selectedLessonId: string | null;
  setSelectedLessonId: (id: string | null) => void;
  activeAssessmentId: string | null;
  setActiveAssessmentId: (id: string | null) => void;
  isAssistantOpen: boolean;
  setIsAssistantOpen: (open: boolean) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(null);
  const [demoAccounts, setDemoAccounts] = useState<DemoAccountInfo[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [activeView, setActiveView] = useState<string>('landing');
  const [selectedLessonId, setSelectedLessonId] = useState<string | null>('sampling-lesson-3');
  const [activeAssessmentId, setActiveAssessmentId] = useState<string | null>(null);
  const [isAssistantOpen, setIsAssistantOpen] = useState<boolean>(false);

  useEffect(() => {
    async function initAuth() {
      try {
        const accounts = await api.getDemoAccounts();
        setDemoAccounts(accounts);

        // By default, initialize as USR-001 (Aarav Sharma) for immediate demonstration
        const res = await api.demoSwitch('USR-001');
        setAuthToken(res.access_token);
        setCurrentUser(res.user);
      } catch (err) {
        console.error('Failed to initialize demo auth:', err);
      } finally {
        setIsLoading(false);
      }
    }
    initAuth();
  }, []);

  const switchDemoUser = async (userId: string) => {
    setIsLoading(true);
    try {
      const res = await api.demoSwitch(userId);
      setAuthToken(res.access_token);
      setCurrentUser(res.user);
      
      // Route appropriately for persona
      if (res.user.role === 'ADMIN') {
        setActiveView('admin');
      } else if (res.user.role === 'REVIEWER') {
        setActiveView('reviewer');
      } else {
        setActiveView('home');
      }
    } catch (err) {
      console.error('Failed to switch user:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    clearAuthToken();
    setCurrentUser(null);
  };

  return (
    <AuthContext.Provider value={{
      currentUser,
      demoAccounts,
      isLoading,
      switchDemoUser,
      logout,
      activeView,
      setActiveView,
      selectedLessonId,
      setSelectedLessonId,
      activeAssessmentId,
      setActiveAssessmentId,
      isAssistantOpen,
      setIsAssistantOpen
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
