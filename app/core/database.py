from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./core.db"

db = create_engine(DATABASE_URL)
Base = declarative_base()

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

