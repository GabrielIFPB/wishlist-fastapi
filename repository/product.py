
from typing import List

import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy import and_, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import models
import schemas
from database import metadata, database


products = sqlalchemy.Table(
	"product",
	metadata,
	sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
	sqlalchemy.Column("title", sqlalchemy.String),
	sqlalchemy.Column("description", sqlalchemy.String),
	sqlalchemy.Column("link", sqlalchemy.String),
	sqlalchemy.Column("image", sqlalchemy.String),
	sqlalchemy.Column("buy", sqlalchemy.Boolean),
	sqlalchemy.Column("user_id", sqlalchemy.Integer, ForeignKey("user.id")),
	# sqlalchemy.orm.relationship()
)

columns = [products.c.title, products.c.description, products.c.link, products.c.image, products.c.buy]


class Product:
	
	@staticmethod
	def get_all(db: Session, user: schemas.LoginUser) -> List[schemas.ShowProduct]:
		return db.query(models.Product).filter(models.Product.user_id == user.id).all()
	
	@staticmethod
	def create(product: schemas.Product, db: Session, user: schemas.LoginUser) -> schemas.Product:
		novo_product = models.Product(
			title=product.title,
			description=product.description,
			link=product.link,
			image=product.image,
			user_id=user.id, buy=False
		)
		db.add(novo_product)
		db.commit()
		db.refresh(novo_product)
		return novo_product
	
	@staticmethod
	def show(product_id: int, db: Session, user: schemas.LoginUser) -> schemas.ShowProduct:
		product = db.query(models.Product) \
			.filter(and_(models.Product.id == product_id, models.Product.user_id == user.id)).first()
		
		if not product:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Items with the id {product_id} is not found."
			)
		return product
	
	@staticmethod
	def update(product_id: int, product: schemas.Product, db: Session, user: schemas.LoginUser) -> str:
		new_product = db.query(models.Product) \
			.filter(and_(models.Product.id == product_id, models.Product.user_id == user.id))
		
		if not new_product.first():
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Items with the id {product_id} is not found."
			)
		
		new_product.update(product)
		db.commit()
		return "updated"
	
	@staticmethod
	def delete(product_id: int, db: Session, user: schemas.LoginUser):
		product = db.query(models.Product) \
			.filter(and_(models.Product.id == product_id, models.Product.user_id == user.id))
		
		if not product.first():
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Items with the id {product_id} is not found."
			)
		
		product.delete(synchronize_session=False)
		db.commit()
	
	@staticmethod
	def show_random(db: Session, user: schemas.LoginUser) -> schemas.ShowProduct:
		item = db.query(models.Product).filter(models.Product.user_id == user.id).offset(
			func.floor(
				func.random() *
				db.query(func.count(models.Product.user_id)).filter(models.Product.user_id == user.id)
			)
		).limit(1).first()
		
		if not item:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"has no items."
			)
		return item
	
	@staticmethod
	def buy(wish_id, win: bool, db: Session, user: schemas.LoginUser):
		product = db.query(models.Product) \
			.filter(and_(models.Product.id == wish_id, models.Product.user_id == user.id))
		
		if not product.first():
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Items with the id {wish_id} is not found."
			)
		
		product.update({"buy": win})
		db.commit()
		return "buy"

	""" usando async """
	
	@staticmethod
	async def get_all_async(user_id: int) -> List[schemas.Product]:
		
		query = products.select().with_only_columns(columns) \
			.where(products.c.user_id == user_id)
		return await database.fetch_all(query)
	
	@staticmethod
	async def create_async(product: schemas.Product, user_id: int) -> schemas.Product:
		query = products.insert().values(
			title=product.title,
			description=product.description,
			link=product.link,
			image=product.image,
			user_id=user_id,
			buy=False
		)
		await database.execute(query)
		return product
	
	@staticmethod
	async def show_async(product_id: int, user_id: int) -> schemas.Product:
		query = products.select().with_only_columns(columns) \
			.where(and_(products.c.id == product_id, products.c.user_id == user_id))
		product = await database.fetch_one(query)
		
		if not product:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"Items with the id {product_id} is not found."
			)
		return schemas.Product(**product)
	
	async def update_async(self, product_id: int, user_id: int, product: schemas.Product) -> str:
		await self.show_async(product_id, user_id)
		query = products.update() \
			.where(and_(products.c.id == product_id, products.c.user_id == user_id)) \
			.values(product.dict())
		await database.execute(query)
		return "updated"
	
	async def delete_async(self, product_id: int, user_id: int):
		await self.show_async(product_id, user_id)
		query = products.delete() \
			.where(and_(products.c.id == product_id, products.c.user_id == user_id))
		await database.execute(query)
	
	async def buy_async(self, wish_id: int, win: bool, user_id: int) -> str:
		await self.show_async(wish_id, user_id)
		query = products.update() \
			.where(and_(products.c.id == wish_id, products.c.user_id == user_id)) \
			.values(buy=win)
		await database.execute(query)
		return "buy"
	
	@staticmethod
	async def show_random_async(user_id: int) -> schemas.Product:
		count = products.count().where(products.c.user_id == user_id)
		query = products.select().where(products.c.user_id == user_id).offset(
				func.floor(
					func.random() * count
				)
		).limit(1)
		item = await database.fetch_one(query)
		
		if not item:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail=f"has no items."
			)
		return schemas.Product(**item)
