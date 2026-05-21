from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column( "id", Integer, primary_key=True, autoincrement=True)
    user_id = Column( "user_id", Integer, ForeignKey("users.id"), nullable=False)
    refresh_token = Column( "refresh_token", String)
    expira_em = Column( "expira_em", DateTime)
    criado_em = Column( "criado_em", DateTime, default=datetime.utcnow)