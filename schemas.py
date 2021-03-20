
from fastapi import Form, UploadFile, File
from typing import Optional, List
from pydantic import BaseModel


class Product(BaseModel):
	title: str
	description: Optional[str] = None
	link: Optional[str] = None
	image: Optional[str] = None
	buy: Optional[bool] = False
	
	# class Config:
	# 	orm_mode = True


class User(BaseModel):
	name: str
	email: str
	password: str


class ShowUser(BaseModel):
	name: str
	email: str
	
	# class Config:
	# 	orm_mode = True


class ShowProduct(BaseModel):
	title: str
	description: Optional[str] = None
	link: Optional[str] = None
	image: Optional[str] = None
	buy: Optional[bool] = None
	
	# class Config:
	# 	orm_mode = True
	
	def __init__(
			self, title: str = Form(...),
			description: str = Form(None),
			link: str = Form(None),
			photo: UploadFile = File(None),
			**kwargs
	):
		super().__init__(**kwargs)
		self.title = title
		self.description = description
		self.link = link
		self.photo = photo.filename


class ShowUserProduct(BaseModel):
	name: str
	email: str
	product: List[Product]
	
	class Config:
		orm_mode = True


class Login(BaseModel):
	email: str
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str


class TokenData(BaseModel):
	email: Optional[str] = None


class LoginUser(ShowUser):
	id: int
