from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.database import get_db_connection
from app.auth import (
    verify_password,
    create_access_token,
    get_current_user,
    DEMO_ACCOUNTS
)
from app.models.auth_schemas import (
    LoginRequest,
    DemoSwitchRequest,
    TokenResponse,
    UserProfile,
    DemoAccountInfo
)
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

DEMO_DESCRIPTIONS = {
    "admin-001": "System Administrator - Full oversight, course management, learner registry",
    "reviewer-001": "Supervisor / Reviewer - Evaluates practical evidence, approves competency promotions",
    "USR-001": "Learner: Aarav Sharma - Junior Statistical Officer preparing for Senior Field Supervisor (Gap: Sampling)",
    "USR-002": "Learner: Isha Verma - Data Processing Assistant preparing for Statistical Officer (Gap: SQL)",
    "USR-011": "Learner: Rohan Mehta - Field Investigator preparing for Junior Statistical Officer (Gap: Python)"
}

@router.get("/demo-accounts", response_model=List[DemoAccountInfo])
def list_demo_accounts():
    """Returns the 5 pre-configured demo personas with descriptions."""
    results = []
    for acc in DEMO_ACCOUNTS:
        results.append(DemoAccountInfo(
            user_id=acc["user_id"],
            email=acc["email"],
            full_name=acc["full_name"],
            role=acc["role"],
            department=acc.get("department"),
            designation=acc.get("designation"),
            description=DEMO_DESCRIPTIONS.get(acc["user_id"], "")
        ))
    return results

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """Authenticates a user by email and password, returning a JWT token."""
    con = get_db_connection()
    try:
        cursor = con.execute(
            "SELECT user_id, email, hashed_password, full_name, role, department, designation, is_active FROM app_users WHERE email = ?",
            (request.email.strip().lower(),)
        )
        user = cursor.fetchone()
        if not user or not verify_password(request.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated. Please contact an administrator."
            )
            
        profile = UserProfile(
            user_id=user["user_id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            department=user["department"],
            designation=user["designation"]
        )
        
        token = create_access_token({"sub": user["user_id"], "role": user["role"], "email": user["email"]})
        return TokenResponse(
            access_token=token,
            expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            user=profile
        )
    finally:
        con.close()

@router.post("/demo-switch", response_model=TokenResponse)
def demo_switch(request: DemoSwitchRequest):
    """
    Instant role/user switcher for demo and testing purposes.
    Allows seamless switching between Admin, Supervisor, and Learners.
    """
    con = get_db_connection()
    try:
        cursor = con.execute(
            "SELECT user_id, email, full_name, role, department, designation, is_active FROM app_users WHERE user_id = ?",
            (request.user_id.strip(),)
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Demo account '{request.user_id}' not found"
            )
            
        profile = UserProfile(
            user_id=user["user_id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            department=user["department"],
            designation=user["designation"]
        )
        
        token = create_access_token({"sub": user["user_id"], "role": user["role"], "email": user["email"]})
        return TokenResponse(
            access_token=token,
            expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            user=profile
        )
    finally:
        con.close()

@router.get("/me", response_model=UserProfile)
def get_current_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Returns the authenticated user's profile."""
    return UserProfile(
        user_id=current_user["user_id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user["role"],
        department=current_user.get("department"),
        designation=current_user.get("designation")
    )
