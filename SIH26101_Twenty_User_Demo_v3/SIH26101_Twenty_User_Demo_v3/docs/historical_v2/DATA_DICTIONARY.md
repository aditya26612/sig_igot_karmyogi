# Data dictionary and relationships

Canonical stored rows carry provenance and matching source_type; created_at/updated_at are package timestamps, not government record timestamps.

## sources

Primary key: `source_id`

| Field | SQL type / constraint | References |
|---|---|---|
| source_id | TEXT NOT NULL |  |
| title | TEXT NOT NULL |  |
| source_url | TEXT |  |
| locator | TEXT |  |
| support_scope | TEXT NOT NULL |  |
| verification_status | TEXT NOT NULL |  |
| reviewed_at | TEXT |  |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## mdos

Primary key: `mdo_id`

| Field | SQL type / constraint | References |
|---|---|---|
| mdo_id | TEXT NOT NULL |  |
| name | TEXT NOT NULL |  |
| description | TEXT |  |
| status | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## divisions

Primary key: `division_id`

| Field | SQL type / constraint | References |
|---|---|---|
| division_id | TEXT NOT NULL |  |
| mdo_id | TEXT NOT NULL | mdos.mdo_id |
| name | TEXT NOT NULL |  |
| abbreviation | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## competencies

Primary key: `competency_id`

| Field | SQL type / constraint | References |
|---|---|---|
| competency_id | TEXT NOT NULL |  |
| label | TEXT NOT NULL |  |
| type | TEXT NOT NULL |  |
| area | TEXT NOT NULL |  |
| description | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: type IN ('FUNCTIONAL','DOMAIN','BEHAVIOURAL'); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## competency_levels

Primary key: `competency_level_id`

| Field | SQL type / constraint | References |
|---|---|---|
| competency_level_id | TEXT NOT NULL |  |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| level_no | INTEGER NOT NULL |  |
| level_name | TEXT NOT NULL |  |
| level_description | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: level_no BETWEEN 1 AND 5; UNIQUE(competency_id,level_no); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## roles

Primary key: `role_id`

| Field | SQL type / constraint | References |
|---|---|---|
| role_id | TEXT NOT NULL |  |
| name | TEXT NOT NULL |  |
| description | TEXT NOT NULL |  |
| tier | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## activities

Primary key: `activity_id`

| Field | SQL type / constraint | References |
|---|---|---|
| activity_id | TEXT NOT NULL |  |
| role_id | TEXT NOT NULL | roles.role_id |
| name | TEXT NOT NULL |  |
| description | TEXT NOT NULL |  |
| is_extension | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## activity_competencies

Primary key: `activity_id, competency_id`

| Field | SQL type / constraint | References |
|---|---|---|
| activity_id | TEXT NOT NULL | activities.activity_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| required_level | INTEGER NOT NULL |  |
| priority | INTEGER NOT NULL |  |
| rationale | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: required_level BETWEEN 1 AND 5; priority BETWEEN 1 AND 3; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## role_competencies

Primary key: `role_id, competency_id`

| Field | SQL type / constraint | References |
|---|---|---|
| role_id | TEXT NOT NULL | roles.role_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| required_level | INTEGER NOT NULL |  |
| priority | INTEGER NOT NULL |  |
| contributing_activity_ids | TEXT NOT NULL |  |
| max_level_activity_ids | TEXT NOT NULL |  |
| aggregation_rule | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: required_level BETWEEN 1 AND 5; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## positions

Primary key: `position_id`

| Field | SQL type / constraint | References |
|---|---|---|
| position_id | TEXT NOT NULL |  |
| mdo_id | TEXT NOT NULL | mdos.mdo_id |
| division_id | TEXT NOT NULL | divisions.division_id |
| name | TEXT NOT NULL |  |
| description | TEXT NOT NULL |  |
| career_band | INTEGER NOT NULL |  |
| status | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: career_band BETWEEN 1 AND 4; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## position_role

Primary key: `position_id, role_id`

| Field | SQL type / constraint | References |
|---|---|---|
| position_id | TEXT NOT NULL | positions.position_id |
| role_id | TEXT NOT NULL | roles.role_id |
| is_primary | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: is_primary IN (0,1); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## users

Primary key: `user_id`

| Field | SQL type / constraint | References |
|---|---|---|
| user_id | TEXT NOT NULL |  |
| mdo_id | TEXT NOT NULL | mdos.mdo_id |
| division_id | TEXT NOT NULL | divisions.division_id |
| position_id | TEXT NOT NULL | positions.position_id |
| target_position_id | TEXT NOT NULL | positions.position_id |
| name | TEXT NOT NULL |  |
| email | TEXT NOT NULL |  |
| designation | TEXT NOT NULL |  |
| experience_years | INTEGER NOT NULL |  |
| status | TEXT NOT NULL |  |
| scenario | TEXT NOT NULL |  |
| career_note | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: experience_years >= 0; UNIQUE(email); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## user_competencies

