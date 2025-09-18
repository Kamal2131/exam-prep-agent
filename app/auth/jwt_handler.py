from google.auth.transport import requests
from google.oauth2 import id_token
from datetime import datetime, timedelta
from jose import jwt
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

def verify_google_token(token: str):
    """Verify Google OAuth token and return user info"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID
        )
        return {
            "email": idinfo["email"],
            "name": idinfo["name"],
            "picture": idinfo.get("picture"),
            "google_id": idinfo["sub"]
        }
    except ValueError:
        return None

def create_access_token(user_data: dict):
    """Create JWT token for authenticated user"""
    to_encode = user_data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """Verify JWT token and return user data"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None