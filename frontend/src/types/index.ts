export interface UserProfile {
  user_id: string;
  email: string;
  full_name: string;
  role: 'ADMIN' | 'REVIEWER' | 'LEARNER';
  department?: string;
  designation?: string;
}

export interface DemoAccountInfo {
  user_id: string;
  email: string;
  full_name: string;
  role: string;
  department?: string;
  designation?: string;
  description: string;
}

export interface NextActionItem {
  action_type: string;
  title: string;
  subtitle: string;
  competency_id: string;
  competency_label: string;
  target_url: string;
  button_label: string;
  badge_label: string;
}

export interface CompetencyGapItem {
  gap_id: string;
  competency_id: string;
  competency_label: string;
  plain_title: string;
  plain_explanation: string;
  current_level: number | null;
  required_level: number;
  unmet_gap: number | null;
  gap_status: string; // 'HIGH', 'MEDIUM', 'NO_GAP', 'INSUFFICIENT_EVIDENCE'
  priority: string;
  target_role_name: string;
  contributing_activities: string[];
  recommendation_status: string;
  has_recommended_course: boolean;
}

export interface LearningPathItemDTO {
  path_item_id: string;
  sequence_no: number;
  stage: string;
  item_type: string;
  competency_id: string;
  competency_label: string;
  course_id?: string;
  course_title?: string;
  status: string;
  action_label: string;
}

export interface LearningPathDTO {
  learning_path_id: string;
  user_id: string;
  readiness_status: string;
  status: string;
  items: LearningPathItemDTO[];
}

export interface LearnerDashboardResponse {
  greeting: string;
  learner_name: string;
  current_role: string;
  target_role: string;
  next_action: NextActionItem;
  priority_gaps: CompetencyGapItem[];
  learning_path_preview: LearningPathItemDTO[];
  readiness_status: string;
  total_gaps_count: number;
  completed_competencies_count: number;
}

export interface CareerReadinessResponse {
  user_id: string;
  learner_name: string;
  current_position: string;
  target_position: string;
  readiness_status: string;
  plain_readiness_label: string;
  notice: string;
  total_required_competencies: number;
  met_competencies_count: number;
  high_priority_gaps_count: number;
  target_gaps: CompetencyGapItem[];
}

export interface CuratedLessonDTO {
  lesson_id: string;
  playlist_id: string;
  sequence_no: number;
  title: string;
  youtube_video_id: string;
  youtube_url: string;
  duration_minutes: number;
  competency_id: string;
  has_transcript: boolean;
  is_completed: boolean;
}

export interface CuratedPlaylistDTO {
  playlist_id: string;
  title: string;
  youtube_url: string;
  channel_name: string;
  competency_id: string;
  competency_label: string;
  description: string;
  category: string;
  total_lessons: number;
  status: string;
  provider_badge: string;
  lessons?: CuratedLessonDTO[];
}

export interface TranscriptChunkDTO {
  chunk_id: string;
  lesson_id: string;
  course_id: string;
  competency_id: string;
  topic: string;
  start_seconds: number;
  end_seconds: number;
  timestamp_label: string;
  text_content: string;
  summary?: string;
}

export interface LessonDetailResponse {
  lesson: CuratedLessonDTO;
  playlist: CuratedPlaylistDTO;
  transcript_chunks: TranscriptChunkDTO[];
  next_lesson_id?: string;
  prev_lesson_id?: string;
  practice_available: boolean;
  provider_notice: string;
}

export interface PracticeOption {
  option_id: string;
  text: string;
}

export interface PracticeQuestionDTO {
  question_id: string;
  question_text: string;
  options: PracticeOption[];
  difficulty: string;
  topic: string;
  timestamp_label?: string;
  chunk_id?: string;
}

export interface PracticeQuizDTO {
  quiz_id: string;
  lesson_id: string;
  title: string;
  topic: string;
  total_questions: number;
  questions: PracticeQuestionDTO[];
  notice: string;
}

export interface QuestionResultItem {
  question_id: string;
  question_text: string;
  selected_option: string;
  correct_option: string;
  is_correct: boolean;
  explanation: string;
  timestamp_label?: string;
  chunk_id?: string;
}

export interface PracticeSubmissionResponse {
  attempt_id: string;
  quiz_id: string;
  lesson_id: string;
  score: number;
  total_questions: number;
  percentage: number;
  weak_topics: string[];
  results: QuestionResultItem[];
  notice: string;
  competency_level_changed: boolean;
}

export interface PracticalTaskItem {
  task_id: string;
  title: string;
  scenario: string;
  instructions: string;
  expected_output_type: string;
}

export interface AssessmentDetailDTO {
  assessment_id: string;
  title: string;
  competency_id: string;
  competency_label: string;
  assessment_type: string;
  rubric_version: string;
  estimated_time_minutes: number;
  prerequisites_met: boolean;
  current_level: number;
  target_level: number;
  rules: string[];
  tasks: PracticalTaskItem[];
  notice: string;
}

export interface ReviewQueueItemDTO {
  submission_id: string;
  user_id: string;
  learner_name: string;
  assessment_id: string;
  assessment_title: string;
  competency_id: string;
  competency_label: string;
  current_level: number;
  proposed_level: number;
  overall_score: number;
  confidence: number;
  coverage: number;
  rubric_version: string;
  submitted_at: string;
  status: string;
}

export interface ReviewDecisionResponse {
  submission_id: string;
  status: string;
  level_promoted: boolean;
  before_level?: number;
  after_level?: number;
  learning_path_recalculated: boolean;
  message: string;
}

export interface AssistantAskResponse {
  answer: string;
  source_lesson_id?: string;
  source_lesson_title?: string;
  timestamp_label?: string;
  chunk_id?: string;
  citation_snippet?: string;
  suggested_actions: string[];
}

export interface QuickPromptItem {
  label: string;
  prompt: string;
  category: string;
}

export interface AdminDashboardMetrics {
  total_learners: number;
  learners_with_critical_gaps: number;
  total_competencies: number;
  assessment_backlog: number;
  content_curated_playlists: number;
  total_lessons: number;
  division_gap_breakdown: Record<string, number>;
}

export interface LearnerAdminListItem {
  user_id: string;
  name: string;
  email: string;
  designation: string;
  division_name: string;
  current_position_name: string;
  target_position_name: string;
  readiness_status: string;
  target_gaps_count: number;
  priority_gaps_count: number;
}
