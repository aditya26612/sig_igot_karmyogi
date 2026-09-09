import sqlite3
from typing import List, Dict, Any, Optional
from app.database import get_db_connection

SEED_PLAYLISTS = [
    {
        "playlist_id": "PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J",
        "title": "Survey Sampling Design & Estimation",
        "youtube_url": "https://youtube.com/playlist?list=PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J",
        "channel_name": "National Statistical Training Academy",
        "competency_id": "COMP-SAMPLING",
        "description": "Comprehensive grounding in probability sampling, stratification, cluster designs, frame auditing, and sampling weights for official surveys.",
        "category": "Survey Methodology",
        "total_lessons": 5
    },
    {
        "playlist_id": "PLLy_2iUCG87A2ywI6ZFJPmgq0nGwfBt15",
        "title": "SQL & Relational Databases for Statistical Data",
        "youtube_url": "https://youtube.com/playlist?list=PLLy_2iUCG87A2ywI6ZFJPmgq0nGwfBt15",
        "channel_name": "MoSPI Digital Training",
        "competency_id": "COMP-027",
        "description": "Relational data extraction, multi-table joins, aggregate queries, null handling, and deduplication for administrative statistical registers.",
        "category": "Data Processing & Engineering",
        "total_lessons": 4
    },
    {
        "playlist_id": "PLunlGNVWDAaY7AeDDzTeu4-DD3g7zmAXs",
        "title": "Python for Official Statistical Analysis",
        "youtube_url": "https://youtube.com/playlist?list=PLunlGNVWDAaY7AeDDzTeu4-DD3g7zmAXs",
        "channel_name": "Open Government Data Labs",
        "competency_id": "COMP-025",
        "description": "Automating statistical data workflows with Python, Pandas microdata cleaning, validation pipelines, and data export.",
        "category": "Data Science & Automation",
        "total_lessons": 4
    },
    {
        "playlist_id": "PLhQjrBD2T383Cqo5I1oRrbC1EKRAKGKUE",
        "title": "R Programming for Statistical Computing",
        "youtube_url": "https://youtube.com/playlist?list=PLhQjrBD2T383Cqo5I1oRrbC1EKRAKGKUE",
        "channel_name": "Statistical Computing Initiative",
        "competency_id": "COMP-026",
        "description": "Survey analysis in R, survey-weighted regressions, indicator computation, and reproducible statistical reporting.",
        "category": "Statistical Computing",
        "total_lessons": 3
    },
    {
        "playlist_id": "PLWPirh4EWFpENnR0p1JvhJkyTK1M0sOLR",
        "title": "Probability Theory & Applied Statistics",
        "youtube_url": "https://youtube.com/playlist?list=PLWPirh4EWFpENnR0p1JvhJkyTK1M0sOLR",
        "channel_name": "Academic Statistics Archive",
        "competency_id": "COMP-009",
        "description": "Foundations of statistical inference, probability distributions, variance estimation, and confidence intervals.",
        "category": "Statistical Theory",
        "total_lessons": 3
    },
    {
        "playlist_id": "PLOspHqNVtKADfxkuDuHduUkDExBpEt3DF",
        "title": "Data Quality, Auditing & Governance",
        "youtube_url": "https://youtube.com/playlist?list=PLOspHqNVtKADfxkuDuHduUkDExBpEt3DF",
        "channel_name": "Public Sector Data Quality",
        "competency_id": "COMP-018",
        "description": "Techniques for error screening, outlier detection, data integrity verification, and data confidentiality frameworks.",
        "category": "Data Governance",
        "total_lessons": 3
    },
    {
        "playlist_id": "PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH",
        "title": "Applied Machine Learning for Government Data",
        "youtube_url": "https://youtube.com/playlist?list=PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH",
        "channel_name": "AI for Public Sector",
        "competency_id": "COMP-028",
        "description": "Predictive modeling, classification techniques, and automated record linkage in large-scale administrative registers.",
        "category": "Advanced Analytics",
        "total_lessons": 3
    }
]

