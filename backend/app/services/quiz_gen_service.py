import json
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.config import settings

SEED_PRACTICE_QUIZZES = [
    {
        "quiz_id": "QUIZ-SAMPLING-01",
        "lesson_id": "sampling-lesson-1",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "title": "Practice Quiz: Probability Sampling & Frame Design",
        "topic": "Probability Sampling Principles & Frame Audits",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SAMPLING-02",
        "lesson_id": "sampling-lesson-2",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "title": "Practice Quiz: Simple Random & Systematic Selection",
        "topic": "SRSWOR, Inclusion Probabilities & Sampling Intervals",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SAMPLING-03",
        "lesson_id": "sampling-lesson-3",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "title": "Practice Quiz: Stratified Sampling & Proportional Allocation",
        "topic": "Stratified Sampling, Weights & Frames",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SAMPLING-04",
        "lesson_id": "sampling-lesson-4",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "title": "Practice Quiz: Cluster Sampling & Multi-Stage Surveys",
        "topic": "Primary Sampling Units, PSU Selection & Dispersion",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SAMPLING-05",
        "lesson_id": "sampling-lesson-5",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "title": "Practice Quiz: Survey Design Weights & Estimation",
        "topic": "Inverse Probability Weighting & Parameter Recovery",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SQL-01",
        "lesson_id": "sql-lesson-1",
        "course_id": "CRS-102",
        "competency_id": "COMP-027",
        "title": "Practice Quiz: Relational Joins & Data Reconciliation",
        "topic": "Multi-Table SQL Joins",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SQL-02",
        "lesson_id": "sql-lesson-2",
        "course_id": "CRS-102",
        "competency_id": "COMP-027",
        "title": "Practice Quiz: Duplicate Detection & Data Reconciliation",
        "topic": "Duplicate Detection & Primary Key Verification",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SQL-03",
        "lesson_id": "sql-lesson-3",
        "course_id": "CRS-102",
        "competency_id": "COMP-027",
        "title": "Practice Quiz: Advanced Grouping & Window Functions",
        "topic": "ROW_NUMBER, PARTITION BY & Aggregate Windows",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-SQL-04",
        "lesson_id": "sql-lesson-4",
        "course_id": "CRS-102",
        "competency_id": "COMP-027",
        "title": "Practice Quiz: NULL Handling & Three-Valued Logic in Registries",
        "topic": "NULL Propagation, COALESCE & Aggregate Filtering",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-PY-01",
        "lesson_id": "python-lesson-1",
        "course_id": "CRS-103",
        "competency_id": "COMP-025",
        "title": "Practice Quiz: Microdata Cleaning with Pandas",
        "topic": "Missing Values, Data Types & Outlier Screening",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-PY-02",
        "lesson_id": "python-lesson-2",
        "course_id": "CRS-103",
        "competency_id": "COMP-025",
        "title": "Practice Quiz: Automated Survey Data Pipelines",
        "topic": "ETL Pipelines, Validation Assertions & Batch Exports",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-PY-03",
        "lesson_id": "python-lesson-3",
        "course_id": "CRS-103",
        "competency_id": "COMP-025",
        "title": "Practice Quiz: Survey Microdata Weighting & Tabulation",
        "topic": "Weighted Aggregations, Crosstabs & Frequency Expansions",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-PY-04",
        "lesson_id": "python-lesson-4",
        "course_id": "CRS-103",
        "competency_id": "COMP-025",
        "title": "Practice Quiz: Automated Data Quality Audits & Anomaly Verification",
        "topic": "Validation Schema Engines & Integrity Reporting",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-R-01",
        "lesson_id": "r-lesson-1",
        "course_id": "CRS-104",
        "competency_id": "COMP-026",
        "title": "Practice Quiz: R Fundamentals for Official Statistics",
        "topic": "Survey Packages, Vectorization & Weighted Summaries",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-R-02",
        "lesson_id": "r-lesson-2",
        "course_id": "CRS-104",
        "competency_id": "COMP-026",
        "title": "Practice Quiz: Complex Survey Designs in R",
        "topic": "svydesign, Strata, Clusters & Replicate Weights",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-R-03",
        "lesson_id": "r-lesson-3",
        "course_id": "CRS-104",
        "competency_id": "COMP-026",
        "title": "Practice Quiz: Variance Estimation & Inequality Indicators in R",
        "topic": "Taylor Series Linearization, Gini & Poverty Metrics",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-PROB-01",
        "lesson_id": "prob-lesson-1",
        "course_id": "CRS-105",
        "competency_id": "COMP-009",
        "title": "Practice Quiz: Probability Distributions & Variance",
        "topic": "Normal, Binomial Distributions & Expectation",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-PROB-02",
        "lesson_id": "prob-lesson-2",
        "course_id": "CRS-105",
        "competency_id": "COMP-009",
        "title": "Practice Quiz: Central Limit Theorem & Finite Population Correction",
        "topic": "Sampling Distributions, Standard Errors & FPC",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-PROB-03",
        "lesson_id": "prob-lesson-3",
        "course_id": "CRS-105",
        "competency_id": "COMP-009",
        "title": "Practice Quiz: Confidence Intervals & Hypothesis Testing in Surveys",
        "topic": "Z-Scores, T-Tests & Survey Margin of Error",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-QUAL-01",
        "lesson_id": "quality-lesson-1",
        "course_id": "CRS-106",
        "competency_id": "COMP-018",
        "title": "Practice Quiz: Data Auditing & Error Screening",
        "topic": "Range Checks, Logical Consistency & Data Governance",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-QUAL-02",
        "lesson_id": "quality-lesson-2",
        "course_id": "CRS-106",
        "competency_id": "COMP-018",
        "title": "Practice Quiz: Imputation Methods & Hot-Deck vs Cold-Deck Protocols",
        "topic": "Item Non-Response, Donor Imputation & Variance Preservation",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-QUAL-03",
        "lesson_id": "quality-lesson-3",
        "course_id": "CRS-106",
        "competency_id": "COMP-018",
        "title": "Practice Quiz: Statistical Disclosure Control & Microdata Anonymization",
        "topic": "k-Anonymity, l-Diversity, Top-Coding & Confidentiality Rules",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-ML-01",
        "lesson_id": "ml-lesson-1",
        "course_id": "CRS-107",
        "competency_id": "COMP-028",
        "title": "Practice Quiz: Supervised Learning & Evaluation",
        "topic": "Precision, Recall, ROC-AUC & Register Imputation",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-ML-02",
        "lesson_id": "ml-lesson-2",
        "course_id": "CRS-107",
        "competency_id": "COMP-028",
        "title": "Practice Quiz: Record Linkage & Entity Resolution Across Registers",
        "topic": "Fellegi-Sunter Methodology, Phonetic Blocking & Deduplication",
        "created_at": "2026-09-06T14:52:00Z"
    },
    {
        "quiz_id": "QUIZ-ML-03",
        "lesson_id": "ml-lesson-3",
        "course_id": "CRS-107",
        "competency_id": "COMP-028",
        "title": "Practice Quiz: Tree Ensembles & Non-Response Prediction Models",
        "topic": "Random Forests, Gradient Boosting & Propensity Weighting",
        "created_at": "2026-09-06T14:52:00Z"
    }
]

