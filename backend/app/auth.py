import hashlib
import hmac
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.database import get_db_connection

security_bearer = HTTPBearer(auto_error=False)

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Hashes a password using SHA-256 with a unique salt."""
    if not salt:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verifies a plain password against the stored salt:hash format."""
    try:
        salt, expected_hash = stored_hash.split(":")
        actual_hash = hashlib.sha256((salt + plain_password).encode('utf-8')).hexdigest()
        return hmac.compare_digest(actual_hash, expected_hash)
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

DEMO_ACCOUNTS = [
    {
        "user_id": "admin-001",
        "email": "admin@mospi.gov.in",
        "password": "AdminPassword123!",
        "full_name": "Dr. Rajesh Kumar (Admin)",
        "role": "ADMIN",
        "department": "Training & Competency Management",
        "designation": "Director of Training"
    },
    {
        "user_id": "reviewer-001",
        "email": "reviewer@mospi.gov.in",
        "password": "ReviewerPassword123!",
        "full_name": "Sunita Rao (Lead Assessor)",
        "role": "REVIEWER",
        "department": "National Sample Survey Office (NSSO)",
        "designation": "Superintending Officer & Assessor"
    },
    {
        "user_id": "USR-001",
        "email": "aarav.sharma@mospi.gov.in",
        "password": "LearnerPassword123!",
        "full_name": "Aarav Sharma",
        "role": "LEARNER",
        "department": "Field Operations Division",
        "designation": "Junior Statistical Officer"
    },
    {
        "user_id": "USR-002",
        "email": "isha.verma@mospi.gov.in",
        "password": "LearnerPassword123!",
        "full_name": "Isha Verma",
        "role": "LEARNER",
        "department": "Data Processing Division",
        "designation": "Data Processing Assistant"
    },
    {
        "user_id": "USR-011",
        "email": "rohan.mehta@mospi.gov.in",
        "password": "LearnerPassword123!",
        "full_name": "Rohan Mehta",
        "role": "LEARNER",
        "department": "National Accounts Division",
        "designation": "Field Investigator"
    }
]

def seed_demo_users(con: sqlite3.Connection):
    """Seeds the 5 demo accounts into the app_users table if not already present."""
    now = datetime.now(timezone.utc).isoformat()
    with con:
        for acc in DEMO_ACCOUNTS:
            cursor = con.execute("SELECT user_id FROM app_users WHERE user_id = ?", (acc['user_id'],))
            if not cursor.fetchone():
                hashed = hash_password(acc['password'])
                con.execute("""
                INSERT INTO app_users (user_id, email, hashed_password, full_name, role, department, designation, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)
                """, (acc['user_id'], acc['email'], hashed, acc['full_name'], acc['role'], acc['department'], acc['designation'], now))

def get_current_user(auth: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)) -> Dict[str, Any]:
    """Dependency to retrieve the authenticated user from JWT token."""
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(auth.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    con = get_db_connection()
    try:
        cursor = con.execute("SELECT user_id, email, full_name, role, department, designation, is_active FROM app_users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if not row or not row["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found or deactivated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return dict(row)
    finally:
        con.close()

def require_role(allowed_roles: List[str]):
    """Role-based access guard dependency."""
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Required role {allowed_roles}, your role is {current_user['role']}"
            )
        return current_user
    return role_checker
