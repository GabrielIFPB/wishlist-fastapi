
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import schemas
from JWTtoken import create_access_token
from database import get_db, database
import models
# import database
from repository.user import users
from hashing import Hash

router = APIRouter(
	tags=["Authentication"]
)


@router.post('/login', response_model=schemas.Token)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	"""
	informe o email e senha para se autenticar, assim poderá usar os recursos da lista de desejos.
	"""
	# user = db.query(models.User).filter(models.User.email == request.username).first()
	query = users.select().where(users.c.email == request.username)
	user = await database.fetch_one(query)

	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=f"Invalid email or password."
		)

	user = schemas.Login(**user)
	password = f"{request.password}"
	if not Hash.verify(user.password, password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail=f"Invalid email or password."
		)

	access_token = create_access_token(
		data={"sub": user.email}
	)
	return {"access_token": access_token, "token_type": "bearer"}
