-- SIH26101 v2 demo schema. Use a NEW empty database/schema. No destructive migration.
CREATE TABLE sources (
  source_id TEXT NOT NULL,
  title TEXT NOT NULL,
  source_url TEXT,
  locator TEXT,
  support_scope TEXT NOT NULL,
  verification_status TEXT NOT NULL,
  reviewed_at TEXT,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE mdos (
  mdo_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  status TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (mdo_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE divisions (
  division_id TEXT NOT NULL,
  mdo_id TEXT NOT NULL,
  name TEXT NOT NULL,
  abbreviation TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (division_id),
  FOREIGN KEY (mdo_id) REFERENCES mdos(mdo_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE competencies (
  competency_id TEXT NOT NULL,
  label TEXT NOT NULL,
  type TEXT NOT NULL,
  area TEXT NOT NULL,
  description TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (type IN ('FUNCTIONAL','DOMAIN','BEHAVIOURAL')),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE competency_levels (
  competency_level_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  level_no INTEGER NOT NULL,
  level_name TEXT NOT NULL,
  level_description TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (competency_level_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (level_no BETWEEN 1 AND 5),
  UNIQUE(competency_id,level_no),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE roles (
  role_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  tier TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (role_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE activities (
  activity_id TEXT NOT NULL,
  role_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  is_extension INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (activity_id),
  FOREIGN KEY (role_id) REFERENCES roles(role_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE activity_competencies (
  activity_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  required_level INTEGER NOT NULL,
  priority INTEGER NOT NULL,
  rationale TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (activity_id,competency_id),
  FOREIGN KEY (activity_id) REFERENCES activities(activity_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (required_level BETWEEN 1 AND 5),
  CHECK (priority BETWEEN 1 AND 3),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE role_competencies (
  role_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  required_level INTEGER NOT NULL,
  priority INTEGER NOT NULL,
  contributing_activity_ids TEXT NOT NULL,
  max_level_activity_ids TEXT NOT NULL,
  aggregation_rule TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (role_id,competency_id),
  FOREIGN KEY (role_id) REFERENCES roles(role_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (required_level BETWEEN 1 AND 5),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE positions (
  position_id TEXT NOT NULL,
  mdo_id TEXT NOT NULL,
  division_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  career_band INTEGER NOT NULL,
  status TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (position_id),
  FOREIGN KEY (mdo_id) REFERENCES mdos(mdo_id),
  FOREIGN KEY (division_id) REFERENCES divisions(division_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (career_band BETWEEN 1 AND 4),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE position_role (
  position_id TEXT NOT NULL,
  role_id TEXT NOT NULL,
  is_primary INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (position_id,role_id),
  FOREIGN KEY (position_id) REFERENCES positions(position_id),
  FOREIGN KEY (role_id) REFERENCES roles(role_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (is_primary IN (0,1)),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE users (
  user_id TEXT NOT NULL,
  mdo_id TEXT NOT NULL,
  division_id TEXT NOT NULL,
  position_id TEXT NOT NULL,
  target_position_id TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  designation TEXT NOT NULL,
  experience_years INTEGER NOT NULL,
  status TEXT NOT NULL,
  scenario TEXT NOT NULL,
  career_note TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (user_id),
  FOREIGN KEY (mdo_id) REFERENCES mdos(mdo_id),
  FOREIGN KEY (division_id) REFERENCES divisions(division_id),
  FOREIGN KEY (position_id) REFERENCES positions(position_id),
  FOREIGN KEY (target_position_id) REFERENCES positions(position_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (experience_years >= 0),
  UNIQUE(email),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE user_competencies (
  user_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  current_level INTEGER,
  level_status TEXT NOT NULL,
  confidence REAL,
  assessed_at TEXT,
  source TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (user_id,competency_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (current_level IS NULL OR current_level BETWEEN 1 AND 5),
  CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
  CHECK ((current_level IS NULL AND level_status='UNKNOWN' AND confidence IS NULL) OR (current_level IS NOT NULL AND level_status='KNOWN' AND confidence IS NOT NULL)),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE competency_evidence (
  evidence_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  assessment_id TEXT NOT NULL,
  assessment_type TEXT NOT NULL,
  evidence_type TEXT NOT NULL,
  score REAL,
  estimated_level INTEGER,
  confidence REAL NOT NULL,
  date TEXT NOT NULL,
  coverage REAL,
  item_count INTEGER,
  rubric_version TEXT,
  reviewed INTEGER NOT NULL,
  state_update_applied INTEGER NOT NULL,
  payload_hash TEXT,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (evidence_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  UNIQUE(user_id,assessment_id,competency_id),
  CHECK (estimated_level IS NULL OR estimated_level BETWEEN 1 AND 5),
  CHECK (score IS NULL OR score BETWEEN 0 AND 100),
  CHECK (confidence BETWEEN 0 AND 1),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE courses (
  course_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  provider TEXT,
  duration_minutes REAL,
  language TEXT,
  license TEXT,
  learning_mode TEXT,
  course_url TEXT,
  destination_verified INTEGER NOT NULL,
  verification_basis TEXT NOT NULL,
  live_access_verified INTEGER NOT NULL,
  last_verified_at TEXT,
  tier INTEGER NOT NULL,
  status TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (course_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (destination_verified IN (0,1)),
  CHECK (destination_verified=0 OR course_url IS NOT NULL),
  CHECK (tier IN (1,2)),
  CHECK (duration_minutes IS NULL OR duration_minutes > 0),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE course_competencies (
  course_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  from_level INTEGER NOT NULL,
  to_level INTEGER NOT NULL,
  relevance_weight REAL NOT NULL,
  approval_status TEXT NOT NULL,
  approval_basis TEXT NOT NULL,
  reviewer_id TEXT,
  reviewed_at TEXT,
  mapping_scope TEXT NOT NULL,
  production_approved INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (course_id,competency_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (from_level BETWEEN 1 AND 5),
  CHECK (to_level BETWEEN 1 AND 5),
  CHECK (from_level < to_level),
  CHECK (relevance_weight BETWEEN 0 AND 1),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE course_learning_outcomes (
  learning_outcome_id TEXT NOT NULL,
  course_id TEXT NOT NULL,
  description TEXT NOT NULL,
  sequence_no INTEGER NOT NULL,
  approval_status TEXT NOT NULL,
  is_published_outcome INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (learning_outcome_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  UNIQUE(course_id,sequence_no),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE learning_outcome_competency (
  learning_outcome_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  target_level INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (learning_outcome_id,competency_id),
  FOREIGN KEY (learning_outcome_id) REFERENCES course_learning_outcomes(learning_outcome_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (target_level BETWEEN 1 AND 5),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE course_prerequisites (
  course_id TEXT NOT NULL,
  prerequisite_course_id TEXT NOT NULL,
  is_mandatory INTEGER NOT NULL,
  note TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (course_id,prerequisite_course_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id),
  FOREIGN KEY (prerequisite_course_id) REFERENCES courses(course_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (course_id <> prerequisite_course_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE training_records (
  training_record_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  course_id TEXT NOT NULL,
  status TEXT NOT NULL,
  started_at TEXT,
  completed_at TEXT,
  progress_percent REAL NOT NULL,
  score REAL,
  completion_verified INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (training_record_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (status IN ('COMPLETED','IN_PROGRESS','NOT_STARTED')),
  CHECK (progress_percent BETWEEN 0 AND 100),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE knowledge_resources (
  resource_id TEXT NOT NULL,
  title TEXT NOT NULL,
  type TEXT NOT NULL,
  url TEXT,
  local_path TEXT,
  description TEXT NOT NULL,
  provider TEXT,
  ingestion_allowed INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (resource_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE course_resources (
  course_id TEXT NOT NULL,
  resource_id TEXT NOT NULL,
  relationship TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (course_id,resource_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id),
  FOREIGN KEY (resource_id) REFERENCES knowledge_resources(resource_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE competency_gaps (
  gap_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  scope TEXT NOT NULL,
  position_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  required_level INTEGER NOT NULL,
  current_level INTEGER,
  signed_gap INTEGER,
  unmet_gap INTEGER,
  gap_status TEXT NOT NULL,
  priority TEXT NOT NULL,
  recommendation_status TEXT NOT NULL,
  contributing_role_ids TEXT NOT NULL,
  contributing_activity_ids TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (gap_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (position_id) REFERENCES positions(position_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  UNIQUE(user_id,scope,competency_id),
  CHECK (required_level BETWEEN 1 AND 5),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE course_recommendations (
  recommendation_id TEXT NOT NULL,
  gap_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  course_id TEXT NOT NULL,
  competency_id TEXT NOT NULL,
  rank INTEGER NOT NULL,
  score REAL NOT NULL,
  score_components TEXT NOT NULL,
  reason TEXT NOT NULL,
  learning_outcome_ids TEXT NOT NULL,
  remaining_gap_after_planned_learning INTEGER NOT NULL,
  is_bridge INTEGER NOT NULL,
  eligibility_mode TEXT NOT NULL,
  production_eligible INTEGER NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (recommendation_id),
  FOREIGN KEY (gap_id) REFERENCES competency_gaps(gap_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  UNIQUE(gap_id,course_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE learning_paths (
  learning_path_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  scope TEXT NOT NULL,
  target_position_id TEXT NOT NULL,
  readiness_status TEXT NOT NULL,
  status TEXT NOT NULL,
  rule_version TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (learning_path_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (target_position_id) REFERENCES positions(position_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE TABLE learning_path_items (
  path_item_id TEXT NOT NULL,
  learning_path_id TEXT NOT NULL,
  sequence_no INTEGER NOT NULL,
  stage TEXT NOT NULL,
  item_type TEXT NOT NULL,
  competency_id TEXT,
  course_id TEXT,
  gap_id TEXT,
  status TEXT NOT NULL,
  action_label TEXT NOT NULL,
  source_id TEXT NOT NULL,
  provenance TEXT NOT NULL,
  source_type TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  PRIMARY KEY (path_item_id),
  FOREIGN KEY (learning_path_id) REFERENCES learning_paths(learning_path_id),
  FOREIGN KEY (competency_id) REFERENCES competencies(competency_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id),
  FOREIGN KEY (gap_id) REFERENCES competency_gaps(gap_id),
  FOREIGN KEY (source_id) REFERENCES sources(source_id),
  UNIQUE(learning_path_id,sequence_no),
  CHECK (provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR')),
  CHECK (source_type = provenance)
);

CREATE VIEW learning_outcomes AS SELECT * FROM course_learning_outcomes;

CREATE UNIQUE INDEX one_primary_role_per_position ON position_role(position_id) WHERE is_primary=1;
CREATE VIEW mdo AS SELECT * FROM mdos;
CREATE VIEW position AS SELECT * FROM positions;
CREATE VIEW role AS SELECT * FROM roles;
CREATE VIEW activity AS SELECT * FROM activities;
CREATE VIEW activity_competency AS SELECT * FROM activity_competencies;
CREATE VIEW competency AS SELECT * FROM competencies;
CREATE VIEW competency_level AS SELECT * FROM competency_levels;
CREATE VIEW role_competency AS SELECT * FROM role_competencies;
CREATE VIEW official_user AS SELECT * FROM users;
CREATE VIEW user_competency AS SELECT * FROM user_competencies;
CREATE VIEW course AS SELECT * FROM courses;
CREATE VIEW course_learning_outcome AS SELECT * FROM course_learning_outcomes;
CREATE VIEW course_competency AS SELECT * FROM course_competencies;
CREATE VIEW training_record AS SELECT * FROM training_records;
CREATE VIEW knowledge_resource AS SELECT * FROM knowledge_resources;
CREATE VIEW course_resource AS SELECT * FROM course_resources;
