from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database file (will be created automatically)
DATABASE_URL = "sqlite:///./messages.db"

# Create engine (connects to database)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session = allows us to talk to DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base = used to create tables
Base = declarative_base()

