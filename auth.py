import hashlib
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
import os
from dotenv import load_dotenv

load_dotenv()

# Check passlib availability for password hashing
try:
    from passlib.context import CryptContext
    PASSLIB_AVAILABLE = True
except ImportError:
    PASSLIB_AVAILABLE = False
    print("Passlib not available - password hashing will use fallback")
    CryptContext = None

# Check jose availability for JWT
try:
    from jose import JWTError, jwt
    JOSE_AVAILABLE = True
except ImportError:
    JOSE_AVAILABLE = False
    print("Python-jose not available - JWT authentication disabled")
    JWTError = None
    jwt = None

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if PASSLIB_AVAILABLE:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
else:
    pwd_context = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    phone: str

class UserLogin(BaseModel):
    email: str
    password: str

def verify_password(plain_password, hashed_password):
    if not PASSLIB_AVAILABLE:
        # Fallback to simple hash comparison for development
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    if not PASSLIB_AVAILABLE:
        # Fallback to SHA256 for development
        return hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if not JOSE_AVAILABLE:
        raise HTTPException(status_code=500, detail="JWT authentication not available")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not JOSE_AVAILABLE:
        raise HTTPException(status_code=500, detail="JWT authentication not available")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# Legacy function for backward compatibility (if needed)
def verify_key(key: str) -> bool:
    # This can be removed once all endpoints use JWT
    return False
