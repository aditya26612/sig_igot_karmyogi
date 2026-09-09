from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, get_db_connection, load_db
from app.auth import seed_demo_users
from app.services.transcript_service import seed_content_catalogue
from app.services.quiz_gen_service import seed_practice_data
from app.routers import (
    auth_router,
    learner_router,
    content_router,
    practice_router,
    assessment_router,
    reviewer_router,
    assistant_router,
    integration_router,
    admin_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize extension tables and seed demo accounts, content, & practice quizzes
    init_db()
    con = get_db_connection()
    try:
        seed_demo_users(con)
        seed_content_catalogue(con)
        seed_practice_data(con)
    finally:
        con.close()
    yield

app = FastAPI(
    title="SIH26101: AI-Enabled Competency & Learning Platform",
    description="Backend API supporting iGOT Karmayogi-inspired competency, learning, practice, and assessment pipelines for MoSPI.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"] if settings.ENVIRONMENT == "development" else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router.router)
app.include_router(learner_router.router)
app.include_router(content_router.router)
app.include_router(practice_router.router)
app.include_router(assessment_router.router)
app.include_router(reviewer_router.router)
app.include_router(assistant_router.router)
app.include_router(integration_router.router)
app.include_router(admin_router.router)

@app.get("/health", tags=["System"])
def health_check():
    """System health check and database status."""
    con = get_db_connection()
    try:
        D = load_db(con)
        user_count = len(D.get("users", []))
        comp_count = len(D.get("competencies", []))
        return {
            "status": "healthy",
            "service": "sih26101-competency-platform",
            "environment": settings.ENVIRONMENT,
            "database": {
                "connected": True,
                "users_loaded": user_count,
                "competencies_loaded": comp_count,
            },
            "provenance": "SYNTHETIC_OFFICIAL_OSS"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }
    finally:
        con.close()

@app.get("/", tags=["System"])
def root():
    return {
        "title": "SIH26101 AI-Enabled Competency & Learning Platform",
        "portal_theme": "iGOT Karmayogi (MoSPI Official Statistical System)",
        "docs_url": "/docs",
        "health_url": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
