const API_BASE = 'http://127.0.0.1:8000';

export function getAuthToken(): string | null {
  return localStorage.getItem('sih_auth_token');
}

export function setAuthToken(token: string) {
  localStorage.setItem('sih_auth_token', token);
}

export function clearAuthToken() {
  localStorage.removeItem('sih_auth_token');
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    let errorDetail = `Request failed: ${response.statusText}`;
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errJson.error || errorDetail;
    } catch {
      // ignore
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const api = {
  // Auth
  demoSwitch: (userId: string) => request<any>('/api/auth/demo-switch', {
    method: 'POST',
    body: JSON.stringify({ user_id: userId })
  }),
  getDemoAccounts: () => request<any[]>('/api/auth/demo-accounts'),
  getMe: () => request<any>('/api/auth/me'),

  // Learner
  getDashboard: (userId?: string) => request<any>(`/api/learner/dashboard${userId ? `?user_id=${userId}` : ''}`),
  getGaps: (scope: 'TARGET' | 'CURRENT' = 'TARGET', userId?: string) => 
    request<any[]>(`/api/learner/gaps?scope=${scope}${userId ? `&user_id=${userId}` : ''}`),
  getLearningPath: (userId?: string) => 
    request<any>(`/api/learner/learning-path${userId ? `?user_id=${userId}` : ''}`),
  getCareerReadiness: (userId?: string) => 
    request<any>(`/api/learner/career-readiness${userId ? `?user_id=${userId}` : ''}`),
  getLearnerProfile: (userId?: string) => 
    request<any>(`/api/learner/me${userId ? `?user_id=${userId}` : ''}`),

  // Content
  getPlaylists: () => request<any[]>('/api/content/playlists'),
  getPlaylistDetail: (id: string) => request<any>(`/api/content/playlists/${id}`),
  getLessonDetail: (id: string) => request<any>(`/api/content/lessons/${id}`),
  searchTranscripts: (query: string) => request<any>(`/api/content/search?q=${encodeURIComponent(query)}`),
  recordLessonProgress: (lessonId: string, completed: boolean = true) => 
    request<any>(`/api/content/lessons/${lessonId}/progress`, {
      method: 'POST',
      body: JSON.stringify({ completed })
    }),

  // Practice
  getPracticeQuiz: (lessonId: string) => request<any>(`/api/practice/${lessonId}`),
  submitPracticeQuiz: (quizId: string, answers: { question_id: string; selected_option: string }[]) =>
    request<any>(`/api/practice/${quizId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ answers })
    }),
  getPracticeHistory: (userId: string) => request<any[]>(`/api/practice/history/${userId}`),

  // Assessment
  getAssessments: () => request<any[]>('/api/assessments'),
  getAssessmentDetail: (id: string) => request<any>(`/api/assessments/${id}`),
  submitAssessment: (id: string, competencyId: string, answers: any, score: number = 86.0) =>
    request<any>(`/api/assessments/${id}/submit`, {
      method: 'POST',
      body: JSON.stringify({
        assessment_id: id,
        competency_id: competencyId,
        practical_answers: answers,
        self_reported_score: score
      })
    }),
  getAssessmentStatus: (id: string) => request<any>(`/api/assessments/${id}/status`),

  // Reviewer
  getReviewQueue: () => request<any[]>('/api/reviewer/queue'),
  submitReviewDecision: (submissionId: string, approved: boolean, reviewerComments: string) =>
    request<any>(`/api/reviewer/${submissionId}/decision`, {
      method: 'POST',
      body: JSON.stringify({
        approved,
        reviewer_comments: reviewerComments
      })
    }),

  // Assistant
  askAssistant: (question: string, contextType: string = 'LESSON', lessonId?: string, competencyId?: string) =>
    request<any>('/api/assistant/ask', {
      method: 'POST',
      body: JSON.stringify({
        question,
        context_type: contextType,
        lesson_id: lessonId,
        competency_id: competencyId
      })
    }),
  getQuickPrompts: () => request<any[]>('/api/assistant/prompts'),

  // Admin
  getAdminDashboard: () => request<any>('/api/admin/dashboard'),
  getAdminLearners: () => request<any[]>('/api/admin/learners'),
  registerLearner: (learnerData: any) => request<any>('/api/admin/learners', {
    method: 'POST',
    body: JSON.stringify(learnerData)
  }),
  uploadTranscript: (data: any) => request<any>('/api/admin/content/upload-transcript', {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  getQuestionsForReview: () => request<any[]>('/api/admin/questions/review'),
  reviewQuestion: (questionId: string, isApproved: boolean, status: string) =>
    request<any>(`/api/admin/questions/${questionId}/review`, {
      method: 'POST',
      body: JSON.stringify({ is_approved: isApproved, review_status: status })
    }),

  // Integrations
  getProviders: () => request<any[]>('/api/integrations/providers'),
  getIgotStatus: () => request<any>('/api/integrations/igot/status'),
  triggerIgotSync: () => request<any>('/api/integrations/igot/sync', { method: 'POST' }),
  getSyncHistory: () => request<any[]>('/api/integrations/sync-history')
};