Primary key: `user_id, competency_id`

| Field | SQL type / constraint | References |
|---|---|---|
| user_id | TEXT NOT NULL | users.user_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| current_level | INTEGER |  |
| level_status | TEXT NOT NULL |  |
| confidence | REAL |  |
| assessed_at | TEXT |  |
| source | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: current_level IS NULL OR current_level BETWEEN 1 AND 5; confidence IS NULL OR confidence BETWEEN 0 AND 1; (current_level IS NULL AND level_status='UNKNOWN' AND confidence IS NULL) OR (current_level IS NOT NULL AND level_status='KNOWN' AND confidence IS NOT NULL); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## competency_evidence

Primary key: `evidence_id`

| Field | SQL type / constraint | References |
|---|---|---|
| evidence_id | TEXT NOT NULL |  |
| user_id | TEXT NOT NULL | users.user_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| assessment_id | TEXT NOT NULL |  |
| assessment_type | TEXT NOT NULL |  |
| evidence_type | TEXT NOT NULL |  |
| score | REAL |  |
| estimated_level | INTEGER |  |
| confidence | REAL NOT NULL |  |
| date | TEXT NOT NULL |  |
| coverage | REAL |  |
| item_count | INTEGER |  |
| rubric_version | TEXT |  |
| reviewed | INTEGER NOT NULL |  |
| state_update_applied | INTEGER NOT NULL |  |
| payload_hash | TEXT |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: UNIQUE(user_id,assessment_id,competency_id); estimated_level IS NULL OR estimated_level BETWEEN 1 AND 5; score IS NULL OR score BETWEEN 0 AND 100; confidence BETWEEN 0 AND 1; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## courses

Primary key: `course_id`

| Field | SQL type / constraint | References |
|---|---|---|
| course_id | TEXT NOT NULL |  |
| title | TEXT NOT NULL |  |
| description | TEXT |  |
| provider | TEXT |  |
| duration_minutes | REAL |  |
| language | TEXT |  |
| license | TEXT |  |
| learning_mode | TEXT |  |
| course_url | TEXT |  |
| destination_verified | INTEGER NOT NULL |  |
| verification_basis | TEXT NOT NULL |  |
| live_access_verified | INTEGER NOT NULL |  |
| last_verified_at | TEXT |  |
| tier | INTEGER NOT NULL |  |
| status | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: destination_verified IN (0,1); destination_verified=0 OR course_url IS NOT NULL; tier IN (1,2); duration_minutes IS NULL OR duration_minutes > 0; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## course_competencies

Primary key: `course_id, competency_id`

| Field | SQL type / constraint | References |
|---|---|---|
| course_id | TEXT NOT NULL | courses.course_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| from_level | INTEGER NOT NULL |  |
| to_level | INTEGER NOT NULL |  |
| relevance_weight | REAL NOT NULL |  |
| approval_status | TEXT NOT NULL |  |
| approval_basis | TEXT NOT NULL |  |
| reviewer_id | TEXT |  |
| reviewed_at | TEXT |  |
| mapping_scope | TEXT NOT NULL |  |
| production_approved | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: from_level BETWEEN 1 AND 5; to_level BETWEEN 1 AND 5; from_level < to_level; relevance_weight BETWEEN 0 AND 1; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## course_learning_outcomes

Primary key: `learning_outcome_id`

| Field | SQL type / constraint | References |
|---|---|---|
| learning_outcome_id | TEXT NOT NULL |  |
| course_id | TEXT NOT NULL | courses.course_id |
| description | TEXT NOT NULL |  |
| sequence_no | INTEGER NOT NULL |  |
| approval_status | TEXT NOT NULL |  |
| is_published_outcome | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: UNIQUE(course_id,sequence_no); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## learning_outcome_competency

Primary key: `learning_outcome_id, competency_id`

| Field | SQL type / constraint | References |
|---|---|---|
| learning_outcome_id | TEXT NOT NULL | course_learning_outcomes.learning_outcome_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| target_level | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: target_level BETWEEN 1 AND 5; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## course_prerequisites

Primary key: `course_id, prerequisite_course_id`

| Field | SQL type / constraint | References |
|---|---|---|
| course_id | TEXT NOT NULL | courses.course_id |
| prerequisite_course_id | TEXT NOT NULL | courses.course_id |
| is_mandatory | INTEGER NOT NULL |  |
| note | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: course_id <> prerequisite_course_id; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## training_records

