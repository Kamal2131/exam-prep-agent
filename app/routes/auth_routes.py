from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.db import get_db
from app.models.user import User
from app.auth.jwt_handler import verify_google_token, create_access_token
from pydantic import BaseModel

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    token: str

@router.post("/auth/google")
async def google_auth(auth_request: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticate user with Google OAuth token"""
    
    # Verify Google token
    user_info = verify_google_token(auth_request.token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
    # Check if user exists
    user = db.query(User).filter(User.email == user_info["email"]).first()
    
    if not user:
        # Create new user
        user = User(
            email=user_info["email"],
            full_name=user_info["name"],
            google_id=user_info["google_id"],
            profile_picture=user_info.get("picture"),
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create JWT token
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "name": user.full_name
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.full_name,
            "picture": user.profile_picture,
            "is_premium": user.is_premium
        }
    }

@router.get("/auth/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current authenticated user"""
    from app.auth.jwt_handler import verify_token
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = auth_header.split(" ")[1]
    user_data = verify_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.full_name,
        "picture": user.profile_picture,
        "is_premium": user.is_premium,
        "created_at": user.created_at
    }