SEED_LESSONS = [
    # Sampling Lessons (PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J)
    {
        "lesson_id": "sampling-lesson-1",
        "playlist_id": "PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J",
        "sequence_no": 1,
        "title": "Lesson 1: Introduction to Probability Sampling & Frame Design",
        "youtube_video_id": "NzZXz3fJf6o",
        "youtube_url": "https://www.youtube.com/watch?v=NzZXz3fJf6o",
        "duration_minutes": 22,
        "competency_id": "COMP-SAMPLING",
        "has_transcript": 1
    },
    {
        "lesson_id": "sampling-lesson-2",
        "playlist_id": "PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J",
        "sequence_no": 2,
        "title": "Lesson 2: Simple Random Sampling & Systematic Sampling",
        "youtube_video_id": "SqG-b5E9vHs",
        "youtube_url": "https://www.youtube.com/watch?v=SqG-b5E9vHs",
        "duration_minutes": 26,
        "competency_id": "COMP-SAMPLING",
        "has_transcript": 1
    },
    {
        "lesson_id": "sampling-lesson-3",
        "playlist_id": "PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J",
        "sequence_no": 3,
        "title": "Lesson 3: Stratified Sampling & Proportional Allocation",
        "youtube_video_id": "lOh2x-UACaU",
        "youtube_url": "https://www.youtube.com/watch?v=lOh2x-UACaU",
        "duration_minutes": 32,
        "competency_id": "COMP-SAMPLING",
        "has_transcript": 1
    },
    {
        "lesson_id": "sampling-lesson-4",
        "playlist_id": "PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J",
        "sequence_no": 4,
        "title": "Lesson 4: Cluster Sampling & Multi-Stage Household Surveys",
        "youtube_video_id": "fZ3D6HQrWzs",
        "youtube_url": "https://www.youtube.com/watch?v=fZ3D6HQrWzs",
        "duration_minutes": 35,
        "competency_id": "COMP-SAMPLING",
        "has_transcript": 1
    },
    {
        "lesson_id": "sampling-lesson-5",
        "playlist_id": "PLShJJCRzJWxhz7SfG4hpaBD5bKOloWx9J",
        "sequence_no": 5,
        "title": "Lesson 5: Calculating & Applying Survey Design Weights",
        "youtube_video_id": "4xrYN2Ecmas",
        "youtube_url": "https://www.youtube.com/watch?v=4xrYN2Ecmas",
        "duration_minutes": 28,
        "competency_id": "COMP-SAMPLING",
        "has_transcript": 1
    },
    # SQL Lessons (PLLy_2iUCG87A2ywI6ZFJPmgq0nGwfBt15)
    {
        "lesson_id": "sql-lesson-1",
        "playlist_id": "PLLy_2iUCG87A2ywI6ZFJPmgq0nGwfBt15",
        "sequence_no": 1,
        "title": "Lesson 1: Multi-Table Relational Joins (INNER, LEFT, FULL)",
        "youtube_video_id": "shmMcZ2ZX0k",
        "youtube_url": "https://www.youtube.com/watch?v=shmMcZ2ZX0k",
        "duration_minutes": 25,
        "competency_id": "COMP-027",
        "has_transcript": 1
    },
    {
        "lesson_id": "sql-lesson-2",
        "playlist_id": "PLLy_2iUCG87A2ywI6ZFJPmgq0nGwfBt15",
        "sequence_no": 2,
        "title": "Lesson 2: Duplicate Detection & Data Reconciliation",
        "youtube_video_id": "AyeANYXcsK4",
        "youtube_url": "https://www.youtube.com/watch?v=AyeANYXcsK4",
        "duration_minutes": 30,
        "competency_id": "COMP-027",
        "has_transcript": 1
    },
    {
        "lesson_id": "sql-lesson-3",
        "playlist_id": "PLLy_2iUCG87A2ywI6ZFJPmgq0nGwfBt15",
        "sequence_no": 3,
        "title": "Lesson 3: Advanced Grouping & Window Functions for Aggregation",
        "youtube_video_id": "XrudT9s3_eY",
        "youtube_url": "https://www.youtube.com/watch?v=XrudT9s3_eY",
        "duration_minutes": 28,
        "competency_id": "COMP-027",
        "has_transcript": 1
    },
    {
        "lesson_id": "sql-lesson-4",
        "playlist_id": "PLLy_2iUCG87A2ywI6ZFJPmgq0nGwfBt15",
        "sequence_no": 4,
        "title": "Lesson 4: NULL Handling, COALESCE & Missing Data Logic in Registries",
        "youtube_video_id": "kK_Wqx3CEvU",
        "youtube_url": "https://www.youtube.com/watch?v=kK_Wqx3CEvU",
        "duration_minutes": 25,
        "competency_id": "COMP-027",
        "has_transcript": 1
    },
    # Python Lessons (PLunlGNVWDAaY7AeDDzTeu4-DD3g7zmAXs)
    {
        "lesson_id": "python-lesson-1",
        "playlist_id": "PLunlGNVWDAaY7AeDDzTeu4-DD3g7zmAXs",
        "sequence_no": 1,
        "title": "Lesson 1: Microdata Cleaning with Pandas & Outlier Screening",
        "youtube_video_id": "o7WkGYIPUM8",
        "youtube_url": "https://www.youtube.com/watch?v=o7WkGYIPUM8",
        "duration_minutes": 30,
        "competency_id": "COMP-025",
        "has_transcript": 1
    },
    {
        "lesson_id": "python-lesson-2",
        "playlist_id": "PLunlGNVWDAaY7AeDDzTeu4-DD3g7zmAXs",
        "sequence_no": 2,
        "title": "Lesson 2: Automated Survey Data Processing Pipelines",
        "youtube_video_id": "kWnHqLJAOj8",
        "youtube_url": "https://www.youtube.com/watch?v=kWnHqLJAOj8",
        "duration_minutes": 32,
        "competency_id": "COMP-025",
        "has_transcript": 1
    },
    {
        "lesson_id": "python-lesson-3",
        "playlist_id": "PLunlGNVWDAaY7AeDDzTeu4-DD3g7zmAXs",
        "sequence_no": 3,
        "title": "Lesson 3: Survey Microdata Weighting & Tabulation with Pandas",
        "youtube_video_id": "r-uOLxNrNk8",
        "youtube_url": "https://www.youtube.com/watch?v=r-uOLxNrNk8",
        "duration_minutes": 28,
        "competency_id": "COMP-025",
        "has_transcript": 1
    },
    {
        "lesson_id": "python-lesson-4",
        "playlist_id": "PLunlGNVWDAaY7AeDDzTeu4-DD3g7zmAXs",
        "sequence_no": 4,
        "title": "Lesson 4: Automated Data Quality Audits & Anomaly Verification",
        "youtube_video_id": "vmEHCJofslg",
        "youtube_url": "https://www.youtube.com/watch?v=vmEHCJofslg",
        "duration_minutes": 26,
        "competency_id": "COMP-025",
        "has_transcript": 1
    },
    # R Lessons (PLhQjrBD2T383Cqo5I1oRrbC1EKRAKGKUE)
    {
        "lesson_id": "r-lesson-1",
        "playlist_id": "PLhQjrBD2T383Cqo5I1oRrbC1EKRAKGKUE",
        "sequence_no": 1,
        "title": "Lesson 1: R Fundamentals for Official Statistical Computing",
        "youtube_video_id": "kmJlnUfMd7I",
        "youtube_url": "https://www.youtube.com/watch?v=kmJlnUfMd7I",
        "duration_minutes": 28,
        "competency_id": "COMP-026",
        "has_transcript": 1
    },
    {
        "lesson_id": "r-lesson-2",
        "playlist_id": "PLhQjrBD2T383Cqo5I1oRrbC1EKRAKGKUE",
        "sequence_no": 2,
        "title": "Lesson 2: Complex Survey Analysis with the survey Package",
        "youtube_video_id": "fDRa82lxzaU",
        "youtube_url": "https://www.youtube.com/watch?v=fDRa82lxzaU",
        "duration_minutes": 30,
        "competency_id": "COMP-026",
        "has_transcript": 1
    },
    {
        "lesson_id": "r-lesson-3",
        "playlist_id": "PLhQjrBD2T383Cqo5I1oRrbC1EKRAKGKUE",
        "sequence_no": 3,
        "title": "Lesson 3: Variance Estimation & Inequality Indicators in R",
        "youtube_video_id": "BvKETZ6kr9Q",
        "youtube_url": "https://www.youtube.com/watch?v=BvKETZ6kr9Q",
        "duration_minutes": 27,
        "competency_id": "COMP-026",
        "has_transcript": 1
    },
    # Probability Lessons (PLWPirh4EWFpENnR0p1JvhJkyTK1M0sOLR)
    {
        "lesson_id": "prob-lesson-1",
        "playlist_id": "PLWPirh4EWFpENnR0p1JvhJkyTK1M0sOLR",
        "sequence_no": 1,
        "title": "Lesson 1: Probability Distributions & Variance Estimation",
        "youtube_video_id": "Uv96qQ3uC6Y",
        "youtube_url": "https://www.youtube.com/watch?v=Uv96qQ3uC6Y",
        "duration_minutes": 35,
        "competency_id": "COMP-009",
        "has_transcript": 1
    },
    {
        "lesson_id": "prob-lesson-2",
        "playlist_id": "PLWPirh4EWFpENnR0p1JvhJkyTK1M0sOLR",
        "sequence_no": 2,
        "title": "Lesson 2: Central Limit Theorem & Finite Population Correction",
        "youtube_video_id": "YAlJCEDH2uY",
        "youtube_url": "https://www.youtube.com/watch?v=YAlJCEDH2uY",
        "duration_minutes": 32,
        "competency_id": "COMP-009",
        "has_transcript": 1
    },
    {
        "lesson_id": "prob-lesson-3",
        "playlist_id": "PLWPirh4EWFpENnR0p1JvhJkyTK1M0sOLR",
        "sequence_no": 3,
        "title": "Lesson 3: Confidence Intervals & Hypothesis Testing in Surveys",
        "youtube_video_id": "tFWsuO9fQdI",
        "youtube_url": "https://www.youtube.com/watch?v=tFWsuO9fQdI",
        "duration_minutes": 30,
        "competency_id": "COMP-009",
        "has_transcript": 1
    },
    # Data Quality (PLOspHqNVtKADfxkuDuHduUkDExBpEt3DF)
    {
        "lesson_id": "quality-lesson-1",
        "playlist_id": "PLOspHqNVtKADfxkuDuHduUkDExBpEt3DF",
        "sequence_no": 1,
        "title": "Lesson 1: Data Auditing, Outlier Detection & Error Screening",
        "youtube_video_id": "mUw27wG7uFA",
        "youtube_url": "https://www.youtube.com/watch?v=mUw27wG7uFA",
        "duration_minutes": 27,
        "competency_id": "COMP-018",
        "has_transcript": 1
    },
    {
        "lesson_id": "quality-lesson-2",
        "playlist_id": "PLOspHqNVtKADfxkuDuHduUkDExBpEt3DF",
        "sequence_no": 2,
        "title": "Lesson 2: Imputation Methods & Hot-Deck vs Cold-Deck Protocols",
        "youtube_video_id": "iO6k0hJ7q_o",
        "youtube_url": "https://www.youtube.com/watch?v=iO6k0hJ7q_o",
        "duration_minutes": 29,
        "competency_id": "COMP-018",
        "has_transcript": 1
    },
    {
        "lesson_id": "quality-lesson-3",
        "playlist_id": "PLOspHqNVtKADfxkuDuHduUkDExBpEt3DF",
        "sequence_no": 3,
        "title": "Lesson 3: Statistical Disclosure Control & Microdata Anonymization",
        "youtube_video_id": "7Uv43s6A9uA",
        "youtube_url": "https://www.youtube.com/watch?v=7Uv43s6A9uA",
        "duration_minutes": 28,
        "competency_id": "COMP-018",
        "has_transcript": 1
    },
    # Machine Learning (PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH)
    {
        "lesson_id": "ml-lesson-1",
        "playlist_id": "PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH",
        "sequence_no": 1,
        "title": "Lesson 1: Supervised Learning & Classifier Evaluation",
        "youtube_video_id": "ZftI2fEz0Fw",
        "youtube_url": "https://www.youtube.com/watch?v=ZftI2fEz0Fw",
        "duration_minutes": 33,
        "competency_id": "COMP-028",
        "has_transcript": 1
    },
    {
        "lesson_id": "ml-lesson-2",
        "playlist_id": "PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH",
        "sequence_no": 2,
        "title": "Lesson 2: Record Linkage & Entity Resolution Across Registers",
        "youtube_video_id": "Gv9_4yMHFhI",
        "youtube_url": "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
        "duration_minutes": 31,
        "competency_id": "COMP-028",
        "has_transcript": 1
    },
    {
        "lesson_id": "ml-lesson-3",
        "playlist_id": "PLKnIA16_Rmvbr7zKYQuBfsVkjoLcJgxHH",
        "sequence_no": 3,
        "title": "Lesson 3: Tree Ensembles & Non-Response Prediction Models",
        "youtube_video_id": "O2L2Uv9pdDA",
        "youtube_url": "https://www.youtube.com/watch?v=O2L2Uv9pdDA",
        "duration_minutes": 30,
        "competency_id": "COMP-028",
        "has_transcript": 1
    }
]

