from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Check Redis availability
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("Redis not available - caching will be disabled")
    redis = None

# PostgreSQL Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/healthcare_voice_ai")

# Check PostgreSQL driver availability
try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("PostgreSQL driver (psycopg2) not available - using SQLite fallback")
    # Fallback to SQLite for development
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./healthcare_voice_ai.db")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    DATABASE_AVAILABLE = True
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Database functionality will be limited")
    DATABASE_AVAILABLE = False
    engine = None
    SessionLocal = None

# Redis for caching and sessions
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
if REDIS_AVAILABLE:
    redis_client = redis.from_url(REDIS_URL)
else:
    redis_client = None

def get_db():
    if not DATABASE_AVAILABLE or SessionLocal is None:
        raise RuntimeError("Database not available. Please check your database configuration.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    return redis_client
