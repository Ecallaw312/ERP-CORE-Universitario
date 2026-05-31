import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
 
DATABASE_URL = os.getenv("DATABASE_URL")
 
db = create_engine(DATABASE_URL, echo=True, future=True)
Base = declarative_base()