# Exact transcript chunks matching assessment/blueprint.json
SEED_TRANSCRIPT_CHUNKS = [
    {
        "chunk_id": "CHK-DEMO-001",
        "lesson_id": "sampling-lesson-3",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "topic": "Stratified sampling",
        "start_seconds": 135,
        "end_seconds": 380,
        "timestamp_label": "02:15",
        "text_content": "Stratified sampling is a probability sampling method where the population is divided into non-overlapping homogeneous subgroups called strata. Samples are drawn independently from each stratum. In proportional allocation, the sample size in each stratum is directly proportional to the population size of that stratum. For example, if a population has strata of 800 and 400 units and total sample size is 120, stratum 1 receives 80 units (120 * 800 / 1200) and stratum 2 receives 40 units (120 * 400 / 1200).",
        "summary": "Definition of stratified sampling and calculation of proportional allocation across strata."
    },
    {
        "chunk_id": "CHK-DEMO-002",
        "lesson_id": "sampling-lesson-3",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "topic": "Stratified sampling",
        "start_seconds": 465,
        "end_seconds": 690,
        "timestamp_label": "07:45",
        "text_content": "The primary statistical advantage of stratified random sampling over simple random sampling is the reduction of sampling variance. By creating strata that are internally homogeneous, variance between strata is eliminated from the overall sampling error. This provides higher precision with smaller sample sizes, especially when stratifying by variables strongly correlated with survey study variables, such as urban/rural sector or land-holding size.",
        "summary": "Variance reduction advantages and precision gains of stratification over simple random sampling."
    },
    {
        "chunk_id": "CHK-DEMO-003",
        "lesson_id": "sampling-lesson-5",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "topic": "Sampling weights",
        "start_seconds": 800,
        "end_seconds": 1050,
        "timestamp_label": "13:20",
        "text_content": "Sampling weights are design weights representing the inverse of the selection probability for each sampling unit. When an unequal probability design is used, such as oversampling rare subpopulations or specific enterprise strata, unweighted estimation leads to biased population statistics. Multiplying each sample observation by its design weight ensures unbiased estimation of population totals, means, and ratios.",
        "summary": "Mathematical definition and rationale for sampling weights as inverse inclusion probabilities."
    },
    {
        "chunk_id": "CHK-DEMO-004",
        "lesson_id": "sampling-lesson-1",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "topic": "Frames and coverage",
        "start_seconds": 1150,
        "end_seconds": 1410,
        "timestamp_label": "19:10",
        "text_content": "A sampling frame is the operational list of all eligible sampling units from which a sample is selected. Frame errors include undercoverage, where valid population units are omitted, and duplication, where units appear multiple times. In survey field audits, verifying the completeness of the village or block boundary listing is the first defense against frame undercoverage error.",
        "summary": "Sampling frame concepts, frame coverage errors, duplication, and field verification procedures."
    },
    {
        "chunk_id": "CHK-DEMO-005",
        "lesson_id": "sampling-lesson-4",
        "course_id": "CRS-101",
        "competency_id": "COMP-SAMPLING",
        "topic": "Strata and clusters",
        "start_seconds": 1535,
        "end_seconds": 1820,
        "timestamp_label": "25:35",
        "text_content": "It is crucial to distinguish between stratification and cluster sampling. In stratified sampling, the population is divided into groups and units are sampled from every stratum. In cluster sampling, the population is divided into clusters (such as villages or census enumeration blocks) and only a sample of clusters is chosen, with all or subsampled units surveyed within selected clusters. Strata should be homogeneous internally, whereas clusters should ideally be as heterogeneous internally as the entire population.",
        "summary": "Key structural differences between stratified sampling and cluster sampling."
    },
    # SQL Chunk
    {
        "chunk_id": "CHK-SQL-001",
        "lesson_id": "sql-lesson-1",
        "course_id": "CRS-102",
        "competency_id": "COMP-027",
        "topic": "Relational joins",
        "start_seconds": 120,
        "end_seconds": 450,
        "timestamp_label": "02:00",
        "text_content": "In relational SQL querying for statistical data, INNER JOIN returns only records where matching keys exist in both tables. LEFT OUTER JOIN retains all records from the primary survey table even when matching records are absent in the secondary register. When reconciling survey microdata against administrative tax registers, LEFT JOIN allows identification of non-matching records which indicate coverage or reporting discrepancies.",
        "summary": "INNER JOIN vs LEFT JOIN in statistical data reconciliation and discrepancy detection."
    },
    # Python Chunk
    {
        "chunk_id": "CHK-PY-001",
        "lesson_id": "python-lesson-1",
        "course_id": "CRS-103",
        "competency_id": "COMP-025",
        "topic": "Data cleaning with Pandas",
        "start_seconds": 150,
        "end_seconds": 480,
        "timestamp_label": "02:30",
        "text_content": "When cleaning statistical microdata using Pandas, handling missing values is the first essential step. Distinguishing between genuine missing values (NaN) and valid zero values is critical to avoid biased calculations of means and standard errors. Outlier screening using interquartile range (IQR) boundaries helps flag data entry anomalies without discarding valid extreme socioeconomic values.",
        "summary": "Missing value handling and IQR-based anomaly detection in survey microdata using Pandas."
    },
    {
        "chunk_id": "CHK-SQL-002",
        "lesson_id": "sql-lesson-4",
        "course_id": "CRS-102",
        "competency_id": "COMP-027",
        "topic": "NULL Handling and Three-Valued Logic",
        "start_seconds": 180,
        "end_seconds": 420,
        "timestamp_label": "03:00",
        "text_content": "In relational statistical registries, SQL NULL signifies absent or unknown measurement rather than numeric zero. Aggregate functions such as SUM, AVG, and STDDEV automatically exclude NULL values, which changes the effective sample size denominator if not explicitly managed. COALESCE allows replacing NULL with justifiable imputation values or zero when justified by administrative metadata.",
        "summary": "Three-valued logic, NULL aggregation rules, and COALESCE in official registers."
    },
    {
        "chunk_id": "CHK-R-001",
        "lesson_id": "r-lesson-2",
        "course_id": "CRS-104",
        "competency_id": "COMP-026",
        "topic": "Complex Survey Designs in R",
        "start_seconds": 120,
        "end_seconds": 360,
        "timestamp_label": "02:00",
        "text_content": "The R survey package by Thomas Lumley provides svydesign() to encapsulate complex sampling elements: strata, clusters (PSUs), finite population corrections (FPC), and design weights. Functions like svymean(), svytotal(), and svyby() then calculate design-consistent point estimates with proper Taylor series linearization standard errors.",
        "summary": "Using svydesign() and svymean() for design-based survey inference in R."
    },
    {
        "chunk_id": "CHK-PROB-001",
        "lesson_id": "prob-lesson-2",
        "course_id": "CRS-105",
        "competency_id": "COMP-009",
        "topic": "Central Limit Theorem and FPC",
        "start_seconds": 140,
        "end_seconds": 400,
        "timestamp_label": "02:20",
        "text_content": "The Central Limit Theorem demonstrates that as sample size n grows large, the distribution of the sample mean approaches normality regardless of underlying population skewness. When sampling from finite populations without replacement, the Finite Population Correction (FPC) factor sqrt((N - n) / (N - 1)) reduces standard error when the sampling fraction n/N exceeds 5 percent.",
        "summary": "Central Limit Theorem foundations and Finite Population Correction adjustment."
    },
    {
        "chunk_id": "CHK-QUAL-001",
        "lesson_id": "quality-lesson-2",
        "course_id": "CRS-106",
        "competency_id": "COMP-018",
        "topic": "Imputation Protocols",
        "start_seconds": 200,
        "end_seconds": 450,
        "timestamp_label": "03:20",
        "text_content": "When dealing with item non-response in official household surveys, deterministic mean imputation distorts variance and attenuates covariance between variables. In contrast, donor hot-deck imputation preserves empirical distributions by substituting values from an observed respondent in the same demographic imputation cell.",
        "summary": "Hot-deck vs cold-deck imputation and variance preservation in survey data."
    },
    {
        "chunk_id": "CHK-ML-001",
        "lesson_id": "ml-lesson-2",
        "course_id": "CRS-107",
        "competency_id": "COMP-028",
        "topic": "Record Linkage and Entity Resolution",
        "start_seconds": 160,
        "end_seconds": 410,
        "timestamp_label": "02:40",
        "text_content": "Probabilistic record linkage uses Fellegi-Sunter methodology to compute agreement and disagreement weights across partially matching identifiers like phonetic name codes and addresses. This enables linking survey respondents to administrative tax registers without relying on single flawless identity keys.",
        "summary": "Fellegi-Sunter record linkage and probabilistic matching for administrative data."
    }
]

