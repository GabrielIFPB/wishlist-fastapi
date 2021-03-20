
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from JWTtoken import verify_token, oauth2_scheme
from database import get_db


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return await verify_token(credentials_exception, token, db)