SEED_PRACTICE_QUESTIONS = [
    # Lesson 1 Questions
    {
        "question_id": "Q-SAMP-L1-01",
        "quiz_id": "QUIZ-SAMPLING-01",
        "lesson_id": "sampling-lesson-1",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What is the defining scientific condition of a probability sampling design?",
        "options": [
            {"option_id": "A", "text": "Every population unit has a known, non-zero inclusion probability"},
            {"option_id": "B", "text": "All sample units are chosen through voluntary public participation"},
            {"option_id": "C", "text": "Units are chosen strictly based on field investigator subjective discretion"},
            {"option_id": "D", "text": "The population is divided into equal convenience segments"}
        ],
        "correct_option": "A",
        "explanation": "Probability sampling strictly requires that every unit in the target population has a known, non-zero probability of being selected into the sample.",
        "chunk_id": "CHK-DEMO-004",
        "timestamp_label": "03:15",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SAMP-L1-02",
        "quiz_id": "QUIZ-SAMPLING-01",
        "lesson_id": "sampling-lesson-1",
        "competency_id": "COMP-SAMPLING",
        "question_text": "Which operational frame error occurs when eligible units in remote hamlets are omitted from the village listing?",
        "options": [
            {"option_id": "A", "text": "Frame duplication error"},
            {"option_id": "B", "text": "Frame undercoverage error"},
            {"option_id": "C", "text": "Measurement error"},
            {"option_id": "D", "text": "Processing error"}
        ],
        "correct_option": "B",
        "explanation": "Omission of eligible target units from the sampling frame constitutes undercoverage error, which introduces bias that cannot be fixed by increasing sample size alone.",
        "chunk_id": "CHK-DEMO-004",
        "timestamp_label": "19:10",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SAMP-L1-03",
        "quiz_id": "QUIZ-SAMPLING-01",
        "lesson_id": "sampling-lesson-1",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What is the primary objective of conducting pre-survey listing and boundary verification audits?",
        "options": [
            {"option_id": "A", "text": "To ensure 100% questionnaire completion rates"},
            {"option_id": "B", "text": "To verify frame completeness and eliminate omissions or duplicate units"},
            {"option_id": "C", "text": "To replace probability sampling with convenience quotas"},
            {"option_id": "D", "text": "To compute final macroeconomic indicators"}
        ],
        "correct_option": "B",
        "explanation": "Auditing the frame verifies boundary demarcations, includes new dwellings, and deletes duplicates to preserve sampling frame integrity.",
        "chunk_id": "CHK-DEMO-004",
        "timestamp_label": "21:40",
        "difficulty": "MEDIUM"
    },

    # Lesson 2 Questions
    {
        "question_id": "Q-SAMP-L2-01",
        "quiz_id": "QUIZ-SAMPLING-02",
        "lesson_id": "sampling-lesson-2",
        "competency_id": "COMP-SAMPLING",
        "question_text": "In Simple Random Sampling Without Replacement (SRSWOR) of n=50 units from a population of N=1,000, what is the inclusion probability of each unit?",
        "options": [
            {"option_id": "A", "text": "0.01 (1%)"},
            {"option_id": "B", "text": "0.05 (5%)"},
            {"option_id": "C", "text": "0.10 (10%)"},
            {"option_id": "D", "text": "0.50 (50%)"}
        ],
        "correct_option": "B",
        "explanation": "In SRSWOR, each unit has an equal selection probability: π_i = n / N = 50 / 1000 = 0.05.",
        "chunk_id": "CHK-DEMO-001",
        "timestamp_label": "04:30",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SAMP-L2-02",
        "quiz_id": "QUIZ-SAMPLING-02",
        "lesson_id": "sampling-lesson-2",
        "competency_id": "COMP-SAMPLING",
        "question_text": "For a 1-in-k systematic sample of n=40 from population N=1,200, what is the sampling interval k?",
        "options": [
            {"option_id": "A", "text": "20"},
            {"option_id": "B", "text": "30"},
            {"option_id": "C", "text": "40"},
            {"option_id": "D", "text": "50"}
        ],
        "correct_option": "B",
        "explanation": "The sampling interval is k = N / n = 1200 / 40 = 30.",
        "chunk_id": "CHK-DEMO-001",
        "timestamp_label": "12:15",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SAMP-L2-03",
        "quiz_id": "QUIZ-SAMPLING-02",
        "lesson_id": "sampling-lesson-2",
        "competency_id": "COMP-SAMPLING",
        "question_text": "Under what condition does systematic sampling suffer from severe estimation bias?",
        "options": [
            {"option_id": "A", "text": "When the frame is in completely random order"},
            {"option_id": "B", "text": "When units are sorted monotonically by size"},
            {"option_id": "C", "text": "When the list has hidden periodic or cyclical patterns coinciding with interval k"},
            {"option_id": "D", "text": "When the sample size is an even number"}
        ],
        "correct_option": "C",
        "explanation": "If the list has periodic variations matching interval k (e.g. corner plots every 10 houses), the sample will systematically over-represent or miss specific groups.",
        "chunk_id": "CHK-DEMO-001",
        "timestamp_label": "18:50",
        "difficulty": "HARD"
    },

    # Lesson 3 Questions
    {
        "question_id": "Q-DEMO-001",
        "quiz_id": "QUIZ-SAMPLING-03",
        "lesson_id": "sampling-lesson-3",
        "competency_id": "COMP-SAMPLING",
        "question_text": "A population has strata of 800 and 400 units. For a proportional stratified sample of 120, which allocation is correct?",
        "options": [
            {"option_id": "A", "text": "80 and 40"},
            {"option_id": "B", "text": "60 and 60"},
            {"option_id": "C", "text": "40 and 80"},
            {"option_id": "D", "text": "100 and 20"}
        ],
        "correct_option": "A",
        "explanation": "Proportional allocation uses the population shares: 120 * 800 / 1200 = 80 and 120 * 400 / 1200 = 40.",
        "chunk_id": "CHK-DEMO-001",
        "timestamp_label": "02:15",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-DEMO-002",
        "quiz_id": "QUIZ-SAMPLING-03",
        "lesson_id": "sampling-lesson-3",
        "competency_id": "COMP-SAMPLING",
        "question_text": "For strata containing 800 and 400 units, which weights combine their sample means into the stratified population mean estimate?",
        "options": [
            {"option_id": "A", "text": "One-half and one-half"},
            {"option_id": "B", "text": "Two-thirds and one-third"},
            {"option_id": "C", "text": "One-third and two-thirds"},
            {"option_id": "D", "text": "Three-quarters and one-quarter"}
        ],
        "correct_option": "B",
        "explanation": "The population shares are 800/1200 (two-thirds) and 400/1200 (one-third).",
        "chunk_id": "CHK-DEMO-002",
        "timestamp_label": "07:45",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-DEMO-003",
        "quiz_id": "QUIZ-SAMPLING-03",
        "lesson_id": "sampling-lesson-3",
        "competency_id": "COMP-SAMPLING",
        "question_text": "A sampled unit has selection probability 0.10. What is its basic design weight?",
        "options": [
            {"option_id": "A", "text": "0.10"},
            {"option_id": "B", "text": "1"},
            {"option_id": "C", "text": "10"},
            {"option_id": "D", "text": "100"}
        ],
        "correct_option": "C",
        "explanation": "The basic design weight is the reciprocal of selection probability: 1 / 0.10 = 10.",
        "chunk_id": "CHK-DEMO-003",
        "timestamp_label": "13:20",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-DEMO-004",
        "quiz_id": "QUIZ-SAMPLING-03",
        "lesson_id": "sampling-lesson-3",
        "competency_id": "COMP-SAMPLING",
        "question_text": "A sampling frame omits eligible units. What is the primary statistical problem?",
        "options": [
            {"option_id": "A", "text": "Undercoverage error"},
            {"option_id": "B", "text": "A higher response-quality score"},
            {"option_id": "C", "text": "Automatic proportional allocation"},
            {"option_id": "D", "text": "Guaranteed unbiased selection"}
        ],
        "correct_option": "A",
        "explanation": "Missing eligible units causes undercoverage error. Increasing sample size from the same frame cannot fix omitted units.",
        "chunk_id": "CHK-DEMO-004",
        "timestamp_label": "19:10",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-DEMO-005",
        "quiz_id": "QUIZ-SAMPLING-03",
        "lesson_id": "sampling-lesson-3",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What is the key difference between stratification and cluster sampling?",
        "options": [
            {"option_id": "A", "text": "Stratification samples from all groups; cluster sampling samples a subset of groups"},
            {"option_id": "B", "text": "Cluster sampling is only used for census counts"},
            {"option_id": "C", "text": "Stratification requires non-probability quotas"},
            {"option_id": "D", "text": "Cluster sampling eliminates all sampling variance"}
        ],
        "correct_option": "A",
        "explanation": "In stratified sampling, units are sampled from every stratum. In cluster sampling, only a sample of clusters is selected.",
        "chunk_id": "CHK-DEMO-005",
        "timestamp_label": "25:35",
        "difficulty": "HARD"
    },

    # Lesson 4 Questions
    {
        "question_id": "Q-SAMP-L4-01",
        "quiz_id": "QUIZ-SAMPLING-04",
        "lesson_id": "sampling-lesson-4",
        "competency_id": "COMP-SAMPLING",
        "question_text": "In contrast to stratified sampling, how should clusters ideally be composed internally to minimize sampling error?",
        "options": [
            {"option_id": "A", "text": "Internally homogeneous with respect to survey study variables"},
            {"option_id": "B", "text": "Internally heterogeneous, mirroring the full diversity of the target population"},
            {"option_id": "C", "text": "Composed exclusively of identical single-member enterprises"},
            {"option_id": "D", "text": "Composed of geographically dispersed non-adjacent units"}
        ],
        "correct_option": "B",
        "explanation": "Clusters should ideally be as heterogeneous internally as the whole population so that selecting a few clusters captures all population characteristics.",
        "chunk_id": "CHK-DEMO-005",
        "timestamp_label": "26:10",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SAMP-L4-02",
        "quiz_id": "QUIZ-SAMPLING-04",
        "lesson_id": "sampling-lesson-4",
        "competency_id": "COMP-SAMPLING",
        "question_text": "In a nationwide NSSO two-stage household design with census villages as PSUs and households as USUs, what happens at the first stage?",
        "options": [
            {"option_id": "A", "text": "All households in every district are listed and interviewed"},
            {"option_id": "B", "text": "A probability sample of census villages (PSUs) is drawn from the district frame"},
            {"option_id": "C", "text": "A convenience quota of accessible households is surveyed"},
            {"option_id": "D", "text": "Only households residing along national highways are enumerated"}
        ],
        "correct_option": "B",
        "explanation": "In two-stage designs, Primary Sampling Units (PSUs, e.g. villages or urban blocks) are sampled in stage 1, and households within selected PSUs are sampled in stage 2.",
        "chunk_id": "CHK-DEMO-005",
        "timestamp_label": "28:40",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SAMP-L4-03",
        "quiz_id": "QUIZ-SAMPLING-04",
        "lesson_id": "sampling-lesson-4",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What is the primary operational advantage of multi-stage cluster designs in official survey administration?",
        "options": [
            {"option_id": "A", "text": "It guarantees lower standard errors than simple random sampling"},
            {"option_id": "B", "text": "It drastically concentrates field listing and reduces investigator travel costs"},
            {"option_id": "C", "text": "It eliminates the need for mathematical estimation weights"},
            {"option_id": "D", "text": "It makes non-response impossible"}
        ],
        "correct_option": "B",
        "explanation": "Cluster designs reduce travel costs and allow field listing to be restricted to sampled clusters rather than creating a complete listing of the entire nation.",
        "chunk_id": "CHK-DEMO-005",
        "timestamp_label": "31:00",
        "difficulty": "EASY"
    },

    # Lesson 5 Questions
    {
        "question_id": "Q-SAMP-L5-01",
        "quiz_id": "QUIZ-SAMPLING-05",
        "lesson_id": "sampling-lesson-5",
        "competency_id": "COMP-SAMPLING",
        "question_text": "An enterprise sub-stratum was sampled with selection probability 0.04. What is the basic design weight for each sampled unit?",
        "options": [
            {"option_id": "A", "text": "4.0"},
            {"option_id": "B", "text": "20.0"},
            {"option_id": "C", "text": "25.0"},
            {"option_id": "D", "text": "40.0"}
        ],
        "correct_option": "C",
        "explanation": "The base design weight is the inverse of the inclusion probability: w_i = 1 / 0.04 = 25.",
        "chunk_id": "CHK-DEMO-003",
        "timestamp_label": "13:20",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SAMP-L5-02",
        "quiz_id": "QUIZ-SAMPLING-05",
        "lesson_id": "sampling-lesson-5",
        "competency_id": "COMP-SAMPLING",
        "question_text": "Why must survey design weights be applied when analyzing sample survey microdata with unequal selection probabilities?",
        "options": [
            {"option_id": "A", "text": "To artificially inflate the sample count"},
            {"option_id": "B", "text": "To restore proportional representation and ensure unbiased estimation of population parameters"},
            {"option_id": "C", "text": "To avoid software syntax warnings"},
            {"option_id": "D", "text": "To normalize the variance across questions"}
        ],
        "correct_option": "B",
        "explanation": "When units have different selection probabilities, unweighted analysis produces biased parameter estimates. Weights compensate for unequal selection to reflect true population totals.",
        "chunk_id": "CHK-DEMO-003",
        "timestamp_label": "15:40",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SAMP-L5-03",
        "quiz_id": "QUIZ-SAMPLING-05",
        "lesson_id": "sampling-lesson-5",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What does an individual sampling weight of 50 indicate in survey interpretation?",
        "options": [
            {"option_id": "A", "text": "The sampled unit represents 50 units in the target population"},
            {"option_id": "B", "text": "The respondent was interviewed 50 times"},
            {"option_id": "C", "text": "The standard error is 50%"},
            {"option_id": "D", "text": "The question had 50 sub-items"}
        ],
        "correct_option": "A",
        "explanation": "Each design weight represents the count of population units in the target universe represented by that single respondent in estimation.",
        "chunk_id": "CHK-DEMO-003",
        "timestamp_label": "18:10",
        "difficulty": "EASY"
    },

    # SQL Questions
    {
        "question_id": "Q-SQL-001",
        "quiz_id": "QUIZ-SQL-01",
        "lesson_id": "sql-lesson-1",
        "competency_id": "COMP-027",
        "question_text": "When reconciling a master survey list with administrative tax filings, which join retains all survey records while showing missing tax matches as NULL?",
        "options": [
            {"option_id": "A", "text": "INNER JOIN"},
            {"option_id": "B", "text": "CROSS JOIN"},
            {"option_id": "C", "text": "LEFT OUTER JOIN"},
            {"option_id": "D", "text": "NATURAL JOIN"}
        ],
        "correct_option": "C",
        "explanation": "A LEFT OUTER JOIN preserves all rows from the primary survey table, assigning NULL to unmatched columns from the tax table.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "02:00",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SQL-002",
        "quiz_id": "QUIZ-SQL-01",
        "lesson_id": "sql-lesson-1",
        "competency_id": "COMP-027",
        "question_text": "Which SQL operation is ideal for discovering survey identifiers present in the frame but completely missing from field enumeration reports?",
        "options": [
            {"option_id": "A", "text": "INNER JOIN with WHERE count > 0"},
            {"option_id": "B", "text": "LEFT OUTER JOIN filtered by WHERE secondary_table.key IS NULL"},
            {"option_id": "C", "text": "CROSS JOIN without conditions"},
            {"option_id": "D", "text": "SELECT DISTINCT ON (id)"}
        ],
        "correct_option": "B",
        "explanation": "A LEFT JOIN combined with 'WHERE right_table.key IS NULL' is the standard SQL anti-join pattern for detecting unmatched or missing frame records.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "05:30",
        "difficulty": "MEDIUM"
    },
    # SQL Lesson 2 Questions
    {
        "question_id": "Q-SQL-L2-01",
        "quiz_id": "QUIZ-SQL-02",
        "lesson_id": "sql-lesson-2",
        "competency_id": "COMP-027",
        "question_text": "Which SQL construct accurately identifies duplicate business registration numbers in an establishment census table?",
        "options": [
            {"option_id": "A", "text": "SELECT reg_id FROM establishments WHERE reg_id IS NOT NULL"},
            {"option_id": "B", "text": "SELECT reg_id, COUNT(*) FROM establishments GROUP BY reg_id HAVING COUNT(*) > 1"},
            {"option_id": "C", "text": "SELECT reg_id FROM establishments ORDER BY reg_id DESC"},
            {"option_id": "D", "text": "SELECT DISTINCT reg_id FROM establishments"}
        ],
        "correct_option": "B",
        "explanation": "Grouping by the key and filtering with 'HAVING COUNT(*) > 1' is the fundamental query for pinpointing duplicate keys in relational databases.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "08:15",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SQL-L2-02",
        "quiz_id": "QUIZ-SQL-02",
        "lesson_id": "sql-lesson-2",
        "competency_id": "COMP-027",
        "question_text": "What severe analytical error occurs when joining microdata tables if duplicate primary keys are left unresolved?",
        "options": [
            {"option_id": "A", "text": "Query syntax error"},
            {"option_id": "B", "text": "Unintended cartesian row explosion leading to falsely inflated survey totals"},
            {"option_id": "C", "text": "Automatic deletion of the database index"},
            {"option_id": "D", "text": "Reversal of sorting order"}
        ],
        "correct_option": "B",
        "explanation": "Joining on non-unique keys multiplies matching rows (a cartesian explosion), artificially multiplying weight values and distorting population aggregates.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "14:40",
        "difficulty": "MEDIUM"
    },
    # SQL Lesson 3 Questions
    {
        "question_id": "Q-SQL-L3-01",
        "quiz_id": "QUIZ-SQL-03",
        "lesson_id": "sql-lesson-3",
        "competency_id": "COMP-027",
        "question_text": "Which window function assigns an ordinal ranking starting at 1 within each statistical division?",
        "options": [
            {"option_id": "A", "text": "COUNT() OVER (ORDER BY division)"},
            {"option_id": "B", "text": "ROW_NUMBER() OVER (PARTITION BY division ORDER BY output DESC)"},
            {"option_id": "C", "text": "GROUP BY division"},
            {"option_id": "D", "text": "SUM(division) OVER ()"}
        ],
        "correct_option": "B",
        "explanation": "ROW_NUMBER() partitioned by division creates independent integer sequences for each division partition.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "06:10",
        "difficulty": "MEDIUM"
    },
    # Python Lesson 1 Questions
    {
        "question_id": "Q-PY-L1-01",
        "quiz_id": "QUIZ-PY-01",
        "lesson_id": "python-lesson-1",
        "competency_id": "COMP-025",
        "question_text": "In Pandas survey data cleaning, why must genuine zero earnings be strictly distinguished from missing non-response (NaN)?",
        "options": [
            {"option_id": "A", "text": "Pandas does not support numbers with zeros"},
            {"option_id": "B", "text": "Treating non-response as zero biases downward mean income estimates, while treating zero as NaN distorts sample size and poverty rates"},
            {"option_id": "C", "text": "Zeros consume twice as much RAM memory as NaN"},
            {"option_id": "D", "text": "Exporting to CSV fails if zeros and NaNs exist"}
        ],
        "correct_option": "B",
        "explanation": "A reported zero is a valid economic measurement; non-response is unknown. Conflating them corrupts parametric estimation.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "04:15",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PY-L1-02",
        "quiz_id": "QUIZ-PY-01",
        "lesson_id": "python-lesson-1",
        "competency_id": "COMP-025",
        "question_text": "Using Tukey's standard boxplot rule for survey outlier detection, what boundary flags an extreme upper outlier?",
        "options": [
            {"option_id": "A", "text": "Mean + 1 Standard Deviation"},
            {"option_id": "B", "text": "Q3 + 1.5 * IQR"},
            {"option_id": "C", "text": "Median * 2"},
            {"option_id": "D", "text": "Maximum value / 2"}
        ],
        "correct_option": "B",
        "explanation": "Tukey's IQR rule flags observations exceeding the 75th percentile (Q3) plus 1.5 times the interquartile range.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "12:30",
        "difficulty": "EASY"
    },
    # Python Lesson 2 Questions
    {
        "question_id": "Q-PY-L2-01",
        "quiz_id": "QUIZ-PY-02",
        "lesson_id": "python-lesson-2",
        "competency_id": "COMP-025",
        "question_text": "Why are vectorized Pandas expressions preferred over python for-loops when batch processing millions of survey records?",
        "options": [
            {"option_id": "A", "text": "Vectorization executes in underlying optimized C loops without Python interpreter overhead"},
            {"option_id": "B", "text": "Python for-loops cannot operate on tabular data"},
            {"option_id": "C", "text": "Loops require specialized GPU hardware"},
            {"option_id": "D", "text": "Vectorized operations prevent file saving"}
        ],
        "correct_option": "A",
        "explanation": "Vectorized operations delegate array computation to optimized compiled C routines (NumPy/Pandas backend), yielding 100x+ performance gains.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "07:20",
        "difficulty": "EASY"
    },
    # R Lesson 1 Questions
    {
        "question_id": "Q-R-L1-01",
        "quiz_id": "QUIZ-R-01",
        "lesson_id": "r-lesson-1",
        "competency_id": "COMP-026",
        "question_text": "Which specialized R package is standard across national statistical agencies for analyzing complex survey designs with strata and clusters?",
        "options": [
            {"option_id": "A", "text": "ggplot2"},
            {"option_id": "B", "text": "survey (by Thomas Lumley)"},
            {"option_id": "C", "text": "tensorflow"},
            {"option_id": "D", "text": "shiny"}
        ],
        "correct_option": "B",
        "explanation": "The 'survey' package in R implements design-based inference, Taylor series linearization, and replicate weights for complex survey microdata.",
        "chunk_id": None,
        "timestamp_label": "05:00",
        "difficulty": "EASY"
    },
    # Probability Lesson 1 Questions
    {
        "question_id": "Q-PROB-L1-01",
        "quiz_id": "QUIZ-PROB-01",
        "lesson_id": "prob-lesson-1",
        "competency_id": "COMP-009",
        "question_text": "Under the Central Limit Theorem (CLT), what can be concluded about the distribution of the sample mean for large n?",
        "options": [
            {"option_id": "A", "text": "It approaches normality regardless of the underlying population distribution"},
            {"option_id": "B", "text": "It becomes strictly uniform"},
            {"option_id": "C", "text": "Its variance grows infinitely large"},
            {"option_id": "D", "text": "It equals the population maximum"}
        ],
        "correct_option": "A",
        "explanation": "The CLT guarantees that the distribution of standardized sample means approaches standard normal N(0,1) as sample size grows.",
        "chunk_id": None,
        "timestamp_label": "10:15",
        "difficulty": "MEDIUM"
    },
    # Quality Lesson 1 Questions
    {
        "question_id": "Q-QUAL-L1-01",
        "quiz_id": "QUIZ-QUAL-01",
        "lesson_id": "quality-lesson-1",
        "competency_id": "COMP-018",
        "question_text": "What type of validation check verifies that an individual's reported years of employment does not exceed their total age minus 14?",
        "options": [
            {"option_id": "A", "text": "Cross-variable logical consistency audit"},
            {"option_id": "B", "text": "Format string regex check"},
            {"option_id": "C", "text": "Network latency ping"},
            {"option_id": "D", "text": "Database collation conversion"}
        ],
        "correct_option": "A",
        "explanation": "Logical consistency audits evaluate plausible relationships between multiple related variables within a questionnaire response.",
        "chunk_id": None,
        "timestamp_label": "06:30",
        "difficulty": "EASY"
    },
    # ML Lesson 1 Questions
    {
        "question_id": "Q-ML-L1-01",
        "quiz_id": "QUIZ-ML-01",
        "lesson_id": "ml-lesson-1",
        "competency_id": "COMP-028",
        "question_text": "In predicting rare non-compliance events in administrative registers (e.g. 0.5% fraud), why is accuracy a misleading evaluation metric?",
        "options": [
            {"option_id": "A", "text": "A trivial model predicting 'no fraud' for all records attains 99.5% accuracy while detecting zero violations"},
            {"option_id": "B", "text": "Accuracy cannot be computed as a percentage"},
            {"option_id": "C", "text": "Precision and accuracy are mathematically identical"},
            {"option_id": "D", "text": "Administrative data cannot use machine learning"}
        ],
        "correct_option": "A",
        "explanation": "With severe class imbalance, accuracy gives a false sense of success. Recall, F1-score, and Precision-Recall AUC must be used.",
        "chunk_id": None,
        "timestamp_label": "14:20",
        "difficulty": "MEDIUM"
    }
]

