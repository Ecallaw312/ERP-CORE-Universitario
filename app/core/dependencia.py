from app.core.database import db
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from fastapi import Depends, HTTPException
from app.models.user import User

SessionLocal = sessionmaker(bind=db, autoflush=False, autocommit=False)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        iduser = int(payload.get("sub"))
        if iduser is None:
            raise JWTError()
        
    except JWTError:    
        raise HTTPException(status_code=401, detail="Token inválido")
    
    usuario = session.query(User).filter(User.id == iduser).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido") 
    return usuario      