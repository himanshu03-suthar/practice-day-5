import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv(".env.local")

# Get DATABASE_URL from environment variable, fallback to sqlite for safety if missing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./salon.db")

# If using PostgreSQL, we might need to adjust the URL if it starts with 'postgres://' to 'postgresql://' (SQLAlchemy requirement)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# connect_args is only needed for sqlite
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()