
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database import metadata, database
import sqlalchemy
import models
import schemas
from hashing import Hash


users = sqlalchemy.Table(
	"user",
	metadata,
	sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
	sqlalchemy.Column("name", sqlalchemy.String),
	sqlalchemy.Column("email", sqlalchemy.String, unique=True),
	sqlalchemy.Column("password", sqlalchemy.String),
	# sqlalchemy.orm.relationship()
)


class User:
	
	@staticmethod
	def get_all(db: Session) -> List[schemas.ShowUser]:
		return db.query(models.User).all()
	
	@staticmethod
	async def get_all_async() -> List[schemas.ShowUser]:
		query = users.select().with_only_columns([users.c.name, users.c.email])
		return await database.fetch_all(query)
	
	@staticmethod
	def create(user: schemas.User, db: Session) -> schemas.User:
		novo_user = models.User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
		db.add(novo_user)
		db.commit()
		db.refresh(novo_user)
		return novo_user
	
	@staticmethod
	async def create_async(user: schemas.User):
		query = users.insert().values(
			name=user.name,
			email=user.email,
			password=Hash.bcrypt(user.password)
		)
		return await database.execute(query)
	
	@staticmethod
	def show(user_id, db: Session) -> schemas.ShowUser:
		user = db.query(models.User) \
			.filter(models.User.id == user_id).first()
		
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"User with the id {user_id} is not found."
			)
		return user
	
	@staticmethod
	async def show_async(user_id: int) -> schemas.ShowUser:
		query = users.select().with_only_columns([users.c.name, users.c.email]) \
			.where(users.c.id == user_id)
		user = await database.fetch_one(query)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"User with the id {user_id} is not found."
			)
		return schemas.ShowUser(**user)
	
	@staticmethod
	def get_user_email(email: str, db: Session) -> schemas.LoginUser:
		user = db.query(models.User).with_entities("id", "name", "email") \
			.filter(models.User.email == email).first()
		
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"User with the email {email} is not found."
			)
		return user
	
	@staticmethod
	async def get_user_email_async(email: str) -> schemas.LoginUser:
		query = users.select().with_only_columns([users.c.id, users.c.name, users.c.email]) \
			.where(users.c.email == email)
		user = await database.fetch_one(query)
		
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"User with the email {email} is not found."
			)
		return schemas.LoginUser(**user)