def seed_content_catalogue(con: sqlite3.Connection):
    """Populates playlists, lessons, and transcript chunks if not already present."""
    with con:
        # Seed Playlists
        for p in SEED_PLAYLISTS:
            cur = con.execute("SELECT playlist_id FROM curated_playlists WHERE playlist_id = ?", (p["playlist_id"],))
            if not cur.fetchone():
                con.execute("""
                INSERT INTO curated_playlists (playlist_id, title, youtube_url, channel_name, competency_id, description, category, total_lessons, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE')
                """, (p["playlist_id"], p["title"], p["youtube_url"], p["channel_name"], p["competency_id"], p["description"], p["category"], p["total_lessons"]))
                
        # Seed Lessons
        for l in SEED_LESSONS:
            cur = con.execute("SELECT lesson_id FROM curated_lessons WHERE lesson_id = ?", (l["lesson_id"],))
            if not cur.fetchone():
                con.execute("""
                INSERT INTO curated_lessons (lesson_id, playlist_id, sequence_no, title, youtube_video_id, youtube_url, duration_minutes, competency_id, has_transcript)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (l["lesson_id"], l["playlist_id"], l["sequence_no"], l["title"], l["youtube_video_id"], l["youtube_url"], l["duration_minutes"], l["competency_id"], l["has_transcript"]))
            else:
                con.execute("""
                UPDATE curated_lessons 
                SET youtube_video_id = ?, youtube_url = ?, title = ?, duration_minutes = ?
                WHERE lesson_id = ?
                """, (l["youtube_video_id"], l["youtube_url"], l["title"], l["duration_minutes"], l["lesson_id"]))
                
        # Seed Transcript Chunks
        for c in SEED_TRANSCRIPT_CHUNKS:
            cur = con.execute("SELECT chunk_id FROM transcript_chunks WHERE chunk_id = ?", (c["chunk_id"],))
            if not cur.fetchone():
                con.execute("""
                INSERT INTO transcript_chunks (chunk_id, lesson_id, course_id, competency_id, topic, start_seconds, end_seconds, timestamp_label, text_content, summary, provenance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'DERIVED')
                """, (c["chunk_id"], c["lesson_id"], c["course_id"], c["competency_id"], c["topic"], c["start_seconds"], c["end_seconds"], c["timestamp_label"], c["text_content"], c["summary"]))

def search_transcripts(con: sqlite3.Connection, query: str) -> List[Dict[str, Any]]:
    """Performs search across all transcript chunks and returns matches with lesson context."""
    search_term = f"%{query.strip().lower()}%"
    cursor = con.execute("""
    SELECT 
        c.chunk_id,
        c.lesson_id,
        l.title as lesson_title,
        p.title as playlist_title,
        c.competency_id,
        c.topic,
        c.timestamp_label,
        c.start_seconds,
        c.text_content
    FROM transcript_chunks c
    LEFT JOIN curated_lessons l ON c.lesson_id = l.lesson_id
    LEFT JOIN curated_playlists p ON l.playlist_id = p.playlist_id
    WHERE LOWER(c.text_content) LIKE ? OR LOWER(c.topic) LIKE ?
    ORDER BY c.start_seconds ASC
    """, (search_term, search_term))
    
    rows = cursor.fetchall()
    results = []
    for r in rows:
        text = r["text_content"]
        # Find index of query in text for snippet highlighting
        q_pos = text.lower().find(query.strip().lower())
        if q_pos != -1:
            start = max(0, q_pos - 40)
            end = min(len(text), q_pos + len(query) + 60)
            snippet = ("..." if start > 0 else "") + text[start:end] + ("..." if end < len(text) else "")
        else:
            snippet = text[:100] + "..."
            
        results.append({
            "chunk_id": r["chunk_id"],
            "lesson_id": r["lesson_id"],
            "lesson_title": r["lesson_title"] or "Curated Lesson",
            "playlist_title": r["playlist_title"] or "Curated Playlist",
            "competency_id": r["competency_id"],
            "topic": r["topic"],
            "timestamp_label": r["timestamp_label"],
            "start_seconds": r["start_seconds"],
            "matching_snippet": snippet
        })
    return results