Primary key: `training_record_id`

| Field | SQL type / constraint | References |
|---|---|---|
| training_record_id | TEXT NOT NULL |  |
| user_id | TEXT NOT NULL | users.user_id |
| course_id | TEXT NOT NULL | courses.course_id |
| status | TEXT NOT NULL |  |
| started_at | TEXT |  |
| completed_at | TEXT |  |
| progress_percent | REAL NOT NULL |  |
| score | REAL |  |
| completion_verified | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: status IN ('COMPLETED','IN_PROGRESS','NOT_STARTED'); progress_percent BETWEEN 0 AND 100; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## knowledge_resources

Primary key: `resource_id`

| Field | SQL type / constraint | References |
|---|---|---|
| resource_id | TEXT NOT NULL |  |
| title | TEXT NOT NULL |  |
| type | TEXT NOT NULL |  |
| url | TEXT |  |
| local_path | TEXT |  |
| description | TEXT NOT NULL |  |
| provider | TEXT |  |
| ingestion_allowed | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## course_resources

Primary key: `course_id, resource_id`

| Field | SQL type / constraint | References |
|---|---|---|
| course_id | TEXT NOT NULL | courses.course_id |
| resource_id | TEXT NOT NULL | knowledge_resources.resource_id |
| relationship | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## competency_gaps

Primary key: `gap_id`

| Field | SQL type / constraint | References |
|---|---|---|
| gap_id | TEXT NOT NULL |  |
| user_id | TEXT NOT NULL | users.user_id |
| scope | TEXT NOT NULL |  |
| position_id | TEXT NOT NULL | positions.position_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| required_level | INTEGER NOT NULL |  |
| current_level | INTEGER |  |
| signed_gap | INTEGER |  |
| unmet_gap | INTEGER |  |
| gap_status | TEXT NOT NULL |  |
| priority | TEXT NOT NULL |  |
| recommendation_status | TEXT NOT NULL |  |
| contributing_role_ids | TEXT NOT NULL |  |
| contributing_activity_ids | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: UNIQUE(user_id,scope,competency_id); required_level BETWEEN 1 AND 5; provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## course_recommendations

Primary key: `recommendation_id`

| Field | SQL type / constraint | References |
|---|---|---|
| recommendation_id | TEXT NOT NULL |  |
| gap_id | TEXT NOT NULL | competency_gaps.gap_id |
| user_id | TEXT NOT NULL | users.user_id |
| course_id | TEXT NOT NULL | courses.course_id |
| competency_id | TEXT NOT NULL | competencies.competency_id |
| rank | INTEGER NOT NULL |  |
| score | REAL NOT NULL |  |
| score_components | TEXT NOT NULL |  |
| reason | TEXT NOT NULL |  |
| learning_outcome_ids | TEXT NOT NULL |  |
| remaining_gap_after_planned_learning | INTEGER NOT NULL |  |
| is_bridge | INTEGER NOT NULL |  |
| eligibility_mode | TEXT NOT NULL |  |
| production_eligible | INTEGER NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: UNIQUE(gap_id,course_id); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## learning_paths

Primary key: `learning_path_id`

| Field | SQL type / constraint | References |
|---|---|---|
| learning_path_id | TEXT NOT NULL |  |
| user_id | TEXT NOT NULL | users.user_id |
| scope | TEXT NOT NULL |  |
| target_position_id | TEXT NOT NULL | positions.position_id |
| readiness_status | TEXT NOT NULL |  |
| status | TEXT NOT NULL |  |
| rule_version | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance

## learning_path_items

Primary key: `path_item_id`

| Field | SQL type / constraint | References |
|---|---|---|
| path_item_id | TEXT NOT NULL |  |
| learning_path_id | TEXT NOT NULL | learning_paths.learning_path_id |
| sequence_no | INTEGER NOT NULL |  |
| stage | TEXT NOT NULL |  |
| item_type | TEXT NOT NULL |  |
| competency_id | TEXT | competencies.competency_id |
| course_id | TEXT | courses.course_id |
| gap_id | TEXT | competency_gaps.gap_id |
| status | TEXT NOT NULL |  |
| action_label | TEXT NOT NULL |  |
| source_id | TEXT NOT NULL | sources.source_id |
| provenance | TEXT NOT NULL |  |
| source_type | TEXT NOT NULL |  |
| created_at | TEXT NOT NULL |  |
| updated_at | TEXT NOT NULL |  |

Additional constraints: UNIQUE(learning_path_id,sequence_no); provenance IN ('PUBLIC_OFFICIAL','DERIVED','SYNTHETIC','MOCK_BEHAVIOUR'); source_type = provenance
