from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List

class LoginRequest(BaseModel):
    email: str
    password: str

class DemoSwitchRequest(BaseModel):
    user_id: str

class UserProfile(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: str
    department: Optional[str] = None
    designation: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in_minutes: int
    user: UserProfile

class DemoAccountInfo(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: str
    department: Optional[str]
    designation: Optional[str]
    description: str
