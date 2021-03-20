
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
	__tablename__ = "user"
	
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String)
	email = Column(String, unique=True)
	password = Column(String)
	
	product = relationship("Product", back_populates="user")


class Product(Base):
	__tablename__ = "product"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String)
	description = Column(String)
	link = Column(String)
	image = Column(String)
	buy = Column(Boolean)
	user_id = Column(Integer, ForeignKey("user.id"))
	
	user = relationship("User", back_populates="product")