def seed_practice_data(con: sqlite3.Connection):
    """Seeds quizzes and baseline questions if not already in database."""
    try:
        from app.services.question_bank import COMPREHENSIVE_QUIZZES, COMPREHENSIVE_QUESTIONS
        quizzes_to_seed = COMPREHENSIVE_QUIZZES
        questions_to_seed = COMPREHENSIVE_QUESTIONS
    except Exception:
        quizzes_to_seed = SEED_PRACTICE_QUIZZES
        questions_to_seed = SEED_PRACTICE_QUESTIONS

    with con:
        for q in quizzes_to_seed:
            con.execute("""
            INSERT OR REPLACE INTO practice_quizzes (quiz_id, lesson_id, course_id, competency_id, title, topic, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (q["quiz_id"], q["lesson_id"], q["course_id"], q["competency_id"], q["title"], q["topic"], q["created_at"]))
            
        for qn in questions_to_seed:
            con.execute("""
            INSERT OR REPLACE INTO practice_questions (
                question_id, quiz_id, lesson_id, competency_id, question_text, options_json,
                correct_option, explanation, chunk_id, timestamp_label, difficulty, is_approved, review_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'APPROVED')
            """, (
                qn["question_id"], qn["quiz_id"], qn["lesson_id"], qn["competency_id"],
                qn["question_text"], json.dumps(qn["options"]), qn["correct_option"],
                qn["explanation"], qn.get("chunk_id"), qn.get("timestamp_label"), qn.get("difficulty", "MEDIUM")
            ))

def generate_ai_quiz_questions(transcript_text: str, topic: str, count: int = 3) -> Optional[List[Dict[str, Any]]]:
    """
    Generates structured practice questions using Groq llama-3.3-70b-versatile.
    Rotates through available API keys in settings.groq_keys.
    """
    keys = settings.groq_keys
    if not keys:
        return None
        
    for key in keys:
        try:
            from groq import Groq
            client = Groq(api_key=key)
            prompt = f"""
You are an expert assessment author for the Indian Official Statistical System (MoSPI).
Based strictly on the following lesson transcript text, generate {count} high-quality, practical multiple-choice questions.

Topic: {topic}
Transcript:
\"\"\"{transcript_text}\"\"\"

Requirements:
1. Every question must be directly answerable from the transcript.
2. Provide exactly 4 options labeled A, B, C, D.
3. Mark exactly one correct option.
4. Provide a clear, educational explanation.
5. Provide a short citation snippet from the text.
6. Return ONLY valid JSON in this exact structure without markdown or backticks:
[
  {{
    "question_text": "...",
    "options": [
      {{"option_id": "A", "text": "..."}},
      {{"option_id": "B", "text": "..."}},
      {{"option_id": "C", "text": "..."}},
      {{"option_id": "D", "text": "..."}}
    ],
    "correct_option": "A",
    "explanation": "...",
    "citation_snippet": "...",
    "difficulty": "MEDIUM"
  }}
]
"""
            completion = client.chat.completions.create(
                model=settings.GROQ_PRIMARY_MODEL,
                messages=[
                    {"role": "system", "content": "You output only valid, parseable JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"} if hasattr(client.chat.completions, "response_format") else None
            )
            raw = completion.choices[0].message.content.strip()
            # Parse json
            if raw.startswith("```"):
                raw = raw.strip("`").removeprefix("json").strip()
            data = json.loads(raw)
            if isinstance(data, dict) and "questions" in data:
                return data["questions"]
            elif isinstance(data, list):
                return data
        except Exception as e:
            # Try next key
            continue
            
    return None
