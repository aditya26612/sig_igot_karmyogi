import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserProfile, DemoAccountInfo } from '../types';
import { api, setAuthToken, clearAuthToken } from '../api/client';

interface AuthContextType {
  currentUser: UserProfile | null;
  demoAccounts: DemoAccountInfo[];
  isLoading: boolean;
  switchDemoUser: (userId: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(null);
  const [demoAccounts, setDemoAccounts] = useState<DemoAccountInfo[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const navigate = useNavigate();

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

  const switchDemoUser = useCallback(async (userId: string) => {
    setIsLoading(true);
    try {
      const res = await api.demoSwitch(userId);
      setAuthToken(res.access_token);
      setCurrentUser(res.user);

      // Route to the persona's default route; browser URL stays truthful for role switching
      const role = res.user.role;
      navigate(role === 'ADMIN' ? '/admin' : role === 'REVIEWER' ? '/reviewer' : '/home', { replace: true });
    } catch (err) {
      console.error('Failed to switch user:', err);
    } finally {
      setIsLoading(false);
    }
  }, [navigate]);

  const logout = useCallback(() => {
    clearAuthToken();
    setCurrentUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{
      currentUser,
      demoAccounts,
      isLoading,
      switchDemoUser,
      logout,
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
