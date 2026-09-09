"""
Official MoSPI Question Bank for iGOT Karmayogi Competency Platform.
Provides exhaustive practice questions and quizzes across all 28 curriculum lessons.
"""

from typing import List, Dict, Any

COMPREHENSIVE_QUIZZES: List[Dict[str, Any]] = [
    # Sampling Lessons (COMP-SAMPLING)
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
    # SQL Lessons (COMP-027)
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
    # Python Lessons (COMP-025)
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
    # R Lessons (COMP-026)
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
    # Probability Lessons (COMP-009)
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
    # Data Quality (COMP-018)
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
    # Machine Learning (COMP-028)
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

COMPREHENSIVE_QUESTIONS: List[Dict[str, Any]] = [
    # -------------------------------------------------------------
    # SAMPLING LESSON 1: Introduction to Probability Sampling & Frame Design
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-SAMP-L1-04",
        "quiz_id": "QUIZ-SAMPLING-01",
        "lesson_id": "sampling-lesson-1",
        "competency_id": "COMP-SAMPLING",
        "question_text": "If a sampling frame contains 5% duplicate enterprise listings, what distortion occurs if left uncorrected in an SRSWOR design?",
        "options": [
            {"option_id": "A", "text": "Duplicate units receive higher inclusion probabilities, leading to over-representation and positive estimation bias"},
            {"option_id": "B", "text": "The sample size automatically shrinks by 5%"},
            {"option_id": "C", "text": "Undercoverage increases proportionally"},
            {"option_id": "D", "text": "Design weights become uniformly equal to zero"}
        ],
        "correct_option": "A",
        "explanation": "Duplicate listings give those units twice the probability of selection, artificially inflating their influence unless de-duplicated prior to sample draw.",
        "chunk_id": "CHK-DEMO-004",
        "timestamp_label": "23:15",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-SAMP-L1-05",
        "quiz_id": "QUIZ-SAMPLING-01",
        "lesson_id": "sampling-lesson-1",
        "competency_id": "COMP-SAMPLING",
        "question_text": "In official government statistics, why can non-probability quota sampling never substitute for probability sampling frames?",
        "options": [
            {"option_id": "A", "text": "Because quota samples are illegal under civil law"},
            {"option_id": "B", "text": "Because non-probability designs do not permit objective mathematical calculation of standard errors or confidence intervals"},
            {"option_id": "C", "text": "Because quota samples require larger budgets than censuses"},
            {"option_id": "D", "text": "Because quota samples cannot be digitized into spreadsheets"}
        ],
        "correct_option": "B",
        "explanation": "Without known inclusion probabilities, design-based statistical inference and sampling error estimation are mathematically impossible.",
        "chunk_id": "CHK-DEMO-004",
        "timestamp_label": "24:50",
        "difficulty": "MEDIUM"
    },

    # -------------------------------------------------------------
    # SAMPLING LESSON 2: Simple Random Sampling & Systematic Selection
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-SAMP-L2-04",
        "quiz_id": "QUIZ-SAMPLING-02",
        "lesson_id": "sampling-lesson-2",
        "competency_id": "COMP-SAMPLING",
        "question_text": "When the sampling fraction f = n/N is negligible (e.g. f < 0.02), what happens to the Finite Population Correction (FPC)?",
        "options": [
            {"option_id": "A", "text": "The FPC factor approaches 1.0, meaning without-replacement variance is nearly identical to with-replacement variance"},
            {"option_id": "B", "text": "The FPC factor approaches 0, reducing standard error to zero"},
            {"option_id": "C", "text": "The variance doubles"},
            {"option_id": "D", "text": "The design weight becomes negative"}
        ],
        "correct_option": "A",
        "explanation": "FPC = sqrt(1 - n/N). When n/N is very small (<5%), (1 - n/N) ≈ 1, so finite correction has negligible impact on variance.",
        "chunk_id": "CHK-DEMO-001",
        "timestamp_label": "21:10",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SAMP-L2-05",
        "quiz_id": "QUIZ-SAMPLING-02",
        "lesson_id": "sampling-lesson-2",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What is circular systematic sampling used for in NSSO field operations?",
        "options": [
            {"option_id": "A", "text": "When the population size N is not an exact multiple of the desired sample size n"},
            {"option_id": "B", "text": "To interview respondents in a circular physical seating arrangement"},
            {"option_id": "C", "text": "To bypass the need for an initial random start"},
            {"option_id": "D", "text": "To double the sample size during bad weather"}
        ],
        "correct_option": "A",
        "explanation": "Circular systematic sampling chooses a random start between 1 and N and adds interval k repeatedly modulo N, guaranteeing fixed sample size n even when N is not a multiple of n.",
        "chunk_id": "CHK-DEMO-001",
        "timestamp_label": "23:45",
        "difficulty": "HARD"
    },

    # -------------------------------------------------------------
    # SAMPLING LESSON 3: Stratified Sampling & Proportional Allocation
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # SAMPLING LESSON 4: Cluster Sampling & Multi-Stage Household Surveys
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-SAMP-L4-04",
        "quiz_id": "QUIZ-SAMPLING-04",
        "lesson_id": "sampling-lesson-4",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What is the Design Effect (DEFF) in complex survey sampling?",
        "options": [
            {"option_id": "A", "text": "The ratio of the variance under the complex design to the variance under an SRS of the same sample size"},
            {"option_id": "B", "text": "The total budget required for field enumerators"},
            {"option_id": "C", "text": "The number of questionnaire pages"},
            {"option_id": "D", "text": "The non-response rate percentage"}
        ],
        "correct_option": "A",
        "explanation": "DEFF = Var(complex) / Var(SRS). In cluster surveys, DEFF is usually > 1 due to positive intra-cluster correlation (homogeneity within villages).",
        "chunk_id": "CHK-DEMO-005",
        "timestamp_label": "33:15",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-SAMP-L4-05",
        "quiz_id": "QUIZ-SAMPLING-04",
        "lesson_id": "sampling-lesson-4",
        "competency_id": "COMP-SAMPLING",
        "question_text": "If the intra-cluster correlation coefficient (roh) is 0.05 and cluster size m=21, what is the approximate design effect DEFF = 1 + (m - 1)*roh?",
        "options": [
            {"option_id": "A", "text": "1.00"},
            {"option_id": "B", "text": "2.00"},
            {"option_id": "C", "text": "3.00"},
            {"option_id": "D", "text": "0.50"}
        ],
        "correct_option": "B",
        "explanation": "DEFF = 1 + (21 - 1) * 0.05 = 1 + 20 * 0.05 = 1 + 1.00 = 2.00. This means twice the sample size is needed compared to SRS to achieve equal precision.",
        "chunk_id": "CHK-DEMO-005",
        "timestamp_label": "34:20",
        "difficulty": "HARD"
    },

    # -------------------------------------------------------------
    # SAMPLING LESSON 5: Calculating & Applying Survey Design Weights
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-SAMP-L5-04",
        "quiz_id": "QUIZ-SAMPLING-05",
        "lesson_id": "sampling-lesson-5",
        "competency_id": "COMP-SAMPLING",
        "question_text": "If 10 out of 50 selected sampled households refuse to respond in an urban stratum, how is non-response weight adjustment computed within the weighting cell?",
        "options": [
            {"option_id": "A", "text": "Multiply base weights of respondents by 50/40 = 1.25"},
            {"option_id": "B", "text": "Divide base weights by 2"},
            {"option_id": "C", "text": "Set non-respondents to zero and leave respondent weights unchanged"},
            {"option_id": "D", "text": "Subtract 10 from all household weights"}
        ],
        "correct_option": "A",
        "explanation": "Non-response adjustment factor is (Selected / Responding) = 50 / 40 = 1.25. This inflates respondent weights so the stratum sum remains equal to the target population total.",
        "chunk_id": "CHK-DEMO-003",
        "timestamp_label": "21:30",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-SAMP-L5-05",
        "quiz_id": "QUIZ-SAMPLING-05",
        "lesson_id": "sampling-lesson-5",
        "competency_id": "COMP-SAMPLING",
        "question_text": "What is post-stratification or calibration weighting in official statistical estimation?",
        "options": [
            {"option_id": "A", "text": "Adjusting sample weights so weighted sample totals match known independent benchmark population counts (e.g. Census age-sex totals)"},
            {"option_id": "B", "text": "Deleting observations that deviate from the regression line"},
            {"option_id": "C", "text": "Discarding weights after data entry"},
            {"option_id": "D", "text": "A method to re-interview non-respondents after 5 years"}
        ],
        "correct_option": "A",
        "explanation": "Calibration/post-stratification aligns survey totals with reliable external demographic controls, reducing variance and correcting for residual frame coverage flaws.",
        "chunk_id": "CHK-DEMO-003",
        "timestamp_label": "25:15",
        "difficulty": "HARD"
    },

    # -------------------------------------------------------------
    # SQL LESSON 1: Multi-Table Relational Joins
    # -------------------------------------------------------------
    {
        "question_id": "Q-SQL-L1-01",
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
        "question_id": "Q-SQL-L1-02",
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
    {
        "question_id": "Q-SQL-L1-03",
        "quiz_id": "QUIZ-SQL-01",
        "lesson_id": "sql-lesson-1",
        "competency_id": "COMP-027",
        "question_text": "If table A has 1,000 households and table B has 3,000 members, what does joining table A to B without an ON condition produce?",
        "options": [
            {"option_id": "A", "text": "An empty result"},
            {"option_id": "B", "text": "A Cartesian product of 3,000,000 rows combining every household with every member"},
            {"option_id": "C", "text": "Exactly 1,000 rows"},
            {"option_id": "D", "text": "A syntax error in all SQL dialects"}
        ],
        "correct_option": "B",
        "explanation": "Omitting the join condition yields a CROSS JOIN (Cartesian product) multiplying row counts: 1,000 * 3,000 = 3,000,000 rows.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "11:20",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SQL-L1-04",
        "quiz_id": "QUIZ-SQL-01",
        "lesson_id": "sql-lesson-1",
        "competency_id": "COMP-027",
        "question_text": "When joining two statistical registers on establishment PAN, why should you verify that PAN is unique in at least one table before joining?",
        "options": [
            {"option_id": "A", "text": "To prevent accidental many-to-many row expansion that artificially multiplies survey revenue totals"},
            {"option_id": "B", "text": "To make the query case-insensitive"},
            {"option_id": "C", "text": "To enable automatic spelling corrections"},
            {"option_id": "D", "text": "Because SQL prohibits joins on non-unique keys"}
        ],
        "correct_option": "A",
        "explanation": "If PAN is duplicated in both tables, each duplicate match multiplies rows, severely distorting weighted sum totals.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "18:40",
        "difficulty": "MEDIUM"
    },

    # -------------------------------------------------------------
    # SQL LESSON 2: Duplicate Detection & Data Reconciliation
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-SQL-L2-03",
        "quiz_id": "QUIZ-SQL-02",
        "lesson_id": "sql-lesson-2",
        "competency_id": "COMP-027",
        "question_text": "When de-duplicating a survey table where multiple entries exist per household_id, which pattern safely selects the latest verified entry?",
        "options": [
            {"option_id": "A", "text": "Using ROW_NUMBER() OVER (PARTITION BY household_id ORDER BY survey_timestamp DESC) and filtering where row_num = 1"},
            {"option_id": "B", "text": "DELETE FROM table WHERE household_id > 0"},
            {"option_id": "C", "text": "SELECT * FROM table LIMIT 1"},
            {"option_id": "D", "text": "TRUNCATE table"}
        ],
        "correct_option": "A",
        "explanation": "ROW_NUMBER() partitioned by the entity ID and ordered by timestamp isolates the latest valid record deterministically.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "21:10",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-SQL-L2-04",
        "quiz_id": "QUIZ-SQL-02",
        "lesson_id": "sql-lesson-2",
        "competency_id": "COMP-027",
        "question_text": "What is the key difference between UNION and UNION ALL when combining two district survey datasets?",
        "options": [
            {"option_id": "A", "text": "UNION removes duplicate rows across datasets with a sorting cost; UNION ALL preserves all rows including duplicates"},
            {"option_id": "B", "text": "UNION works only on numbers; UNION ALL works on text"},
            {"option_id": "C", "text": "UNION ALL deletes matching keys"},
            {"option_id": "D", "text": "UNION is for 2 tables; UNION ALL is for 3 or more tables"}
        ],
        "correct_option": "A",
        "explanation": "UNION runs a deduplication step across all columns, while UNION ALL simply concatenates the record sets without deduplication.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "26:30",
        "difficulty": "EASY"
    },

    # -------------------------------------------------------------
    # SQL LESSON 3: Advanced Grouping & Window Functions
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-SQL-L3-02",
        "quiz_id": "QUIZ-SQL-03",
        "lesson_id": "sql-lesson-3",
        "competency_id": "COMP-027",
        "question_text": "How does a window function differ from a traditional GROUP BY clause?",
        "options": [
            {"option_id": "A", "text": "GROUP BY collapses multiple rows into a single summary row; window functions compute aggregate values while preserving individual row identities"},
            {"option_id": "B", "text": "Window functions can only calculate counts"},
            {"option_id": "C", "text": "GROUP BY works in memory; window functions require temporary disk files"},
            {"option_id": "D", "text": "There is no functional difference"}
        ],
        "correct_option": "A",
        "explanation": "Window functions retain all original detail rows while attaching computed partition metrics (such as division mean or running total) to each row.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "12:40",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SQL-L3-03",
        "quiz_id": "QUIZ-SQL-03",
        "lesson_id": "sql-lesson-3",
        "competency_id": "COMP-027",
        "question_text": "How do RANK() and DENSE_RANK() differ when two enterprises have tied employment figures?",
        "options": [
            {"option_id": "A", "text": "RANK() skips subsequent rank numbers (e.g. 1, 2, 2, 4); DENSE_RANK() leaves no gaps (e.g. 1, 2, 2, 3)"},
            {"option_id": "B", "text": "DENSE_RANK() excludes ties from the output"},
            {"option_id": "C", "text": "RANK() is non-deterministic"},
            {"option_id": "D", "text": "DENSE_RANK() only works with integer data"}
        ],
        "correct_option": "A",
        "explanation": "RANK() produces gaps matching the tie count, whereas DENSE_RANK() always increments by 1 for the next distinct value.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "18:25",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-SQL-L3-04",
        "quiz_id": "QUIZ-SQL-03",
        "lesson_id": "sql-lesson-3",
        "competency_id": "COMP-027",
        "question_text": "Which clause calculates a running cumulative survey total over time without resetting?",
        "options": [
            {"option_id": "A", "text": "SUM(sample_weight) OVER (ORDER BY survey_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)"},
            {"option_id": "B", "text": "GROUP BY survey_date"},
            {"option_id": "C", "text": "SUM(sample_weight) OVER (PARTITION BY survey_date)"},
            {"option_id": "D", "text": "SELECT DISTINCT sample_weight"}
        ],
        "correct_option": "A",
        "explanation": "A window specification with ORDER BY and 'ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW' produces an accumulating cumulative sum.",
        "chunk_id": "CHK-SQL-001",
        "timestamp_label": "24:15",
        "difficulty": "HARD"
    },

    # -------------------------------------------------------------
    # SQL LESSON 4: NULL Handling & Three-Valued Logic in Registries
    # -------------------------------------------------------------
    {
        "question_id": "Q-SQL-L4-01",
        "quiz_id": "QUIZ-SQL-04",
        "lesson_id": "sql-lesson-4",
        "competency_id": "COMP-027",
        "question_text": "In SQL three-valued logic, what does the expression `revenue = NULL` evaluate to?",
        "options": [
            {"option_id": "A", "text": "TRUE"},
            {"option_id": "B", "text": "FALSE"},
            {"option_id": "C", "text": "UNKNOWN"},
            {"option_id": "D", "text": "NULL"}
        ],
        "correct_option": "C",
        "explanation": "Direct comparisons with NULL evaluate to UNKNOWN. To check for missing values, you must use `IS NULL` or `IS NOT NULL`.",
        "chunk_id": "CHK-SQL-002",
        "timestamp_label": "03:45",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SQL-L4-02",
        "quiz_id": "QUIZ-SQL-04",
        "lesson_id": "sql-lesson-4",
        "competency_id": "COMP-027",
        "question_text": "What is the crucial difference between `COUNT(*)` and `COUNT(income)` in a survey respondents table?",
        "options": [
            {"option_id": "A", "text": "`COUNT(*)` counts all rows including those with missing income; `COUNT(income)` counts only rows where income is NOT NULL"},
            {"option_id": "B", "text": "`COUNT(*)` only counts primary keys"},
            {"option_id": "C", "text": "`COUNT(income)` sums total income"},
            {"option_id": "D", "text": "They are mathematically identical in all SQL engines"}
        ],
        "correct_option": "A",
        "explanation": "Column aggregate `COUNT(column)` ignores NULL values, whereas `COUNT(*)` counts total rows regardless of column nullability.",
        "chunk_id": "CHK-SQL-002",
        "timestamp_label": "08:30",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SQL-L4-03",
        "quiz_id": "QUIZ-SQL-04",
        "lesson_id": "sql-lesson-4",
        "competency_id": "COMP-027",
        "question_text": "What does `COALESCE(subsidy_amount, 0.0)` accomplish in economic microdata processing?",
        "options": [
            {"option_id": "A", "text": "It returns `subsidy_amount` if it is NOT NULL; otherwise, it returns `0.0`"},
            {"option_id": "B", "text": "It sets all subsidies to zero"},
            {"option_id": "C", "text": "It averages `subsidy_amount` with zero"},
            {"option_id": "D", "text": "It deletes rows where subsidy is missing"}
        ],
        "correct_option": "A",
        "explanation": "COALESCE returns the first non-null expression in its argument list, providing a safe fallback value for calculations.",
        "chunk_id": "CHK-SQL-002",
        "timestamp_label": "14:15",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-SQL-L4-04",
        "quiz_id": "QUIZ-SQL-04",
        "lesson_id": "sql-lesson-4",
        "competency_id": "COMP-027",
        "question_text": "Why does adding a WHERE filter like `WHERE secondary.status = 'ACTIVE'` turn a LEFT JOIN into an accidental INNER JOIN?",
        "options": [
            {"option_id": "A", "text": "Because unmatched rows have NULL for `secondary.status`, and `NULL = 'ACTIVE'` evaluates to UNKNOWN which WHERE filters out"},
            {"option_id": "B", "text": "Because SQL converts LEFT to INNER automatically after 100 rows"},
            {"option_id": "C", "text": "Because status is a reserved keyword"},
            {"option_id": "D", "text": "It does not affect the join behaviour"}
        ],
        "correct_option": "A",
        "explanation": "Filtering the right table's columns in the WHERE clause discards all unmatched rows from the left table unless placed in the ON clause or wrapped in `OR secondary.status IS NULL`.",
        "chunk_id": "CHK-SQL-002",
        "timestamp_label": "20:40",
        "difficulty": "HARD"
    },

    # -------------------------------------------------------------
    # PYTHON LESSON 1: Microdata Cleaning with Pandas
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-PY-L1-03",
        "quiz_id": "QUIZ-PY-01",
        "lesson_id": "python-lesson-1",
        "competency_id": "COMP-025",
        "question_text": "Which Pandas method safely downcasts numeric integer columns to reduce RAM memory consumption when loading 10M record survey files?",
        "options": [
            {"option_id": "A", "text": "pd.to_numeric(df['col'], downcast='integer')"},
            {"option_id": "B", "text": "df.drop()"},
            {"option_id": "C", "text": "df.astype(str)"},
            {"option_id": "D", "text": "df.dropna()"}
        ],
        "correct_option": "A",
        "explanation": "pd.to_numeric with downcast='integer' automatically converts 64-bit integers to int8, int16, or int32 based on min/max range, cutting RAM by up to 75%.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "18:45",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PY-L1-04",
        "quiz_id": "QUIZ-PY-01",
        "lesson_id": "python-lesson-1",
        "competency_id": "COMP-025",
        "question_text": "Why should statistical analysts avoid blindly dropping rows containing missing survey items using `df.dropna()`?",
        "options": [
            {"option_id": "A", "text": "It can introduce severe non-response attrition bias if data is Missing At Random (MAR) or Missing Not At Random (MNAR)"},
            {"option_id": "B", "text": "Pandas throws an unrecoverable exception"},
            {"option_id": "C", "text": "It deletes the CSV on disk"},
            {"option_id": "D", "text": "Because Python only allows deleting 1 row at a time"}
        ],
        "correct_option": "A",
        "explanation": "Complete-case analysis (listwise deletion) severely truncates sample size and produces biased population estimates if non-response is correlated with study variables.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "25:20",
        "difficulty": "HARD"
    },

    # -------------------------------------------------------------
    # PYTHON LESSON 2: Automated Survey Data Processing Pipelines
    # -------------------------------------------------------------
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
    {
        "question_id": "Q-PY-L2-02",
        "quiz_id": "QUIZ-PY-02",
        "lesson_id": "python-lesson-2",
        "competency_id": "COMP-025",
        "question_text": "Which column file format is standard for storing high-volume official survey microdata with fast read times and schema preservation?",
        "options": [
            {"option_id": "A", "text": "Apache Parquet (.parquet)"},
            {"option_id": "B", "text": "Plain Text (.txt)"},
            {"option_id": "C", "text": "Rich Text (.rtf)"},
            {"option_id": "D", "text": "Word Document (.docx)"}
        ],
        "correct_option": "A",
        "explanation": "Apache Parquet is a columnar binary format with snappy compression, strict type schemas, and rapid projection/filter pushdown.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "14:10",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-PY-L2-03",
        "quiz_id": "QUIZ-PY-02",
        "lesson_id": "python-lesson-2",
        "competency_id": "COMP-025",
        "question_text": "In building automated ingestion pipelines, why is establishing defensive `assert` statements or Pandera schema validations critical?",
        "options": [
            {"option_id": "A", "text": "They halt processing immediately if survey data types, ranges, or primary key uniqueness violate official specifications"},
            {"option_id": "B", "text": "They convert code into encrypted bytecode"},
            {"option_id": "C", "text": "They prevent users from downloading data"},
            {"option_id": "D", "text": "They generate random test surveys automatically"}
        ],
        "correct_option": "A",
        "explanation": "Schema assertions prevent corrupt or misaligned field survey files from entering downstream aggregation registers unnoticed.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "21:35",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PY-L2-04",
        "quiz_id": "QUIZ-PY-02",
        "lesson_id": "python-lesson-2",
        "competency_id": "COMP-025",
        "question_text": "When processing huge microdata files that exceed available system RAM, which Pandas `read_csv` parameter enables stream processing?",
        "options": [
            {"option_id": "A", "text": "`chunksize=N` to iterate through batches of N rows at a time"},
            {"option_id": "B", "text": "`fast=True`"},
            {"option_id": "C", "text": "`ram_override=True`"},
            {"option_id": "D", "text": "`compress_all=True`"}
        ],
        "correct_option": "A",
        "explanation": "Specifying `chunksize` returns an iterator yielding DataFrames of chunk size rows, keeping memory footprint constant regardless of file size.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "28:15",
        "difficulty": "MEDIUM"
    },

    # -------------------------------------------------------------
    # PYTHON LESSON 3: Survey Microdata Weighting & Tabulation
    # -------------------------------------------------------------
    {
        "question_id": "Q-PY-L3-01",
        "quiz_id": "QUIZ-PY-03",
        "lesson_id": "python-lesson-3",
        "competency_id": "COMP-025",
        "question_text": "How do you calculate a weighted mean of survey consumption expenditure in Pandas using design weight column `wgt`?",
        "options": [
            {"option_id": "A", "text": "`np.average(df['expenditure'], weights=df['wgt'])`"},
            {"option_id": "B", "text": "`df['expenditure'].mean()`"},
            {"option_id": "C", "text": "`df['expenditure'] * df['wgt'].sum()`"},
            {"option_id": "D", "text": "`df['expenditure'].median()`"}
        ],
        "correct_option": "A",
        "explanation": "NumPy's `np.average()` with the `weights` argument computes sum(x * w) / sum(w), the mathematically correct Horvitz-Thompson weighted mean.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "05:10",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-PY-L3-02",
        "quiz_id": "QUIZ-PY-03",
        "lesson_id": "python-lesson-3",
        "competency_id": "COMP-025",
        "question_text": "When generating official weighted contingency tables (crosstabs) across Sector (Rural/Urban) and Employment status, which Pandas function is used?",
        "options": [
            {"option_id": "A", "text": "`pd.crosstab(df['sector'], df['status'], values=df['weight'], aggfunc='sum')`"},
            {"option_id": "B", "text": "`df.plot()`"},
            {"option_id": "C", "text": "`df.describe()`"},
            {"option_id": "D", "text": "`pd.concat()`"}
        ],
        "correct_option": "A",
        "explanation": "Passing `values=df['weight']` and `aggfunc='sum'` to `pd.crosstab` aggregates sampling weights to produce population-representative frequency tables.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "12:45",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PY-L3-03",
        "quiz_id": "QUIZ-PY-03",
        "lesson_id": "python-lesson-3",
        "competency_id": "COMP-025",
        "question_text": "What is the standard error formula consequence when weights have high variability (unequal weighting effect UWE)?",
        "options": [
            {"option_id": "A", "text": "Variance increases by factor `1 + CV(w)^2` (Kish's design effect formula for unequal weights)"},
            {"option_id": "B", "text": "Variance decreases to zero"},
            {"option_id": "C", "text": "Standard error remains identical to SRS"},
            {"option_id": "D", "text": "The sample size increases automatically"}
        ],
        "correct_option": "A",
        "explanation": "Kish's formula states that variance inflation from unequal weights equals 1 + (std(w)/mean(w))^2, reducing effective sample size.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "19:20",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-PY-L3-04",
        "quiz_id": "QUIZ-PY-03",
        "lesson_id": "python-lesson-3",
        "competency_id": "COMP-025",
        "question_text": "How can weight trimming (winsorization) be applied in Pandas to prevent extreme outlier weights from dominating survey estimates?",
        "options": [
            {"option_id": "A", "text": "`df['weight'] = df['weight'].clip(upper=df['weight'].quantile(0.99))`"},
            {"option_id": "B", "text": "`df['weight'] = 0`"},
            {"option_id": "C", "text": "`df.drop(columns=['weight'])`"},
            {"option_id": "D", "text": "`df['weight'] = df['weight'] * -1`"}
        ],
        "correct_option": "A",
        "explanation": "Clipping weights at the 99th percentile caps extreme weights, trading a small amount of bias for a large reduction in sampling variance.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "25:40",
        "difficulty": "HARD"
    },

    # -------------------------------------------------------------
    # PYTHON LESSON 4: Automated Data Quality Audits & Anomaly Verification
    # -------------------------------------------------------------
    {
        "question_id": "Q-PY-L4-01",
        "quiz_id": "QUIZ-PY-04",
        "lesson_id": "python-lesson-4",
        "competency_id": "COMP-025",
        "question_text": "Which condition checks that household total expenditure equals the sum of food, fuel, and non-food sub-components within a tolerance epsilon?",
        "options": [
            {"option_id": "A", "text": "`np.isclose(df['total'], df['food'] + df['fuel'] + df['non_food'], atol=1e-2)`"},
            {"option_id": "B", "text": "`df['total'] > 0`"},
            {"option_id": "C", "text": "`df['total'].sum() == 0`"},
            {"option_id": "D", "text": "`df['food'] == df['fuel']`"}
        ],
        "correct_option": "A",
        "explanation": "Floating point comparisons must use `np.isclose` or `abs(a - b) < tol` to avoid rounding discrepancies in financial balances.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "06:15",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PY-L4-02",
        "quiz_id": "QUIZ-PY-04",
        "lesson_id": "python-lesson-4",
        "competency_id": "COMP-025",
        "question_text": "What is the primary role of generating automated HTML QA audit reports during multi-round survey operations?",
        "options": [
            {"option_id": "A", "text": "To provide field supervisors with daily tracking of missing rates, digit preference spikes (Heaping), and outlier tallies"},
            {"option_id": "B", "text": "To print paper forms for field investigators"},
            {"option_id": "C", "text": "To convert survey data into multimedia slides"},
            {"option_id": "D", "text": "To encrypt files for military archiving"}
        ],
        "correct_option": "A",
        "explanation": "Automated QA dashboards flag enumerator errors, age heaping at multiples of 5, and high non-response while field teams can still re-visit households.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "13:30",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-PY-L4-03",
        "quiz_id": "QUIZ-PY-04",
        "lesson_id": "python-lesson-4",
        "competency_id": "COMP-025",
        "question_text": "Which index tests for age heaping (digit preference at digits 0 and 5) in demographic census returns?",
        "options": [
            {"option_id": "A", "text": "Whipple's Index and Myers' Blended Index"},
            {"option_id": "B", "text": "Gini Coefficient"},
            {"option_id": "C", "text": "Herfindahl-Hirschman Index"},
            {"option_id": "D", "text": "Consumer Price Index"}
        ],
        "correct_option": "A",
        "explanation": "Whipple's Index measures preference for terminal digits 0 and 5 in reported single-year ages; values above 125 indicate substantial reporting inaccuracies.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "19:40",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-PY-L4-04",
        "quiz_id": "QUIZ-PY-04",
        "lesson_id": "python-lesson-4",
        "competency_id": "COMP-025",
        "question_text": "In a pipeline audit script, what does `df.duplicated(subset=['state_code', 'district_code', 'sample_hh_no']).any()` verify?",
        "options": [
            {"option_id": "A", "text": "Whether any duplicate composite household identifier exists in the enumerated dataset"},
            {"option_id": "B", "text": "Whether all households are in the same state"},
            {"option_id": "C", "text": "The total number of districts in the country"},
            {"option_id": "D", "text": "Whether household size is greater than zero"}
        ],
        "correct_option": "A",
        "explanation": "Checking `duplicated()` on composite primary keys flags duplicate household schedules prior to relational database insertion.",
        "chunk_id": "CHK-PY-001",
        "timestamp_label": "23:50",
        "difficulty": "EASY"
    },

    # =============================================================
    # R LESSON 1: R Fundamentals for Official Statistical Computing
    # =============================================================
    {
        "question_id": "Q-R-L1-01",
        "quiz_id": "QUIZ-R-01",
        "lesson_id": "r-lesson-1",
        "competency_id": "COMP-026",
        "question_text": "Why are vectorized operations (e.g., `colSums`, `rowMeans`) preferred over iterative `for` loops when computing survey statistics in R?",
        "options": [
            {"option_id": "A", "text": "They leverage compiled C/Fortran routines that operate over contiguous memory blocks without interpreter overhead"},
            {"option_id": "B", "text": "Loops in R cannot execute arithmetic operations on floating point numbers"},
            {"option_id": "C", "text": "Vectorized functions eliminate the need for survey weights"},
            {"option_id": "D", "text": "For-loops automatically round all numbers to integers"}
        ],
        "correct_option": "A",
        "explanation": "Vectorized operations in base R execute in compiled C code without per-iteration interpreter overhead, delivering orders-of-magnitude speedups on large survey microdata frames.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "04:15",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-R-L1-02",
        "quiz_id": "QUIZ-R-01",
        "lesson_id": "r-lesson-1",
        "competency_id": "COMP-026",
        "question_text": "In base R, what does `mean(df$income, na.rm = TRUE)` do when the column contains missing entries?",
        "options": [
            {"option_id": "A", "text": "It computes the arithmetic mean strictly across non-missing observations, omitting NA values"},
            {"option_id": "B", "text": "It replaces all NA values with 0 before computing the mean"},
            {"option_id": "C", "text": "It returns NA whenever any missing value is detected"},
            {"option_id": "D", "text": "It imputes missing values using hot-deck donor matching"}
        ],
        "correct_option": "A",
        "explanation": "Setting `na.rm = TRUE` instructs R summary functions to exclude NA values from the calculation. Without it, R adheres to three-valued logic and returns `NA`.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "09:30",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-R-L1-03",
        "quiz_id": "QUIZ-R-01",
        "lesson_id": "r-lesson-1",
        "competency_id": "COMP-026",
        "question_text": "When cross-tabulating demographic survey variables, why is defining columns as `factor` with explicit `levels` critical?",
        "options": [
            {"option_id": "A", "text": "It guarantees that zero-count categories appear in published frequency tables rather than being silently omitted"},
            {"option_id": "B", "text": "Factors consume more RAM than plain character strings"},
            {"option_id": "C", "text": "Factors prevent researchers from applying survey weights"},
            {"option_id": "D", "text": "Factors automatically delete outlier responses"}
        ],
        "correct_option": "A",
        "explanation": "Explicit factor levels preserve the complete demographic coding schema (e.g., all administrative category codes), ensuring unobserved strata still appear with count zero in official reports.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "15:45",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-R-L1-04",
        "quiz_id": "QUIZ-R-01",
        "lesson_id": "r-lesson-1",
        "competency_id": "COMP-026",
        "question_text": "What is a principal data integrity advantage of using a `tibble` over a traditional base `data.frame` in MoSPI data pipelines?",
        "options": [
            {"option_id": "A", "text": "Tibbles never use partial column name matching and prevent silent type coercion of character vectors to factors"},
            {"option_id": "B", "text": "Tibbles can only store up to 100 rows"},
            {"option_id": "C", "text": "Tibbles automatically convert missing data into the overall mean"},
            {"option_id": "D", "text": "Tibbles allow duplicate primary keys across all observations"}
        ],
        "correct_option": "A",
        "explanation": "Tibbles throw explicit errors instead of guessing column names via partial matching (e.g. `df$st` matching `state_code`), preventing subtle bugs in official statistical scripts.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "22:10",
        "difficulty": "MEDIUM"
    },

    # =============================================================
    # R LESSON 2: Complex Survey Analysis with the survey Package
    # =============================================================
    {
        "question_id": "Q-R-L2-01",
        "quiz_id": "QUIZ-R-02",
        "lesson_id": "r-lesson-2",
        "competency_id": "COMP-026",
        "question_text": "In the R survey package, what design element does the argument `ids = ~psu_id` capture in `svydesign()`?",
        "options": [
            {"option_id": "A", "text": "Primary Sampling Units (clusters) used for multi-stage variance clustering adjustments"},
            {"option_id": "B", "text": "Unique individual respondent identification numbers"},
            {"option_id": "C", "text": "The finite population correction multiplier"},
            {"option_id": "D", "text": "The name of the interview supervisor"}
        ],
        "correct_option": "A",
        "explanation": "The `ids` parameter identifies cluster stages (PSUs, SSUs). Specifying clusters allows `svydesign` to properly account for intracluster correlation and design effects.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "04:50",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-R-L2-02",
        "quiz_id": "QUIZ-R-02",
        "lesson_id": "r-lesson-2",
        "competency_id": "COMP-026",
        "question_text": "Why must domain estimates (subgroup means) be calculated using `svyby()` or `subset.survey.design()` rather than simply filtering the raw data frame before creating the design object?",
        "options": [
            {"option_id": "A", "text": "Subsetting the raw data drops PSUs with zero domain units, causing standard errors and degrees of freedom to be miscalculated"},
            {"option_id": "B", "text": "The R survey package does not support data frames with fewer than 10,000 rows"},
            {"option_id": "C", "text": "Subsetting raw data converts all weights to negative values"},
            {"option_id": "D", "text": "Raw filtering eliminates sampling bias automatically"}
        ],
        "correct_option": "A",
        "explanation": "Subpopulation domain estimation in complex surveys requires keeping all PSUs and strata in the design structure to obtain correct Taylor series linearization standard errors.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "12:15",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-R-L2-03",
        "quiz_id": "QUIZ-R-02",
        "lesson_id": "r-lesson-2",
        "competency_id": "COMP-026",
        "question_text": "What is the role of `fpc = ~stratum_population` in `svydesign()`?",
        "options": [
            {"option_id": "A", "text": "It applies the Finite Population Correction to reduce variance when sampling without replacement from small populations"},
            {"option_id": "B", "text": "It specifies the inflation factor for consumer price index series"},
            {"option_id": "C", "text": "It filters out non-responding households"},
            {"option_id": "D", "text": "It forces sample weights to sum to 100"}
        ],
        "correct_option": "A",
        "explanation": "Supplying the stratum population size enables `survey` to apply finite population correction factors $\\sqrt{(N-n)/(N-1)}$, reducing variance as the sampling fraction grows.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "18:40",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-R-L2-04",
        "quiz_id": "QUIZ-R-02",
        "lesson_id": "r-lesson-2",
        "competency_id": "COMP-026",
        "question_text": "Which function in the `survey` package aligns multi-dimensional sample weight distributions to known census population margins?",
        "options": [
            {"option_id": "A", "text": "`rake()`"},
            {"option_id": "B", "text": "`lm()`"},
            {"option_id": "C", "text": "`sample()`"},
            {"option_id": "D", "text": "`t.test()`"}
        ],
        "correct_option": "A",
        "explanation": "`rake()` performs iterative proportional fitting (raking) across multiple marginal distributions (e.g., age-group, sex, rural/urban sector) to produce calibrated weights.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "25:10",
        "difficulty": "HARD"
    },

    # =============================================================
    # R LESSON 3: Variance Estimation & Inequality Indicators in R
    # =============================================================
    {
        "question_id": "Q-R-L3-01",
        "quiz_id": "QUIZ-R-03",
        "lesson_id": "r-lesson-3",
        "competency_id": "COMP-026",
        "question_text": "Why is Taylor Series Linearization preferred for ratio estimators and smooth survey statistics in large official surveys?",
        "options": [
            {"option_id": "A", "text": "It calculates analytical standard errors in a single computational pass without generating hundreds of replicate data sets"},
            {"option_id": "B", "text": "It works even when survey weights are missing"},
            {"option_id": "C", "text": "It requires no knowledge of strata or cluster assignments"},
            {"option_id": "D", "text": "It guarantees that all standard errors equal exactly zero"}
        ],
        "correct_option": "A",
        "explanation": "Taylor series linearization provides fast, closed-form variance approximations for smooth statistics (totals, ratios, means) by approximating non-linear statistics with linear first-order Taylor expansions.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "05:20",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-R-L3-02",
        "quiz_id": "QUIZ-R-03",
        "lesson_id": "r-lesson-3",
        "competency_id": "COMP-026",
        "question_text": "Which R package extension is specifically designed to calculate Gini coefficients, Quintile Share Ratios, and poverty headcount indices with complex survey designs?",
        "options": [
            {"option_id": "A", "text": "`convey` (or `ineq` with survey objects)"},
            {"option_id": "B", "text": "`ggplot2`"},
            {"option_id": "C", "text": "`lubridate`"},
            {"option_id": "D", "text": "`stringr`"}
        ],
        "correct_option": "A",
        "explanation": "The `convey` package integrates with Lumley's `survey` package to estimate income inequality metrics (Gini, Theil, Atkinson, Foster-Greer-Thorbecke) along with design-accurate standard errors.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "11:45",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-R-L3-03",
        "quiz_id": "QUIZ-R-03",
        "lesson_id": "r-lesson-3",
        "competency_id": "COMP-026",
        "question_text": "What severe statistical error occurs if an analyst runs standard `sd()` or `summary()` on a complex multistage cluster survey sample?",
        "options": [
            {"option_id": "A", "text": "Standard errors are severely underestimated because positive intracluster correlation is ignored, leading to spurious statistical significance"},
            {"option_id": "B", "text": "Estimates are biased downward by exactly 50%"},
            {"option_id": "C", "text": "R refuses to execute and crashes the operating system"},
            {"option_id": "D", "text": "Degrees of freedom become infinite"}
        ],
        "correct_option": "A",
        "explanation": "Standard i.i.d. formulas assume independent observations. Ignoring clustering neglects the design effect (DEFF), producing artificially narrow confidence intervals.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "17:30",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-R-L3-04",
        "quiz_id": "QUIZ-R-03",
        "lesson_id": "r-lesson-3",
        "competency_id": "COMP-026",
        "question_text": "In Balanced Repeated Replication (BRR) with Fay's adjustment, why are weights perturbed by a factor $k$ rather than setting half-sample weights to zero?",
        "options": [
            {"option_id": "A", "text": "To prevent subpopulation domain sample sizes from dropping to zero in small demographic cells"},
            {"option_id": "B", "text": "To artificially inflate the degrees of freedom"},
            {"option_id": "C", "text": "To eliminate the need for Hadamard matrices"},
            {"option_id": "D", "text": "To guarantee that all replicates have identical means"}
        ],
        "correct_option": "A",
        "explanation": "Fay's adjustment uses perturbation factors such as $1 \\pm k$ (e.g., $k=0.5$), ensuring all observations retain positive weight so non-linear estimators do not fail due to empty domains.",
        "chunk_id": "CHK-R-001",
        "timestamp_label": "23:15",
        "difficulty": "HARD"
    },

    # =============================================================
    # PROBABILITY LESSON 1: Probability Distributions & Variance Estimation
    # =============================================================
    {
        "question_id": "Q-PROB-L1-01",
        "quiz_id": "QUIZ-PROB-01",
        "lesson_id": "prob-lesson-1",
        "competency_id": "COMP-009",
        "question_text": "For $n$ independent and identically distributed random variables with population variance $\\sigma^2$, what is the variance of the sample mean $\\bar{X}$?",
        "options": [
            {"option_id": "A", "text": "$\\sigma^2 / n$"},
            {"option_id": "B", "text": "$n \\cdot \\sigma^2$"},
            {"option_id": "C", "text": "$\\sigma / \\sqrt{n}$"},
            {"option_id": "D", "text": "$\\sigma^2$"}
        ],
        "correct_option": "A",
        "explanation": "The variance of the sample mean is $\\text{Var}(\\bar{X}) = \\sigma^2 / n$. Its square root $\\sigma / \\sqrt{n}$ is the standard error.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "05:10",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-PROB-L1-02",
        "quiz_id": "QUIZ-PROB-01",
        "lesson_id": "prob-lesson-1",
        "competency_id": "COMP-009",
        "question_text": "When sampling without replacement from a finite registry of $N$ establishments, which distribution models the exact number of defective returns?",
        "options": [
            {"option_id": "A", "text": "Hypergeometric distribution"},
            {"option_id": "B", "text": "Binomial distribution"},
            {"option_id": "C", "text": "Geometric distribution"},
            {"option_id": "D", "text": "Normal distribution"}
        ],
        "correct_option": "A",
        "explanation": "Sampling without replacement causes successive draws to be dependent, which is governed exactly by the Hypergeometric distribution.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "12:40",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PROB-L1-03",
        "quiz_id": "QUIZ-PROB-01",
        "lesson_id": "prob-lesson-1",
        "competency_id": "COMP-009",
        "question_text": "In an establishment safety audit where industrial accidents occur rarely at rate $\\lambda = 4$ per quarter, what is the expected variance of the quarterly accident count under a Poisson model?",
        "options": [
            {"option_id": "A", "text": "4"},
            {"option_id": "B", "text": "2"},
            {"option_id": "C", "text": "16"},
            {"option_id": "D", "text": "0.25"}
        ],
        "correct_option": "A",
        "explanation": "A defining property of the Poisson distribution is that its variance equals its mean: $\\text{Var}(X) = E[X] = \\lambda = 4$.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "18:25",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PROB-L1-04",
        "quiz_id": "QUIZ-PROB-01",
        "lesson_id": "prob-lesson-1",
        "competency_id": "COMP-009",
        "question_text": "According to Chebyshev's Inequality, what is the maximum proportion of values in any arbitrary statistical distribution that can lie beyond 3 standard deviations from the mean?",
        "options": [
            {"option_id": "A", "text": "$1 / 3^2 = 1/9 \\approx 11.11\\%$"},
            {"option_id": "B", "text": "$5.0\\%$"},
            {"option_id": "C", "text": "$0.27\\%$"},
            {"option_id": "D", "text": "$50.0\\%$"}
        ],
        "correct_option": "A",
        "explanation": "Chebyshev's inequality guarantees $P(|X - \\mu| \\ge k\\sigma) \\le 1/k^2$. For $k=3$, at most $1/9 \\approx 11.1\\%$ can fall beyond 3 standard deviations.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "24:50",
        "difficulty": "HARD"
    },

    # =============================================================
    # PROBABILITY LESSON 2: Central Limit Theorem & Finite Population Correction
    # =============================================================
    {
        "question_id": "Q-PROB-L2-01",
        "quiz_id": "QUIZ-PROB-02",
        "lesson_id": "prob-lesson-2",
        "competency_id": "COMP-009",
        "question_text": "Why does the Central Limit Theorem allow survey statisticians to construct normal confidence intervals for average household expenditure even when microdata is heavily right-skewed?",
        "options": [
            {"option_id": "A", "text": "The distribution of the sample mean converges to normality as sample size increases, even if the underlying population distribution is skewed"},
            {"option_id": "B", "text": "Right-skewed data is automatically transformed into a Gaussian bell curve during field collection"},
            {"option_id": "C", "text": "Survey weighting eliminates all skewness from the original population"},
            {"option_id": "D", "text": "The sample mean cannot exceed the population median"}
        ],
        "correct_option": "A",
        "explanation": "Under the Central Limit Theorem, the sum or average of independent random variables tends toward a normal distribution as $n$ grows large, regardless of underlying skewness.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "04:15",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PROB-L2-02",
        "quiz_id": "QUIZ-PROB-02",
        "lesson_id": "prob-lesson-2",
        "competency_id": "COMP-009",
        "question_text": "A population contains $N = 10,000$ enterprises and a sample of $n = 1,900$ is drawn without replacement. What is the approximate Finite Population Correction (FPC) factor $\\sqrt{(N-n)/(N-1)}$?",
        "options": [
            {"option_id": "A", "text": "$\\sqrt{8100 / 9999} \\approx \\sqrt{0.81} = 0.90$"},
            {"option_id": "B", "text": "$1.00$"},
            {"option_id": "C", "text": "$0.19$"},
            {"option_id": "D", "text": "$0.50$"}
        ],
        "correct_option": "A",
        "explanation": "The FPC is $\\sqrt{(10000 - 1900)/(10000 - 1)} = \\sqrt{8100 / 9999} \\approx \\sqrt{0.81} = 0.90$, reducing the standard error by $10\\%$.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "11:20",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-PROB-L2-03",
        "quiz_id": "QUIZ-PROB-02",
        "lesson_id": "prob-lesson-2",
        "competency_id": "COMP-009",
        "question_text": "What standard rule of thumb determines when the Finite Population Correction can be safely ignored in survey estimation?",
        "options": [
            {"option_id": "A", "text": "When the sampling fraction $n / N < 0.05$ (less than 5 percent of the population is sampled)"},
            {"option_id": "B", "text": "When the population size is less than 50"},
            {"option_id": "C", "text": "When the standard deviation is unknown"},
            {"option_id": "D", "text": "When the sample size is odd"}
        ],
        "correct_option": "A",
        "explanation": "When $n/N < 0.05$, the FPC $\\sqrt{1 - n/N} > \\sqrt{0.95} \\approx 0.975$, meaning the variance adjustment is under $2.5\\%$ and negligibly affects standard errors.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "17:45",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-PROB-L2-04",
        "quiz_id": "QUIZ-PROB-02",
        "lesson_id": "prob-lesson-2",
        "competency_id": "COMP-009",
        "question_text": "What does the Weak Law of Large Numbers (WLLN) state regarding the sample mean $\\bar{X}_n$?",
        "options": [
            {"option_id": "A", "text": "For any $\\epsilon > 0$, $\\lim_{n \\to \\infty} P(|\\bar{X}_n - \\mu| < \\epsilon) = 1$ (convergence in probability)"},
            {"option_id": "B", "text": "The sample mean is always exactly equal to the population mean for every sample"},
            {"option_id": "C", "text": "The variance of the population shrinks to zero as more units are sampled"},
            {"option_id": "D", "text": "Sample sizes must exceed 1,000,000 for means to be calculated"}
        ],
        "correct_option": "A",
        "explanation": "The Weak Law of Large Numbers ensures that the sample mean converges in probability to the expected value $\\mu$ as sample size $n$ approaches infinity.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "23:30",
        "difficulty": "HARD"
    },

    # =============================================================
    # PROBABILITY LESSON 3: Confidence Intervals & Hypothesis Testing
    # =============================================================
    {
        "question_id": "Q-PROB-L3-01",
        "quiz_id": "QUIZ-PROB-03",
        "lesson_id": "prob-lesson-3",
        "competency_id": "COMP-009",
        "question_text": "In a survey of $n = 400$ households, an estimated proportion $\\hat{p} = 0.50$ is obtained with simple random sampling. What is the margin of error for a 95% confidence interval ($z = 1.96$)?",
        "options": [
            {"option_id": "A", "text": "$1.96 \\times \\sqrt{0.50 \\times 0.50 / 400} = 1.96 \\times 0.025 = 0.049$ (4.9 percentage points)"},
            {"option_id": "B", "text": "0.10 (10 percentage points)"},
            {"option_id": "C", "text": "0.01 (1 percentage point)"},
            {"option_id": "D", "text": "0.25 (25 percentage points)"}
        ],
        "correct_option": "A",
        "explanation": "Standard error is $\\sqrt{0.25/400} = 0.5/20 = 0.025$. Multiplying by 1.96 yields a margin of error of $\\pm 0.049$ or $4.9\\%$.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "06:10",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PROB-L3-02",
        "quiz_id": "QUIZ-PROB-03",
        "lesson_id": "prob-lesson-3",
        "competency_id": "COMP-009",
        "question_text": "What is a Type I error in statistical quality control audits of survey data?",
        "options": [
            {"option_id": "A", "text": "Rejecting a true null hypothesis (e.g., falsely concluding an enumerator's data is fraudulent when it is clean)"},
            {"option_id": "B", "text": "Failing to reject a false null hypothesis (missing genuine fraud)"},
            {"option_id": "C", "text": "Entering data into the wrong column"},
            {"option_id": "D", "text": "Calculating an average with non-response weights"}
        ],
        "correct_option": "A",
        "explanation": "A Type I error is a false positive: rejecting $H_0$ when $H_0$ is actually true. The significance level $\\alpha$ bounds its probability.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "12:45",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-PROB-L3-03",
        "quiz_id": "QUIZ-PROB-03",
        "lesson_id": "prob-lesson-3",
        "competency_id": "COMP-009",
        "question_text": "What is the precise statistical definition of a p-value?",
        "options": [
            {"option_id": "A", "text": "The probability of observing a test statistic as extreme or more extreme than observed, assuming the null hypothesis is true"},
            {"option_id": "B", "text": "The probability that the alternative hypothesis is true"},
            {"option_id": "C", "text": "The proportion of sample units that answered the survey question"},
            {"option_id": "D", "text": "The margin of error of the sample estimate"}
        ],
        "correct_option": "A",
        "explanation": "A p-value measures evidence against $H_0$; it is $P(\\text{data as or more extreme} \\mid H_0)$. It is not the probability that $H_0$ is true.",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "18:30",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-PROB-L3-04",
        "quiz_id": "QUIZ-PROB-03",
        "lesson_id": "prob-lesson-3",
        "competency_id": "COMP-009",
        "question_text": "In a complex survey design with 80 strata and 160 sampled PSUs (2 PSUs per stratum), what are the nominal design degrees of freedom for hypothesis testing?",
        "options": [
            {"option_id": "A", "text": "$160 - 80 = 80$ degrees of freedom (Number of PSUs minus Number of Strata)"},
            {"option_id": "B", "text": "The total number of interview respondents minus 1"},
            {"option_id": "C", "text": "80 degrees of freedom times 2"},
            {"option_id": "D", "text": "Infinity"}
        ],
        "correct_option": "A",
        "explanation": "In stratified multistage designs, design degrees of freedom equal the total number of primary sampling units minus the number of strata ($PSU - Strata = 160 - 80 = 80$).",
        "chunk_id": "CHK-PROB-001",
        "timestamp_label": "24:15",
        "difficulty": "HARD"
    },

    # =============================================================
    # DATA QUALITY LESSON 1: Data Auditing, Outlier Detection & Error Screening
    # =============================================================
    {
        "question_id": "Q-QUAL-L1-01",
        "quiz_id": "QUIZ-QUAL-01",
        "lesson_id": "quality-lesson-1",
        "competency_id": "COMP-018",
        "question_text": "Why is Tukey's Fences method ($[Q_1 - 1.5\\text{IQR}, Q_3 + 1.5\\text{IQR}]$) preferred over $Z$-score thresholds ($|Z| > 3$) for screening economic survey variables?",
        "options": [
            {"option_id": "A", "text": "Tukey's IQR relies on medians and quartiles which are not inflated by extreme outliers, avoiding the masking effect"},
            {"option_id": "B", "text": "Z-scores cannot be calculated for variables with positive values"},
            {"option_id": "C", "text": "Tukey's fences automatically delete all flagged values"},
            {"option_id": "D", "text": "Z-scores require knowing the exact census population"}
        ],
        "correct_option": "A",
        "explanation": "Extreme outliers inflate the sample mean and standard deviation, causing other genuine anomalies to hide (masking). Quartiles are robust against extreme values.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "05:15",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-QUAL-L1-02",
        "quiz_id": "QUIZ-QUAL-01",
        "lesson_id": "quality-lesson-1",
        "competency_id": "COMP-018",
        "question_text": "What is the operational distinction between a 'hard edit' and a 'soft edit' in CAPI survey field applications?",
        "options": [
            {"option_id": "A", "text": "A hard edit halts survey entry until an impossible value is corrected; a soft edit triggers a warning allowing enumerators to confirm unusual but valid situations"},
            {"option_id": "B", "text": "Hard edits run on desktop computers; soft edits run on tablets"},
            {"option_id": "C", "text": "Soft edits permanently delete respondent records"},
            {"option_id": "D", "text": "Hard edits are applied only after field work is completed"}
        ],
        "correct_option": "A",
        "explanation": "Hard edits prevent mathematically impossible entries (e.g. age = 250). Soft edits alert the field investigator to probe unusual responses (e.g. household food spend 10x median).",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "11:30",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-QUAL-L1-03",
        "quiz_id": "QUIZ-QUAL-01",
        "lesson_id": "quality-lesson-1",
        "competency_id": "COMP-018",
        "question_text": "Which demographic consistency check represents a deterministic relational constraint in household microdata?",
        "options": [
            {"option_id": "A", "text": "Mother's age at childbirth must be at least 13–15 years greater than the biological child's current age"},
            {"option_id": "B", "text": "All household members must share the same occupation"},
            {"option_id": "C", "text": "Household monthly income must exceed exactly 10,000 rupees"},
            {"option_id": "D", "text": "Every person must own agricultural land"}
        ],
        "correct_option": "A",
        "explanation": "Relational constraints compare attributes across household members to prevent biological impossibilities or contradictory familial relationships.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "17:50",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-QUAL-L1-04",
        "quiz_id": "QUIZ-QUAL-01",
        "lesson_id": "quality-lesson-1",
        "competency_id": "COMP-018",
        "question_text": "How does Benford's Law assist data quality auditors in identifying enumerator fabrication (curbstoning) in financial survey returns?",
        "options": [
            {"option_id": "A", "text": "Naturally occurring unconstrained numbers exhibit leading digit 1 approximately 30.1% of the time; fabricated numbers deviate with uniform digit distributions"},
            {"option_id": "B", "text": "It checks whether all GPS coordinates fall inside the designated district boundary"},
            {"option_id": "C", "text": "It verifies that household signatures are unique"},
            {"option_id": "D", "text": "It requires every respondent to provide a tax return"}
        ],
        "correct_option": "A",
        "explanation": "Benford's Law describes logarithmic first-digit frequency ($P(d) = \\log_{10}(1 + 1/d)$). Fabricators intuitively spread first digits uniformly, alerting auditors.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "23:40",
        "difficulty": "HARD"
    },

    # =============================================================
    # DATA QUALITY LESSON 2: Imputation Methods & Hot-Deck vs Cold-Deck
    # =============================================================
    {
        "question_id": "Q-QUAL-L2-01",
        "quiz_id": "QUIZ-QUAL-02",
        "lesson_id": "quality-lesson-2",
        "competency_id": "COMP-018",
        "question_text": "Why is simple unconditional mean imputation considered statistically unacceptable for official statistical microdata?",
        "options": [
            {"option_id": "A", "text": "It artificially creates a spike at the mean, severely underestimating variance and distorting correlation with other variables"},
            {"option_id": "B", "text": "It converts all numeric columns to text"},
            {"option_id": "C", "text": "It increases computational run times by 100x"},
            {"option_id": "D", "text": "It can only be used when 100% of data is missing"}
        ],
        "correct_option": "A",
        "explanation": "Mean imputation adds values with zero variance, artificially shrinking standard errors and biasing hypothesis tests toward false significance.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "05:40",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-QUAL-L2-02",
        "quiz_id": "QUIZ-QUAL-02",
        "lesson_id": "quality-lesson-2",
        "competency_id": "COMP-018",
        "question_text": "In survey methodology, what characterizes 'Sequential Hot-Deck Imputation'?",
        "options": [
            {"option_id": "A", "text": "Missing values are replaced by the valid value of the most recently processed respondent within the same demographic imputation class"},
            {"option_id": "B", "text": "Values are copied from a previous decade's census (Cold-Deck)"},
            {"option_id": "C", "text": "Missing values are set to zero"},
            {"option_id": "D", "text": "An automated regression model generates continuous synthetic numbers"}
        ],
        "correct_option": "A",
        "explanation": "Hot-deck imputation substitutes values from an actual responding unit in the current survey round within the same stratum or demographic cell, preserving realistic discrete values.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "12:10",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-QUAL-L2-03",
        "quiz_id": "QUIZ-QUAL-02",
        "lesson_id": "quality-lesson-2",
        "competency_id": "COMP-018",
        "question_text": "What is the primary advantage of Predictive Mean Matching (PMM) over standard linear regression imputation?",
        "options": [
            {"option_id": "A", "text": "It borrows an observed value from the nearest real donor, guaranteeing that imputed values are feasible and never out-of-bounds (e.g., negative incomes)"},
            {"option_id": "B", "text": "It requires no explanatory predictors"},
            {"option_id": "C", "text": "It runs without requiring any observed donor records"},
            {"option_id": "D", "text": "It is restricted to binary yes/no variables"}
        ],
        "correct_option": "A",
        "explanation": "PMM models the outcome, finds donor cases whose predicted values match the recipient's prediction, and copies the actual donor's observed value, preserving valid support and non-linearities.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "18:20",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-QUAL-L2-04",
        "quiz_id": "QUIZ-QUAL-02",
        "lesson_id": "quality-lesson-2",
        "competency_id": "COMP-018",
        "question_text": "Under MoSPI data transparency protocols, what metadata artifact must accompany every imputed variable in a released microdata file?",
        "options": [
            {"option_id": "A", "text": "A corresponding imputation flag column (e.g., `var_imp = 1` for imputed, `0` for raw observed)"},
            {"option_id": "B", "text": "The home address of the respondent who donated the value"},
            {"option_id": "C", "text": "A notarized affidavit from the state director"},
            {"option_id": "D", "text": "A deletion log removing the column from public access"}
        ],
        "correct_option": "A",
        "explanation": "Imputation flags allow independent researchers to evaluate imputation rates, exclude imputed cases for sensitivity checks, or apply specialized variance formulas.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "24:50",
        "difficulty": "EASY"
    },

    # =============================================================
    # DATA QUALITY LESSON 3: Statistical Disclosure Control & Anonymization
    # =============================================================
    {
        "question_id": "Q-QUAL-L3-01",
        "quiz_id": "QUIZ-QUAL-03",
        "lesson_id": "quality-lesson-3",
        "competency_id": "COMP-018",
        "question_text": "What does the criterion of $k$-anonymity guarantee when publishing public-use survey microdata?",
        "options": [
            {"option_id": "A", "text": "Each unique combination of quasi-identifiers (e.g. age, gender, district) is shared by at least $k$ individuals in the published dataset"},
            {"option_id": "B", "text": "Exactly $k$ variables are deleted from the survey questionnaire"},
            {"option_id": "C", "text": "The sample size must be a multiple of $k$"},
            {"option_id": "D", "text": "Only $k$ government officials have access to the encryption key"}
        ],
        "correct_option": "A",
        "explanation": "$k$-anonymity ensures an individual cannot be distinguished from at least $k-1$ other respondents based on published quasi-identifiers.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "05:10",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-QUAL-L3-02",
        "quiz_id": "QUIZ-QUAL-03",
        "lesson_id": "quality-lesson-3",
        "competency_id": "COMP-018",
        "question_text": "What vulnerability in pure $k$-anonymity does $l$-diversity overcome?",
        "options": [
            {"option_id": "A", "text": "Homogeneity attacks where all $k$ records in an equivalence class share the exact same sensitive value (e.g., all have defaulted on loans)"},
            {"option_id": "B", "text": "SQL injection attacks against web databases"},
            {"option_id": "C", "text": "Excessive computational time during sorting"},
            {"option_id": "D", "text": "Inability to calculate sample means"}
        ],
        "correct_option": "A",
        "explanation": "If all $k$ individuals in a group have the same sensitive attribute, an attacker knowing a person belongs to that group discovers their sensitive value with certainty. $l$-diversity requires at least $l$ distinct sensitive values.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "11:50",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-QUAL-L3-03",
        "quiz_id": "QUIZ-QUAL-03",
        "lesson_id": "quality-lesson-3",
        "competency_id": "COMP-018",
        "question_text": "Why do official statistical agencies apply 'top-coding' to income and wealth variables in public datasets?",
        "options": [
            {"option_id": "A", "text": "To prevent identification of ultra-high-net-worth individuals whose extreme values stand out in public registries"},
            {"option_id": "B", "text": "To increase the calculated national GDP total"},
            {"option_id": "C", "text": "To ensure income values fit into 16-bit integer database fields"},
            {"option_id": "D", "text": "To eliminate the need for income tax reporting"}
        ],
        "correct_option": "A",
        "explanation": "Top-coding replaces values above a threshold (e.g., top 1%) with the threshold value or mean, preventing re-identification of conspicuous outliers.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "18:15",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-QUAL-L3-04",
        "quiz_id": "QUIZ-QUAL-03",
        "lesson_id": "quality-lesson-3",
        "competency_id": "COMP-018",
        "question_text": "In Differential Privacy, what parameter $\\epsilon$ (epsilon) governs the privacy budget?",
        "options": [
            {"option_id": "A", "text": "The privacy loss parameter: smaller $\\epsilon$ provides stronger privacy by injecting more calibrated noise, while larger $\\epsilon$ provides higher utility with less privacy"},
            {"option_id": "B", "text": "The total number of rows in the confidential database"},
            {"option_id": "C", "text": "The survey response rate percentage"},
            {"option_id": "D", "text": "The number of survey supervisors"}
        ],
        "correct_option": "A",
        "explanation": "Epsilon $(\\epsilon)$ controls the privacy-utility tradeoff. As $\\epsilon \\to 0$, outputs become statistically indistinguishable regardless of any single individual's inclusion.",
        "chunk_id": "CHK-QUAL-001",
        "timestamp_label": "24:30",
        "difficulty": "HARD"
    },

    # =============================================================
    # MACHINE LEARNING LESSON 1: Supervised Learning & Evaluation
    # =============================================================
    {
        "question_id": "Q-ML-L1-01",
        "quiz_id": "QUIZ-ML-01",
        "lesson_id": "ml-lesson-1",
        "competency_id": "COMP-028",
        "question_text": "In automated anomaly detection for official survey returns, why is Precision prioritized over Recall when flagging records for manual re-survey audits?",
        "options": [
            {"option_id": "A", "text": "Re-survey field investigations are expensive; high precision minimizes costly false alarms sent to field teams"},
            {"option_id": "B", "text": "High precision guarantees 100% of all errors are discovered"},
            {"option_id": "C", "text": "Recall can only be calculated for regression models"},
            {"option_id": "D", "text": "Precision eliminates the need for test datasets"}
        ],
        "correct_option": "A",
        "explanation": "Precision = $TP / (TP + FP)$. When field visits have substantial real-world costs, high precision ensures audit teams only investigate highly probable irregularities.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "06:20",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-ML-L1-02",
        "quiz_id": "QUIZ-ML-01",
        "lesson_id": "ml-lesson-1",
        "competency_id": "COMP-028",
        "question_text": "What does an Area Under the ROC Curve (ROC-AUC) score of 0.50 indicate about a classification model?",
        "options": [
            {"option_id": "A", "text": "The model has zero discriminative ability, performing no better than random guessing"},
            {"option_id": "B", "text": "The model has 50% accuracy on the training set"},
            {"option_id": "C", "text": "The model achieves perfect classification without errors"},
            {"option_id": "D", "text": "The model is overfitted to the training data"}
        ],
        "correct_option": "A",
        "explanation": "An ROC-AUC of 0.50 corresponds to the diagonal chance line (random guessing), whereas an AUC of 1.0 represents perfect discrimination across all classification thresholds.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "12:50",
        "difficulty": "EASY"
    },
    {
        "question_id": "Q-ML-L1-03",
        "quiz_id": "QUIZ-ML-01",
        "lesson_id": "ml-lesson-1",
        "competency_id": "COMP-028",
        "question_text": "Why must Stratified K-Fold cross-validation be utilized when training models to predict rare events (such as business bankruptcy or extreme poverty)?",
        "options": [
            {"option_id": "A", "text": "It ensures each fold contains the same proportion of target classes as the complete population, preventing folds with zero positive cases"},
            {"option_id": "B", "text": "It speeds up model execution by dropping 90% of the training data"},
            {"option_id": "C", "text": "It removes all correlation between input features"},
            {"option_id": "D", "text": "It eliminates the need for hyperparameter tuning"}
        ],
        "correct_option": "A",
        "explanation": "In imbalanced datasets, random splitting can yield validation splits with no positive examples. Stratification guarantees representative proportions in every fold.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "19:15",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-ML-L1-04",
        "quiz_id": "QUIZ-ML-01",
        "lesson_id": "ml-lesson-1",
        "competency_id": "COMP-028",
        "question_text": "From a confusion matrix with $TP = 80$, $FP = 20$, $FN = 10$, $TN = 890$, what is the calculated F1-score?",
        "options": [
            {"option_id": "A", "text": "Precision = $80/100 = 0.80$; Recall = $80/90 \\approx 0.889$; $\\text{F1} = 2 \\times (0.80 \\times 0.889)/(0.80 + 0.889) \\approx 0.842$"},
            {"option_id": "B", "text": "0.50"},
            {"option_id": "C", "text": "0.97"},
            {"option_id": "D", "text": "0.10"}
        ],
        "correct_option": "A",
        "explanation": "F1 is the harmonic mean of precision ($80/100 = 0.80$) and recall ($80/90 \\approx 0.889$). $2 \\times (0.8 \\times 0.8889) / (0.8 + 0.8889) \\approx 0.842$.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "25:30",
        "difficulty": "HARD"
    },

    # =============================================================
    # MACHINE LEARNING LESSON 2: Record Linkage & Entity Resolution
    # =============================================================
    {
        "question_id": "Q-ML-L2-01",
        "quiz_id": "QUIZ-ML-02",
        "lesson_id": "ml-lesson-2",
        "competency_id": "COMP-028",
        "question_text": "Under the Fellegi-Sunter methodology for probabilistic record linkage, what determines the agreement weight for a matching field?",
        "options": [
            {"option_id": "A", "text": "$\\log_2(m / u)$, where $m = P(\\text{agree} \\mid \\text{match})$ and $u = P(\\text{agree} \\mid \\text{non-match})$"},
            {"option_id": "B", "text": "The length of the string in characters"},
            {"option_id": "C", "text": "The ratio of sample size to population size"},
            {"option_id": "D", "text": "The number of missing values in the register"}
        ],
        "correct_option": "A",
        "explanation": "Fellegi-Sunter agreement weight is the log likelihood ratio $\\log_2(m/u)$. Agreement on a rare identifier gives higher weight than agreement on a common name.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "05:10",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-ML-L2-02",
        "quiz_id": "QUIZ-ML-02",
        "lesson_id": "ml-lesson-2",
        "competency_id": "COMP-028",
        "question_text": "Why is 'blocking' an indispensable first stage when linking two administrative databases containing millions of establishment records?",
        "options": [
            {"option_id": "A", "text": "It groups records sharing high-confidence keys (e.g., district code or phonetic name soundex) to avoid comparing all $N_A \\times N_B$ pairs"},
            {"option_id": "B", "text": "It blocks unauthorized external users from downloading confidential tax records"},
            {"option_id": "C", "text": "It deletes all records with minor spelling typos"},
            {"option_id": "D", "text": "It enforces strict alphabetical ordering for printed books"}
        ],
        "correct_option": "A",
        "explanation": "Pairwise comparison of $10^6$ by $10^6$ records requires $10^{12}$ comparisons. Blocking reduces the candidate pair search space to computationally tractable subsets.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "12:15",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-ML-L2-03",
        "quiz_id": "QUIZ-ML-02",
        "lesson_id": "ml-lesson-2",
        "competency_id": "COMP-028",
        "question_text": "What makes the Jaro-Winkler string distance especially effective for entity matching of Indian establishment names?",
        "options": [
            {"option_id": "A", "text": "It emphasizes character transpositions and assigns higher similarity to matches sharing common leading prefixes"},
            {"option_id": "B", "text": "It translates regional languages into English automatically"},
            {"option_id": "C", "text": "It ignores all vowel differences entirely"},
            {"option_id": "D", "text": "It requires strings to have identical lengths"}
        ],
        "correct_option": "A",
        "explanation": "Jaro-Winkler gives higher ratings to strings that match from the beginning (prefix bonus $p$), which accurately captures typical transcription and truncation patterns.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "18:40",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-ML-L2-04",
        "quiz_id": "QUIZ-ML-02",
        "lesson_id": "ml-lesson-2",
        "competency_id": "COMP-028",
        "question_text": "In entity resolution, what is the purpose of the 1-to-1 matching constraint solved via bipartite graph matching (the Hungarian algorithm)?",
        "options": [
            {"option_id": "A", "text": "It prevents a single administrative tax ID from being incorrectly linked to multiple distinct survey enterprises"},
            {"option_id": "B", "text": "It ensures both databases have the exact same number of records"},
            {"option_id": "C", "text": "It forces every candidate link to be approved by a supervisor"},
            {"option_id": "D", "text": "It replaces missing values with zeroes"}
        ],
        "correct_option": "A",
        "explanation": "When resolving legally distinct business entities, enforcing 1-to-1 matching via max-weight bipartite matching avoids assigning one tax identity to multiple survey establishments.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "24:50",
        "difficulty": "HARD"
    },

    # =============================================================
    # MACHINE LEARNING LESSON 3: Tree Ensembles & Non-Response Prediction
    # =============================================================
    {
        "question_id": "Q-ML-L3-01",
        "quiz_id": "QUIZ-ML-03",
        "lesson_id": "ml-lesson-3",
        "competency_id": "COMP-028",
        "question_text": "How do Random Forests achieve variance reduction compared to individual decision trees?",
        "options": [
            {"option_id": "A", "text": "By averaging predictions across decorrelated trees grown on bootstrap samples and restricted to random feature subsets at each split"},
            {"option_id": "B", "text": "By pruning all leaf nodes with fewer than 100 observations"},
            {"option_id": "C", "text": "By converting all non-linear relationships into linear equations"},
            {"option_id": "D", "text": "By training only a single shallow tree with depth 1"}
        ],
        "correct_option": "A",
        "explanation": "Bagging (bootstrap aggregation) plus feature sub-sampling decorrelates the individual trees, substantially decreasing ensemble variance without increasing bias.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "05:30",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-ML-L3-02",
        "quiz_id": "QUIZ-ML-03",
        "lesson_id": "ml-lesson-3",
        "competency_id": "COMP-028",
        "question_text": "How do Gradient Boosting machines (e.g. XGBoost, LightGBM) differ fundamentally from Random Forests in their tree construction strategy?",
        "options": [
            {"option_id": "A", "text": "Trees are built sequentially, with each new tree trained to predict the negative gradient (pseudo-residuals) of the loss function"},
            {"option_id": "B", "text": "Trees are constructed independently in parallel without communication"},
            {"option_id": "C", "text": "Gradient boosting only works on continuous time series data"},
            {"option_id": "D", "text": "Gradient boosting does not use a loss function"}
        ],
        "correct_option": "A",
        "explanation": "Boosting fits trees sequentially to correct the residual errors of the current ensemble, iteratively driving down bias along the gradient of the objective function.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "12:20",
        "difficulty": "MEDIUM"
    },
    {
        "question_id": "Q-ML-L3-03",
        "quiz_id": "QUIZ-ML-03",
        "lesson_id": "ml-lesson-3",
        "competency_id": "COMP-028",
        "question_text": "How are predicted response propensities $\\hat{p}_i$ from an ensemble model used to adjust survey design weights $w_i$ for unit non-response?",
        "options": [
            {"option_id": "A", "text": "Non-response adjusted weight is calculated as $w_i^* = w_i / \\hat{p}_i$, giving higher weight to respondents resembling non-respondents"},
            {"option_id": "B", "text": "Weights are multiplied by $\\hat{p}_i$, shrinking weights of non-respondents to zero"},
            {"option_id": "C", "text": "Weights are replaced by $\\hat{p}_i$ directly"},
            {"option_id": "D", "text": "The weights are discarded and simple random sampling is assumed"}
        ],
        "correct_option": "A",
        "explanation": "Inverse propensity weighting multiplies design weights by $1 / \\hat{p}_i$. Respondents with lower estimated likelihood of responding represent themselves and similar non-respondents.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "18:40",
        "difficulty": "HARD"
    },
    {
        "question_id": "Q-ML-L3-04",
        "quiz_id": "QUIZ-ML-03",
        "lesson_id": "ml-lesson-3",
        "competency_id": "COMP-028",
        "question_text": "What makes SHAP (Shapley Additive exPlanations) values the preferred interpretability framework for official statistical prediction models?",
        "options": [
            {"option_id": "A", "text": "They satisfy game-theoretic axioms of efficiency, symmetry, and additivity, ensuring consistent local attribution for each predictor variable"},
            {"option_id": "B", "text": "They guarantee the model will achieve 100% test accuracy"},
            {"option_id": "C", "text": "They replace the tree ensemble with a single decision rule"},
            {"option_id": "D", "text": "They can only be calculated for linear regression"}
        ],
        "correct_option": "A",
        "explanation": "Shapley values allocate payout among cooperating players based on marginal contributions, providing legally defensible, additive feature attribution in public administration.",
        "chunk_id": "CHK-ML-001",
        "timestamp_label": "25:10",
        "difficulty": "HARD"
    }
]

