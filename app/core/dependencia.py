from app.core.database import db
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=db, autoflush=False, autocommit=False)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
